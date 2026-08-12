"""Permissions Registry."""

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING, overload

from pydantic import ValidationError

from nardole.const import PERMISSIONS_FILE_PATH
from nardole.const.services import PermissionGrant, ServicePermission
from nardole.exceptions import PermissionManagerError
from nardole.models.nardole.registry import ServiceCallApprovalRecord, ServiceCallPermissionRecord

if TYPE_CHECKING:
    from nardole.models.nardole.registry import ServiceEntry

logger = logging.getLogger(__name__)


class PermissionsRegistry:
    """Permissions registry."""

    def __init__(
        self,
        permissions_registry_file_path: Path = PERMISSIONS_FILE_PATH,
    ) -> None:
        """Initialize class."""
        self._registered_permission_records: list[ServiceCallPermissionRecord] = load_permission_file(
            permission_file_path=permissions_registry_file_path,
        )
        self._permissions_registry_file_path = permissions_registry_file_path

    @overload
    def get_service_permission_record(
        self,
        service_domain: str,
        service_name: str,
    ) -> ServiceCallPermissionRecord: ...

    @overload
    def get_service_permission_record(
        self,
        service_domain: str,
        service_name: str,
        strict: bool,
    ) -> ServiceCallPermissionRecord | None: ...

    def get_service_permission_record(
        self,
        service_domain: str,
        service_name: str,
        strict: bool = True,
    ) -> ServiceCallPermissionRecord | None:
        """Retrieve the permission record for a service."""
        permissions = [
            permission
            for permission in self._registered_permission_records
            if permission.service_domain == service_domain and permission.service_name == service_name
        ]
        if not permissions:
            if strict:
                msg = (
                    f"Service {service_name} for domain {service_domain}"
                    " has not been registered in the permissions registry yet!"
                )
                raise PermissionManagerError(msg)
            return None
        return permissions[0]

    def get_registered_permission(
        self,
        service_domain: str,
        service_name: str,
        username: str | None = None,
        model_name: str | None = None,
        grant_opt: str | None = None,
    ) -> ServicePermission:
        """Get the permission for a service which has already been registered."""
        if not username and not model_name:
            msg = f"Cannot get {service_name} permissions for {service_domain}. No user/model names were passed."
            raise PermissionManagerError(msg)
        permission_record = self.get_service_permission_record(service_domain=service_domain, service_name=service_name)

        if model_name and permission_record.deny_all_models:
            return ServicePermission.ALWAYS_DENY

        permissions = []
        for permission in permission_record.permissions:
            if username and permission.username != username:
                continue
            if model_name and permission.model_name != model_name:
                continue
            if grant_opt == permission.grant_opt:
                permissions.append(permission)

        if not permissions:
            return ServicePermission.UNSET
        return permissions[0].permission

    async def request_user_permission(
        self,
        service_domain: str,
        service_name: str,
        username: str,
        model_name: str | None = None,
        grant_opts: list[str] | None = None,  # noqa: ARG002
    ) -> PermissionGrant:
        """Request user permission for approval."""
        # TODO: build function  # noqa: FIX002, TD002, TD003

        granted = {"grant": PermissionGrant.DENY}
        self.update_permissions(
            service_domain=service_domain,
            service_name=service_name,
            grant_opts=granted,
            username=username,
            model_name=model_name,
        )
        return PermissionGrant.DENY

    async def get_or_request_user_permission(
        self,
        service_domain: str,
        service_name: str,
        username: str,
        model_name: str | None = None,
        grant_opts: list[str] | None = None,
    ) -> PermissionGrant:
        """Get or request user for permissions.

        Return permissions if all are always allow or any are always ask.
        Request user permission if any are always ask/unset.
        """
        used_grant_opts = [None] if grant_opts is None else grant_opts

        request_permission_grants = []
        for grant_opt in used_grant_opts:
            permission = self.get_registered_permission(
                service_domain=service_domain,
                service_name=service_name,
                username=username,
                model_name=model_name,
                grant_opt=grant_opt,
            )
            if permission == ServicePermission.ALWAYS_ALLOW:
                continue
            if permission == ServicePermission.ALWAYS_DENY:
                return PermissionGrant.ALWAYS_DENY
            request_permission_grants.append(grant_opt)
        if not request_permission_grants:
            return PermissionGrant.ALLOW
        return await self.request_user_permission(
            service_domain=service_domain,
            service_name=service_name,
            username=username,
            model_name=model_name,
            grant_opts=grant_opts,
        )

    def update_permissions(
        self,
        service_domain: str,
        service_name: str,
        grant_opts: dict[str, PermissionGrant] | PermissionGrant,
        username: str,
        model_name: str | None = None,
    ) -> None:
        """Update recorded permissions."""
        permissions = self._registered_permission_records.copy()
        updated_permissions = []
        for permission in permissions:
            if permission.service_domain == service_domain and permission.service_name == service_name:
                updated_permissions.append(
                    self._update_user_grants_for_service(
                        permission_record=permission,
                        permission_grants=grant_opts,
                        username=username,
                        model_name=model_name,
                    ),
                )
            else:
                updated_permissions.append(permission)
        self._registered_permission_records = updated_permissions
        with open(self._permissions_registry_file_path, "w") as f:
            f.write(json.dumps(updated_permissions))

    def _update_user_grants_for_service(
        self,
        permission_record: ServiceCallPermissionRecord,
        permission_grants: dict[str, PermissionGrant] | PermissionGrant,
        username: str,
        model_name: str | None = None,
    ) -> ServiceCallPermissionRecord:
        """Update a single service permission grant with new permissions."""
        if permission_grants != PermissionGrant.ALWAYS_DENY_ALL_MODELS:
            grant_opts = permission_grants if isinstance(permission_grants, dict) else {None: permission_grants}

            permissions = [
                permission
                for permission in permission_record.permissions
                if permission.username != username
                and permission.model_name != model_name
                and permission.grant_opt not in grant_opts
            ]
            for grant_opt, permission in grant_opts.items():
                if permission == PermissionGrant.ALWAYS_DENY_ALL_MODELS:
                    msg = "Can only set permission to deny all models if grant opt is None."
                    raise PermissionManagerError(msg)
                permissions.append(
                    ServiceCallApprovalRecord(
                        username=username,
                        model_name=model_name,
                        grant_opt=grant_opt,
                        is_model=model_name is not None,
                        permission=permission,
                    ),
                )
            permission_record.permissions = permissions
        else:
            permission_record.deny_all_models = True
        return permission_record

    def register_service_permissions(
        self,
        service_entry: "ServiceEntry",
        strict: bool = True,
    ) -> None:
        """Register a single service in the permissions registry."""
        domain = service_entry.service_domain
        service = service_entry.service_name
        existing_record = self.get_service_permission_record(
            service_domain=domain,
            service_name=service,
            strict=False,
        )
        if existing_record:
            if strict:
                msg = f"Cannot register service {service} for domain {domain}: Service already registered."
                logger.error(msg)
            return
        record = ServiceCallPermissionRecord(
            service_domain=service_entry.service_domain,
            service_name=service_entry.service_name,
            deny_all_models=False,
            permissions=[],
        )
        self._registered_permission_records.append(record)
        with open(self._permissions_registry_file_path, "w") as f:
            f.write(json.dumps(self._registered_permission_records))


def load_permission_file(permission_file_path: Path) -> list[ServiceCallPermissionRecord]:
    """Load the permission file."""
    if not permission_file_path.exists():
        _create_permission_file(permission_file_path=permission_file_path)
    with open(permission_file_path) as f:
        raw_perms = f.read()
    try:
        js = json.loads(raw_perms)
        assert isinstance(js, list)
        permission_models = [ServiceCallPermissionRecord.model_validate(record) for record in js]
    except Exception as e:
        if isinstance(e, json.JSONDecodeError):
            msg = "Failed to parse JSON from permissions file."
        elif isinstance(e, AssertionError):
            msg = f"failed to parse data in permissions file. Expected a list of permissions record, got {type(js)}"
        elif isinstance(e, ValidationError):
            msg = "Failed to parse the records in the permission file as service call permission records."
        else:
            msg = f"Unknown error parsing permissions file: {e}"
        msg += (
            f"\nExisting file will be backed up as {permission_file_path.as_posix()}.bak "
            "and replaced with a blank file."
        )
        logger.exception(msg)
        backup_path = f"{permission_file_path.as_posix()}.bak"
        permission_file_path.rename(backup_path)
        _create_permission_file(permission_file_path=permission_file_path, overwrite=True)
        return []
    return permission_models


def _create_permission_file(permission_file_path: Path, overwrite: bool = False) -> None:
    """Create the permission file."""
    permission_file_path.touch(mode=600, exist_ok=overwrite)
    with open(permission_file_path, "w") as f:
        f.write("[]")

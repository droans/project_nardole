"""Service constants."""

from enum import StrEnum


class ServicePermission(StrEnum):
    """Service permissions."""

    ALWAYS_ASK = "always_ask"
    ALWAYS_ALLOW = "always_allow"
    ALWAYS_DENY = "always_deny"
    UNSET = "unset"


class PermissionGrant(StrEnum):
    """Permission granted by user."""

    ALLOW = "allow"
    DENY = "deny"
    ALWAYS_ALLOW = "always_allow"
    ALWAYS_DENY = "always_deny"
    ALWAYS_DENY_ALL_MODELS = "always_deny_all_models"


class CallServiceStatus(StrEnum):
    """Service call status."""

    SUCCESS = "success"  # Service successfully called
    REQUIRES_APPROVAL = "requires_approval"  # Service call requires user approval
    FORBIDDEN = "forbidden"  # User set permissions to always deny
    DENIED = "denied"  # User denied service call
    REJECTED = "rejected"  # Service call rejected for any other reason
    FAILURE = "failure"  # Service call failed
    NOT_REGISTERED = "not_registered"  # Service not yet registered

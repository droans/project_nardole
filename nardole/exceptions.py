"""Exception classes."""


class ConfigEntryLoadError(Exception):
    """Exception class for errors loading config entries."""


class IntegrationRegistrationError(Exception):
    """Exception class for errors when registering integrations."""


class IntegrationError(Exception):
    """Exception class for general integration errors."""


class ServiceCallPermissionError(Exception):
    """Exception class for permission failures."""


class ServiceCallRegistryError(Exception):
    """Exception class for errors with the service registry."""


class PermissionManagerError(Exception):
    """Exception class for errors with the permission registry."""

"""Contains the package version string.

See Also:
    `PEP 396 <https://www.python.org/dev/peps/pep-0396/>`_

"""

import pkg_resources

__all__ = ['__version__', 'is_compatible']

#: The package version string.
__version__: str = pkg_resources.require('pymap-admin')[0].version


def is_compatible(client_version: str, server_version: str) -> bool:
    """Check if the given client version is backwards- and forwards-compatible
    with the server version.

    Args:
        client_version: The provided client version string.
        server_version: The server version string, usually :attr:`__version__`.

    """
    major_server, _, extra_server = server_version.partition('.')
    major_client, _, extra_client = client_version.partition('.')
    major_server_int = int(major_server)
    major_client_int = int(major_client)
    if major_server_int != major_client_int:
        return False
    elif major_client_int == 0:
        return is_compatible(extra_client, server_version=extra_server)
    else:
        return True

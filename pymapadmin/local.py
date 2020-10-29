
from __future__ import annotations

import os
from pathlib import Path
from typing import Union

from tempfile import gettempdir

__all__ = ['get_admin_socket', 'get_token_file']


def _get_path(path: Union[None, str, Path], mkdir: bool,
              envvar: str, name: str) -> Path:
    if path is None:
        if f'PYMAP_ADMIN_{envvar}' in os.environ:
            path = Path(os.environ[f'PYMAP_ADMIN_{envvar}'])
        else:
            tmpdir = gettempdir()
            path = Path(tmpdir, 'pymap', name)
    elif isinstance(path, str):
        path = Path(path)
    path = path.expanduser()
    if mkdir:
        path.parent.mkdir(mode=0o700, exist_ok=True)
    return path


def get_admin_socket(path: Union[None, str, Path], *,
                     mkdir: bool = False) -> Path:
    """Returns a path that should be consistent between a ``pymap-admin``
    client and a ``pymap`` server.

    Use *path* or the ``$PYMAP_ADMIN_SOCK`` environment variable to override
    with an explicit path, otherwise the default is:

    ```bash
    $TMPDIR/pymap/pymap-admin.sock
    ```

    Args:
        path: Path provided by command-line arguments.
        mkdir: Whether the intermediate directory should be created.

    """
    return _get_path(path, mkdir, 'SOCK', 'pymap-admin.sock')


def get_token_file(path: Union[None, str, Path], *,
                   mkdir: bool = False) -> Path:
    """Returns the path that should be used to read and write the auth token
    for use by the ``pymap-admin`` client.

    Use *path* or the ``$PYMAP_ADMIN_TOKEN_FILE`` environment variable to
    override with an explicit path, otherwise the default is:

    ```bash
    $TMPDIR/pymap/pymap-admin.token
    ```

    Args:
        path: Path provided by command-line arguments.

    """
    return _get_path(path, mkdir, 'TOKEN_FILE', 'pymap-admin.token')

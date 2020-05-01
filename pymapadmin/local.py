
from __future__ import annotations

import os
import os.path

from tempfile import gettempdir

__all__ = ['get_admin_socket']


def get_admin_socket(*, mkdir: bool = False) -> str:
    """Returns a path in :func:`~tempfile.gettempdir` that should be consistent
    between a ``pymap-admin`` client and a ``pymap`` server.

    Use the ``$PYMAP_ADMIN_SOCK`` environment variable to override this
    behavior with an explicit value.

    Args:
        mkdir: Whether the intermediate directory should be created.

    """
    if 'PYMAP_ADMIN_SOCK' in os.environ:
        return os.environ['PYMAP_ADMIN_SOCK']
    tmpdir = gettempdir()
    pymap_dir = os.path.join(tmpdir, 'pymap')
    if mkdir and not os.path.isdir(pymap_dir):
        os.mkdir(pymap_dir, mode=0o700)
    return os.path.join(pymap_dir, 'pymap-admin.sock')


from __future__ import annotations

import os
from argparse import Action, ArgumentParser, Namespace
from collections.abc import Sequence
from functools import partial
from pathlib import Path
from typing import Any, Union, Final, Optional

from tempfile import gettempdir

__all__ = ['LocalFile', 'config_file', 'token_file', 'socket_file']


class _AddAction(Action):

    def __init__(self, local_file: LocalFile, *args, **kwargs) -> None:
        kwargs['metavar'] = 'PATH'
        super().__init__(*args, **kwargs)
        self._local_file = local_file

    def __call__(self, parser: ArgumentParser, namespace: Namespace,
                 values: Any, option_string: str = None) -> None:
        setattr(namespace, self.dest, values)
        self._local_file.add(values)


class LocalFile:
    """Defines a file that is kept on the local filesystem but could be in a
    number of different places.

    Args:
        envvar: The environment variable used to custom the file path.
        filename: The default filename.

    """

    def __init__(self, envvar: str, filename: str) -> None:
        super().__init__()
        self.envvar: Final = envvar
        self.filename: Final = filename
        self._custom: list[Path] = []

    @property
    def add_action(self) -> type[Action]:
        """Use as an ``action=`` in :mod:`argparse` to add command-line
        arguments as custom paths.

        """
        return partial(_AddAction, self)  # type: ignore

    @property
    def custom(self) -> Sequence[Path]:
        """The custom paths added by :meth:`.add`, followed by any path
        specified by environment variable.

        """
        try:
            envvar_val = os.environ[self.envvar]
        except KeyError:
            return self._custom
        else:
            return self._custom + [Path(envvar_val).expanduser()]

    @property
    def _config_home(self) -> Path:
        try:
            config_home = os.environ['XDG_CONFIG_HOME']
        except KeyError:
            return Path(Path.home(), '.config')
        else:
            return Path(config_home).expanduser()

    @property
    def _temp_path(self) -> Path:
        return Path(gettempdir(), 'pymap', self.filename)

    @property
    def _home_path(self) -> Path:
        return Path(self._config_home, 'pymap', self.filename)

    def add(self, *custom: Union[None, str, Path]) -> None:
        """Append the *custom* paths to :attr:`.custom`.

        Args:
            custom: The custom paths to the file, e.g. from config or
                command-line.

        """
        new_custom = [*self._custom,
                      *(Path(path).expanduser() for path in custom if path)]
        self._custom = new_custom

    def get_home(self, *, mkdir: bool = False) -> Path:
        """Returns *filename* inside ``~/.config/pymap/``. If :attr:`.custom`
        is not empty, its first value is returned instead.

        Args:
            mkdir: Whether any intermediate directories should be created.

        """
        try:
            path = self.custom[0]
        except IndexError:
            path = self._home_path
        if mkdir:
            path.parent.mkdir(mode=0o700, exist_ok=True)
        return path

    def get_temp(self, *, mkdir: bool = False) -> Path:
        """Returns *filename* inside the ``pymap/`` subdirectory of
        :func:`~tempfile.gettempdir`. If :attr:`.custom` is not empty, its
        first value is returned instead.

        Args:
            mkdir: Whether any intermediate directories should be created.

        """
        try:
            path = self.custom[0]
        except IndexError:
            path = self._temp_path
        if mkdir:
            path.parent.mkdir(mode=0o700, exist_ok=True)
        return path

    def get_all(self) -> Sequence[Path]:
        """Return all the paths that may contain the file."""
        return list(self.custom) + [self._home_path, self._temp_path]

    def find(self) -> Optional[Path]:
        """Return the :class:`~pathlib.Path` of an existing file, if one
        exists.

        The order of searched paths looks like this:

        1. The :attr:`.custom` paths.
        2. A path defined in the *envvar* environment variable.
        3. *filename* in ``~/.config/pymap/``.
        4. *filename* in the ``pymap`` subdirectory of
           :func:`tempfile.gettempdir`.

        """
        all_paths = self.get_all()
        return next((path for path in all_paths if path.exists()), None)


#: The config file for default command-line arguments.
config_file = LocalFile('PYMAP_ADMIN_CONFIG', 'pymap-admin.conf')

#: The token file for pymap-admin authentication.
token_file = LocalFile('PYMAP_ADMIN_TOKEN_FILE', 'pymap-admin.token')

#: The socket file for connecting to a running pymap server.
socket_file = LocalFile('PYMAP_ADMIN_SOCKET', 'pymap-admin.sock')

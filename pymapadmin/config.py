
from __future__ import annotations

import os
import os.path
from configparser import ConfigParser, SectionProxy
from typing import Optional

__all__ = ['Config']


class Config:
    """Reads and manages access to a config file, e.g. ``~/.pymaprc``.

    Args:
        config_file: The path to a :mod:`configparser` config file.

    """

    def __init__(self, config_file: str = os.devnull) -> None:
        super().__init__()
        self._config_file = os.path.expanduser(config_file)
        self._config_parser = ConfigParser()
        self._config_parser.read(self._config_file)

    def flush(self) -> None:
        """Re-build and save the config file, flushing any changes made."""
        with open(self._config_file, 'w') as out:
            self._config_parser.write(out)

    @property
    def _section(self) -> SectionProxy:
        if 'pymap-admin' not in self._config_parser:
            self._config_parser['pymap-admin'] = {}
        return self._config_parser['pymap-admin']

    def __getattr__(self, attr: str) -> Optional[str]:
        return self._section.get(attr, None)

    def __setattr__(self, attr: str, val: Optional[str]) -> None:
        if attr.startswith('_'):
            super().__setattr__(attr, val)
        elif val is not None:
            self._section[attr] = val
        else:
            self._section.pop(attr)

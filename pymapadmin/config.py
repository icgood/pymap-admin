
from __future__ import annotations

import os
from argparse import Namespace
from configparser import ConfigParser
from typing import Optional

from .local import config_file, token_file, socket_file

__all__ = ['Config']


class Config:
    """Provides values that may be overridden by command-line arguments,
    environment variables, or config files (in that order).

    Args:
        args: The parsed command-line arguments.

    """

    def __init__(self, args: Namespace) -> None:
        super().__init__()
        self._args = args
        self._parser = parser = ConfigParser()
        parser.read(config_file.get_all())
        if not parser.has_section('pymap-admin'):
            parser.add_section('pymap-admin')
        self._section = section = parser['pymap-admin']
        if 'path' in section:
            socket_file.add(section['path'])
        if 'token_file' in section:
            token_file.add(section['token_file'])

    @classmethod
    def build(cls, args: Namespace) -> ConfigParser:
        """Build and return a new :class:`~configparser.ConfigParser`
        pre-loaded with the arguments from *args*.

        Args:
            args: The command-line arguments to pre-load.

        """
        parser = ConfigParser()
        parser.add_section('pymap-admin')
        section = parser['pymap-admin']
        if args.host is not None:
            section['host'] = args.host
        if args.port is not None:
            section['port'] = args.port
        if args.path is not None:
            section['path'] = args.path
        if args.token_file is not None:
            section['token_file'] = args.token_file
        if args.cert is not None:
            section['cert'] = args.cert
        if args.key is not None:
            section['key'] = args.key
        if args.cafile is not None:
            section['cafile'] = args.cafile
        if args.capath is not None:
            section['capath'] = args.capath
        if args.no_verify_cert:
            section['no_verify_cert'] = str(args.no_verify_cert)
        return parser

    def _getstr(self, attr: str, envvar: str) -> Optional[str]:
        val: Optional[str] = getattr(self._args, attr)
        if val is not None:
            return val
        if envvar in os.environ:
            return os.environ[envvar]
        return self._section.get(attr, fallback=None)

    def _getint(self, attr: str, envvar: str) -> Optional[int]:
        val: Optional[int] = getattr(self._args, attr)
        if val is not None:
            return val
        if envvar in os.environ:
            return int(os.environ[envvar])
        return self._section.getint(attr, fallback=None)

    def _getbool(self, attr: str, envvar: str) -> bool:
        val: bool = getattr(self._args, attr)
        if val:
            return True
        if envvar in os.environ:
            val_str = os.environ[envvar].lower()
            return val_str in ('1', 'yes', 'true', 'on')
        return self._section.getboolean(attr, fallback=False)

    @property
    def host(self) -> Optional[str]:
        return self._getstr('host', 'PYMAP_ADMIN_HOST')

    @property
    def port(self) -> Optional[int]:
        return self._getint('port', 'PYMAP_ADMIN_PORT')

    @property
    def token(self) -> Optional[str]:
        return self._getstr('token', 'PYMAP_ADMIN_TOKEN')

    @property
    def cert(self) -> Optional[str]:
        return self._getstr('cert', 'PYMAP_ADMIN_CERT')

    @property
    def key(self) -> Optional[str]:
        return self._getstr('key', 'PYMAP_ADMIN_KEY')

    @property
    def cafile(self) -> Optional[str]:
        return self._getstr('cafile', 'PYMAP_ADMIN_CAFILE')

    @property
    def capath(self) -> Optional[str]:
        return self._getstr('capath', 'PYMAP_ADMIN_CAPATH')

    @property
    def no_verify_cert(self) -> bool:
        return self._getbool('no_verify_cert', 'PYMAP_ADMIN_NO_VERIFY_CERT')

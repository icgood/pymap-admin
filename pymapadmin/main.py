"""Admin functions for a running pymap server.

Many arguments may also be given with a $PYMAP_ADMIN_* environment variable.

"""

from __future__ import annotations

import os
import os.path
import sys
import asyncio
from argparse import ArgumentParser, Namespace, SUPPRESS
from ssl import create_default_context, CERT_NONE
from typing import Type, Optional

from grpclib.client import Channel
from pymapadmin import __version__

from .commands import load_commands
from .commands.base import Command
from .config import Config
from .local import get_admin_socket


def main() -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version',
                        version='%(prog)s' + __version__)
    parser.add_argument('--config', metavar='PATH', type=Config,
                        default=_def('CONFIG', '~/.pymaprc'),
                        help='configuration file path')
    parser.add_argument('--host', metavar='HOST',
                        default=_def('HOST'), help='server host')
    parser.add_argument('--port', metavar='PORT',
                        default=_def('PORT'), help='server port')
    parser.add_argument('--path', metavar='FILE',
                        default=_def('PATH'), help=SUPPRESS)
    parser.add_argument('--token', metavar='STR', default=_def('TOKEN'),
                        help='auth token')

    group = parser.add_argument_group('tls options')
    group.add_argument('--cert', metavar='FILE', default=_def('CERT'),
                       help='client certificate')
    group.add_argument('--key', metavar='FILE', default=_def('KEY'),
                       help='client private key')
    group.add_argument('--cafile', metavar='FILE', default=_def('CAFILE'),
                       help='CA cert file')
    group.add_argument('--capath', metavar='PATH', default=_def('CAPATH'),
                       help='CA cert path')
    group.add_argument('--no-verify-cert', action='store_true',
                       help='skip TLS certificate verification')

    subparsers = parser.add_subparsers(dest='command', metavar='COMMAND')
    commands = load_commands('pymapadmin.commands')
    for command_name, command_cls in commands.items():
        command_cls.add_subparser(command_name, subparsers)
    args = parser.parse_args()

    if not args.command:
        parser.error('Expected command name.')
    command = commands[args.command]

    return asyncio.run(run(parser, args, command), debug=False)


async def run(parser: ArgumentParser, args: Namespace,
              command_cls: Type[Command]) -> int:
    ssl = create_default_context(cafile=args.cafile, capath=args.capath)
    if args.no_verify_cert:
        ssl.check_hostname = False
        ssl.verify_mode = CERT_NONE
    if args.host is not None or args.port is not None:
        channel = Channel(host=args.host, port=args.port, ssl=ssl)
    else:
        path = args.path or get_admin_socket()
        channel = Channel(path=path)
    command = command_cls(args, channel)
    try:
        return await command(sys.stdout)
    finally:
        channel.close()


def _def(name: str, val: str = None) -> Optional[str]:
    return os.environ.get(f'PYMAP_ADMIN_{name}', val)

"""Admin functions for a running pymap server.

Many arguments may also be given with a $PYMAP_ADMIN_* environment variable.

"""

from __future__ import annotations

import os
import os.path
import sys
import asyncio
from argparse import ArgumentParser, Namespace
from ssl import create_default_context, CERT_NONE, SSLContext
from typing import Type, Optional

from grpclib.client import Channel
from pymapadmin import __version__

from .local import get_admin_socket
from .commands import Command
from .commands.load import load_commands


def main() -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version',
                        version='%(prog)s' + __version__)
    parser.add_argument('--host', metavar='HOST',
                        default=_def('HOST'), help='server host')
    parser.add_argument('--port', metavar='PORT', type=int,
                        default=_def('PORT'), help='server port')
    parser.set_defaults(path=get_admin_socket())

    group = parser.add_argument_group('tls options')
    group.add_argument('--tls', action='store_true', default=_def('TLS'),
                       help='enable TLS')
    group.add_argument('--cafile', metavar='FILE', default=_def('CAFILE'),
                       help='CA cert file')
    group.add_argument('--capath', metavar='PATH', default=_def('CAPATH'),
                       help='CA cert path')
    group.add_argument('--no-verify-cert', action='store_true',
                       help='skip TLS certificate verification')

    group = parser.add_argument_group('auth options')
    group.add_argument('--username', metavar='NAME', dest='admin_username',
                       default=_def('USERNAME'), help='auth username')
    group.add_argument('--password', metavar='PASS', dest='admin_password',
                       default=_def('PASSWORD'), help='auth password')
    group.add_argument('--ask-password', action='store_true',
                       help='prompt for the auth password')

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
    ssl: Optional[SSLContext] = None
    if args.tls:
        ssl = create_default_context(cafile=args.cafile, capath=args.capath)
        if args.no_verify_cert:
            ssl.check_hostname = False
            ssl.verify_mode = CERT_NONE
    if args.host is None:
        if not os.path.exists(args.path):
            parser.error(f'File not found: {args.path}\n\n'
                         f'Is pymap running? Use --host to connect to a '
                         f'remote host.')
        channel = Channel(path=args.path)
    else:
        channel = Channel(host=args.host, port=args.port, ssl=ssl)
    client = command_cls.get_client(channel)
    command = command_cls(args, client)
    try:
        return await command(sys.stdout)
    finally:
        channel.close()


def _def(name: str, val: str = None) -> Optional[str]:
    return os.environ.get(f'PYMAP_ADMIN_{name}', val)

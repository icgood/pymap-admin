"""Admin functions for a running pymap server.

Many arguments may also be given with a $PYMAP_ADMIN_* environment variable.

"""

from __future__ import annotations

import sys
import asyncio
from argparse import ArgumentParser, Namespace
from ssl import create_default_context, CERT_NONE

from grpclib.client import Channel
from pymapadmin import __version__

from .commands import load_commands
from .commands.base import Command
from .config import Config
from .local import config_file, token_file, socket_file


def main() -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument('--config', action=config_file.add_action,
                        help='connection info config file')
    parser.add_argument('--host', metavar='HOST', help='server host')
    parser.add_argument('--port', metavar='PORT', help='server port')
    parser.add_argument('--path', action=socket_file.add_action,
                        help='server socket file')
    parser.add_argument('--token-file', action=token_file.add_action,
                        help='auth token file')

    group = parser.add_argument_group('tls options')
    group.add_argument('--cert', metavar='FILE',
                       help='client certificate')
    group.add_argument('--key', metavar='FILE',
                       help='client private key')
    group.add_argument('--cafile', metavar='FILE',
                       help='CA cert file')
    group.add_argument('--capath', metavar='PATH',
                       help='CA cert path')
    group.add_argument('--no-verify-cert', action='store_true',
                       help='disable TLS certificate verification')

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
              command_cls: type[Command]) -> int:
    config = Config(args)
    ssl = create_default_context(cafile=config.cafile, capath=config.capath)
    if config.no_verify_cert:
        ssl.check_hostname = False
        ssl.verify_mode = CERT_NONE
    if config.host is not None or config.port is not None:
        channel = Channel(host=config.host, port=config.port, ssl=ssl)
    else:
        path = socket_file.find()
        if path is None:
            parser.error('Running server not found, please provide '
                         '--host, --port, or --path.')
        channel = Channel(path=str(path))
    command = command_cls(args, channel)
    try:
        return await command(sys.stdout)
    finally:
        channel.close()

"""Admin functions for a running pymap server.

Many arguments may also be given with a $PYMAP_ADMIN_* environment variable.

"""

from __future__ import annotations

import os
import sys
import asyncio
from argparse import ArgumentParser, Namespace, FileType
from ssl import create_default_context
from typing import Type, Optional, Mapping

from grpclib.client import Channel
from pkg_resources import iter_entry_points, DistributionNotFound
from pymapadmin import __version__

from .command import ClientCommand


def main() -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version',
                        version='%(prog)s' + __version__)
    parser.add_argument('--outfile', metavar='PATH',
                        type=FileType('w'), default=sys.stdout,
                        help='the output file (default: stdout)')
    parser.add_argument('--host', metavar='HOST',
                        default=_def('HOST', 'localhost'), help='server host')
    parser.add_argument('--port', metavar='PORT', type=int,
                        default=_def('PORT', '9090'), help='server port')
    parser.add_argument('--cafile', metavar='FILE', default=_def('CAFILE'),
                        help='CA cert file')
    parser.add_argument('--capath', metavar='PATH', default=_def('CAPATH'),
                        help='CA cert path')
    parser.add_argument('--username', metavar='NAME', dest='admin_username',
                        default=_def('USERNAME'), help='auth username')
    parser.add_argument('--password', metavar='PASS', dest='admin_password',
                        default=_def('PASSWORD'), help='auth password')

    subparsers = parser.add_subparsers(dest='command',
                                       help='which admin command to run')
    commands = _load_entry_points('pymapadmin.client')
    for command_name, command_cls in commands.items():
        command_cls.add_subparser(command_name, subparsers)
    args = parser.parse_args()

    if not args.command:
        parser.error('Expected command name.')
    command = commands[args.command]

    return asyncio.run(run(parser, args, command), debug=False)


async def run(parser: ArgumentParser, args: Namespace,
              command_cls: Type[ClientCommand]) -> int:
    ssl = create_default_context(cafile=args.cafile, capath=args.capath)
    channel = Channel(host=args.host, port=args.port, ssl=ssl)
    stub = command_cls.get_stub(channel)
    command = command_cls(stub, args)
    try:
        return await command()
    finally:
        channel.close()


def _def(name: str, val: str = None) -> Optional[str]:
    return os.environ.get(f'PYMAP_ADMIN_{name}', val)


def _load_entry_points(group: str) -> Mapping[str, Type[ClientCommand]]:
    ret = {}
    for entry_point in iter_entry_points(group):
        try:
            cls = entry_point.load()
        except DistributionNotFound:
            pass  # optional dependencies not installed
        else:
            ret[entry_point.name] = cls
    return ret

"""Ping the server."""

from __future__ import annotations

import sys
import traceback
from typing import Any, TextIO

from .command import ClientCommand
from .. import __version__ as client_version
from ..grpc.admin_pb2 import PingRequest


class PingCommand(ClientCommand):

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> None:  # pragma: no cover
        subparsers.add_parser(
            name, description=__doc__,
            help='ping the server')

    async def run(self, fileobj: TextIO) -> int:
        req = PingRequest(client_version=client_version)
        try:
            res = await self.stub.Ping(req)
        except OSError:
            traceback.print_exc()
            return 1
        except Exception:
            traceback.print_exc()
            return 1
        else:
            print(res, file=sys.stderr)
            return 0

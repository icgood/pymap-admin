
from __future__ import annotations

from typing import Any, TextIO, AsyncContextManager

from grpclib.client import Channel, Stream

from .command import RequestT, ResponseT, ClientCommand
from .. import __version__ as client_version
from ..grpc.admin_grpc import SystemStub
from ..grpc.admin_pb2 import PingRequest, PingResponse


class SystemBase(ClientCommand[SystemStub, RequestT, ResponseT]):

    @classmethod
    def get_stub(cls, channel: Channel) -> SystemStub:
        return SystemStub(channel)


class PingCommand(SystemBase[PingRequest, PingResponse]):
    """Ping the server."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> None:  # pragma: no cover
        subparsers.add_parser(
            name, description=cls.__doc__,
            help='ping the server')

    def open(self) -> AsyncContextManager[Stream[PingRequest, PingResponse]]:
        return self.stub.Ping.open()

    def build_request(self) -> PingRequest:
        return PingRequest(client_version=client_version)

    def print_success(self, res: PingResponse, outfile: TextIO) -> None:
        print(res, file=outfile)

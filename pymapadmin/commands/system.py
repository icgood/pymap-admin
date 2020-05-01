
from __future__ import annotations

from argparse import ArgumentParser
from typing import Any, TextIO

from grpclib.client import Channel

from . import Command
from .. import __version__ as client_version
from ..typing import RequestT, ResponseT, MethodProtocol
from ..grpc.admin_grpc import SystemStub
from ..grpc.admin_pb2 import PingRequest, PingResponse


class SystemCommand(Command[SystemStub, RequestT, ResponseT]):

    @classmethod
    def get_client(cls, channel: Channel) -> SystemStub:
        return SystemStub(channel)


class PingCommand(SystemCommand[PingRequest, PingResponse]):
    """Ping the server."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> ArgumentParser:  # pragma: no cover
        return subparsers.add_parser(
            name, description=cls.__doc__,
            help='ping the server')

    @property
    def method(self) -> MethodProtocol[PingRequest, PingResponse]:
        return self.client.Ping

    def build_request(self) -> PingRequest:
        return PingRequest(client_version=client_version)

    def print_success(self, res: PingResponse, outfile: TextIO) -> None:
        print(res, file=outfile)

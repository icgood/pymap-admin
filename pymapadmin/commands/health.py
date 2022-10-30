
from __future__ import annotations

from argparse import ArgumentParser
from typing import Any, TextIO

from .base import ClientCommand
from ..grpc.health_grpc import HealthStub
from ..grpc.health_pb2 import HealthCheckRequest, HealthCheckResponse
from ..typing import RequestT, ResponseT, MethodProtocol

__all__ = ['CheckCommand']


class HealthCommand(ClientCommand[HealthStub, RequestT, ResponseT]):

    @property
    def client(self) -> HealthStub:
        return HealthStub(self.channel)


class CheckCommand(HealthCommand[HealthCheckRequest,
                                 HealthCheckResponse]):
    """Check the health of the server."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> ArgumentParser:  # pragma: no cover
        argparser: ArgumentParser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='check the server health')
        return argparser

    @property
    def method(self) -> MethodProtocol[HealthCheckRequest,
                                       HealthCheckResponse]:
        return self.client.Check

    def build_request(self) -> HealthCheckRequest:
        return HealthCheckRequest()

    def _is_serving(self, response: HealthCheckResponse) -> bool:
        return response.status == HealthCheckResponse.ServingStatus.SERVING

    def handle_response(self, response: HealthCheckResponse,
                        outfile: TextIO) -> int:
        print(response, file=outfile)
        return 0 if self._is_serving(response) else 1


from io import StringIO
from argparse import Namespace
from typing import Any

from grpclib.server import Stream
from grpclib.testing import ChannelFor

from pymapadmin.commands.health import CheckCommand
from pymapadmin.grpc.health_grpc import HealthBase
from pymapadmin.grpc.health_pb2 import HealthCheckRequest, HealthCheckResponse

from handler import MockHandler

_CheckStream = Stream[HealthCheckRequest, HealthCheckResponse]
_WatchStream = Stream[HealthCheckRequest, HealthCheckResponse]


class Handler(HealthBase, MockHandler[Any, Any]):

    async def Check(self, stream: _CheckStream) -> None:
        await self._run(stream)

    async def Watch(self, stream: _WatchStream) -> None:
        raise NotImplementedError()


class TestCheckCommand:

    async def test_check(self) -> None:
        handler = Handler(HealthCheckRequest, [HealthCheckResponse(
            status=HealthCheckResponse.ServingStatus.SERVING)])
        args = Namespace(token=None, token_file=None)
        async with ChannelFor([handler]) as channel:
            command = CheckCommand(args, channel)
            code = await command(StringIO())
        assert 0 == code

    async def test_check_not_serving(self) -> None:
        handler = Handler(HealthCheckRequest, [HealthCheckResponse(
            status=HealthCheckResponse.ServingStatus.NOT_SERVING)])
        args = Namespace(token=None, token_file=None)
        async with ChannelFor([handler]) as channel:
            command = CheckCommand(args, channel)
            code = await command(StringIO())
        assert 1 == code

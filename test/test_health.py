
from io import StringIO
from argparse import Namespace

import pytest
from grpclib.testing import ChannelFor
from pymapadmin.commands.health import CheckCommand
from grpclib.health.v1.health_grpc import HealthBase
from grpclib.health.v1.health_pb2 import HealthCheckRequest, \
    HealthCheckResponse

from handler import RequestT, ResponseT, MockHandler

pytestmark = pytest.mark.asyncio


class Handler(HealthBase, MockHandler[RequestT, ResponseT]):

    async def Check(self, stream) -> None:
        await self._run(stream)

    async def Watch(self, stream) -> None:
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


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
        handler = Handler() \
            .expect(HealthCheckRequest, [HealthCheckResponse(
                status=HealthCheckResponse.ServingStatus.SERVING)])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None, service='test')
        async with ChannelFor([handler]) as channel:
            command = CheckCommand(args, channel)
            code = await command(outfile, errfile)
        assert [HealthCheckRequest(service='test')] == handler.requests
        assert 0 == code
        assert 'status: SERVING\n\n' == outfile.getvalue()
        assert '' == errfile.getvalue()

    async def test_check_not_serving(self) -> None:
        handler = Handler() \
            .expect(HealthCheckRequest, [HealthCheckResponse(
                status=HealthCheckResponse.ServingStatus.NOT_SERVING)])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None, service='')
        async with ChannelFor([handler]) as channel:
            command = CheckCommand(args, channel)
            code = await command(outfile, errfile)
        assert [HealthCheckRequest(service='')] == handler.requests
        assert 1 == code
        assert '' == outfile.getvalue()
        assert 'status: NOT_SERVING\n\n' == errfile.getvalue()

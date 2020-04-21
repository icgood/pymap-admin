
from io import StringIO
from argparse import Namespace

import pytest  # type: ignore
from pymapadmin.client.ping import PingCommand
from pymapadmin.grpc.admin_pb2 import PingResponse

from stub import StubChannel

pytestmark = pytest.mark.asyncio


class TestPingCommand:

    async def test_ping(self):
        stub = StubChannel(PingResponse(server_version='test'))
        args = Namespace()
        command = PingCommand(stub, args)
        code = await command.run(StringIO())
        assert 'Ping' == stub.method
        assert 0 == code

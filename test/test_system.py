
from io import StringIO
from argparse import Namespace

import pytest  # type: ignore
from pymapadmin.commands.system import PingCommand
from pymapadmin.grpc.admin_pb2 import PingResponse

from client import MockClient

pytestmark = pytest.mark.asyncio


class TestPingCommand:

    async def test_ping(self):
        client = MockClient([PingResponse(server_version='test')])
        args = Namespace()
        command = PingCommand(args, client)
        code = await command(StringIO())
        assert 'Ping' == client.method
        assert 0 == code


from io import StringIO
from argparse import Namespace

import pytest  # type: ignore
from pymapadmin.client.system import PingCommand
from pymapadmin.grpc.admin_pb2 import PingResponse

from stub import TestStub

pytestmark = pytest.mark.asyncio


class TestPingCommand:

    async def test_ping(self):
        stub = TestStub([PingResponse(server_version='test')])
        args = Namespace(outfile=StringIO())
        command = PingCommand(stub, args)
        code = await command()
        assert 'Ping' == stub.method
        assert 0 == code


from io import StringIO
from argparse import Namespace
from typing import Any, Optional

import pytest  # type: ignore
from pymapadmin.client.ping import PingCommand
from pymapadmin.grpc.admin_pb2 import PingResponse

pytestmark = pytest.mark.asyncio


class _Stub:

    def __init__(self, response) -> None:
        self.method: Optional[str] = None
        self.request: Optional[Any] = None
        self.response = response

    async def _action(self, request):
        self.request = request
        return self.response

    def __getattr__(self, method):
        self.method = method
        return self._action


class TestPingcCommand:

    async def test_ping(self):
        stub = _Stub(PingResponse(server_version='test'))
        args = Namespace()
        command = PingCommand(stub, args)
        code = await command.run(StringIO())
        assert 'Ping' == stub.method
        assert 0 == code


from io import BytesIO, StringIO
from argparse import Namespace
from typing import Any, Optional

import pytest  # type: ignore
from pymapadmin.client.append import AppendCommand
from pymapadmin.grpc.admin_pb2 import AppendResponse, SUCCESS

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


class TestAdminClient:

    async def test_append(self):
        stub = _Stub(AppendResponse(result=SUCCESS))
        args = Namespace(user='testuser', sender=None, recipient=None,
                         mailbox='INBOX', data=BytesIO(b'test data'),
                         flags=['\\Flagged', '\\Seen'],
                         timestamp=1234567890)
        command = AppendCommand(stub, args)
        code = await command.run(StringIO())
        request = stub.request
        assert 'Append' == stub.method
        assert 0 == code
        assert b'test data' == request.data
        assert 1234567890.0 == request.when
        assert ['\\Flagged', '\\Seen'] == request.flags
        assert 'testuser' == request.login.user
        assert 'INBOX' == request.mailbox

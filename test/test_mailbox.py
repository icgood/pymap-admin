
from io import BytesIO, StringIO
from argparse import Namespace

import pytest  # type: ignore
from pymapadmin.client.mailbox import AppendCommand
from pymapadmin.grpc.admin_pb2 import AppendResponse, Result, FAILURE

from stub import TestStub

pytestmark = pytest.mark.asyncio


class TestAppendCommand:

    async def test_append(self):
        stub = TestStub([AppendResponse()])
        outfile = StringIO()
        args = Namespace(outfile=outfile,
                         admin_username='admuser', admin_password='admpass',
                         user='testuser', sender=None, recipient=None,
                         mailbox='INBOX', data=BytesIO(b'test data'),
                         flags=['\\Flagged', '\\Seen'],
                         timestamp=1234567890)
        command = AppendCommand(stub, args)
        code = await command()
        request = stub.request
        assert 'Append' == stub.method
        assert 0 == code
        assert b'test data' == request.data
        assert 1234567890.0 == request.when
        assert ['\\Flagged', '\\Seen'] == request.flags
        assert 'testuser' == request.login.authzid
        assert 'INBOX' == request.mailbox
        assert '2.0.0 Message delivered\n' == outfile.getvalue()

    async def test_append_failure(self):
        stub = TestStub([AppendResponse(
            result=Result(code=FAILURE, key='MailboxNotFound'))])
        outfile = StringIO()
        args = Namespace(outfile=outfile,
                         admin_username='admuser', admin_password='admpass',
                         user='testuser', sender=None, recipient=None,
                         mailbox='Bad', data=BytesIO(b'test data'),
                         flags=['\\Flagged', '\\Seen'],
                         timestamp=1234567890)
        command = AppendCommand(stub, args)
        code = await command()
        request = stub.request
        assert 1 == code
        assert 'Bad' == request.mailbox
        assert '4.2.0 Message not deliverable\n' == outfile.getvalue()

    async def test_append_unknown(self):
        stub = TestStub([AppendResponse(
            result=Result(code=FAILURE, key='SomeUnknownKey'))])
        outfile = StringIO()
        args = Namespace(outfile=outfile,
                         admin_username='admuser', admin_password='admpass',
                         user='testuser', sender=None, recipient=None,
                         mailbox='INBOX', data=BytesIO(b'test data'),
                         flags=['\\Flagged', '\\Seen'],
                         timestamp=1234567890)
        command = AppendCommand(stub, args)
        code = await command()
        request = stub.request
        assert 1 == code
        assert 'INBOX' == request.mailbox
        assert '4.3.0 Unhandled system error\n' == outfile.getvalue()

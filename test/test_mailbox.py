
from io import BytesIO, StringIO
from argparse import Namespace
from typing import Any

from grpclib.server import Stream
from grpclib.testing import ChannelFor

from pymapadmin.commands.mailbox import AppendCommand
from pymapadmin.grpc.admin_grpc import MailboxBase
from pymapadmin.grpc.admin_pb2 import Result, FAILURE, \
    AppendRequest, AppendResponse

from handler import MockHandler

_AppendStream = Stream[AppendRequest, AppendResponse]


class Handler(MailboxBase, MockHandler[Any, Any]):

    async def Append(self, stream: _AppendStream) -> None:
        await self._run(stream)


class TestAppendCommand:

    async def test_append(self) -> None:
        handler = Handler() \
            .expect(AppendRequest, [AppendResponse()])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None,
                         username='testuser', sender=None, recipient=None,
                         mailbox='INBOX', data=BytesIO(b'test data'),
                         flags=['\\Flagged', '\\Seen'],
                         timestamp=1234567890)
        async with ChannelFor([handler]) as channel:
            command = AppendCommand(args, channel)
            code = await command(outfile, errfile)
        assert 0 == code
        assert '2.0.0 Message delivered\n' == outfile.getvalue()
        assert '\n' == errfile.getvalue()
        request = handler.requests[0]
        assert b'test data' == request.data
        assert 1234567890.0 == request.when
        assert ['\\Flagged', '\\Seen'] == request.flags
        assert 'testuser' == request.user
        assert not request.HasField('sender')
        assert not request.HasField('recipient')
        assert 'INBOX' == request.mailbox

    async def test_append_failure(self) -> None:
        handler = Handler() \
            .expect(AppendRequest, [AppendResponse(result=Result(
                code=FAILURE, key='MailboxNotFound'))])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None,
                         username='testuser', sender=None, recipient=None,
                         mailbox='Bad', data=BytesIO(b'test data'),
                         flags=['\\Flagged', '\\Seen'],
                         timestamp=1234567890)
        async with ChannelFor([handler]) as channel:
            command = AppendCommand(args, channel)
            code = await command(outfile, errfile)
        assert 1 == code
        assert '4.2.0 Message not deliverable\n' == outfile.getvalue()
        assert 'code: FAILURE\nkey: "MailboxNotFound"\n\n' \
            == errfile.getvalue()
        request = handler.requests[0]
        assert 'Bad' == request.mailbox

    async def test_append_unknown(self) -> None:
        handler = Handler() \
            .expect(AppendRequest, [AppendResponse(result=Result(
                code=FAILURE, key='SomeUnknownKey'))])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None,
                         username='testuser', sender=None, recipient=None,
                         mailbox='INBOX', data=BytesIO(b'test data'),
                         flags=['\\Flagged', '\\Seen'],
                         timestamp=1234567890)
        async with ChannelFor([handler]) as channel:
            command = AppendCommand(args, channel)
            code = await command(outfile, errfile)
        assert 1 == code
        assert '4.3.0 Unhandled system error\n' == outfile.getvalue()
        assert 'code: FAILURE\nkey: "SomeUnknownKey"\n\n' == errfile.getvalue()
        request = handler.requests[0]
        assert 'INBOX' == request.mailbox

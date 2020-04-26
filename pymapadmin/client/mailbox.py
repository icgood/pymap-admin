
from __future__ import annotations

import sys
import time
from argparse import FileType
from typing import Any, TextIO, AsyncContextManager

from grpclib.client import Channel, Stream

from .command import RequestT, ResponseT, ClientCommand
from ..grpc.admin_grpc import MailboxStub
from ..grpc.admin_pb2 import AppendRequest, AppendResponse


class MailboxBase(ClientCommand[MailboxStub, RequestT, ResponseT]):

    @classmethod
    def get_stub(cls, channel: Channel) -> MailboxStub:
        return MailboxStub(channel)


class AppendCommand(MailboxBase[AppendRequest, AppendResponse]):
    """Append a message directly to a user's mailbox."""

    success = '2.0.0 Message delivered'
    messages = {'InvalidAuth': '5.7.8 Authentication credentials invalid',
                'TimedOut': '4.4.2 Connection timed out',
                'ConnectionFailed': '4.3.0 Connection failed',
                'UnhandledError': '4.3.0 Unhandled system error',
                'MailboxNotFound': '4.2.0 Message not deliverable',
                'AppendFailure': '4.2.0 Message not deliverable'}

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> None:  # pragma: no cover
        subparser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='append a message to a mailbox')
        subparser.add_argument('--from', metavar='ADDRESS', dest='sender',
                               default='', help='the message envelope sender')
        subparser.add_argument('--to', metavar='ADDRESS', dest='recipient',
                               help='the message envelope recipient')
        subparser.add_argument('--mailbox', metavar='NAME',
                               help='the mailbox name')
        subparser.add_argument('--timestamp', type=int, metavar='SECONDS',
                               help='the message timestamp (default: now)')
        subparser.add_argument('--data', type=FileType('rb'), metavar='FILE',
                               default=sys.stdin.buffer,
                               help='the message data (default: stdin)')
        subparser.add_argument('user', help='the user name')
        flags = subparser.add_argument_group('message flags')
        flags.add_argument('--flag', dest='flags', action='append',
                           metavar='VAL', help='a message flag or keyword')
        flags.add_argument('--flagged', dest='flags', action='append_const',
                           const='\\Flagged', help='the message is flagged')
        flags.add_argument('--seen', dest='flags', action='append_const',
                           const='\\Seen', help='the message is seen')
        flags.add_argument('--draft', dest='flags', action='append_const',
                           const='\\Draft', help='the message is a draft')
        flags.add_argument('--deleted', dest='flags', action='append_const',
                           const='\\Deleted', help='the message is deleted')
        flags.add_argument('--answered', dest='flags', action='append_const',
                           const='\\Answered', help='the message is answered')

    def open(self) -> AsyncContextManager[
            Stream[AppendRequest, AppendResponse]]:
        return self.stub.Append.open()

    def build_request(self) -> AppendRequest:
        args = self.args
        recipient = args.recipient or args.user
        data = args.data.read()
        when: int = args.timestamp or int(time.time())
        login = self.get_login(args.user)
        return AppendRequest(login=login, sender=args.sender,
                             recipient=recipient, mailbox=args.mailbox,
                             data=data, flags=args.flags, when=when)

    def print_success(self, res: AppendResponse, outfile: TextIO) -> None:
        print(res, file=sys.stderr)
        print(self.success, file=outfile)

    def print_failure(self, res: AppendResponse, outfile: TextIO) -> None:
        print(res.result, file=sys.stderr)
        print(self.messages[res.result.key], file=outfile)

    def handle_exception(self, exc: Exception, outfile: TextIO) -> int:
        ret = super().handle_exception(exc, outfile)
        print(self.messages['UnhandledError'], file=outfile)
        return ret

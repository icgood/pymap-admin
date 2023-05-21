
from io import StringIO
from argparse import Namespace
from typing import Any

from grpclib.server import Stream
from grpclib.testing import ChannelFor

from pymapadmin.commands.system import LoginCommand, PingCommand
from pymapadmin.grpc.admin_grpc import SystemBase
from pymapadmin.grpc.admin_pb2 import LoginRequest, LoginResponse, \
    PingRequest, PingResponse, Result, FAILURE

from handler import MockHandler

_PingStream = Stream[PingRequest, PingResponse]
_LoginStream = Stream[LoginRequest, LoginResponse]


class Handler(SystemBase, MockHandler[Any, Any]):

    async def Ping(self, stream: _PingStream) -> None:
        await self._run(stream)

    async def Login(self, stream: _LoginStream) -> None:
        await self._run(stream)


class TestLoginCommand:

    async def test_login(self) -> None:
        handler = Handler() \
            .expect(LoginRequest, [LoginResponse(bearer_token='123abc')])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None,
                         user='testuser', password='testpass',
                         authzid=None, expiration=None, save=False,
                         ask_password=False, password_file=None)
        async with ChannelFor([handler]) as channel:
            command = LoginCommand(args, channel)
            code = await command(outfile, errfile)
        assert 0 == code
        assert 'bearer_token: "123abc"\n\n' == outfile.getvalue()
        assert '' == errfile.getvalue()
        request = handler.requests[0]
        assert 'testuser' == request.authcid
        assert 'testpass' == request.secret
        assert not request.HasField('authzid')
        assert not request.HasField('token_expiration')

    async def test_login_password_file(self) -> None:
        handler = Handler() \
            .expect(LoginRequest, [LoginResponse(bearer_token='123abc')])
        outfile = StringIO()
        errfile = StringIO()
        pw_file = StringIO('testpass\n')
        args = Namespace(token=None, token_file=None,
                         user='testuser', password=None,
                         authzid=None, expiration=None, save=False,
                         ask_password=False, password_file=pw_file)
        async with ChannelFor([handler]) as channel:
            command = LoginCommand(args, channel)
            code = await command(outfile, errfile)
        assert 0 == code
        assert 'bearer_token: "123abc"\n\n' == outfile.getvalue()
        assert '' == errfile.getvalue()
        request = handler.requests[0]
        assert 'testuser' == request.authcid
        assert 'testpass' == request.secret
        assert not request.HasField('authzid')
        assert not request.HasField('token_expiration')


class TestPingCommand:

    async def test_ping(self) -> None:
        handler = Handler() \
            .expect(PingRequest, [PingResponse(pymap_version='test1',
                                               pymap_admin_version='test2')])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None)
        async with ChannelFor([handler]) as channel:
            command = PingCommand(args, channel)
            code = await command(outfile, errfile)
        assert 0 == code
        assert 'pymap_version: "test1"\npymap_admin_version: "test2"\n\n' \
            == outfile.getvalue()
        assert '' == errfile.getvalue()

    async def test_ping_failure(self) -> None:
        handler = Handler() \
            .expect(PingRequest, [PingResponse(result=Result(code=FAILURE))])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None)
        async with ChannelFor([handler]) as channel:
            command = PingCommand(args, channel)
            code = await command(outfile, errfile)
        assert 1 == code
        assert '' == outfile.getvalue()
        assert 'code: FAILURE\n\n' == errfile.getvalue()

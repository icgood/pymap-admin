
from io import StringIO
from argparse import Namespace

import pytest
from grpclib.testing import ChannelFor
from pymapadmin.commands.system import LoginCommand, PingCommand
from pymapadmin.grpc.admin_grpc import SystemBase
from pymapadmin.grpc.admin_pb2 import LoginRequest, LoginResponse, \
    PingRequest, PingResponse, Result, FAILURE

from handler import RequestT, ResponseT, MockHandler

pytestmark = pytest.mark.asyncio


class Handler(SystemBase, MockHandler[RequestT, ResponseT]):

    async def Ping(self, stream) -> None:
        await self._run(stream)

    async def Login(self, stream) -> None:
        await self._run(stream)


class TestLoginCommand:

    async def test_login(self) -> None:
        handler = Handler(LoginRequest, [LoginResponse(
            bearer_token='123abc')])
        args = Namespace(token=None, token_file=None,
                         user='testuser', password='testpass',
                         authzid=None, expiration=None, save=False,
                         ask_password=False, password_file=None)
        async with ChannelFor([handler]) as channel:
            command = LoginCommand(args, channel)
            code = await command(StringIO())
        request = handler.request
        assert 0 == code
        assert 'testuser' == request.authcid
        assert 'testpass' == request.secret
        assert not request.HasField('authzid')
        assert not request.HasField('token_expiration')

    async def test_login_password_file(self) -> None:
        handler = Handler(LoginRequest, [LoginResponse(
            bearer_token='123abc')])
        pw_file = StringIO('testpass\n')
        args = Namespace(token=None, token_file=None,
                         user='testuser', password=None,
                         authzid=None, expiration=None, save=False,
                         ask_password=False, password_file=pw_file)
        async with ChannelFor([handler]) as channel:
            command = LoginCommand(args, channel)
            code = await command(StringIO())
        request = handler.request
        assert 0 == code
        assert 'testuser' == request.authcid
        assert 'testpass' == request.secret
        assert not request.HasField('authzid')
        assert not request.HasField('token_expiration')


class TestPingCommand:

    async def test_ping(self) -> None:
        handler = Handler(PingRequest, [PingResponse(
            pymap_version='test1', pymap_admin_version='test2')])
        args = Namespace(token=None, token_file=None)
        async with ChannelFor([handler]) as channel:
            command = PingCommand(args, channel)
            code = await command(StringIO())
        assert 0 == code

    async def test_ping_failure(self) -> None:
        handler = Handler(PingRequest, [PingResponse(
            result=Result(code=FAILURE))])
        args = Namespace(token=None, token_file=None)
        async with ChannelFor([handler]) as channel:
            command = PingCommand(args, channel)
            code = await command(StringIO())
        assert 1 == code

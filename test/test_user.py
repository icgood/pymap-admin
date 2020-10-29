
from io import StringIO
from argparse import Namespace

import pytest  # type: ignore
from grpclib.testing import ChannelFor
from unittest.mock import MagicMock

from pymapadmin.commands.user import GetUserCommand, SetUserCommand, \
    DeleteUserCommand
from pymapadmin.grpc.admin_grpc import UserBase
from pymapadmin.grpc.admin_pb2 import \
    GetUserRequest, SetUserRequest, DeleteUserRequest, UserResponse

from handler import RequestT, ResponseT, MockHandler

pytestmark = pytest.mark.asyncio


class Handler(UserBase, MockHandler[RequestT, ResponseT]):

    async def GetUser(self, stream) -> None:
        await self._run(stream)

    async def SetUser(self, stream) -> None:
        await self._run(stream)

    async def DeleteUser(self, stream) -> None:
        await self._run(stream)


class TestGetUserCommand:

    async def test_get_user(self) -> None:
        handler = Handler(GetUserRequest, [UserResponse(username='user1')])
        outfile = StringIO()
        args = Namespace(token=None, token_file=None, username='user1')
        async with ChannelFor([handler]) as channel:
            command = GetUserCommand(args, channel)
            code = await command(outfile)
        request = handler.request
        assert 0 == code
        assert request is not None
        assert 'user1' == request.user
        assert 'username: "user1"\n\n' == outfile.getvalue()


class TestDeleteUserCommand:

    async def test_delete_user(self) -> None:
        handler = Handler(DeleteUserRequest, [UserResponse(username='user1')])
        outfile = StringIO()
        args = Namespace(token=None, token_file=None, username='user1')
        async with ChannelFor([handler]) as channel:
            command = DeleteUserCommand(args, channel)
            code = await command(outfile)
        request = handler.request
        assert 0 == code
        assert request is not None
        assert 'user1' == request.user
        assert 'username: "user1"\n\n' == outfile.getvalue()


class TestSetUserCommand:

    async def test_set_user_no_password(self) -> None:
        handler = Handler(SetUserRequest, [UserResponse(username='user1')])
        outfile = StringIO()
        args = Namespace(token=None, token_file=None,
                         username='user1', no_password=True,
                         params=['identity=test'])
        async with ChannelFor([handler]) as channel:
            command = SetUserCommand(args, channel)
            code = await command(outfile)
        request = handler.request
        assert 0 == code
        assert request is not None
        assert 'user1' == request.user
        assert '' == request.data.password
        assert {'identity': 'test'} == request.data.params
        assert 'username: "user1"\n\n' == outfile.getvalue()

    async def test_set_user_password_file(self) -> None:
        handler = Handler(SetUserRequest, [UserResponse(username='user1')])
        outfile = StringIO()
        pw_file = MagicMock()
        pw_file.readline.return_value = 'testpass'
        args = Namespace(token=None, token_file=None,
                         username='user1', no_password=False,
                         password_file=pw_file, params=['identity=test'])
        async with ChannelFor([handler]) as channel:
            command = SetUserCommand(args, channel)
            code = await command(outfile)
        request = handler.request
        assert 0 == code
        assert request is not None
        assert 'user1' == request.user
        assert 'testpass' == request.data.password
        assert {'identity': 'test'} == request.data.params
        assert 'username: "user1"\n\n' == outfile.getvalue()


from io import StringIO
from argparse import Namespace
from typing import Any

import pytest
from grpclib.server import Stream
from grpclib.testing import ChannelFor

from pymapadmin.commands.user import GetUserCommand, SetUserCommand, \
    DeleteUserCommand
from pymapadmin.grpc.admin_grpc import UserBase
from pymapadmin.grpc.admin_pb2 import \
    GetUserRequest, SetUserRequest, DeleteUserRequest, UserResponse

from handler import MockHandler

_GetUserStream = Stream[GetUserRequest, UserResponse]
_SetUserStream = Stream[SetUserRequest, UserResponse]
_DeleteUserStream = Stream[DeleteUserRequest, UserResponse]


class Handler(UserBase, MockHandler[Any, UserResponse]):

    async def GetUser(self, stream: _GetUserStream) -> None:
        await self._run(stream)

    async def SetUser(self, stream: _SetUserStream) -> None:
        await self._run(stream)

    async def DeleteUser(self, stream: _DeleteUserStream) -> None:
        await self._run(stream)


class TestGetUserCommand:

    async def test_get_user(self) -> None:
        handler = Handler(GetUserRequest, [UserResponse(user='user1')])
        outfile = StringIO()
        args = Namespace(token=None, token_file=None, user='user1')
        async with ChannelFor([handler]) as channel:
            command = GetUserCommand(args, channel)
            code = await command(outfile)
        request = handler.request
        assert 0 == code
        assert request is not None
        assert 'user1' == request.user
        assert 'user: "user1"\n\n' == outfile.getvalue()


class TestDeleteUserCommand:

    async def test_delete_user(self) -> None:
        handler = Handler(DeleteUserRequest, [UserResponse(user='user1')])
        outfile = StringIO()
        args = Namespace(token=None, token_file=None, user='user1')
        async with ChannelFor([handler]) as channel:
            command = DeleteUserCommand(args, channel)
            code = await command(outfile)
        request = handler.request
        assert 0 == code
        assert request is not None
        assert 'user1' == request.user
        assert 'user: "user1"\n\n' == outfile.getvalue()


class TestSetUserCommand:

    async def test_set_user_bad_param(self) -> None:
        handler = Handler(SetUserRequest, [UserResponse(user='user1')])
        outfile = StringIO()
        args = Namespace(token=None, token_file=None,
                         user='user1', no_password=True, roles=[],
                         params=['identity=test', 'badparam'])
        async with ChannelFor([handler]) as channel:
            command = SetUserCommand(args, channel)
            with pytest.raises(ValueError):
                await command(outfile)

    async def test_set_user_no_password(self) -> None:
        handler = Handler(SetUserRequest, [UserResponse(user='user1')])
        outfile = StringIO()
        args = Namespace(token=None, token_file=None,
                         user='user1', no_password=True, roles=['fancy'],
                         params=['identity=test'])
        async with ChannelFor([handler]) as channel:
            command = SetUserCommand(args, channel)
            code = await command(outfile)
        request = handler.request
        assert 0 == code
        assert request is not None
        assert 'user1' == request.user
        assert '' == request.data.password
        assert ['fancy'] == request.data.roles
        assert {'identity': 'test'} == request.data.params
        assert 'user: "user1"\n\n' == outfile.getvalue()

    async def test_set_user_password_file(self) -> None:
        handler = Handler(SetUserRequest, [UserResponse(user='user1')])
        outfile = StringIO()
        pw_file = StringIO('testpass\n')
        args = Namespace(token=None, token_file=None,
                         user='user1', no_password=False, roles=[],
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
        assert 'user: "user1"\n\n' == outfile.getvalue()

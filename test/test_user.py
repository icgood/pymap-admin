
from io import StringIO
from argparse import Namespace
from typing import Any

import pytest
from grpclib.server import Stream
from grpclib.testing import ChannelFor

from pymapadmin.commands.user import GetUserCommand, SetUserCommand, \
    ChangePasswordCommand, DeleteUserCommand
from pymapadmin.grpc.admin_grpc import UserBase
from pymapadmin.grpc.admin_pb2 import \
    Result, FAILURE, UserResponse, \
    GetUserRequest, SetUserRequest, DeleteUserRequest

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
        handler = Handler() \
            .expect(GetUserRequest, [UserResponse(user='user1')])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None, user='user1')
        async with ChannelFor([handler]) as channel:
            command = GetUserCommand(args, channel)
            code = await command(outfile, errfile)
        assert 0 == code
        assert 'user: "user1"\n\n' == outfile.getvalue()
        assert '' == errfile.getvalue()
        request = handler.requests[0]
        assert request is not None
        assert 'user1' == request.user

    async def test_get_user_missing(self) -> None:
        handler = Handler() \
            .expect(GetUserRequest,
                    [UserResponse(result=Result(code=FAILURE))])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None, user='missing')
        async with ChannelFor([handler]) as channel:
            command = GetUserCommand(args, channel)
            code = await command(outfile, errfile)
        assert 1 == code
        assert '' == outfile.getvalue()
        assert 'code: FAILURE\n\n' == errfile.getvalue()
        request = handler.requests[0]
        assert request is not None
        assert 'missing' == request.user


class TestDeleteUserCommand:

    async def test_delete_user(self) -> None:
        handler = Handler() \
            .expect(DeleteUserRequest, [UserResponse(user='user1')])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None, user='user1')
        async with ChannelFor([handler]) as channel:
            command = DeleteUserCommand(args, channel)
            code = await command(outfile, errfile)
        assert 0 == code
        assert 'user: "user1"\n\n' == outfile.getvalue()
        assert '' == errfile.getvalue()
        request = handler.requests[0]
        assert request is not None
        assert 'user1' == request.user


class TestSetUserCommand:

    async def test_set_user_bad_param(self) -> None:
        handler = Handler() \
            .expect(SetUserRequest, [UserResponse(user='user1')])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None, overwrite=True,
                         user='user1', no_password=True, roles=[],
                         params=['identity=test', 'badparam'])
        async with ChannelFor([handler]) as channel:
            command = SetUserCommand(args, channel)
            with pytest.raises(ValueError):
                await command(outfile, errfile)

    async def test_set_user_no_password(self) -> None:
        handler = Handler() \
            .expect(SetUserRequest, [UserResponse(user='user1')])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None, overwrite=True,
                         user='user1', no_password=True, roles=['fancy'],
                         params=['identity=test'])
        async with ChannelFor([handler]) as channel:
            command = SetUserCommand(args, channel)
            code = await command(outfile, errfile)
        assert 0 == code
        assert 'user: "user1"\n\n' == outfile.getvalue()
        assert '' == errfile.getvalue()
        request = handler.requests[0]
        assert request is not None
        assert 'user1' == request.user
        assert '' == request.data.password
        assert ['fancy'] == request.data.roles
        assert {'identity': 'test'} == request.data.params

    async def test_set_user_password_file(self) -> None:
        handler = Handler() \
            .expect(SetUserRequest, [UserResponse(user='user1')])
        outfile = StringIO()
        errfile = StringIO()
        pw_file = StringIO('testpass\n')
        args = Namespace(token=None, token_file=None, overwrite=True,
                         user='user1', no_password=False, roles=[],
                         password_file=pw_file, params=['identity=test'])
        async with ChannelFor([handler]) as channel:
            command = SetUserCommand(args, channel)
            code = await command(outfile, errfile)
        assert 0 == code
        assert 'user: "user1"\n\n' == outfile.getvalue()
        assert '' == errfile.getvalue()
        request = handler.requests[0]
        assert request is not None
        assert 'user1' == request.user
        assert 'testpass' == request.data.password
        assert {'identity': 'test'} == request.data.params


class TestChangePasswordCommand:

    async def test_change_password(self) -> None:
        handler = Handler() \
            .expect(GetUserRequest,
                    [UserResponse(user='user1', entity_tag=12345)]) \
            .expect(SetUserRequest,
                    [UserResponse(user='user1')])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None,
                         user='user1', no_password=True, password_file=None)
        async with ChannelFor([handler]) as channel:
            command = ChangePasswordCommand(args, channel)
            code = await command(outfile, errfile)
        assert 0 == code
        assert 'user: "user1"\n\n' == outfile.getvalue()
        assert '' == errfile.getvalue()
        get_request = handler.requests[0]
        assert get_request is not None
        assert 'user1' == get_request.user
        set_request = handler.requests[1]
        assert set_request is not None
        assert 'user1' == set_request.user
        assert 12345 == set_request.previous_entity_tag

    async def test_change_password_invalid_user(self) -> None:
        handler = Handler() \
            .expect(GetUserRequest,
                    [UserResponse(result=Result(code=FAILURE))])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None,
                         user='user1', no_password=True, password_file=None)
        async with ChannelFor([handler]) as channel:
            command = ChangePasswordCommand(args, channel)
            code = await command(outfile, errfile)
        assert 1 == code
        assert '' == outfile.getvalue()
        assert 'code: FAILURE\n\n' == errfile.getvalue()

    async def test_change_password_failure(self) -> None:
        handler = Handler() \
            .expect(GetUserRequest,
                    [UserResponse(user='user1', entity_tag=12345)]) \
            .expect(SetUserRequest,
                    [UserResponse(result=Result(code=FAILURE))])
        outfile = StringIO()
        errfile = StringIO()
        args = Namespace(token=None, token_file=None,
                         user='user1', no_password=True, password_file=None)
        async with ChannelFor([handler]) as channel:
            command = ChangePasswordCommand(args, channel)
            code = await command(outfile, errfile)
        assert 1 == code
        assert '' == outfile.getvalue()
        assert 'code: FAILURE\n\n' == errfile.getvalue()

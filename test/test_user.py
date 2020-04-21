
from io import StringIO
from argparse import Namespace

import pytest  # type: ignore
from pymapadmin.client.user import ListUsersCommand, GetUserCommand, \
    SetUserCommand, DeleteUserCommand
from pymapadmin.grpc.admin_pb2 import UserResponse

from stub import StubChannel

pytestmark = pytest.mark.asyncio


class TestListUsersCommand:

    async def test_list_users(self):
        stub = StubChannel([UserResponse(username='user1'),
                            UserResponse(username='user2')])
        outfile = StringIO()
        args = Namespace(match=None)
        command = ListUsersCommand(stub, args)
        code = await command.run(outfile)
        request = stub.request
        assert 'ListUsers' == stub.method
        assert 0 == code
        assert '' == request.match
        assert 'user1\nuser2\n' == outfile.getvalue()


class TestGetUserCommand:

    async def test_get_user(self):
        stub = StubChannel([UserResponse(username='user1')])
        outfile = StringIO()
        args = Namespace(username='user1')
        command = GetUserCommand(stub, args)
        code = await command.run(outfile)
        request = stub.request
        assert 'GetUser' == stub.method
        assert 0 == code
        assert 'user1' == request[0].username
        assert 'username: "user1"\n\n' == outfile.getvalue()


class TestDeleteUserCommand:

    async def test_delete_user(self):
        stub = StubChannel([UserResponse(username='user1')])
        outfile = StringIO()
        args = Namespace(username='user1')
        command = DeleteUserCommand(stub, args)
        code = await command.run(outfile)
        request = stub.request
        assert 'DeleteUser' == stub.method
        assert 0 == code
        assert 'user1' == request[0].username
        assert '\n' == outfile.getvalue()


class TestSetUserCommand:

    def setup_method(self):
        SetUserCommand.getpass = lambda s: 'testpass'

    async def test_set_user(self):
        stub = StubChannel([UserResponse(username='user1')])
        outfile = StringIO()
        args = Namespace(username='user1', no_password=False, no_hash=False,
                         passlib_config=None,  param=[['identity', 'test']])
        command = SetUserCommand(stub, args)
        code = await command.run(outfile)
        request = stub.request
        assert 'SetUser' == stub.method
        assert 0 == code
        assert 'user1' == request[0].username
        assert '\n' == outfile.getvalue()

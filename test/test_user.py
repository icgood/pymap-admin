
from io import StringIO
from argparse import Namespace

import pytest  # type: ignore
from grpclib.client import Channel
from unittest.mock import MagicMock

from pymapadmin.client.user import ListUsersCommand, GetUserCommand, \
    SetUserCommand, DeleteUserCommand
from pymapadmin.grpc.admin_pb2 import ListUsersResponse, UserResponse

from stub import TestStub

pytestmark = pytest.mark.asyncio

channel = MagicMock(Channel)


class TestListUsersCommand:

    async def test_list_users(self):
        stub = TestStub([ListUsersResponse(users=['user1', 'user2']),
                         ListUsersResponse(users=['user3'])])
        outfile = StringIO()
        args = Namespace(outfile=outfile,
                         admin_username='admuser', admin_password='admpass',
                         match=None)
        command = ListUsersCommand(stub, args)
        code = await command()
        request = stub.request
        assert 'ListUsers' == stub.method
        assert 0 == code
        assert '' == request.match
        assert 'user1\nuser2\nuser3\n' == outfile.getvalue()


class TestGetUserCommand:

    async def test_get_user(self):
        stub = TestStub([UserResponse(username='user1')])
        outfile = StringIO()
        args = Namespace(outfile=outfile,
                         admin_username='admuser', admin_password='admpass',
                         username='user1')
        command = GetUserCommand(stub, args)
        code = await command()
        request = stub.request
        assert 'GetUser' == stub.method
        assert 0 == code
        assert 'user1' == request.login.authzid
        assert '' == outfile.getvalue()


class TestDeleteUserCommand:

    async def test_delete_user(self):
        stub = TestStub([UserResponse(username='user1')])
        outfile = StringIO()
        args = Namespace(outfile=outfile,
                         admin_username='admuser', admin_password='admpass',
                         username='user1')
        command = DeleteUserCommand(stub, args)
        code = await command()
        request = stub.request
        assert 'DeleteUser' == stub.method
        assert 0 == code
        assert 'user1' == request.login.authzid
        assert '' == outfile.getvalue()


class TestSetUserCommand:

    async def test_set_user_no_password(self):
        stub = TestStub([UserResponse(username='user1')])
        outfile = StringIO()
        args = Namespace(outfile=outfile,
                         admin_username='admuser', admin_password='admpass',
                         username='user1', no_password=True,
                         param=[['identity', 'test']])
        command = SetUserCommand(stub, args)
        code = await command()
        request = stub.request
        assert 'SetUser' == stub.method
        assert 0 == code
        assert 'user1' == request.login.authzid
        assert '' == request.data.password
        assert {'identity': 'test'} == request.data.params
        assert '' == outfile.getvalue()

    async def test_set_user_password_file(self):
        stub = TestStub([UserResponse(username='user1')])
        outfile = StringIO()
        pw_file = MagicMock()
        pw_file.readline.return_value = 'testpass'
        args = Namespace(outfile=outfile,
                         admin_username='admuser', admin_password='admpass',
                         username='user1', no_password=False,
                         password_file=pw_file,
                         param=[['identity', 'test']])
        command = SetUserCommand(stub, args)
        code = await command()
        request = stub.request
        assert 'SetUser' == stub.method
        assert 0 == code
        assert 'user1' == request.login.authzid
        assert 'testpass' == request.data.password
        assert {'identity': 'test'} == request.data.params
        assert '' == outfile.getvalue()

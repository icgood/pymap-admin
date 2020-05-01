
from io import StringIO
from argparse import Namespace

import pytest  # type: ignore
from grpclib.client import Channel
from unittest.mock import MagicMock

from pymapadmin.commands.user import ListUsersCommand, GetUserCommand, \
    SetUserCommand, DeleteUserCommand
from pymapadmin.grpc.admin_pb2 import ListUsersResponse, UserResponse

from client import MockClient

pytestmark = pytest.mark.asyncio

channel = MagicMock(Channel)


class TestListUsersCommand:

    async def test_list_users(self):
        client = MockClient([ListUsersResponse(users=['user1', 'user2']),
                             ListUsersResponse(users=['user3'])])
        outfile = StringIO()
        args = Namespace(admin_username='admuser', admin_password='admpass',
                         ask_password=False, match=None)
        command = ListUsersCommand(args, client)
        code = await command(outfile)
        request = client.request
        assert 'ListUsers' == client.method
        assert 0 == code
        assert '' == request.match
        assert 'user1\nuser2\nuser3\n' == outfile.getvalue()


class TestGetUserCommand:

    async def test_get_user(self):
        client = MockClient([UserResponse(username='user1')])
        outfile = StringIO()
        args = Namespace(admin_username='admuser', admin_password='admpass',
                         ask_password=False, username='user1')
        command = GetUserCommand(args, client)
        code = await command(outfile)
        request = client.request
        assert 'GetUser' == client.method
        assert 0 == code
        assert 'user1' == request.login.authzid
        assert 'username: "user1"\n\n' == outfile.getvalue()


class TestDeleteUserCommand:

    async def test_delete_user(self):
        client = MockClient([UserResponse(username='user1')])
        outfile = StringIO()
        args = Namespace(admin_username='admuser', admin_password='admpass',
                         ask_password=False, username='user1')
        command = DeleteUserCommand(args, client)
        code = await command(outfile)
        request = client.request
        assert 'DeleteUser' == client.method
        assert 0 == code
        assert 'user1' == request.login.authzid
        assert 'username: "user1"\n\n' == outfile.getvalue()


class TestSetUserCommand:

    async def test_set_user_no_password(self):
        client = MockClient([UserResponse(username='user1')])
        outfile = StringIO()
        args = Namespace(admin_username='admuser', admin_password='admpass',
                         ask_password=False, username='user1',
                         no_password=True, param=[['identity', 'test']])
        command = SetUserCommand(args, client)
        code = await command(outfile)
        request = client.request
        assert 'SetUser' == client.method
        assert 0 == code
        assert 'user1' == request.login.authzid
        assert '' == request.data.password
        assert {'identity': 'test'} == request.data.params
        assert 'username: "user1"\n\n' == outfile.getvalue()

    async def test_set_user_password_file(self):
        client = MockClient([UserResponse(username='user1')])
        outfile = StringIO()
        pw_file = MagicMock()
        pw_file.readline.return_value = 'testpass'
        args = Namespace(admin_username='admuser', admin_password='admpass',
                         ask_password=False, username='user1',
                         no_password=False, password_file=pw_file,
                         param=[['identity', 'test']])
        command = SetUserCommand(args, client)
        code = await command(outfile)
        request = client.request
        assert 'SetUser' == client.method
        assert 0 == code
        assert 'user1' == request.login.authzid
        assert 'testpass' == request.data.password
        assert {'identity': 'test'} == request.data.params
        assert 'username: "user1"\n\n' == outfile.getvalue()

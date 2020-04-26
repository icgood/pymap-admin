
from __future__ import annotations

import getpass
from argparse import FileType
from typing import Any, Optional, Dict, TextIO, AsyncContextManager

from grpclib.client import Channel, Stream

from .command import RequestT, ResponseT, ClientCommand
from ..grpc.admin_grpc import UserStub
from ..grpc.admin_pb2 import ListUsersRequest, ListUsersResponse, \
    UserData, UserResponse, GetUserRequest, SetUserRequest, DeleteUserRequest


class UserBase(ClientCommand[UserStub, RequestT, ResponseT]):

    @classmethod
    def get_stub(self, channel: Channel) -> UserStub:
        return UserStub(channel)


class ListUsersCommand(UserBase[ListUsersRequest, ListUsersResponse]):
    """List all matching users."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> None:  # pragma: no cover
        subparser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='list users')
        subparser.add_argument('match', nargs='?',
                               help='the user name match string')

    def open(self) -> AsyncContextManager[
            Stream[ListUsersRequest, ListUsersResponse]]:
        return self.stub.ListUsers.open()

    def build_request(self) -> ListUsersRequest:
        return ListUsersRequest(login=self.get_login(), match=self.args.match)

    def print_success(self, res: ListUsersResponse, outfile: TextIO) -> None:
        for user in res.users:
            print(user, file=outfile)


class GetUserCommand(UserBase[GetUserRequest, UserResponse]):
    """Print a user and its metadata."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> None:  # pragma: no cover
        subparser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='get a user')
        subparser.add_argument('username', help='the user name')

    def open(self) -> AsyncContextManager[
            Stream[GetUserRequest, UserResponse]]:
        return self.stub.GetUser.open()

    def build_request(self) -> GetUserRequest:
        login = self.get_login(self.args.username)
        return GetUserRequest(login=login)


class SetUserCommand(UserBase[SetUserRequest, UserResponse]):
    """Set the metadata for a user, creating it if it does not exist."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> None:  # pragma: no cover
        subparser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='assign a password to a user')
        subparser.add_argument('--password-file', type=FileType('r'),
                               metavar='FILE',
                               help='read the password from a file')
        subparser.add_argument('--param', action='append',
                               nargs=2, metavar=('KEY', 'VAL'),
                               help='additional parameters for the request')
        subparser.add_argument('--no-password', action='store_true',
                               help='send the request with no password value')
        subparser.add_argument('username', help='the user name')

    def open(self) -> AsyncContextManager[
            Stream[SetUserRequest, UserResponse]]:
        return self.stub.SetUser.open()

    def getpass(self) -> Optional[str]:
        if self.args.no_password:
            return None
        elif self.args.password_file:
            line = self.args.password_file.readline()
            return line.rstrip('\r\n')
        else:
            return getpass.getpass()

    def build_request(self) -> SetUserRequest:
        args = self.args
        login = self.get_login(args.username)
        params: Dict[str, str] = dict(args.param or [])
        password = self.getpass()
        new_data = UserData(password=password,
                            params=params)
        return SetUserRequest(login=login, data=new_data)


class DeleteUserCommand(UserBase[DeleteUserRequest, UserResponse]):
    """Delete a user and its mail data."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> None:  # pragma: no cover
        subparser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='delete a user')
        subparser.add_argument('username', help='the user name')

    def open(self) -> AsyncContextManager[
            Stream[DeleteUserRequest, UserResponse]]:
        return self.stub.DeleteUser.open()

    def build_request(self) -> DeleteUserRequest:
        args = self.args
        login = self.get_login(args.username)
        return DeleteUserRequest(login=login)

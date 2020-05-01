
from __future__ import annotations

import getpass
from argparse import ArgumentParser, FileType
from typing import Any, Optional, Dict, TextIO

from grpclib.client import Channel

from . import Command
from ..typing import RequestT, ResponseT, MethodProtocol
from ..grpc.admin_grpc import UserStub
from ..grpc.admin_pb2 import ListUsersRequest, ListUsersResponse, \
    UserData, UserResponse, GetUserRequest, SetUserRequest, DeleteUserRequest


class UserCommand(Command[UserStub, RequestT, ResponseT]):

    @classmethod
    def get_client(self, channel: Channel) -> UserStub:
        return UserStub(channel)


class ListUsersCommand(UserCommand[ListUsersRequest, ListUsersResponse]):
    """List all matching users."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> ArgumentParser:  # pragma: no cover
        subparser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='list users')
        subparser.add_argument('match', nargs='?',
                               help='the user name match string')
        return subparser

    @property
    def method(self) -> MethodProtocol[ListUsersRequest, ListUsersResponse]:
        return self.client.ListUsers

    def build_request(self) -> ListUsersRequest:
        return ListUsersRequest(login=self.get_login(), match=self.args.match)

    def print_success(self, res: ListUsersResponse, outfile: TextIO) -> None:
        for user in res.users:
            print(user, file=outfile)


class GetUserCommand(UserCommand[GetUserRequest, UserResponse]):
    """Print a user and its metadata."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> ArgumentParser:  # pragma: no cover
        subparser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='get a user')
        subparser.add_argument('username', help='the user name')
        return subparser

    @property
    def method(self) -> MethodProtocol[GetUserRequest, UserResponse]:
        return self.client.GetUser

    def build_request(self) -> GetUserRequest:
        login = self.get_login(self.args.username)
        return GetUserRequest(login=login)


class SetUserCommand(UserCommand[SetUserRequest, UserResponse]):
    """Set the metadata for a user, creating it if it does not exist."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> ArgumentParser:  # pragma: no cover
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
        return subparser

    @property
    def method(self) -> MethodProtocol[SetUserRequest, UserResponse]:
        return self.client.SetUser

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


class DeleteUserCommand(UserCommand[DeleteUserRequest, UserResponse]):
    """Delete a user and its mail data."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> ArgumentParser:  # pragma: no cover
        subparser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='delete a user')
        subparser.add_argument('username', help='the user name')
        return subparser

    @property
    def method(self) -> MethodProtocol[DeleteUserRequest, UserResponse]:
        return self.client.DeleteUser

    def build_request(self) -> DeleteUserRequest:
        args = self.args
        login = self.get_login(args.username)
        return DeleteUserRequest(login=login)

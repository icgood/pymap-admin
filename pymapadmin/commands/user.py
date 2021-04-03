
from __future__ import annotations

import getpass
from argparse import ArgumentParser, FileType
from collections.abc import Mapping, Sequence
from typing import Any, Optional

from .base import ClientCommand
from ..typing import RequestT, ResponseT, MethodProtocol
from ..grpc.admin_grpc import UserStub
from ..grpc.admin_pb2 import \
    UserData, UserResponse, GetUserRequest, SetUserRequest, DeleteUserRequest

__all__ = ['GetUserCommand', 'SetUserCommand', 'DeleteUserCommand']


class UserCommand(ClientCommand[UserStub, RequestT, ResponseT]):

    @property
    def client(self) -> UserStub:
        return UserStub(self.channel)


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
        return GetUserRequest(user=self.args.username)


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
        subparser.add_argument('--param', action='append', dest='params',
                               default=[], metavar='KEY=VAL',
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
        params = self._parse_params(args.params)
        password = self.getpass()
        new_data = UserData(params=params)
        if password is not None:
            new_data.password = password
        return SetUserRequest(user=args.username, data=new_data)

    def _parse_params(self, params: Sequence[str]) -> Mapping[str, str]:
        ret = {}
        for param in params:
            key, splitter, val = param.partition('=')
            if not splitter:
                raise ValueError(f'Expected key=val format: {param!r}')
            ret[key] = val
        return ret


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
        return DeleteUserRequest(user=self.args.username)

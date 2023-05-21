
from __future__ import annotations

import getpass
from argparse import ArgumentParser, FileType
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, TypeAlias

from .base import AdminCommand
from ..grpc.admin_grpc import UserStub
from ..grpc.admin_pb2 import \
    SUCCESS, UserData, UserResponse, GetUserRequest, SetUserRequest, \
    DeleteUserRequest
from ..operation import SingleOperation, CompoundOperation
from ..typing import AdminRequestT, AdminResponseT, MethodProtocol

__all__ = ['GetUserCommand', 'SetUserCommand', 'ChangePasswordCommand',
           'DeleteUserCommand']

_Password: TypeAlias = str | None


@dataclass(frozen=True)
class _ChangePasswordRequest:
    user: str
    password: _Password


class UserCommand(AdminCommand[UserStub, AdminRequestT, AdminResponseT]):

    @property
    def client(self) -> UserStub:
        return UserStub(self.channel)

    def getpass(self) -> _Password:
        if self.args.no_password:
            return None
        elif self.args.password_file:
            line: str = self.args.password_file.readline()
            return line.rstrip('\r\n')
        else:  # pragma: no cover
            return getpass.getpass()


class GetUserCommand(UserCommand[GetUserRequest, UserResponse],
                     SingleOperation[GetUserRequest, UserResponse]):
    """Print a user and its metadata."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> ArgumentParser:  # pragma: no cover
        subparser: ArgumentParser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='get a user')
        subparser.add_argument('user', help='the user name')
        return subparser

    @property
    def method(self) -> MethodProtocol[GetUserRequest, UserResponse]:
        return self.client.GetUser

    def build_request(self) -> GetUserRequest:
        return GetUserRequest(user=self.args.user)


class SetUserCommand(UserCommand[SetUserRequest, UserResponse],
                     SingleOperation[SetUserRequest, UserResponse]):
    """Set the metadata for a user, creating it if it does not exist."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> ArgumentParser:  # pragma: no cover
        subparser: ArgumentParser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='add or overwrite a user')
        subparser.add_argument('--no-overwrite',
                               action='store_false', dest='overwrite',
                               help='do not overwrite existing users')
        subparser.add_argument('--password-file',
                               type=FileType('r'), metavar='FILE',
                               help='read the password from a file')
        subparser.add_argument('--no-password', action='store_true',
                               help='send the request with no password value')
        subparser.add_argument('--param', action='append', dest='params',
                               default=[], metavar='KEY=VAL',
                               help='additional parameters for the request')
        subparser.add_argument('--role', action='append', dest='roles',
                               default=[], metavar='ROLE',
                               help='assigned roles for the user')
        subparser.add_argument('user', help='the user name')
        return subparser

    @property
    def method(self) -> MethodProtocol[SetUserRequest, UserResponse]:
        return self.client.SetUser

    def build_request(self) -> SetUserRequest:
        args = self.args
        params = self._parse_params(args.params)
        password = self.getpass()
        new_data = UserData(params=params, roles=args.roles)
        if password is not None:
            new_data.password = password
        return SetUserRequest(user=args.user,
                              overwrite=args.overwrite,
                              data=new_data)

    def _parse_params(self, params: Sequence[str]) -> Mapping[str, str]:
        ret = {}
        for param in params:
            key, splitter, val = param.partition('=')
            if not splitter:
                raise ValueError(f'Expected key=val format: {param!r}')
            ret[key] = val
        return ret


class ChangePasswordCommand(UserCommand[_ChangePasswordRequest, UserResponse],
                            CompoundOperation[_ChangePasswordRequest,
                                              GetUserRequest, UserResponse,
                                              SetUserRequest, UserResponse]):
    """Change a password for an existing user, without modifying any other
    metadata.

    """

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> ArgumentParser:  # pragma: no cover
        subparser: ArgumentParser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='assign a new password to a user')
        subparser.add_argument('--password-file', type=FileType('r'),
                               metavar='FILE',
                               help='read the password from a file')
        subparser.add_argument('--no-password', action='store_true',
                               help='send the request with no password value')
        subparser.add_argument('user', help='the user name')
        return subparser

    @property
    def first(self) -> GetUserCommand:
        return GetUserCommand(self.args, self.channel)

    @property
    def second(self) -> SetUserCommand:
        return SetUserCommand(self.args, self.channel)

    def build_first(self, request: _ChangePasswordRequest) -> GetUserRequest:
        return GetUserRequest(user=request.user)

    def build_second(self, request: _ChangePasswordRequest,
                     first_response: UserResponse) \
            -> tuple[SetUserRequest | None, UserResponse | None]:
        password = request.password
        if first_response.result.code != SUCCESS:
            return None, first_response
        user_data = first_response.data
        if password is None:
            user_data.ClearField('password')
        else:
            user_data.password = password
        second_request = SetUserRequest(
            user=request.user,
            previous_entity_tag=first_response.entity_tag,
            data=user_data)
        return second_request, None

    def build_request(self) -> _ChangePasswordRequest:
        args = self.args
        password = self.getpass()
        return _ChangePasswordRequest(args.user, password)


class DeleteUserCommand(UserCommand[DeleteUserRequest, UserResponse],
                        SingleOperation[DeleteUserRequest, UserResponse]):
    """Delete a user and its mail data."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> ArgumentParser:  # pragma: no cover
        subparser: ArgumentParser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='delete a user')
        subparser.add_argument('user', help='the user name')
        return subparser

    @property
    def method(self) -> MethodProtocol[DeleteUserRequest, UserResponse]:
        return self.client.DeleteUser

    def build_request(self) -> DeleteUserRequest:
        return DeleteUserRequest(user=self.args.user)

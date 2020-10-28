
from __future__ import annotations

import getpass
from argparse import ArgumentParser, FileType
from contextlib import closing
from typing import Any, Optional, TextIO

from .base import ClientCommand
from ..typing import RequestT, ResponseT, MethodProtocol
from ..grpc.admin_grpc import SystemStub
from ..grpc.admin_pb2 import LoginRequest, LoginResponse, \
    PingRequest, PingResponse

__all__ = ['LoginCommand', 'PingCommand']


class SystemCommand(ClientCommand[SystemStub, RequestT, ResponseT]):

    @property
    def client(self) -> SystemStub:
        return SystemStub(self.channel)


class LoginCommand(SystemCommand[LoginRequest, LoginResponse]):
    """Login as a user for future requests."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> ArgumentParser:  # pragma: no cover
        subparser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='login as a user')
        subparser.add_argument('-s', '--save', action='store_true',
                               help='save the login token')
        subparser.add_argument('-z', '--authzid', metavar='NAME',
                               help='authorization identity name')
        subparser.add_argument('--expiration', metavar='TIMESTAMP', type=float,
                               help='token expiration timestamp')
        password = subparser.add_mutually_exclusive_group(required=True)
        password.add_argument('--password', metavar='VAL',
                              help='login password')
        password.add_argument('--password-file', metavar='PATH',
                              type=FileType(),
                              help='file containing login password')
        password.add_argument('-i', '--ask-password', action='store_true',
                              help='read login password from terminal')
        subparser.add_argument('user', help='login username')
        return subparser

    @property
    def method(self) -> MethodProtocol[LoginRequest, LoginResponse]:
        return self.client.Login

    def build_request(self) -> LoginRequest:
        username: str = self.args.user
        authzid: Optional[str] = self.args.authzid
        expiration: Optional[float] = self.args.expiration
        if self.args.ask_password:
            password = getpass.getpass(f'{username} Password: ')
        elif self.args.password_file is not None:
            with closing(self.args.password_file) as pw_file:
                password = pw_file.read()
        else:
            password = self.args.password
        return LoginRequest(authcid=username, secret=password, authzid=authzid,
                            token_expiration=expiration)

    def handle_success(self, response: LoginResponse, outfile: TextIO) -> None:
        super().handle_success(response, outfile)
        token = response.bearer_token
        if token and self.args.save:
            self.config.token = token
            self.config.flush()


class PingCommand(SystemCommand[PingRequest, PingResponse]):
    """Ping the server."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> ArgumentParser:  # pragma: no cover
        return subparsers.add_parser(
            name, description=cls.__doc__,
            help='ping the server')

    @property
    def method(self) -> MethodProtocol[PingRequest, PingResponse]:
        return self.client.Ping

    def build_request(self) -> PingRequest:
        return PingRequest()
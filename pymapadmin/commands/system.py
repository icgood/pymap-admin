
from __future__ import annotations

import getpass
from argparse import ArgumentParser, FileType
from contextlib import closing
from typing import Any, Optional, TextIO

from .base import Command, ClientCommand
from ..config import Config
from ..local import config_file, token_file
from ..typing import RequestT, ResponseT, MethodProtocol
from ..grpc.admin_grpc import SystemStub
from ..grpc.admin_pb2 import LoginRequest, LoginResponse, \
    PingRequest, PingResponse

__all__ = ['SaveArgsCommand', 'LoginCommand', 'PingCommand']


class SystemCommand(ClientCommand[SystemStub, RequestT, ResponseT]):

    @property
    def client(self) -> SystemStub:
        return SystemStub(self.channel)


class SaveArgsCommand(Command):
    """Save the connection settings given as command-line arguments (e.g.
    --host, --port, etc) to a config file.

    """

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> ArgumentParser:  # pragma: no cover
        subparser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='save connection arguments to config file')
        return subparser

    async def __call__(self, outfile: TextIO) -> int:
        path = config_file.get_home(mkdir=True)
        parser = Config.build(self.args)
        with open(path, 'w') as cfg:
            parser.write(cfg)
        print('Config file written:', path, file=outfile)
        return 0


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
                password = pw_file.readline().rstrip('\r\n')
        else:
            password = self.args.password
        request = LoginRequest(authcid=username, secret=password)
        if authzid is not None:
            request.authzid = authzid
        if expiration is not None:
            request.token_expiration = expiration
        return request

    def handle_success(self, response: LoginResponse, outfile: TextIO) -> None:
        super().handle_success(response, outfile)
        token = response.bearer_token
        if token and self.args.save:
            path = token_file.get_home(mkdir=True)
            path.write_text(token)
            path.chmod(0o600)


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


from __future__ import annotations

import getpass
from argparse import Namespace
from typing import Any, Optional, Dict, TextIO

from pysasl.hashing import get_hash

from .command import ClientCommand
from ..grpc.admin_pb2 import UserData, ListUsersRequest, \
    GetUserRequest, SetUserRequest, DeleteUserRequest


class ListUsersCommand(ClientCommand):
    """List all matching users."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> None:  # pragma: no cover
        subparser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='list users')
        subparser.add_argument('match', nargs='?',
                               help='the user name match string')

    async def run(self, outfile: TextIO) -> int:
        args = self.args
        req = ListUsersRequest(match=args.match)
        res_list = await self.stub.ListUsers(req)
        for res in res_list:
            print(res.username, file=outfile)
        return 0


class GetUserCommand(ClientCommand):
    """Print a user and its metadata."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> None:  # pragma: no cover
        subparser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='get a user')
        subparser.add_argument('username', help='the user name')

    async def run(self, outfile: TextIO) -> int:
        args = self.args
        req = GetUserRequest(username=args.username)
        res = await self.stub.GetUser([req])
        print(res[0], file=outfile)
        return res[0].username != req.username


class SetUserCommand(ClientCommand):
    """Set the metadata for a user, creating it if it does not exist."""

    @classmethod
    def getpass(cls) -> str:
        return getpass.getpass()

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> None:  # pragma: no cover
        subparser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='assign a password to a user')
        subparser.add_argument('--param', action='append',
                               nargs=2, metavar=('KEY', 'VAL'),
                               help='additional parameters for the request')
        subparser.add_argument('--no-password', action='store_true',
                               help='send the request with no password value')
        subparser.add_argument('username', help='the user name')
        group = subparser.add_argument_group('password hashing')
        group.add_argument('--no-hash', action='store_true',
                           help='disable password hashing')
        group.add_argument('--passlib-config', metavar='FILE',
                           help='passlib configuration file')

    async def run(self, outfile: TextIO) -> int:
        args = self.args
        params: Dict[str, str] = dict(args.param or [])
        password: Optional[str] = None
        if not args.no_password:
            password = self.getpass()
            if not args.no_hash:
                password = self._hash(args, password)
        new_data = UserData(password=password,
                            params=params)
        req = SetUserRequest(username=args.username, data=new_data)
        res = await self.stub.SetUser([req])
        print(res[0].result, file=outfile)
        return res[0].username != req.username

    def _hash(self, args: Namespace, password: str) -> str:
        hash_ctx = get_hash(passlib_config=args.passlib_config)
        return hash_ctx.hash(password)


class DeleteUserCommand(ClientCommand):
    """Delete a user and its mail data."""

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) \
            -> None:  # pragma: no cover
        subparser = subparsers.add_parser(
            name, description=cls.__doc__,
            help='delete a user')
        subparser.add_argument('username', help='the user name')

    async def run(self, outfile: TextIO) -> int:
        args = self.args
        req = DeleteUserRequest(username=args.username)
        res = await self.stub.DeleteUser([req])
        print(res[0].result, file=outfile)
        return res[0].username != req.username

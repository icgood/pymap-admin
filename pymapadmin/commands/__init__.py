
from __future__ import annotations

import sys
import getpass
import traceback
from abc import abstractmethod, ABCMeta
from argparse import ArgumentParser, Namespace
from typing import Generic, Any, TextIO
from typing_extensions import Final

from grpclib.client import Channel

from ..typing import StubT, RequestT, ResponseT, MethodProtocol
from ..grpc.admin_pb2 import Login, SUCCESS

__all__ = ['Command']


class Command(Generic[StubT, RequestT, ResponseT], metaclass=ABCMeta):
    """Interface for client command implementations.

    Args:
        args: The command line arguments.
        client: The client object.

    """

    def __init__(self, args: Namespace, client: StubT) -> None:
        super().__init__()
        self.args: Final = args
        self.client: Final = client

    @classmethod
    @abstractmethod
    def get_client(cls, channel: Channel) -> StubT:
        """Get the client object for the command.

        Args:
            channel: The GRPC channel for executing commands.

        """
        ...

    @classmethod
    @abstractmethod
    def add_subparser(cls, name: str, subparsers: Any) -> ArgumentParser:
        """Add the command-line argument subparser for the command.

        Args:
            name: The name to use for the subparser.
            subparsers: The special action object as returned by
                :meth:`~argparse.ArgumentParser.add_subparsers`.

        Returns:
            The new sub-parser object.

        """
        ...

    def get_login(self, user: str = None) -> Login:
        """Build and return a ``Login`` object containing the admin credentials
        and optionally the *user* to authorize as.

        Args:
            user: The user to authorize as using the admin credentials.

        """
        if self.args.admin_username is None:
            admin_username = user
        else:
            admin_username = self.args.admin_username
        if self.args.ask_password:
            admin_password = getpass.getpass(f'{admin_username} Password: ')
        else:
            admin_password = self.args.admin_password
        return Login(authcid=admin_username, secret=admin_password,
                     authzid=user)

    @property
    @abstractmethod
    def method(self) -> MethodProtocol[RequestT, ResponseT]:
        """The GRPC client method."""
        ...

    @abstractmethod
    def build_request(self) -> RequestT:
        """Build the request."""
        ...

    def handle_response(self, response: ResponseT, outfile: TextIO) -> int:
        """Handle each response. For streaming responses, this will be
        called once for each streamed response as long as ``0`` is returned.

        The default implementation calls :meth:`.print_success` or
        :meth:`.print_failure` depending on the result code.

        Args:
            response: The response from the server.
            outfile: The file object to print the output to.

        """
        if response.result.code == SUCCESS:
            self.print_success(response, outfile)
            return 0
        else:
            self.print_failure(response, outfile)
            return 1

    def print_success(self, response: ResponseT, outfile: TextIO) -> None:
        """Print a successful response.

        Args:
            response: The response from the server.
            outfile: The file object to print the output to.

        """
        print(response, file=outfile)

    def print_failure(self, response: ResponseT, outfile: TextIO) -> None:
        """Print a failure response.

        Args:
            response: The response from the server.
            outfile: The file object to print the output to.

        """
        print(response.result, file=sys.stderr)

    def handle_exception(self, exc: Exception, outfile: TextIO) -> int:
        """Handle an exception that occurred while calling the RPC function.

        Args:
            exc: The raised exception object.
            outfile: The file object to print the output to.

        """
        traceback.print_exc()
        return 1

    async def __call__(self, outfile: TextIO) -> int:
        req = self.build_request()
        try:
            async with self.method.open() as stream:
                await stream.send_message(req, end=True)
                async for res in stream:
                    ret = self.handle_response(res, outfile)
                    if ret != 0:
                        return ret
        except Exception as exc:
            return self.handle_exception(exc, outfile)
        else:
            return 0

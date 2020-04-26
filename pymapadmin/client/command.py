
from __future__ import annotations

import sys
import traceback
from abc import abstractmethod, ABCMeta
from argparse import Namespace
from typing import Generic, Any, TextIO, AsyncContextManager
from typing_extensions import Final

from grpclib.client import Channel, Stream

from ..typing import StubT, RequestT, ResponseT
from ..grpc.admin_pb2 import Login, SUCCESS

__all__ = ['ClientCommand']


class ClientCommand(Generic[StubT, RequestT, ResponseT], metaclass=ABCMeta):
    """Interface for client command implementations.

    Args:
        stub: The client stub object.
        args: The command line arguments.

    """

    def __init__(self, stub: StubT, args: Namespace) -> None:
        super().__init__()
        self.stub: Final = stub
        self.args: Final = args

    @classmethod
    @abstractmethod
    def get_stub(cls, channel: Channel) -> StubT:
        """Get the client stub object for the command.

        Args:
            channel: The GRPC channel for executing commands.

        """
        ...

    @classmethod
    @abstractmethod
    def add_subparser(cls, name: str, subparsers: Any) -> None:
        """Add the command-line argument subparser for the command.

        Args:
            name: The name to use for the subparser.
            subparsers: The special action object as returned by
                :meth:`~argparse.ArgumentParser.add_subparsers`.

        """
        ...

    def get_login(self, user: str = None) -> Login:
        """Build and return a ``Login`` object containing the admin credentials
        and optionally the *user* to authorize as.

        Args:
            user: The user to authorize as using the admin credentials.

        """
        return Login(authcid=self.args.admin_username,
                     secret=self.args.admin_password,
                     authzid=user)

    @abstractmethod
    def open(self) -> AsyncContextManager[Stream[RequestT, ResponseT]]:
        """Opens a stream for the GRPC command."""
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
        print(response, file=sys.stderr)

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

    async def __call__(self) -> int:
        args = self.args
        req = self.build_request()
        try:
            async with self.open() as stream:
                await stream.send_message(req, end=True)
                async for res in stream:
                    ret = self.handle_response(res, args.outfile)
                    if ret != 0:
                        return ret
        except Exception as exc:
            return self.handle_exception(exc, args.outfile)
        else:
            return 0

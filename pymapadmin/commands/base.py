
from __future__ import annotations

import os
import traceback
from abc import abstractmethod, ABCMeta
from argparse import ArgumentParser, Namespace
from collections.abc import Mapping
from typing import Generic, Any, Final, TextIO

from grpclib.client import Channel

from ..__about__ import __version__ as client_version
from ..local import token_file
from ..operation import Operation
from ..typing import StubT, RequestT, ResponseT, \
    AdminRequestT, AdminResponseT
from ..grpc.admin_pb2 import SUCCESS

# This import ensures error details are displayed correctly
# https://grpclib.readthedocs.io/en/latest/errors.html#error-details
from ..grpc import error_details_pb2  # noqa

__all__ = ['Command', 'ClientCommand', 'AdminCommand']


class Command(metaclass=ABCMeta):
    """Interface for command implementations.

    Args:
        args: The command-line arguments.
        channel: The GRPC channel for executing commands.

    """

    def __init__(self, args: Namespace, channel: Channel) -> None:
        super().__init__()
        self.args: Final = args
        self.channel: Final = channel

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

    @abstractmethod
    async def __call__(self, outfile: TextIO, errfile: TextIO) -> int:
        ...


class ClientCommand(Command, Operation[RequestT, ResponseT],
                    Generic[StubT, RequestT, ResponseT],
                    metaclass=ABCMeta):
    """Interface for client command implementations.

    Args:
        args: The command line arguments.
        client: The client object.

    """

    @property
    @abstractmethod
    def client(self) -> StubT:
        """Get the client object for the command.

        Args:
            channel: The GRPC channel for executing commands.

        """
        ...

    def _get_metadata(self) -> Mapping[str, str]:
        metadata = {'client-version': client_version}
        token: str | None = None
        if 'PYMAP_ADMIN_TOKEN' in os.environ:
            token = os.environ['PYMAP_ADMIN_TOKEN']
        else:
            path = token_file.find()
            if path is not None:
                token = path.read_text().strip()
        if token:
            metadata['auth-token'] = token
        return metadata

    @abstractmethod
    def build_request(self) -> RequestT:
        """Build the request."""
        ...

    @abstractmethod
    def handle_response(self, response: ResponseT,
                        outfile: TextIO, errfile: TextIO) -> int:
        """Handle each response. For streaming responses, this will be
        called once for each streamed response as long as ``0`` is returned.

        Args:
            response: The response from the server.
            outfile: The file object to print the output to.
            errfile: The file object to print errors to.

        """
        ...

    def handle_exception(self, exc: Exception,
                         outfile: TextIO, errfile: TextIO) -> int:
        """Handle an exception that occurred while calling the RPC function.

        Args:
            exc: The raised exception object.
            outfile: The file object to print the output to.
            errfile: The file object to print errors to.

        """
        traceback.print_exc()
        return 1

    async def __call__(self, outfile: TextIO, errfile: TextIO) -> int:
        req = self.build_request()
        try:
            response = await self.execute(req)
            ret = self.handle_response(response, outfile, errfile)
            if ret != 0:
                return ret
        except Exception as exc:
            return self.handle_exception(exc, outfile, errfile)
        else:
            return 0


class AdminCommand(ClientCommand[StubT, AdminRequestT, AdminResponseT],
                   metaclass=ABCMeta):
    """Interface for admin command implementations.

    The request and response must conform to the
    :class:`~pymapadmin.typing.AdminRequestProtocol` and
    :class:`~pymapadmin.typing.AdminResponseProtocol` protocols, respectively.

    The default :meth:`.handle_response` implementation calls
    :meth:`.handle_success` or :meth:`.handle_failure` depending on the result
    code.

    Args:
        args: The command line arguments.
        client: The client object.

    """

    def handle_response(self, response: AdminResponseT,
                        outfile: TextIO, errfile: TextIO) -> int:
        if response.result.code == SUCCESS:
            self.handle_success(response, outfile, errfile)
            return 0
        else:
            self.handle_failure(response, outfile, errfile)
            return 1

    def handle_success(self, response: AdminResponseT,
                       outfile: TextIO, errfile: TextIO) -> None:
        """Print a successful response.

        Args:
            response: The response from the server.
            outfile: The file object to print the output to.
            errfile: The file object to print errors to.

        """
        print(response, file=outfile)

    def handle_failure(self, response: AdminResponseT,
                       outfile: TextIO, errfile: TextIO) -> None:
        """Print a failure response.

        Args:
            response: The response from the server.
            outfile: The file object to print the output to.
            errfile: The file object to print errors to.

        """
        print(response.result, file=errfile)

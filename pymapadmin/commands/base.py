
from __future__ import annotations

import os
import sys
import traceback
from abc import abstractmethod, ABCMeta
from argparse import ArgumentParser, Namespace
from collections.abc import Mapping
from typing import Generic, Any, Final, Optional, TextIO

from grpclib.client import Channel

from .. import __version__ as client_version
from ..local import token_file
from ..typing import StubT, RequestT, ResponseT, MethodProtocol
from ..grpc.admin_pb2 import SUCCESS

try:
    # This import ensures error details are displayed correctly
    # https://grpclib.readthedocs.io/en/latest/errors.html#error-details
    from google.rpc import error_details_pb2  # noqa
except ImportError:  # pragma: no cover
    pass

__all__ = ['Command', 'ClientCommand']


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
    async def __call__(self, outfile: TextIO) -> int:
        ...


class ClientCommand(Command, Generic[StubT, RequestT, ResponseT],
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
        token: Optional[str] = None
        if 'PYMAP_ADMIN_TOKEN' in os.environ:
            token = os.environ['PYMAP_ADMIN_TOKEN']
        else:
            path = token_file.find()
            if path is not None:
                token = path.read_text().strip()
        if token:
            metadata['auth-token'] = token
        return metadata

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

        The default implementation calls :meth:`.handle_success` or
        :meth:`.handle_failure` depending on the result code.

        Args:
            response: The response from the server.
            outfile: The file object to print the output to.

        """
        if response.result.code == SUCCESS:
            self.handle_success(response, outfile)
            return 0
        else:
            self.handle_failure(response, outfile)
            return 1

    def handle_success(self, response: ResponseT, outfile: TextIO) -> None:
        """Print a successful response.

        Args:
            response: The response from the server.
            outfile: The file object to print the output to.

        """
        print(response, file=outfile)

    def handle_failure(self, response: ResponseT, outfile: TextIO) -> None:
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
        metadata = self._get_metadata()
        try:
            async with self.method.open(metadata=metadata) as stream:
                await stream.send_message(req, end=True)
                async for res in stream:
                    ret = self.handle_response(res, outfile)
                    if ret != 0:
                        return ret
        except Exception as exc:
            return self.handle_exception(exc, outfile)
        else:
            return 0

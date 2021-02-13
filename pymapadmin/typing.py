
from __future__ import annotations

from abc import abstractmethod
from collections.abc import Mapping
from contextlib import AbstractAsyncContextManager
from typing import TypeVar, Protocol

from grpclib.client import Stream

from .grpc.admin_pb2 import Result

__all__ = ['StubT', 'RequestT', 'ResponseT', 'MethodProtocol',
           'RequestProtocol', 'ResponseProtocol']

#: A type variable corresponding to an admin stub object.
StubT = TypeVar('StubT')

#: A type variable corresponding to an admin request object.
RequestT = TypeVar('RequestT', bound='RequestProtocol')

#: A type variable corresponding to an admin response object.
ResponseT = TypeVar('ResponseT', bound='ResponseProtocol')


class MethodProtocol(Protocol[RequestT, ResponseT]):
    """Protocol defining an admin method, for a command."""

    @abstractmethod
    def open(self, *, metadata: Mapping[str, str]) \
            -> AbstractAsyncContextManager[Stream[RequestT, ResponseT]]:
        ...


class RequestProtocol(Protocol):
    """Protocol defining the fields that all admin request objects are expected
    to have.

    Note:
        There are currently no fields common to all requests.

    """
    pass


class ResponseProtocol(Protocol):
    """Protocol defining the fields that all admin response objects are
    expected to have.

    """

    @property
    @abstractmethod
    def result(self) -> Result:
        """The result protobuf, containing a code and additional data."""
        ...

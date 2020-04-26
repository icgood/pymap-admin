
from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar
from typing_extensions import Protocol

from .grpc.admin_pb2 import Result

__all__ = ['StubT', 'RequestT', 'ResponseT',
           'RequestProtocol', 'ResponseProtocol']

#: A type variable corresponding to an admin client stub object.
StubT = TypeVar('StubT')

#: A type variable corresponding to an admin request object.
RequestT = TypeVar('RequestT', bound='RequestProtocol')

#: A type variable corresponding to an admin response object.
ResponseT = TypeVar('ResponseT', bound='ResponseProtocol')


class RequestProtocol(Protocol):
    """Protocol defining the fields that all admin request objects are expected
    to have.

    """
    pass


class ResponseProtocol(Protocol):
    """Protocol defining the fields that all admin response objects are
    expected to have.

    """

    @property
    @abstractmethod
    def result(self) -> Result:
        ...


from __future__ import annotations

import os
from abc import abstractmethod, ABCMeta
from collections.abc import Mapping
from typing import Generic, TypeVar

from .__about__ import __version__ as client_version
from .local import token_file
from .typing import MethodProtocol, RequestT, ResponseT

__all__ = ['CompoundRequestT', 'FirstResponseT', 'SecondRequestT',
           'Operation', 'SingleOperation', 'CompoundOperation']

#: Type variable for the compound request in :class:`CompoundOperation`.
CompoundRequestT = TypeVar('CompoundRequestT')

#: Type variable for the first response in :class:`CompoundOperation`.
FirstResponseT = TypeVar('FirstResponseT')

#: Type variable for the second request in :class:`CompoundOperation`.
SecondRequestT = TypeVar('SecondRequestT')


class Operation(Generic[RequestT, ResponseT], metaclass=ABCMeta):
    """Base class for a GRPC operation."""

    def get_metadata(self) -> Mapping[str, str]:
        """Get the GRPC metadata to use for the operation."""
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
    async def execute(self, /, request: RequestT) -> ResponseT:
        """Execute the operation and return the response.

        Args:
            request: The operation request.

        """
        ...


class SingleOperation(Operation[RequestT, ResponseT], metaclass=ABCMeta):
    """Implements :class:`Operation` using a single GRPC call."""

    @property
    @abstractmethod
    def method(self) -> MethodProtocol[RequestT, ResponseT]:
        """The GRPC client method."""
        ...

    async def execute(self, request: RequestT) -> ResponseT:
        metadata = self.get_metadata()
        async with self.method.open(metadata=metadata) as stream:
            await stream.send_message(request, end=True)
            async for response in stream:
                return response
            else:
                raise RuntimeError('No response received.')


class CompoundOperation(Operation[CompoundRequestT, ResponseT],
                        Generic[CompoundRequestT,
                                RequestT, FirstResponseT,
                                SecondRequestT, ResponseT],
                        metaclass=ABCMeta):
    """Implements :class:`Operation` using two steps. The second step may rely
    on the response of the first step.

    """

    @property
    @abstractmethod
    def first(self) -> Operation[RequestT, FirstResponseT]:
        """The first step in the compound operation."""
        ...

    @property
    @abstractmethod
    def second(self) -> Operation[SecondRequestT, ResponseT]:
        """The second step in the compound operation."""
        ...

    @abstractmethod
    def build_first(self, /, request: CompoundRequestT) -> RequestT:
        """Build the request object for the first step.

        Args:
            request: The compound operation request.

        """
        ...

    @abstractmethod
    def build_second(self, /, request: CompoundRequestT,
                     first_response: FirstResponseT) \
            -> tuple[SecondRequestT | None, ResponseT | None]:
        """Build the request object for the second step.

        Args:
            request: The compound operation request.
            first_response: The response received by the first step.

        Returns:
            If the second step should proceed, returns a two-tuple where the
            first item is the request object for the second step and the second
            item is ignored.

            If the compound request should be aborted, returns a two-tuple
            where the first item is ``None`` and the second item can be a
            response to use instead of executing the second step.

            If both items in the tuple are ``None``, the compound operation
            raises a :exc:`RuntimeError` displaying the response to the first
            step.

        """
        ...

    async def execute(self, request: CompoundRequestT) -> ResponseT:
        first_request = self.build_first(request)
        first_response = await self.first.execute(first_request)
        second_request, response = self.build_second(request, first_response)
        if second_request is not None:
            response = await self.second.execute(second_request)
        elif response is None:
            raise RuntimeError('Compound request aborted after first response',
                               first_response)
        return response


from __future__ import annotations

from abc import ABCMeta
from collections.abc import Sequence
from typing import Self, TypeAlias, TypeVar, Generic

from grpclib.server import Stream

RequestT = TypeVar('RequestT')
ResponseT = TypeVar('ResponseT')

_Operation: TypeAlias = tuple[type[RequestT], Sequence[ResponseT]]


class MockHandler(Generic[RequestT, ResponseT], metaclass=ABCMeta):

    def __init__(self) -> None:
        super().__init__()
        self._operations: list[_Operation[RequestT, ResponseT]] = []
        self._requests: list[RequestT] = []

    def expect(self, req_type: type[RequestT],
               responses: Sequence[ResponseT]) -> Self:
        self._operations.append((req_type, responses))
        return self

    @property
    def requests(self) -> Sequence[RequestT]:
        return self._requests

    async def _run(self, stream: Stream[RequestT, ResponseT]) -> None:
        req_type, responses = self._operations[len(self._requests)]
        req = await stream.recv_message()
        assert isinstance(req, req_type), f'{req!r}'
        self._requests.append(req)
        for resp in responses:
            await stream.send_message(resp)

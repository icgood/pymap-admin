
from __future__ import annotations

from abc import ABCMeta
from collections.abc import Sequence
from typing import TypeVar, Generic

from grpclib.server import Stream

RequestT = TypeVar('RequestT')
ResponseT = TypeVar('ResponseT')


class MockHandler(Generic[RequestT, ResponseT], metaclass=ABCMeta):

    def __init__(self, req_type: type[RequestT],
                 responses: Sequence[ResponseT]) -> None:
        super().__init__()
        self.req_type = req_type
        self.responses = responses
        self._request: RequestT | None = None

    @property
    def request(self) -> RequestT:
        req = self._request
        assert req is not None
        return req

    async def _run(self, stream: Stream[RequestT, ResponseT]) -> None:
        self._request = req = await stream.recv_message()
        assert isinstance(req, self.req_type)
        for resp in self.responses:
            await stream.send_message(resp)

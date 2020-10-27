
from __future__ import annotations

from abc import ABCMeta
from typing import TypeVar, Generic, Type, Optional, Sequence

from grpclib.server import Stream

RequestT = TypeVar('RequestT')
ResponseT = TypeVar('ResponseT')


class MockHandler(Generic[RequestT, ResponseT], metaclass=ABCMeta):

    def __init__(self, req_type: Type[RequestT],
                 responses: Sequence[ResponseT]) -> None:
        super().__init__()
        self.req_type = req_type
        self.responses = responses
        self._request: Optional[RequestT] = None

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

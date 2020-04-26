
from typing import Any, Optional


class TestStream:

    def __init__(self, stub) -> None:
        self.stub = stub

    def open(self):
        return self

    async def send_message(self, request, end):
        self.stub.request = request

    def __aiter__(self):
        return self.aiter()

    async def aiter(self):
        for res in self.stub.responses:
            yield res

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass


class TestStub:

    def __init__(self, responses) -> None:
        self.method: Optional[str] = None
        self.request: Optional[Any] = None
        self.responses = responses

    async def _action(self, request):
        self.request = request
        return self.response

    def __getattr__(self, method):
        self.method = method
        return TestStream(self)

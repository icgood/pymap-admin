
from typing import Any, Optional


class MockStream:

    def __init__(self, client) -> None:
        self.client = client

    def open(self):
        return self

    async def send_message(self, request, end):
        self.client.request = request

    def __aiter__(self):
        return self.aiter()

    async def aiter(self):
        for res in self.client.responses:
            yield res

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass


class MockClient:

    def __init__(self, responses) -> None:
        self.method: Optional[str] = None
        self.request: Optional[Any] = None
        self.responses = responses

    async def _action(self, request):
        self.request = request
        return self.response

    def __getattr__(self, method):
        self.method = method
        return MockStream(self)

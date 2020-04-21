
from typing import Any, Optional


class StubChannel:

    def __init__(self, response) -> None:
        self.method: Optional[str] = None
        self.request: Optional[Any] = None
        self.response = response

    async def _action(self, request):
        self.request = request
        return self.response

    def __getattr__(self, method):
        self.method = method
        return self._action

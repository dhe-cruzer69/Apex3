"""Simple in-process event bus."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any


Handler = Callable[[dict[str, Any]], None]

class EventBus:
    """Lightweight synchronous pub/sub event bus."""
    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = defaultdict(list)

    def on(self, event: str, handler: Handler) -> None:
        if not isinstance(event, str) or not event:
            raise ValueError("event must be a non-empty string")
        if not callable(handler):
            raise TypeError("handler must be callable")
        self._handlers[event].append(handler)

    def emit(self, event: str, payload: dict[str, Any] | None = None) -> None:
        data = {} if payload is None else payload
        for handler in tuple(self._handlers.get(event, ())):
            handler(data)

    def clear(self, event: str | None = None) -> None:
        if event is None:
            self._handlers.clear()
        else:
            self._handlers.pop(event, None)

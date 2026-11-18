"""Tests for canonical EventBus semantics."""
import pytest

from x4 import EventBus
from x4.core import EventBus as CoreEventBus


def test_event_bus_emit() -> None:
    bus = EventBus()
    received: list[dict] = []
    bus.on("test.event", lambda payload: received.append(payload))
    bus.emit("test.event", {"ok": True})
    assert received == [{"ok": True}]

def test_event_bus_clear_one_or_all() -> None:
    bus = EventBus()
    received: list[str] = []
    bus.on("one", lambda payload: received.append("one"))
    bus.on("two", lambda payload: received.append("two"))
    bus.clear("one")
    bus.emit("one")
    bus.emit("two")
    assert received == ["two"]
    bus.clear()
    bus.emit("two")
    assert received == ["two"]

def test_event_bus_rejects_invalid_registration() -> None:
    bus = EventBus()
    with pytest.raises(ValueError):
        bus.on("", lambda payload: None)
    with pytest.raises(TypeError):
        bus.on("event", None)  # type: ignore[arg-type]

def test_root_and_core_event_bus_are_identical() -> None:
    assert EventBus is CoreEventBus

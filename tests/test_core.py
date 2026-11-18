"""Compatibility and smoke tests for the public x4 API."""
from x4 import Config, EventBus, Logger, Permission
from x4.core import (Config as CoreConfig, EventBus as CoreEventBus,
                     Logger as CoreLogger, Permission as CorePermission)

def test_import_paths_share_canonical_implementations() -> None:
    assert Config is CoreConfig
    assert EventBus is CoreEventBus
    assert Logger is CoreLogger
    assert Permission is CorePermission

def test_config_load_and_get() -> None:
    cfg = Config.load({"env": "test", "debug": True})
    assert cfg.get("env") == "test"
    assert cfg.get("debug") is True
    assert cfg.get("missing", "default") == "default"

def test_config_require_raises() -> None:
    try:
        Config.load().require("does_not_exist")
    except KeyError:
        pass
    else:
        raise AssertionError("require() must raise for missing keys")

def test_event_bus() -> None:
    bus = EventBus()
    received = []
    bus.on("test.event", lambda payload: received.append(payload))
    bus.emit("test.event", {"ok": True})
    assert received == [{"ok": True}]

def test_permission_grant_and_check() -> None:
    policy = Permission()
    policy.grant("agent", "filesystem.read", "./workspace")
    assert policy.check("agent", "filesystem.read", "./workspace").allowed
    assert not policy.check("agent", "filesystem.write", "./workspace").allowed

def test_logger_smoke() -> None:
    Logger("test", level="DEBUG").info("hello", key="value")
    Logger("test.numeric", level=10).debug("debug message")

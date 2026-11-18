"""Tests for canonical Config semantics."""
from x4 import Config
from x4.core import Config as CoreConfig


def test_config_load_defaults() -> None:
    cfg = Config.load({"mode": "test"})
    assert cfg.get("mode") == "test"
    assert cfg.get("missing", "fallback") == "fallback"

def test_config_precedence(monkeypatch) -> None:
    monkeypatch.setenv("X4_MODE", "environment")
    monkeypatch.setenv("X4_DEBUG", "1")
    cfg = Config.load({"mode": "default", "debug": False},
                      overrides={"mode": "override"})
    assert cfg.get("mode") == "override"
    assert cfg.get("debug") == "1"

def test_root_and_core_config_are_identical() -> None:
    assert Config is CoreConfig

def test_config_require_raises() -> None:
    try:
        Config.load({}).require("nonexistent")
    except KeyError:
        pass
    else:
        raise AssertionError("Expected KeyError")

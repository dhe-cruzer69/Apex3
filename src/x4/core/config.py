"""Typed configuration loading with deterministic precedence."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Config:
    """Configuration precedence: defaults, X4_* environment, explicit overrides."""
    data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls, defaults: dict[str, Any] | None = None,
             overrides: dict[str, Any] | None = None) -> Config:
        cfg: dict[str, Any] = dict(defaults or {})
        for key, value in os.environ.items():
            if key.startswith("X4_"):
                cfg[key[3:].lower()] = value
        if overrides:
            cfg.update(overrides)
        return cls(data=cfg)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def require(self, key: str) -> Any:
        if key not in self.data:
            raise KeyError(f"Required config key missing: {key}")
        return self.data[key]

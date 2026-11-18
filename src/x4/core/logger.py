"""Structured logger wrapper with string and integer level support."""
from __future__ import annotations
import logging
import sys
from typing import Any

class Logger:
    """Stdlib logging wrapper; keyword fields are rendered into the message."""
    def __init__(self, name: str = "x4", level: str | int = logging.INFO) -> None:
        self._logger = logging.getLogger(name)
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"))
            self._logger.addHandler(handler)
        self._logger.setLevel(self._normalize_level(level))

    @staticmethod
    def _normalize_level(level: str | int) -> int:
        if isinstance(level, bool):
            raise TypeError("level must be a logging level name or integer")
        if isinstance(level, int):
            if level < 0:
                raise ValueError("logging level must be non-negative")
            return level
        if not isinstance(level, str):
            raise TypeError("level must be a logging level name or integer")
        normalized = logging.getLevelName(level.upper())
        if not isinstance(normalized, int):
            raise ValueError(f"Unknown logging level: {level!r}")
        return normalized

    @staticmethod
    def _format(message: str, fields: dict[str, Any]) -> str:
        if not fields:
            return message
        suffix = " ".join(f"{key}={value!r}" for key, value in fields.items())
        return f"{message} | {suffix}"

    def debug(self, msg: str, **kwargs: Any) -> None:
        self._logger.debug(self._format(msg, kwargs))
    def info(self, msg: str, **kwargs: Any) -> None:
        self._logger.info(self._format(msg, kwargs))
    def warning(self, msg: str, **kwargs: Any) -> None:
        self._logger.warning(self._format(msg, kwargs))
    def error(self, msg: str, **kwargs: Any) -> None:
        self._logger.error(self._format(msg, kwargs))

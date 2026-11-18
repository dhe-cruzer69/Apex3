"""Least-privilege permission checks."""
from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class PermissionDecision:
    """Immutable result of a permission check."""
    allowed: bool
    reason: str = ""
    def raise_if_denied(self) -> None:
        if not self.allowed:
            raise PermissionError(self.reason or "Permission denied")

PermissionResult = PermissionDecision

class Permission:
    """In-memory grant checker; not an authentication or isolation boundary."""
    def __init__(self) -> None:
        self._rules: dict[str, set[str]] = {}

    def grant(self, actor: str, action: str, resource: str = "*") -> None:
        self._validate(actor, "actor")
        self._validate(action, "action")
        self._validate(resource, "resource")
        self._rules.setdefault(actor, set()).add(f"{action}:{resource}")

    def revoke(self, actor: str, action: str, resource: str = "*") -> None:
        self._validate(actor, "actor")
        self._validate(action, "action")
        self._validate(resource, "resource")
        rules = self._rules.get(actor)
        if rules is not None:
            rules.discard(f"{action}:{resource}")
            if not rules:
                self._rules.pop(actor, None)

    def check(self, actor: str, action: str, resource: str = "*") -> PermissionDecision:
        self._validate(actor, "actor")
        self._validate(action, "action")
        self._validate(resource, "resource")
        rules = self._rules.get(actor, set())
        candidates = (f"{action}:{resource}", f"{action}:*", f"*:{resource}", "*:*")
        if any(rule in rules for rule in candidates):
            return PermissionDecision(True, "granted")
        return PermissionDecision(False,
            f"actor={actor!r} denied action={action!r} resource={resource!r}")

    @staticmethod
    def _validate(value: str, label: str) -> None:
        if not isinstance(value, str) or not value:
            raise ValueError(f"{label} must be a non-empty string")

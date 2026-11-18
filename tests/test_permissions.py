"""Tests for canonical permission checker and decision model."""
import pytest

from x4 import Permission, PermissionDecision, PermissionResult
from x4.core import Permission as CorePermission


def test_permission_allow_and_deny() -> None:
    policy = Permission()
    policy.grant("agent", "read", "./workspace")
    allowed = policy.check("agent", "read", "./workspace")
    denied = policy.check("agent", "write", "./workspace")
    assert allowed.allowed and allowed.reason == "granted"
    assert not denied.allowed
    with pytest.raises(PermissionError):
        denied.raise_if_denied()

def test_permission_wildcards_and_revoke() -> None:
    policy = Permission()
    policy.grant("agent", "read", "*")
    assert policy.check("agent", "read", "/tmp").allowed
    policy.revoke("agent", "read", "*")
    assert not policy.check("agent", "read", "/tmp").allowed

def test_decision_is_immutable_and_alias_is_compatible() -> None:
    decision = PermissionDecision(allowed=True, reason="approved")
    assert PermissionResult is PermissionDecision
    with pytest.raises((AttributeError, TypeError)):
        decision.allowed = False  # type: ignore[misc]

def test_root_and_core_permission_are_identical() -> None:
    assert Permission is CorePermission

def test_permission_rejects_empty_identifiers() -> None:
    with pytest.raises(ValueError):
        Permission().grant("", "read")

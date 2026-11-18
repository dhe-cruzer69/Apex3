# x4-core

**Core runtime and shared infrastructure for the X4 open-source ecosystem.**

Config • Logging • Events • Permissions

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-v0.1-orange)](CHANGELOG.md)

Part of **CruzX by ARIEX4Ops** — secure AI agents, automation, and developer infrastructure.

## Why x4-core exists

Higher-level projects should share a small, stable set of configuration, logging, event, and permission primitives rather than maintain parallel implementations. Telemetry, authentication, and plugin-registry capabilities shown in broader ecosystem diagrams are not claimed as implemented by this package.

## Installation

~~~bash
pip install x4-core
pip install -e ".[dev]"
~~~

## Quickstart

~~~python
from x4 import Config, EventBus, Logger, Permission

config = Config.load(defaults={"env": "development"},
                     overrides={"env": "local"})
logger = Logger("x4", level="INFO")
events = EventBus()
policy = Permission()
policy.grant("agent", "filesystem.read", "./workspace")

decision = policy.check("agent", "filesystem.read", "./workspace")
decision.raise_if_denied()
logger.info("runtime.ready", environment=config.get("env"))
events.emit("runtime.ready", {"environment": config.get("env")})
~~~

## Public API and compatibility

Canonical implementations live under x4.core. Existing imports from x4 and historical x4.config, x4.events, x4.logger, and x4.permissions modules remain supported and re-export the same class objects.

Configuration precedence is defaults, then X4_* environment variables, then explicit overrides. Environment values remain strings; parse domain-specific values at their boundary.

Permission is an in-memory grant checker, not an authentication system, persistent policy store, or security boundary. PermissionDecision (also exported as PermissionResult) is an immutable allow/deny result.

## Development and validation

~~~bash
python -m pip install -e ".[dev]"
ruff check .
mypy src
pytest -q
python -m build
~~~

## Architecture

This package is the shared primitive layer. Agent orchestration, memory, sandboxing, MCP, and model providers are consumers; this repository does not claim those systems are implemented here.

## Security

See [SECURITY.md](SECURITY.md). Permission checks are application-level helpers and must not replace OS isolation, authentication, or defense-in-depth controls.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

Apache-2.0 — see [LICENSE](LICENSE).

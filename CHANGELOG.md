# Changelog

## Unreleased

### Changed
- Consolidated configuration, event, logging, and permission primitives under x4.core.
- Preserved legacy x4 and x4.* imports as compatibility re-exports.
- Standardized configuration precedence: defaults, environment, explicit overrides.
- Unified logger level handling for string names and integer levels.
- Standardized permissions around a stateful grant checker and immutable decisions.

### Compatibility
- PermissionResult remains available as an alias of PermissionDecision.
- The previous class-level Permission.check(..., allow=...) decision constructor is replaced by an instance policy API: instantiate Permission, call grant(), then check(). This deliberate API correction is documented in README.

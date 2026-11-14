# Engineering and GitHub Copilot Instructions

## Repository context and safe workflow
- This repository describes the shared X4 runtime and infrastructure. Treat source, tests, package metadata, README, and workflows as authoritative; architecture diagrams and roadmap items do not prove implementation.
- Before editing, inspect the relevant source, tests, package configuration, and CI. Preserve established architecture, public interfaces, and unrelated work.
- Make small, reviewable diffs. Avoid speculative abstractions, broad rewrites, unrelated formatting, and lockfile churn.
- Validate external input at trust boundaries. Use least privilege, safe defaults, parameterized queries, and context-appropriate output encoding. Never commit credentials, tokens, private keys, or real secrets.
- Use explicit timeouts, bounded retries, idempotency where applicable, cancellation, and safe failure behavior for network, subprocess, model, and storage operations.
- Add deterministic regression tests for changed behavior, edge cases, failure paths, and security boundaries. Do not delete or weaken tests to obtain a green build.

## Model-assisted completion standards
1. Read the task, acceptance criteria, relevant implementation/tests, and existing instructions first. State assumptions before substantial work.
2. Treat generated code and commands as untrusted proposals. Inspect commands before running them; never auto-run generated deployment, migration, destructive, or privilege-changing operations.
3. Prefer existing APIs, patterns, and dependencies. Patch the smallest necessary surface; do not replace whole files when a focused diff is sufficient.
4. Validate syntax, types, schemas, authorization boundaries, injection risks, dependency changes, resource bounds, and error handling.
5. Add/update tests, run documented checks, inspect the final diff, and report each check as PASS, FAIL, NOT RUN, or BLOCKED with exact command and evidence. Never fabricate test, coverage, benchmark, security, or deployment results.
6. Use bounded repair attempts. If correctness or security remains uncertain, stop and report UNKNOWN — HUMAN REVIEW REQUIRED.
7. Do not merge, deploy, delete data, change permissions/visibility, or write to the default branch without explicit task-specific authorization.

## Build, test, and CI
- Follow the existing README, contributing guide, pyproject configuration, and CI workflow. Current CI declares Python 3.10–3.12, installs the development extra, runs `pip check`, builds a wheel, runs Ruff, and executes pytest; do not claim these checks passed unless a run confirms it.
- Prefer reproducible installs and lockfile-respecting dependency resolution. Run formatting/lint, static/type checks, unit/integration tests, and build/package checks when supported by project configuration.
- Keep workflows least-privileged (`contents: read` by default), time-bounded, concurrency-aware, and safe for pull requests. Pin third-party actions to reviewed immutable SHAs where practical.
- Never mask failures with `|| true`, swallowed exit codes, unconditional success fallbacks, or misleading status badges.
- Codecov is opt-in: do not add an uploader or badge unless CI actually generates coverage and the Codecov project/token/public-upload configuration is verified. If unverified, omit Codecov and report the gap.

## Review and evidence
- Keep changes on a dedicated branch and open a reviewable PR; never merge it automatically.
- Separate OBSERVED, VALIDATED, CORRELATED, and HYPOTHESIS. Report branch, PR, commit SHA, changed paths, exact checks/results, and unverified gaps.
- If a check was not executed, state `NOT RUN — HUMAN REVIEW REQUIRED`.

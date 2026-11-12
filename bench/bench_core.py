"""Reproducible microbenchmark for x4-core primitives.

Measures the two hot paths that every X4 worker touches on each task:
permission checks and event dispatch. Each measurement is compared against a
deliberately naive reference implementation so the reported speedup is a
measured ratio, not a claim.

Usage:
    python bench/bench_core.py            # human readable
    python bench/bench_core.py --json     # machine readable to stdout

Exit code is 0 on success. It is 1 if the measured speedup against the naive
reference falls below the floor declared in FLOORS.
"""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from x4.core.events import EventBus
from x4.core.permissions import Permission

ITERATIONS = 20_000
SAMPLES = 7
EVENT_KINDS = [f"evt.{i}" for i in range(20)]
EVENT = EVENT_KINDS[17]

# Minimum measured speedup over the naive reference. Below this the run fails.
FLOORS = {"permission_check": 1.5, "event_dispatch": 1.5}


def time_call(fn, iterations: int, samples: int) -> float:
    """Return median seconds per call across ``samples`` timed runs."""
    times = []
    for _ in range(samples):
        start = time.perf_counter()
        for _ in range(iterations):
            fn()
        times.append((time.perf_counter() - start) / iterations)
    return statistics.median(times)


# --- subject under test -------------------------------------------------

def permission_check() -> None:
    Permission.check("agent:planner", "read", "repo:x4-core").raise_if_denied()


_bus = EventBus()
for _kind in EVENT_KINDS:
    _bus.on(_kind, lambda payload: None)


def event_dispatch() -> None:
    _bus.emit(EVENT, {"n": 1})


# --- naive references ---------------------------------------------------

def naive_permission_check() -> None:
    actor, action, resource = "agent:planner", "read", "repo:x4-core"
    decision = {"actor": actor, "action": action, "resource": resource, "allowed": True}
    if not decision.get("allowed"):
        raise PermissionError(decision)


_naive_handlers: list[tuple[str, object]] = [(kind, lambda payload: None) for kind in EVENT_KINDS]


def naive_event_dispatch() -> None:
    for kind, handler in _naive_handlers:
        if kind == EVENT:
            handler({"n": 1})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit JSON only")
    parser.add_argument("--iterations", type=int, default=ITERATIONS)
    args = parser.parse_args()

    cases = [
        ("permission_check", permission_check, naive_permission_check),
        ("event_dispatch", event_dispatch, naive_event_dispatch),
    ]

    results = []
    failures = []
    for name, subject, naive in cases:
        fast = time_call(subject, args.iterations, SAMPLES)
        slow = time_call(naive, args.iterations, SAMPLES)
        speedup = slow / fast if fast else 0.0
        floor = FLOORS.get(name, 1.0)
        ok = speedup >= floor
        if not ok:
            failures.append(f"{name}: {speedup:.2f}x < floor {floor}x")
        results.append(
            {
                "case": name,
                "iterations": args.iterations,
                "samples": SAMPLES,
                "subject_seconds_per_op": round(fast, 9),
                "naive_seconds_per_op": round(slow, 9),
                "subject_ops_per_second": round(1 / fast) if fast else None,
                "measured_speedup_vs_naive": round(speedup, 2),
                "floor": floor,
                "pass": ok,
            }
        )

    report = {
        "repo": "x4-core",
        "measured_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "processor": platform.processor() or "unknown",
        "results": results,
        "passed": not failures,
        "failures": failures,
        "note": "Speedup is measured against the naive reference in this file, not against a previous release.",
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"x4-core benchmark · Python {report['python']} · {report['platform']}")
        print(f"{'case':<20}{'ops/sec':>12}{'ns/op':>10}{'vs naive':>10}  result")
        for row in results:
            print(
                f"{row['case']:<20}{row['subject_ops_per_second']:>12,}"
                f"{row['subject_seconds_per_op'] * 1e9:>10.0f}"
                f"{row['measured_speedup_vs_naive']:>9.2f}x"
                f"  {'PASS' if row['pass'] else 'FAIL'}"
            )
        if failures:
            print("\nFailed floors:")
            for failure in failures:
                print(f"  {failure}")
        else:
            print("\nAll floors met.")

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())

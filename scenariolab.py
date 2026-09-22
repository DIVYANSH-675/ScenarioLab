"""Audit proposed multivariate time-series changes against explicit constraints."""
import argparse
import json
import math
from pathlib import Path


def matrix(value, name):
    if not isinstance(value, list) or not value or not isinstance(value[0], list) or not value[0]:
        raise ValueError(f"{name} must be a nonempty time-by-feature matrix")
    width = len(value[0])
    for row in value:
        if not isinstance(row, list) or len(row) != width:
            raise ValueError(f"{name} must be rectangular")
        if any(type(x) not in (int, float) or not math.isfinite(x) for x in row):
            raise ValueError(f"{name} must contain finite numbers")
    return value


def audit(original, candidate, constraints):
    original, candidate = matrix(original, "original"), matrix(candidate, "candidate")
    if len(original) != len(candidate) or len(original[0]) != len(candidate[0]):
        raise ValueError("Candidate shape must match original")
    width = len(original[0])
    immutable = constraints.get("immutable_features", [])
    if any(type(x) is not int or not 0 <= x < width for x in immutable):
        raise ValueError("Immutable feature index outside matrix")
    bounds = constraints.get("bounds", {})
    for key, interval in bounds.items():
        if not str(key).isdigit() or not 0 <= int(key) < width:
            raise ValueError("Bound feature index outside matrix")
        if not isinstance(interval, list) or len(interval) != 2:
            raise ValueError("Bounds must be [lower, upper]")
        if any(type(x) not in (int, float) or not math.isfinite(x) for x in interval) or interval[0] > interval[1]:
            raise ValueError("Bounds must be finite and ordered")
    budget = constraints.get("max_l1_change")
    if budget is not None and (type(budget) not in (int, float) or not math.isfinite(budget) or budget < 0):
        raise ValueError("Change budget must be finite and nonnegative")
    changes, violations = [], []
    for t, (before, after) in enumerate(zip(original, candidate)):
        for feature, (old, new) in enumerate(zip(before, after)):
            if new != old:
                changes.append({"time": t, "feature": feature, "before": old, "after": new, "delta": new-old})
                if feature in immutable:
                    violations.append({"kind": "immutable", "time": t, "feature": feature})
            if str(feature) in bounds:
                low, high = bounds[str(feature)]
                if not low <= new <= high:
                    violations.append({"kind": "bounds", "time": t, "feature": feature})
    distance = sum(abs(item["delta"]) for item in changes)
    if budget is not None and distance > budget:
        violations.append({"kind": "budget", "actual": distance, "maximum": budget})
    return {"feasible": not violations, "l1_change": distance,
            "changed_points": len(changes), "changes": changes, "violations": violations,
            "scope": "Checks supplied constraints; does not establish causal validity or model prediction changes."}



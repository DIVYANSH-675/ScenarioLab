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



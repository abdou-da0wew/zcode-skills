#!/usr/bin/env python3
"""Merge major_recommendation.json and school_recommendation.json into analysis.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise RuntimeError(f"cannot read {path}: {e}") from e


def merge(majors_data: dict, schools_data: dict) -> dict:
    return {
        "student": majors_data.get("student") or {},
        "analysis": {
            "intro": majors_data.get("intro") or "",
            "strategy": majors_data.get("strategy") or "",
            "major_directions": majors_data.get("major_directions") or [],
            "school_strategy": schools_data.get("school_strategy") or "",
        },
        "recommended_majors": majors_data.get("recommended_majors") or [],
        "recommended_schools": schools_data.get("recommended_schools") or [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge major/school recommendations into analysis.json")
    parser.add_argument("--majors", type=Path, required=True, help="major_recommendation.json")
    parser.add_argument("--schools", type=Path, required=True, help="school_recommendation.json")
    parser.add_argument("-o", "--output", type=Path, required=True, help="output analysis.json")
    args = parser.parse_args()

    try:
        majors_data = load_json(args.majors)
        schools_data = load_json(args.schools)
        result = merge(majors_data, schools_data)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"Merged: {args.output} ({len(result['recommended_majors'])} majors, "
        f"{len(result['recommended_schools'])} schools)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
profile_match.py — match a user's skill list against a keyword library and output a fit report

Usage:
    python profile_match.py --skills "SQL,Python,product planning,A/B testing" \
                            --library internet \
                            [--out report.md]

library values: internet / tech / finance / general
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LIB_MAP = {
    "internet": "keywords_internet.md",
    "tech": "keywords_tech.md",
    "finance": "keywords_finance.md",
    "general": "keywords_general.md",
}


def extract_keywords(md_path: Path) -> list[str]:
    """Simple markdown parser: collect all bullet items as keywords (both CJK and Latin)."""
    text = md_path.read_text(encoding="utf-8")
    # Match lines starting with -
    bullets = re.findall(r"^\s*[-*]\s+(.+)$", text, flags=re.MULTILINE)
    keywords: set[str] = set()
    for line in bullets:
        # Strip parenthetical explanations, placeholders, and markdown control characters
        clean = re.sub(r"[\uff08(][^\uff09)]*[\uff09)]", "", line)
        clean = re.sub(r"_{2,}", "", clean)
        clean = clean.replace("**", "").replace("__", "")
        for token in re.split(r"[\u3001,\uff0c/\uff0f\s]+", clean):
            token = token.strip("\uff1a:.\u3002\uff0c\u201c\u201d\u2018\u2019`*").lower()
            # Filter out tokens containing only punctuation / dashes / digits
            if not re.search(r"[\u4e00-\u9fa5A-Za-z]", token):
                continue
            if 1 < len(token) < 30:
                keywords.add(token)
    return sorted(keywords)


def match_score(user_skills: list[str], lib_keywords: list[str]) -> dict:
    """Return hits, missing, and hit rate. Fuzzy matching: substring containment counts as a hit."""
    user_lower = [s.strip().lower() for s in user_skills if s.strip()]
    hits, missing = [], []
    for kw in lib_keywords:
        if any(kw in u or u in kw for u in user_lower):
            hits.append(kw)
        else:
            missing.append(kw)
    rate = len(hits) / len(lib_keywords) if lib_keywords else 0
    return {
        "hits": hits,
        "missing": missing,
        "rate": rate,
        "user_skills": user_lower,
    }


def render_report(result: dict, library: str) -> str:
    rate_pct = f"{result['rate'] * 100:.1f}%"
    # Top 20 gaps to keep the report short
    top_missing = result["missing"][:20]
    lines = [
        f"# Role Profile Match Report — {library}",
        "",
        f"- **Hit rate**: {rate_pct} ({len(result['hits'])} / {len(result['hits']) + len(result['missing'])})",
        f"- **User-provided skills**: {', '.join(result['user_skills'])}",
        "",
        "## ✅ Matched keywords",
        "",
        ", ".join(result["hits"]) if result["hits"] else "(none)",
        "",
        "## ⚠️ Gaps (top 20, alphabetical)",
        "",
        ", ".join(top_missing) if top_missing else "(none)",
        "",
        "## Interpretation",
        "",
        "- Hit rate < 20%: direction mismatch; re-evaluate the target role",
        "- Hit rate 20-50%: applicable, but key gaps need filling",
        "- Hit rate > 50%: core match; worth prioritizing",
        "",
        "Note: this tool is a keyword-level coarse screen and cannot replace a real JD comparison (use jd-resume-tailor for precise matching).",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills", required=True, help="User skill list, comma-separated")
    parser.add_argument(
        "--library", choices=list(LIB_MAP), required=True, help="Keyword library"
    )
    parser.add_argument("--out", help="Output markdown report path; prints to stdout by default")
    parser.add_argument(
        "--references-dir",
        default=str(Path(__file__).resolve().parent.parent / "references"),
        help="Path to the references directory",
    )
    args = parser.parse_args()

    lib_path = Path(args.references_dir) / LIB_MAP[args.library]
    if not lib_path.exists():
        print(f"✗ Keyword library not found: {lib_path}", file=sys.stderr)
        sys.exit(1)

    lib_keywords = extract_keywords(lib_path)
    user_skills = [s for s in args.skills.split(",") if s.strip()]
    result = match_score(user_skills, lib_keywords)
    report = render_report(result, args.library)

    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"✓ Report generated: {args.out}")
    else:
        print(report)


if __name__ == "__main__":
    main()

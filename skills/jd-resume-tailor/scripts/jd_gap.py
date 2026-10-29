#!/usr/bin/env python3
"""
jd_gap.py — Run a gap analysis between parse_jd.py's JSON and the resume text

Usage:
    python jd_gap.py --jd jd_parsed.json --resume resume.md --out gap.md

Outputs a markdown report with three categories — perfect hits / implicit hits / true gaps — plus rewrite advice.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def load_resume_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return path.read_text(encoding="utf-8")
    if suffix == ".docx":
        try:
            from docx import Document
        except ImportError:
            print(
                "✗ python-docx is missing: pip install python-docx --break-system-packages",
                file=sys.stderr,
            )
            sys.exit(1)
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    print(f"✗ Unsupported format: {suffix}", file=sys.stderr)
    sys.exit(1)


def find_evidence(resume_text: str, keyword: str, window: int = 30) -> str | None:
    """Search the resume for the keyword; return a context snippet, or None if absent."""
    pattern = re.escape(keyword)
    m = re.search(pattern, resume_text, flags=re.IGNORECASE)
    if not m:
        return None
    start = max(0, m.start() - window)
    end = min(len(resume_text), m.end() + window)
    snippet = resume_text[start:end].replace("\n", " ").strip()
    return snippet


def fuzzy_hit(resume_text: str, keyword: str) -> str | None:
    """Fuzzy hit: match on the keyword's stem fragments (prefix / suffix) for containment."""
    # Take the first / last 4 characters as stem candidates
    candidates = []
    if len(keyword) >= 4:
        candidates.append(keyword[:4].lower())
        candidates.append(keyword[-4:].lower())
    text_low = resume_text.lower()
    for c in candidates:
        if c and c in text_low:
            return c
    return None


def analyze(jd: dict, resume_text: str) -> dict:
    perfect, implicit, missing = [], [], []

    # Compare against the skills extracted from must-have sentences
    candidates = jd.get("skills_extracted", []) + jd.get("must_have", [])

    seen = set()
    for c in candidates:
        # Sentences are too long; shorten them
        keyword = c.strip()
        if len(keyword) > 30:
            # Extract shorter keywords from long sentences
            short_tokens = re.findall(
                r"[A-Za-z][A-Za-z0-9+/.\-_]{1,20}",
                keyword,
            )
            for t in short_tokens:
                if t.lower() not in seen:
                    seen.add(t.lower())
                    process_one(t, resume_text, perfect, implicit, missing)
        else:
            if keyword.lower() not in seen:
                seen.add(keyword.lower())
                process_one(keyword, resume_text, perfect, implicit, missing)

    return {"perfect": perfect, "implicit": implicit, "missing": missing}


def process_one(keyword, resume_text, perfect, implicit, missing):
    ev = find_evidence(resume_text, keyword)
    if ev:
        perfect.append({"keyword": keyword, "evidence": ev})
        return
    fuzzy = fuzzy_hit(resume_text, keyword)
    if fuzzy:
        implicit.append({"keyword": keyword, "fuzzy_match": fuzzy})
    else:
        missing.append(keyword)


def render(jd: dict, gap: dict) -> str:
    lines = ["# JD ⇄ Resume Gap Analysis Report", ""]

    spec = jd.get("special_requirements", {})
    if spec:
        lines += ["## JD Hard Requirements", ""]
        for k, v in spec.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")

    lines += ["## ✅ Perfect Hits (clear evidence in the resume)", ""]
    if gap["perfect"]:
        for item in gap["perfect"][:30]:
            lines.append(f"- **{item['keyword']}** — evidence: `...{item['evidence']}...`")
    else:
        lines.append("(none)")
    lines.append("")

    lines += ["## 🟡 Implicit Hits (related experience with different wording; align terms when rewriting)", ""]
    if gap["implicit"]:
        for item in gap["implicit"][:20]:
            lines.append(f"- **JD keyword: {item['keyword']}** (found in resume as: `{item['fuzzy_match']}`)")
    else:
        lines.append("(none)")
    lines.append("")

    lines += ["## 🔴 True Gaps (entirely absent from the resume; confirm / add / reframe)", ""]
    if gap["missing"]:
        for kw in gap["missing"][:30]:
            lines.append(f"- **{kw}**")
    else:
        lines.append("(none)")
    lines.append("")

    lines += [
        "---",
        "## Rewrite Advice",
        "",
        "1. **Perfect hits**: keep them, but make sure the wording matches the JD (e.g. if the JD says 'A/B testing', don't write 'AB experiment')",
        "2. **Implicit hits** are the highest-leverage optimization — replace the resume's near-synonyms with the JD's exact wording",
        "3. **True gaps** come in two kinds:",
        "   - You did it but never wrote it down? → add it to the matching experience's bullets",
        "   - You never did it? → **don't fabricate**. Address transferable skills honestly in the cover letter / Summary",
        "4. Re-run ats_check.py on the rewritten resume to see whether the hit rate improved",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jd", required=True, help="JSON produced by parse_jd.py")
    parser.add_argument("--resume", required=True, help="Resume file (.md/.txt/.docx)")
    parser.add_argument("--out", help="Output markdown path")
    args = parser.parse_args()

    jd = json.loads(Path(args.jd).read_text(encoding="utf-8"))
    resume_text = load_resume_text(Path(args.resume))
    gap = analyze(jd, resume_text)
    report = render(jd, gap)

    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"✓ Gap report written to: {args.out}")
    else:
        print(report)


if __name__ == "__main__":
    main()

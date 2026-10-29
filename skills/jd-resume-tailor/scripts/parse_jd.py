#!/usr/bin/env python3
"""
parse_jd.py — Parse JD text and extract must-haves / nice-to-haves / responsibilities / special requirements

Usage:
    python parse_jd.py --jd-file jd.txt --out jd_parsed.json
    python parse_jd.py --jd-text "..." --out jd_parsed.json

The output JSON feeds the next step (jd_gap.py) and can also be shown to the user directly.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MUST_PATTERNS = [
    r"required", r"must\s*have", r"mandatory", r"essential", r"prerequisite",
    r"should\s+have", r"needs?\s+to", r"hard\s+requirement",
    r"at\s*least\s*\d+\s*years", r"\d+\+?\s*years",
    r"minimum\s+\d+\s+years",
]
NICE_PATTERNS = [
    r"preferred", r"nice\s*to\s*have", r"plus", r"bonus", r"desirable",
    r"familiarity\s+with\s*.+\s*(?:is\s+)?a\s+plus",
    r".+\s+experience\s+(?:is\s+)?(?:a\s+)?(?:plus|preferred)",
]
ACTION_VERBS = [
    "lead", "drive", "build", "design", "architect", "develop", "implement",
    "optimize", "manage", "coordinate", "execute", "own", "launch", "scale",
    "refactor", "plan", "iterate", "operate", "deliver", "establish",
]


def split_sentences(text: str) -> list[str]:
    # Split on sentence punctuation and newlines while keeping bullet lines
    raw = re.split(r"[.!?;\n]+", text)
    return [s.strip(" \t-•·*") for s in raw if s.strip()]


def classify_sentences(sentences: list[str]) -> dict:
    must, nice, resp, others = [], [], [], []
    for s in sentences:
        s_low = s.lower()
        if any(re.search(p, s_low) for p in NICE_PATTERNS):
            nice.append(s)
        elif any(re.search(p, s_low) for p in MUST_PATTERNS):
            must.append(s)
        elif any(v in s_low for v in ACTION_VERBS):
            resp.append(s)
        else:
            others.append(s)
    return {"must": must, "nice": nice, "responsibilities": resp, "others": others}


def extract_special(text: str) -> dict:
    out: dict[str, str] = {}

    # Education
    edu = re.search(r"(Bachelor(?:'s)?|Master(?:'s)?|Ph\.?D|Associate)(?:\s*degree)?(?:\s+or\s+above)?", text, flags=re.IGNORECASE)
    if edu:
        out["education"] = edu.group(0)

    # Years of experience
    years = re.search(r"(\d+)\s*[-~–to]+\s*(\d+)\s*years?|(\d+)\s*\+?\s*years?(?:\s+(?:or\s+above|and\s+above))?", text, flags=re.IGNORECASE)
    if years:
        out["years"] = years.group(0)

    # Language
    lang_pat = re.search(
        r"(fluent\s+(?:in\s+)?english|business\s+english|native\s+(?:english\s+)?speaker|CET[-\s]?[46]|IELTS\s*\d(?:\.\d)?|TOEFL\s*\d{2,3})",
        text,
        flags=re.IGNORECASE,
    )
    if lang_pat:
        out["language"] = lang_pat.group(0)

    # Location
    cities = re.findall(
        r"(Beijing|Shanghai|Guangzhou|Shenzhen|Hangzhou|Nanjing|Suzhou|Chengdu|Wuhan|Xi'an|Hong\s*Kong|Singapore|New\s*York|London|remote|hybrid|overseas)",
        text,
        flags=re.IGNORECASE,
    )
    if cities:
        out["location"] = "/".join(sorted(set(c.lower() for c in cities)))

    # Travel / overtime signals
    travel = re.search(r"(business\s+travel|relocation|on[-\s]?site|project[-\s]based|overtime|996|9[69]5|6[-\s]?day\s+work\s*week)", text, flags=re.IGNORECASE)
    if travel:
        out["working_style"] = travel.group(0)

    # Certifications
    certs = re.findall(
        r"(CFA(?:\s*Level\s*[I123]+)?|CPA|FRM|ACCA|PMP|AWS\s*[\w\s]*Certifi\w*|Azure\s*[\w]*|GCP\s*[\w]*)",
        text,
        flags=re.IGNORECASE,
    )
    if certs:
        out["certificates"] = "/".join(sorted(set(c.strip() for c in certs)))

    return out


def extract_skills(sentences: list[str]) -> list[str]:
    """Extract candidate skill words from all sentences (short tokens first; avoid extracting whole sentences)."""
    text = " ".join(sentences)
    # English skill tokens (CamelCase or capitalized words, identifiers containing . or +/-)
    en = re.findall(r"\b[A-Za-z][A-Za-z0-9+/.\-_#]{1,20}\b", text)
    raw = en

    stop = {
        # Generic filler / verbs that are not skills
        "company", "we", "you", "will", "team", "need", "needs", "able", "possess",
        "good", "excellent", "experience", "ability", "skill", "skills", "role",
        "responsibilities", "requirements", "required", "above", "related",
        "perform", "complete", "responsible", "drive", "driving", "achieve",
        "improve", "and", "including", "follows", "following", "work", "working",
        "project", "projects", "business", "and", "or", "with", "the", "for",
        "bachelor", "master", "phd", "preferred", "based", "support", "supporting",
        "participate", "provide", "establish", "design", "decision", "analysis",
        "iterate", "planning", "operation", "operations", "collaboration",
        "cross", "functional", "senior", "staff", "plus", "various", "multiple",
        # English filler
        "a", "an", "as", "at", "be", "by", "in", "is", "are", "on", "of", "to",
        "our", "us", "your", "this", "that", "these", "those", "it", "its",
        "all", "with", "and", "or", "the", "for", "you", "we", "will",
    }
    # Filter bare-number tokens like "3" or "5" too
    digit_only = re.compile(r"^\d+$")

    seen = set()
    out = []
    for token in raw:
        key = token.lower()
        if key in seen or key in stop or len(token) < 2 or digit_only.match(token):
            continue
        seen.add(key)
        out.append(token)
    return out[:60]


def main() -> None:
    parser = argparse.ArgumentParser()
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--jd-file", help="Path to a JD text file")
    src.add_argument("--jd-text", help="Pass JD text directly")
    parser.add_argument("--out", help="Output JSON path; prints to stdout by default")
    args = parser.parse_args()

    if args.jd_file:
        path = Path(args.jd_file).expanduser()
        if not path.exists():
            print(f"✗ JD file not found: {path}", file=sys.stderr)
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
    else:
        text = args.jd_text

    sentences = split_sentences(text)
    classified = classify_sentences(sentences)
    special = extract_special(text)
    skills = extract_skills(classified["must"] + classified["responsibilities"])

    result = {
        "must_have": classified["must"],
        "nice_to_have": classified["nice"],
        "responsibilities": classified["responsibilities"],
        "skills_extracted": skills,
        "special_requirements": special,
        "raw_sentence_count": len(sentences),
    }

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        out_path = Path(args.out).expanduser()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(payload, encoding="utf-8")
        print(f"✓ JD parse results saved to: {out_path}")
    else:
        print(payload)


if __name__ == "__main__":
    main()

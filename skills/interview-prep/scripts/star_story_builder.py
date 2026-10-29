#!/usr/bin/env python3
"""
star_story_builder.py — Extract work / project experiences from resume text and
generate a "story matrix" skeleton

Usage:
    python star_story_builder.py --resume resume.md --out stories.md

Outputs a markdown file containing:
- The N experiences detected (reverse-chronological)
- A STAR skeleton placeholder for each experience (for the user / model to fill in)
- The list of behavioral questions each story can answer
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


COMMON_BEHAVIORAL_QUESTIONS = {
    "ownership": [
        "Describe the experience where you demonstrated ownership best",
        "The project you're most proud of",
        "Describe a time you proactively drove something forward",
    ],
    "collab": [
        "Describe a time you drove an initiative across departments / teams",
        "Describe a time you disagreed with a colleague and how you resolved it",
        "Describe a time you persuaded someone to change their mind",
    ],
    "challenge": [
        "Describe a time you delivered a goal with insufficient resources / time",
        "Describe a time you made a difficult decision",
        "Describe a time you broke convention / innovated",
    ],
    "failure": [
        "Describe a time you failed / missed a goal",
        "Describe your biggest mistake",
        "Describe how you responded to negative feedback",
    ],
    "learning": [
        "Describe a time you quickly learned a completely new domain",
        "What's the most important thing you've learned recently?",
    ],
}


def load_resume_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return path.read_text(encoding="utf-8")
    if suffix == ".docx":
        try:
            from docx import Document
        except ImportError:
            print("✗ python-docx is missing", file=sys.stderr)
            sys.exit(1)
        return "\n".join(p.text for p in Document(str(path)).paragraphs)
    print(f"✗ Unsupported format: {suffix}", file=sys.stderr)
    sys.exit(1)


def extract_experiences(text: str) -> list[dict]:
    """
    Lightweight extraction: treat lines shaped like "Company | Role | Dates"
    or "Project | ..." as anchors, then collect everything after that line and
    before the next anchor as the experience content.
    """
    lines = text.splitlines()
    experiences: list[dict] = []
    current = None

    # Match anchors (containing | and a date / year)
    anchor_re = re.compile(
        r"^(?P<title>[^\n]+?[|][^\n]+?[|][^\n]+)$"
    )

    for line in lines:
        if anchor_re.match(line.strip()):
            if current and current["bullets"]:
                experiences.append(current)
            current = {"title": line.strip(), "bullets": []}
        else:
            stripped = line.strip()
            if current and stripped.startswith(("-", "*", "•")):
                current["bullets"].append(stripped.lstrip("-*• "))
    if current and current["bullets"]:
        experiences.append(current)

    return experiences


def categorize_story(bullets: list[str]) -> list[str]:
    """Based on bullet keywords, decide which category of behavioral question this story fits best."""
    text = " ".join(bullets).lower()
    cats = []
    if any(k in text for k in ["led", "led the", "owner", "owned", "drove", "drive", "lead", "0-1", "0 to 1"]):
        cats.append("ownership")
    if any(k in text for k in ["cross-team", "cross-functional", "cross-department", "collaborat", "stakeholder", "partner"]):
        cats.append("collab")
    if any(k in text for k in ["tight deadline", "limited resources", "resource", "decision", "breakthrough", "urgent"]):
        cats.append("challenge")
    if any(k in text for k in ["failed", "failure", "rollback", "retro", "lesson", "pitfall", "postmortem", "post-mortem"]):
        cats.append("failure")
    if any(k in text for k in ["new", "learn", "first time", "from scratch", "unfamiliar"]):
        cats.append("learning")
    return cats or ["ownership"]


def render(experiences: list[dict]) -> str:
    if not experiences:
        return (
            "# Story Matrix (no experiences detected)\n\n"
            "No work / project experiences could be auto-extracted from the resume. Possible reasons:\n"
            "1. The resume doesn't follow the common `Company | Role | Dates` structure\n"
            "2. Experiences are written as plain paragraphs with no clear anchors\n\n"
            "Suggestion: tell me your 3-5 most representative experiences manually, and I'll build the STAR breakdown for you.\n"
        )

    out = ["# Story Matrix", ""]
    out.append(f"Detected {len(experiences)} experiences from the resume; STAR breakdown below.")
    out.append("**Please fill in every `[placeholder]` in each STAR section** — once ready, these stories can cover 80% of behavioral questions.")
    out.append("")

    for idx, exp in enumerate(experiences[:8], start=1):
        cats = categorize_story(exp["bullets"])
        out.append(f"## Story {idx}: {exp['title']}")
        out.append("")
        out.append("**Original resume bullets:**")
        for b in exp["bullets"][:5]:
            out.append(f"- {b}")
        out.append("")
        out.append("**STAR breakdown (fill in):**")
        out.append("- **S (Situation)**: [placeholder - one sentence framing the context / pain point]")
        out.append("- **T (Task)**: [placeholder - your specific task and goal]")
        out.append("- **A (Action)**: [placeholder - 2-4 steps, each with a verb + decision rationale]")
        out.append("- **R (Result)**: [placeholder - quantified result + one line of reflection]")
        out.append("")

        question_pool = []
        for cat in cats:
            question_pool.extend(COMMON_BEHAVIORAL_QUESTIONS.get(cat, []))
        out.append(f"**Behavioral questions this story answers best ({', '.join(cats)}):**")
        for q in question_pool[:4]:
            out.append(f"- {q}")
        out.append("")
        out.append("---")
        out.append("")

    out.append("## Usage Tips")
    out.append("")
    out.append("- Fill in each story's STAR sections; keep each segment within 30-90 seconds when spoken")
    out.append("- Mix and match in the interview: the same story can answer different questions from different angles")
    out.append("- Prepare at least **3 complete stories** (one success + one failure + one collaboration) to cover 80% of behavioral questions")
    out.append('- Within each story emphasize what "I" did; avoid heavy use of "we"')
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()

    resume_text = load_resume_text(Path(args.resume).expanduser())
    experiences = extract_experiences(resume_text)
    report = render(experiences)

    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"✓ Story matrix written to: {args.out}")
    else:
        print(report)


if __name__ == "__main__":
    main()

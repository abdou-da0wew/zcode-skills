#!/usr/bin/env python3
"""
build_quiz_html.py - Injects a question JSON array into a template HTML file,
producing a standalone practice web page.

Usage:
    python3 build_quiz_html.py <questions_json> [options]

Arguments:
    questions_json   Path to the questions JSON file (required)
                     Format: a question array; per-question fields are listed
                     under "Question fields" below

Options:
    --output <path>  Output HTML path (default: ./quiz_<timestamp>.html)
    --title <str>    Page title (default: "Quiz Practice")
    --subtitle <str> Subtitle (auto-generated from the questions by default)
    --id <str>       Question bank ID (for localStorage isolation; defaults to a timestamp)
    --open           Automatically open the page in a browser after generating

Question fields (standard JSON format from quiz-mastery):
    type            single_choice | true_false | fill_blank | short_answer
    prompt          Question text (required)
    options         Options array, used only by single_choice, ["A. xxx", "B. yyy", ...]
    answer          Correct answer
    explanation     Explanation (recommended, especially for K-12 students)
    knowledge_point Knowledge point (used for sidebar grouping)
    category        Category path (recommended format "Subject / Submodule",
                    e.g. "Physics / Electricity")
    level           Difficulty 1-3 (optional)
    memory_tip      Memory tip (optional, highlighted in an orange card)

Exit codes:
    0   Success
    1   Bad arguments / file not found
    2   JSON parse failure / invalid data format
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import webbrowser
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = SKILL_DIR / "templates" / "quiz_template.html"

REQUIRED_FIELDS = {"type", "prompt", "answer"}
VALID_TYPES = {"single_choice", "true_false", "fill_blank", "short_answer"}


def load_questions(path: Path) -> list[dict[str, Any]]:
    """Load the questions JSON and perform basic format validation."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"❌ Cannot read file: {path} - {e}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse failed: {e}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(data, list):
        print(f"❌ Questions must be an array (list); got {type(data).__name__}", file=sys.stderr)
        sys.exit(2)

    if not data:
        print("❌ Question array is empty", file=sys.stderr)
        sys.exit(2)

    cleaned: list[dict[str, Any]] = []
    for i, q in enumerate(data, 1):
        if not isinstance(q, dict):
            print(f"⚠️ Question {i} is not an object; skipped", file=sys.stderr)
            continue
        miss = REQUIRED_FIELDS - set(q.keys())
        if miss:
            # Tolerate the legacy `question` field name used by some quiz-mastery output
            if "prompt" in miss and "question" in q:
                q["prompt"] = q["question"]
                miss.discard("prompt")
        if miss:
            print(f"⚠️ Question {i} is missing fields {miss}; skipped", file=sys.stderr)
            continue
        if q.get("type") not in VALID_TYPES:
            print(f"⚠️ Question {i} has an invalid type: {q.get('type')} (expected one of {VALID_TYPES}); skipped", file=sys.stderr)
            continue
        # Multiple-choice validation: options must exist
        if q["type"] == "single_choice" and not q.get("options"):
            print(f"⚠️ Question {i} (choice question) is missing options; skipped", file=sys.stderr)
            continue
        cleaned.append(q)

    if not cleaned:
        print("❌ No valid questions found", file=sys.stderr)
        sys.exit(2)

    return cleaned


def auto_subtitle(questions: list[dict[str, Any]]) -> str:
    """Auto-generate a subtitle from the questions: count + categories covered."""
    cats = sorted({(q.get("category") or "").strip() for q in questions if q.get("category")})
    type_count: dict[str, int] = {}
    for q in questions:
        t = q.get("type", "?")
        type_count[t] = type_count.get(t, 0) + 1
    type_names = {
        "single_choice": "choice",
        "true_false": "true-false",
        "fill_blank": "fill-blank",
        "short_answer": "short-answer",
    }
    breakdown = " · ".join(f"{type_names.get(t, t)}×{n}" for t, n in type_count.items())
    parts = [f"{len(questions)} questions"]
    if breakdown:
        parts.append(breakdown)
    if cats:
        # Extract top-level subjects (split on "/")
        top_cats = sorted({c.split("/")[0].strip() for c in cats if c})
        if top_cats:
            parts.append(", ".join(top_cats))
    return " · ".join(parts)


def render(questions: list[dict[str, Any]], title: str, subtitle: str, qid: str) -> str:
    """Inject the question data into the template."""
    if not TEMPLATE_PATH.exists():
        print(f"❌ Template file not found: {TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(1)

    html = TEMPLATE_PATH.read_text(encoding="utf-8")

    meta = {"id": qid, "title": title, "subtitle": subtitle}
    quiz_json = json.dumps(questions, ensure_ascii=False)
    meta_json = json.dumps(meta, ensure_ascii=False)

    # Replace in order so a title/subtitle containing {{...}} is not re-interpreted
    html = html.replace("{{TITLE}}", _safe(title))
    html = html.replace("{{SUBTITLE}}", _safe(subtitle))
    html = html.replace("{{QUIZ_DATA}}", quiz_json)
    html = html.replace("{{META}}", meta_json)
    return html


def _safe(s: str) -> str:
    """HTML-safe escaping (used only for plain-text placeholders like title/subtitle)."""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _slug(s: str) -> str:
    """Produce a filename-safe slug."""
    s = re.sub(r"[^\w\u4e00-\u9fa5-]+", "_", s).strip("_")
    return s[:40] or "quiz"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Injects a question JSON array into a template to build a standalone practice web page",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("questions", type=Path, help="Path to the questions JSON file")
    ap.add_argument("--output", "-o", type=Path, help="Output HTML path")
    ap.add_argument("--title", default="📚 Quiz Practice", help="Page title")
    ap.add_argument("--subtitle", default=None, help="Subtitle (auto-generated by default)")
    ap.add_argument("--id", dest="qid", default=None, help="Question bank ID (for localStorage isolation)")
    ap.add_argument("--open", action="store_true", help="Open in the browser after generating")
    args = ap.parse_args()

    if not args.questions.exists():
        print(f"❌ File not found: {args.questions}", file=sys.stderr)
        return 1

    questions = load_questions(args.questions)
    title = args.title
    subtitle = args.subtitle or auto_subtitle(questions)
    qid = args.qid or f"q_{int(time.time())}"

    html = render(questions, title, subtitle, qid)

    # Output path: default to the questions file's directory
    if args.output:
        output = args.output
    else:
        ts = time.strftime("%Y%m%d_%H%M%S")
        output = args.questions.parent / f"quiz_{_slug(title)}_{ts}.html"

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")

    # Emit a single JSON object so the agent can parse it easily
    result = {
        "success": True,
        "output_path": str(output.resolve()),
        "question_count": len(questions),
        "title": title,
        "subtitle": subtitle,
        "id": qid,
        "size_bytes": output.stat().st_size,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if args.open:
        webbrowser.open(f"file://{output.resolve()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

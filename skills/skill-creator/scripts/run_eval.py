#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Tests whether a skill's description causes the agent to trigger (invoke or
read the skill) for a set of queries. Outputs results as JSON.

Works with any OpenAI-compatible LLM server (Ollama, vLLM, LM Studio,
OpenRouter, ...) — no vendor SDK or CLI required. Configure via environment
variables:

    LLM_BASE_URL  (default: http://localhost:11434/v1)
    LLM_API_KEY   (default: "" — only sent if set)
    LLM_MODEL     (default: qwen2.5)
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from scripts.utils import parse_skill_md

# --- OpenAI-compatible endpoint configuration ---
BASE_URL = os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1").rstrip("/")
API_KEY = os.environ.get("LLM_API_KEY", "")
MODEL = os.environ.get("LLM_MODEL", "qwen2.5")


def find_project_root() -> Path:
    """Find the project root by walking up from cwd.

    Kept for interface compatibility with run_loop.py, which passes the
    result through to run_eval(). With the HTTP-based evaluator the value
    is informational only.
    """
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".git").is_dir() or (parent / ".opencode").is_dir():
            return parent
    return current


def chat_completions(body: dict, timeout: int = 60) -> dict:
    """POST to the /chat/completions endpoint of an OpenAI-compatible server."""
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            **({"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}),
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(
            f"LLM request failed ({e.code}): {e.read().decode('utf-8', errors='replace')}"
    )


# Tools offered to the model, mirroring the agent's surface: a Skill tool
# (invoke a skill by name) and a Read tool (read a file by path). Trigger
# detection = the model calls one of these with the skill under test.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "Skill",
            "description": "Invoke one of the available skills by name to handle the user's request.",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill": {
                        "type": "string",
                        "description": "The name of the skill to invoke, exactly as listed in available_skills.",
                    }
                },
                "required": ["skill"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "Read",
            "description": "Read a file from disk.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Absolute path of the file to read.",
                    }
                },
                "required": ["file_path"],
            },
        },
    },
]


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str = "",
    model: str | None = None,
) -> bool:
    """Run a single query and return whether the skill was triggered.

    The skill under test is presented to the model through an
    "available_skills" block in the system prompt (name + description),
    mimicking how the agent lists skills. The query is sent as a user
    message together with the Skill/Read tools; the model has triggered
    the skill if it calls Skill with this skill's name or Read on the
    skill's SKILL.md file.
    """
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{skill_name}-skill-{unique_id}"

    system_prompt = (
        "You are a coding agent. You have a set of skills available.\n"
        "available_skills:\n"
        f"- {clean_name}: {skill_description}\n"
        "\n"
        "When one of the available skills is relevant to the user's request, "
        "invoke it with the Skill tool (or read its SKILL.md with the Read "
        "tool). If no skill is relevant, do not call any tool."
    )

    body = {
        "model": model or MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        "tools": TOOLS,
        "tool_choice": "auto",
    }

    try:
        response = chat_completions(body, timeout=timeout)
    except Exception as e:
        print(f"Warning: LLM request failed: {e}", file=sys.stderr)
        return False

    choices = response.get("choices") or []
    message = choices[0].get("message", {}) if choices else {}

    for tool_call in message.get("tool_calls") or []:
        fn = tool_call.get("function", {}) or {}
        tool_name = fn.get("name", "")
        raw_args = fn.get("arguments", "")
        try:
            args = json.loads(raw_args) if isinstance(raw_args, str) else (raw_args or {})
        except json.JSONDecodeError:
            args = {}
        args_blob = json.dumps(args, ensure_ascii=False) if args else ""

        if tool_name == "Skill" and clean_name in args_blob:
            return True
        if tool_name == "Read" and clean_name in args_blob:
            return True
        # Any other tool call (or a call for a different skill) = no trigger
        return False

    return False


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
) -> dict:
    """Run the full eval set and return results."""
    results = []

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append({
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Model to use (default: $LLM_MODEL or qwen2.5)")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, content = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}", file=sys.stderr)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Bulk-test the batch/list API: provinces x correct/wrong classify x high/low scores."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# Allow running directly from the scripts/ directory
sys.path.insert(0, str(Path(__file__).resolve().parent))

from province_config import (  # noqa: E402
    MODE_312,
    MODE_33,
    MODE_OLD,
    UNSUPPORTED_PROVINCES,
    batch_list_query_params,
    infer_grade_type,
)

BASE_URL = os.environ.get("ZP_API_BASE_URL", "")  # set to your gaokao volunteer API server
BATCH_LIST_PATH = "/zp/volunteer/batch/list"

PROVINCE_CLASSIFY: dict[str, list[str]] = {}
for p in MODE_33:
    PROVINCE_CLASSIFY[p] = ["\u7efc\u5408"]  # comprehensive
for p in MODE_312:
    PROVINCE_CLASSIFY[p] = ["\u7269\u7406", "\u5386\u53f2"]  # physics / history
for p in MODE_OLD:
    PROVINCE_CLASSIFY[p] = ["\u6587\u79d1", "\u7406\u79d1"]  # liberal arts / science
for p in UNSUPPORTED_PROVINCES:
    PROVINCE_CLASSIFY[p] = ["\u7efc\u5408"]

WRONG_CLASSIFY = {
    "\u7efc\u5408": "\u7269\u7406",  # comprehensive -> physics (wrong on purpose)
    "\u7269\u7406": "\u7efc\u5408",
    "\u5386\u53f2": "\u7406\u79d1",
    "\u6587\u79d1": "\u7269\u7406",
    "\u7406\u79d1": "\u5386\u53f2",
}

HIGH_SCORE = 650
LOW_SCORE = 280


def call_batch_from_payload(payload: dict) -> dict:
    params = batch_list_query_params(dict(payload))
    query = urlencode(params)
    url = f"{BASE_URL.rstrip('/')}{BATCH_LIST_PATH}?{query}"
    req = Request(url, method="GET", headers={"Accept": "*/*"})
    try:
        with urlopen(req, timeout=30) as resp:
            text = resp.read().decode(resp.headers.get_content_charset() or "utf-8")
    except HTTPError as e:
        return {"http": e.code, "body": e.read().decode("utf-8", errors="replace")}
    except URLError as e:
        return {"error": str(e.reason)}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "invalid json", "body": text[:200]}


def summarize_result(raw: dict) -> str:
    if "error" in raw or "http" in raw:
        return f"FAIL:{raw.get('http') or raw.get('error')}"
    status = raw.get("status")
    msg = raw.get("message", "")
    result = raw.get("result")
    if status != 0:
        return f"FAIL:status={status},{msg}"
    if not isinstance(result, list):
        return "FAIL:result not list"
    if not result:
        return "OK:empty[]"
    batches = [f"{x.get('batch')}({x.get('gradeType')}/{x.get('type')})" for x in result[:3]]
    extra = f"+{len(result)-3}" if len(result) > 3 else ""
    return f"OK:{len(result)} items [{', '.join(batches)}{extra}]"


def main() -> int:
    rows: list[dict] = []
    provinces = sorted(PROVINCE_CLASSIFY.keys(), key=lambda x: (x not in UNSUPPORTED_PROVINCES, x))

    print("=== Correct classify x high/low scores (Beijing/Shanghai/Tianjin include gradeType) ===")
    for province in provinces:
        classifies = PROVINCE_CLASSIFY[province]
        primary = classifies[0]
        for score_label, score in [("high", HIGH_SCORE), ("low", LOW_SCORE)]:
            payload = {
                "province": province,
                "classify": primary,
                "score": score,
                "batch": "\u672c\u79d1\u6279",
            }
            if province in ("\u5317\u4eac", "\u4e0a\u6d77", "\u5929\u6d25"):
                payload["gradeType"] = infer_grade_type(province, score, batch_pref="\u672c\u79d1\u6279")
            try:
                raw = call_batch_from_payload(payload)
            except ValueError as e:
                raw = {"status": -1, "message": str(e)}
            summary = summarize_result(raw)
            rows.append({
                "province": province,
                "classify": primary,
                "score": score,
                "score_label": score_label,
                "gradeType": payload.get("gradeType"),
                "wrong_classify": False,
                "summary": summary,
                "status": raw.get("status"),
                "message": raw.get("message"),
                "count": len(raw.get("result") or []) if isinstance(raw.get("result"), list) else None,
            })
            mark = "✓" if summary.startswith("OK") and "empty" not in summary else "✗"
            gt = payload.get("gradeType") or ""
            print(f"  {mark} {province:4s} {primary} {gt:2s} {score_label} ({score}) -> {summary}")
            time.sleep(0.12)

    print("\n=== Wrong-classify probe (high score) ===")
    for province in provinces:
        if province in UNSUPPORTED_PROVINCES:
            continue
        primary = PROVINCE_CLASSIFY[province][0]
        wrong = WRONG_CLASSIFY.get(primary, "\u7efc\u5408" if primary != "\u7efc\u5408" else "\u7269\u7406")
        ok_payload = {"province": province, "classify": primary, "score": HIGH_SCORE, "batch": "\u672c\u79d1\u6279"}
        wrong_payload = dict(ok_payload, classify=wrong)
        if province in ("\u5317\u4eac", "\u4e0a\u6d77", "\u5929\u6d25"):
            ok_payload["gradeType"] = infer_grade_type(province, HIGH_SCORE, batch_pref="\u672c\u79d1\u6279")
            wrong_payload["gradeType"] = ok_payload["gradeType"]
        try:
            raw_ok = call_batch_from_payload(ok_payload)
            raw_wrong = call_batch_from_payload(wrong_payload)
        except ValueError as e:
            print(f"  ! {province}: validate error {e}")
            continue
        ok_s = summarize_result(raw_ok)
        wrong_s = summarize_result(raw_wrong)
        if wrong_s != ok_s:
            print(f"  ! {province}: correct({primary})={ok_s} vs wrong({wrong})={wrong_s}")
        time.sleep(0.12)

    out = Path(__file__).resolve().parent.parent / "output" / "batch_api_test_results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDetailed results saved: {out}")

    fails = [
        r for r in rows
        if not r["summary"].startswith("OK") or "empty[]" in r["summary"]
        if not r.get("wrong_classify")
    ]
    print(f"\n=== Summary: {len(fails)} unexpected failures with correct parameters ===")
    for r in fails:
        print(f"  {r['province']} {r['classify']} {r['score_label']} -> {r['summary']} | {r.get('message')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

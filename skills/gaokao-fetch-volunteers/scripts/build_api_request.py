#!/usr/bin/env python3
"""Build the API request body from student.json, mapping student preferences to
optional API parameters.

NOTE: city/province/tag/major-class values below are the gaokao API's Chinese string
values, written as \\uXXXX escapes (Python decodes them identically) so this source
stays ASCII.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Preferred city -> API provinces value (province preference). Keys and values are the
# API's Chinese names, unicode-escaped. Romanized: Beijing->Beijing (municipality),
# Shanghai->Shanghai, Tianjin->Tianjin, Chongqing->Chongqing, Shenzhen->Guangdong,
# Guangzhou->Guangdong, Dongguan->Guangdong, Foshan->Guangdong, Wuhan->Hubei,
# Chengdu->Sichuan, Hangzhou->Zhejiang, Ningbo->Zhejiang, Nanjing->Jiangsu,
# Suzhou->Jiangsu, Wuxi->Jiangsu, Xi'an->Shaanxi, Changsha->Hunan, Zhengzhou->Henan,
# Jinan->Shandong, Qingdao->Shandong, Hefei->Anhui, Xiamen->Fujian, Fuzhou->Fujian,
# Dalian->Liaoning, Shenyang->Liaoning, Harbin->Heilongjiang, Changchun->Jilin,
# Kunming->Yunnan, Nanning->Guangxi, Haikou->Hainan, Shijiazhuang->Hebei,
# Taiyuan->Shanxi, Nanchang->Jiangxi, Lanzhou->Gansu, Guiyang->Guizhou,
# Hohhot->Inner Mongolia, Urumqi->Xinjiang, Yinchuan->Ningxia, Xining->Qinghai,
# Lhasa->Tibet.
CITY_TO_PROVINCE: dict[str, str] = {
    "\u5317\u4eac": "\u5317\u4eac",  # Beijing
    "\u4e0a\u6d77": "\u4e0a\u6d77",  # Shanghai
    "\u5929\u6d25": "\u5929\u6d25",  # Tianjin
    "\u91cd\u5e86": "\u91cd\u5e86",  # Chongqing
    "\u6df1\u5733": "\u5e7f\u4e1c",  # Shenzhen -> Guangdong
    "\u5e7f\u5dde": "\u5e7f\u4e1c",  # Guangzhou -> Guangdong
    "\u4e1c\u839e": "\u5e7f\u4e1c",  # Dongguan -> Guangdong
    "\u4f5b\u5c71": "\u5e7f\u4e1c",  # Foshan -> Guangdong
    "\u6b66\u6c49": "\u6e56\u5317",  # Wuhan -> Hubei
    "\u6210\u90fd": "\u56db\u5ddd",  # Chengdu -> Sichuan
    "\u676d\u5dde": "\u6d59\u6c5f",  # Hangzhou -> Zhejiang
    "\u5b81\u6ce2": "\u6d59\u6c5f",  # Ningbo -> Zhejiang
    "\u5357\u4eac": "\u6c5f\u82cf",  # Nanjing -> Jiangsu
    "\u82cf\u5dde": "\u6c5f\u82cf",  # Suzhou -> Jiangsu
    "\u65e0\u9521": "\u6c5f\u82cf",  # Wuxi -> Jiangsu
    "\u897f\u5b89": "\u9655\u897f",  # Xi'an -> Shaanxi
    "\u957f\u6c99": "\u6e56\u5357",  # Changsha -> Hunan
    "\u90d1\u5dde": "\u6cb3\u5357",  # Zhengzhou -> Henan
    "\u6d4e\u5357": "\u5c71\u4e1c",  # Jinan -> Shandong
    "\u9752\u5c9b": "\u5c71\u4e1c",  # Qingdao -> Shandong
    "\u5408\u80a5": "\u5b89\u5fbd",  # Hefei -> Anhui
    "\u53a6\u95e8": "\u798f\u5efa",  # Xiamen -> Fujian
    "\u798f\u5dde": "\u798f\u5efa",  # Fuzhou -> Fujian
    "\u5927\u8fde": "\u8fbd\u5b81",  # Dalian -> Liaoning
    "\u6c88\u9633": "\u8fbd\u5b81",  # Shenyang -> Liaoning
    "\u54c8\u5c14\u6ee8": "\u9ed1\u9f99\u6c5f",  # Harbin -> Heilongjiang
    "\u957f\u6625": "\u5409\u6797",  # Changchun -> Jilin
    "\u6606\u660e": "\u4e91\u5357",  # Kunming -> Yunnan
    "\u5357\u5b81": "\u5e7f\u897f",  # Nanning -> Guangxi
    "\u6d77\u53e3": "\u6d77\u5357",  # Haikou -> Hainan
    "\u77f3\u5bb6\u5e84": "\u6cb3\u5317",  # Shijiazhuang -> Hebei
    "\u592a\u539f": "\u5c71\u897f",  # Taiyuan -> Shanxi
    "\u5357\u660c": "\u6c5f\u897f",  # Nanchang -> Jiangxi
    "\u5170\u5dde": "\u7518\u8083",  # Lanzhou -> Gansu
    "\u8d35\u9633": "\u8d35\u5dde",  # Guiyang -> Guizhou
    "\u547c\u548c\u6d69\u7279": "\u5185\u8499\u53e4",  # Hohhot -> Inner Mongolia
    "\u4e4c\u9c81\u6728\u9f50": "\u65b0\u7586",  # Urumqi -> Xinjiang
    "\u94f6\u5ddd": "\u5b81\u590f",  # Yinchuan -> Ningxia
    "\u897f\u5b81": "\u9752\u6d77",  # Xining -> Qinghai
    "\u62c9\u8428": "\u897f\u85cf",  # Lhasa -> Tibet
}

DEFAULT_API_OPTIONS: dict[str, Any] = {
    "universityNum": 30,
    "majorNum": 6,
    "isAdjust": True,
    "volunteerType": "ACADEMY_GROUP",
    "returnUniversityNum": 30,
    "intentionNum": 0,
}


def _join_csv(values: list[str] | None) -> str | None:
    if not values:
        return None
    cleaned = [str(v).strip() for v in values if str(v).strip()]
    return ",".join(cleaned) if cleaned else None


def cities_to_provinces(cities: list[str] | None) -> list[str]:
    """Map preferred cities (deduplicated) to the list of API province values."""
    if not cities:
        return []
    provinces: list[str] = []
    seen: set[str] = set()
    for city in cities:
        # Strip the Chinese suffixes for "city" and "province" (unicode-escaped).
        key = str(city).strip().replace("\u5e02", "").replace("\u7701", "")
        if not key:
            continue
        province = CITY_TO_PROVINCE.get(key, key)
        if province not in seen:
            seen.add(province)
            provinces.append(province)
    return provinces


def student_to_api_payload(student: dict[str, Any]) -> dict[str, Any]:
    """Convert student.json into the API request body."""
    preferred_provinces = student.get("preferred_provinces") or []
    if not preferred_provinces:
        preferred_provinces = cities_to_provinces(student.get("preferred_cities"))

    payload: dict[str, Any] = {
        "province": student.get("province"),
        "classify": student.get("classify"),
        "subjects": student.get("subjects"),
        "gradeType": student.get("gradeType"),
        "score": student.get("score"),
        "rank": student.get("rank"),
        "batch": student.get("batch"),
        "universitys": _join_csv(student.get("preferred_universities")),
        "provinces": _join_csv(preferred_provinces),
        "tags": _join_csv(student.get("preferred_tags")),
        "majorClass": _join_csv(student.get("preferred_major_classes")),
        **DEFAULT_API_OPTIONS,
    }

    overrides = student.get("api_overrides") or {}
    for key, value in overrides.items():
        if value is not None:
            payload[key] = value

    return payload


def summarize_preferences(student: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    """Return a preference-mapping summary so the agent can explain it to the user."""
    return {
        "universitys": payload.get("universitys"),
        "provinces": payload.get("provinces"),
        "tags": payload.get("tags"),
        "majorClass": payload.get("majorClass"),
        "sources": {
            "preferred_universities": student.get("preferred_universities"),
            "preferred_cities": student.get("preferred_cities"),
            "preferred_provinces": student.get("preferred_provinces"),
            "preferred_tags": student.get("preferred_tags"),
            "preferred_major_classes": student.get("preferred_major_classes"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the API request JSON from student.json")
    parser.add_argument("-i", "--input", type=Path, required=True, help="path to student.json")
    parser.add_argument("-o", "--output", type=Path, required=True, help="output api_request.json")
    parser.add_argument(
        "--summary",
        type=Path,
        help="optional: output a preference-mapping summary JSON (for the agent to verify)",
    )
    args = parser.parse_args()

    try:
        student = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error: cannot read student.json - {e}", file=sys.stderr)
        return 1

    payload = student_to_api_payload(student)
    try:
        from province_config import validate_classify, validate_subjects_for_volunteer_api

        validate_classify(str(payload.get("province", "")), payload.get("classify"))
        validate_subjects_for_volunteer_api(payload)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    required = ["province", "classify", "score"]
    missing = [k for k in required if not payload.get(k)]
    if missing:
        print(f"Error: student.json is missing API-required fields {missing}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"API request written: {args.output}")

    if args.summary:
        summary = summarize_preferences(student, payload)
        args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Preference-mapping summary written: {args.summary}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

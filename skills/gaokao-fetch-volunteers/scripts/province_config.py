#!/usr/bin/env python3
"""Per-province gaokao modes, classify validation, and API parameter normalization.

NOTE: string values compared below (provinces, classify, subjects, gradeType) are the
gaokao API's Chinese string values, written as \\uXXXX escapes so this source stays
ASCII. Python decodes them to the exact same characters.
"""

from __future__ import annotations

from typing import Any

# Only Beijing / Shanghai / Tianjin need gradeType for the batch and volunteer APIs.
PROVINCES_REQUIRING_GRADE_TYPE = frozenset({"\u5317\u4eac", "\u4e0a\u6d77", "\u5929\u6d25"})

# The batch/volunteer APIs do not support this province in the test environment (Tibet).
UNSUPPORTED_PROVINCES = frozenset({"\u897f\u85cf"})

# 3+3 mode: Shanghai, Beijing, Tianjin, Shandong, Zhejiang, Hainan.
MODE_33 = frozenset({"\u4e0a\u6d77", "\u5317\u4eac", "\u5929\u6d25", "\u5c71\u4e1c", "\u6d59\u6c5f", "\u6d77\u5357"})
# 3+1+2 mode: Guangdong, Jiangsu, Hebei, Hubei, Hunan, Fujian, Liaoning, Chongqing,
# Gansu, Heilongjiang, Jilin, Anhui, Jiangxi, Guizhou, Guangxi, Yunnan, Inner Mongolia,
# Sichuan, Ningxia, Shanxi, Henan, Shaanxi, Qinghai.
MODE_312 = frozenset({
    "\u5e7f\u4e1c", "\u6c5f\u82cf", "\u6cb3\u5317", "\u6e56\u5317", "\u6e56\u5357", "\u798f\u5efa", "\u8fbd\u5b81", "\u91cd\u5e86", "\u7518\u8083",
    "\u9ed1\u9f99\u6c5f", "\u5409\u6797", "\u5b89\u5fbd", "\u6c5f\u897f", "\u8d35\u5dde", "\u5e7f\u897f", "\u4e91\u5357", "\u5185\u8499\u53e4",
    "\u56db\u5ddd", "\u5b81\u590f", "\u5c71\u897f", "\u6cb3\u5357", "\u9655\u897f", "\u9752\u6d77",
})
# Old gaokao system (liberal arts / science): Xinjiang.
MODE_OLD = frozenset({"\u65b0\u7586"})

# classify values: comprehensive / physics / history / liberal arts / science.
VALID_CLASSIFY_BY_MODE: dict[str, frozenset[str]] = {
    "33": frozenset({"\u7efc\u5408"}),
    "312": frozenset({"\u7269\u7406", "\u5386\u53f2"}),
    "old": frozenset({"\u6587\u79d1", "\u7406\u79d1"}),
}

MODE_LABELS: dict[str, str] = {
    "33": "3+3",
    "312": "3+1+2",
    "old": "old system",
}

# Subjects: chemistry, biology, politics, geography / physics, history, ...
SUBJECTS_312_ELECTIVES = frozenset({"\u5316\u5b66", "\u751f\u7269", "\u653f\u6cbb", "\u5730\u7406"})
SUBJECTS_33_POOL = frozenset({"\u7269\u7406", "\u5386\u53f2", "\u5316\u5b66", "\u751f\u7269", "\u653f\u6cbb", "\u5730\u7406"})
SUBJECTS_33_ZHEJIANG = SUBJECTS_33_POOL | frozenset({"\u6280\u672f"})


def parse_subjects_list(subjects: Any) -> list[str]:
    if subjects in (None, "", "null", "NULL"):
        return []
    return [s.strip() for s in str(subjects).split(",") if s.strip()]


def get_province_mode(province: str | None) -> str:
    if not province:
        return "unknown"
    if province in UNSUPPORTED_PROVINCES:
        return "unsupported"
    if province in MODE_OLD:
        return "old"
    if province in MODE_33:
        return "33"
    if province in MODE_312:
        return "312"
    return "unknown"


def validate_classify(province: str, classify: str | None) -> None:
    """Validate that classify matches the province's subject-combination mode."""
    mode = get_province_mode(province)
    if mode == "unsupported":
        raise ValueError(
            f"Province {province} is not supported by the test environment yet "
            f"(the platform has not integrated this province's data)"
        )
    if mode == "unknown":
        return
    if not classify:
        valid = VALID_CLASSIFY_BY_MODE[mode]
        raise ValueError(
            f"Missing classify: {province} uses the {MODE_LABELS[mode]} mode; "
            f"classify must be one of {'/'.join(sorted(valid))}"
        )
    valid = VALID_CLASSIFY_BY_MODE[mode]
    if classify not in valid:
        raise ValueError(
            f"classify does not match the province: {province} uses the {MODE_LABELS[mode]} mode; "
            f"classify should be {'/'.join(sorted(valid))}, got {classify!r}. "
            f"A wrong classify makes the batch API return an empty list."
        )


def infer_grade_type(
    province: str | None,
    score: int | None,
    explicit: str | None = None,
    batch_pref: str | None = None,
) -> str | None:
    """Infer undergraduate/vocational for Beijing/Shanghai/Tianjin; None for other provinces."""
    if province not in PROVINCES_REQUIRING_GRADE_TYPE:
        return None
    # API values (escaped): "\u672c\u79d1" = undergraduate, "\u4e13\u79d1" = vocational,
    # "\u4e13\u79d1\u6279" = vocational batch, "\u672c\u79d1\u6279" = undergraduate batch.
    if explicit in ("\u672c\u79d1", "\u4e13\u79d1"):
        return explicit
    if batch_pref == "\u4e13\u79d1\u6279":
        return "\u4e13\u79d1"
    if batch_pref == "\u672c\u79d1\u6279":
        return "\u672c\u79d1"
    if score is not None and score <= 450:
        return "\u4e13\u79d1"
    return "\u672c\u79d1"


def batch_list_query_params(payload: dict[str, Any]) -> dict[str, Any]:
    """Build batch/list query parameters from the request payload."""
    province = payload.get("province")
    classify = payload.get("classify")
    score = payload.get("score")
    if not province or not classify or score is None:
        raise ValueError("batch/list requires province, classify, and score")

    validate_classify(str(province), str(classify))

    params: dict[str, Any] = {
        "province": province,
        "classify": classify,
        "score": int(score),
    }
    grade_type = payload.get("gradeType")
    if not grade_type and province in PROVINCES_REQUIRING_GRADE_TYPE:
        grade_type = infer_grade_type(
            str(province),
            int(score),
            batch_pref=payload.get("batch"),
        )
        if grade_type:
            payload["gradeType"] = grade_type
    if province in PROVINCES_REQUIRING_GRADE_TYPE and grade_type:
        params["gradeType"] = grade_type
    return params


def normalize_subjects_for_api(payload: dict[str, Any]) -> None:
    """Normalize the subjects field per province rules."""
    province = payload.get("province")
    grade_type = payload.get("gradeType")
    subjects = payload.get("subjects")

    if province == "\u65b0\u7586":  # Xinjiang: subjects must be absent
        if subjects in (None, "", "null", "NULL"):
            payload.pop("subjects", None)
        return

    if province in PROVINCES_REQUIRING_GRADE_TYPE and grade_type == "\u4e13\u79d1":
        if subjects in (None, "", "null", "NULL"):
            payload["subjects"] = "null"
        return

    if subjects in ("null", "NULL", ""):
        payload["subjects"] = None


def sanitize_payload_for_api(payload: dict[str, Any]) -> None:
    """Clean up the request body per province rules before calling the volunteer API."""
    province = payload.get("province")
    if province not in PROVINCES_REQUIRING_GRADE_TYPE:
        payload.pop("gradeType", None)
    normalize_subjects_for_api(payload)


def validate_subjects_for_volunteer_api(payload: dict[str, Any]) -> None:
    """Validate that subjects satisfies the province requirements before the volunteer API."""
    province = str(payload.get("province") or "")
    mode = get_province_mode(province)
    label = MODE_LABELS.get(mode, mode)

    if province == "\u65b0\u7586":  # Xinjiang
        return
    if province in PROVINCES_REQUIRING_GRADE_TYPE and payload.get("gradeType") == "\u4e13\u79d1":
        return

    subjects = payload.get("subjects")
    if subjects in (None, "", "null", "NULL"):
        raise ValueError(
            f"Missing subjects: {province} ({label}) requires a subject combination, "
            f"e.g. physics,chemistry,biology"
        )

    parts = parse_subjects_list(subjects)
    classify = payload.get("classify")

    if mode == "312":
        if len(parts) != 3:
            raise ValueError(
                f"Invalid subjects: {province} (3+1+2) requires all three subjects "
                f"(primary subject + two electives), comma-separated, "
                f"e.g. with classify=physics use subjects=physics,chemistry,biology; "
                f"never send only the two electives. Got {subjects!r} ({len(parts)} subjects)"
            )
        if classify not in parts:
            raise ValueError(
                f"subjects inconsistent with classify: {province} classify={classify!r}; "
                f"subjects must include the primary subject {classify!r}, got {subjects!r}"
            )
        electives = [p for p in parts if p != classify]
        if len(electives) != 2:
            raise ValueError(
                f"Invalid subjects: {province} (3+1+2) requires two electives besides the "
                f"primary subject (chemistry/biology/politics/geography), got {subjects!r}"
            )
        invalid = [p for p in electives if p not in SUBJECTS_312_ELECTIVES]
        if invalid:
            raise ValueError(
                f"subjects contains invalid electives {invalid}: "
                f"3+1+2 electives are limited to chemistry/biology/politics/geography"
            )
        return

    if mode == "33" and province not in PROVINCES_REQUIRING_GRADE_TYPE:
        if len(parts) != 3:
            raise ValueError(
                f"Invalid subjects: {province} (3+3) requires all three elective subjects, "
                f"comma-separated, e.g. physics,chemistry,biology; "
                f"got {subjects!r} ({len(parts)} subjects)"
            )
        pool = SUBJECTS_33_ZHEJIANG if province == "\u6d59\u6c5f" else SUBJECTS_33_POOL  # Zhejiang
        invalid = [p for p in parts if p not in pool]
        if invalid:
            raise ValueError(f"subjects contains invalid subjects {invalid}: see reference.md for {province}'s subject pool")
        return

    if mode == "33" and province in PROVINCES_REQUIRING_GRADE_TYPE:
        if payload.get("gradeType") == "\u672c\u79d1" and len(parts) != 3:
            raise ValueError(
                f"Invalid subjects: {province} (3+3 undergraduate) requires all three "
                f"subjects, e.g. physics,chemistry,biology; got {subjects!r}"
            )

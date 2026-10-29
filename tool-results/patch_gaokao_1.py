#!/usr/bin/env python3
"""One-off patcher for gaokao-fetch-volunteers scripts (localization to ASCII/English)."""
from pathlib import Path

BASE = Path("/home/z/my-project/skills/gaokao-fetch-volunteers/scripts")


def patch(path: Path, repls: list[tuple[str, str]]) -> None:
    src = path.read_text(encoding="utf-8")
    miss = 0
    for old, new in repls:
        n = src.count(old)
        if n == 0:
            print(f"MISS in {path.name}: {old[:60]!r}")
            miss += 1
            continue
        src = src.replace(old, new)
    path.write_text(src, encoding="utf-8")
    print(f"{path.name}: done, {miss} misses")


# ---------------- province_config.py ----------------
PC = []
PC.append((
    '"""各省高考模式、classify 校验与 API 参数规范化。"""',
    '"""Per-province gaokao modes, classify validation, and API parameter normalization.\n\n'
    'NOTE: string values compared below (provinces, classify, subjects, gradeType) are the\n'
    'gaokao API\'s Chinese string values, written as \\uXXXX escapes so this source stays\n'
    'ASCII. Python decodes them to the exact same characters.\n"""',
))
PC.append((
    '# 仅京沪津批次接口与志愿接口需要 gradeType\nPROVINCES_REQUIRING_GRADE_TYPE = frozenset({"北京", "上海", "天津"})',
    '# Only Beijing / Shanghai / Tianjin need gradeType for the batch and volunteer APIs.\nPROVINCES_REQUIRING_GRADE_TYPE = frozenset({"\\u5317\\u4eac", "\\u4e0a\\u6d77", "\\u5929\\u6d25"})',
))
PC.append((
    '# 测试环境批次接口暂不支持\nUNSUPPORTED_PROVINCES = frozenset({"西藏"})',
    '# The batch/volunteer APIs do not support this province in the test environment (Tibet).\nUNSUPPORTED_PROVINCES = frozenset({"\\u897f\\u85cf"})',
))
PC.append((
    'MODE_33 = frozenset({"上海", "北京", "天津", "山东", "浙江", "海南"})',
    '# 3+3 mode: Shanghai, Beijing, Tianjin, Shandong, Zhejiang, Hainan.\nMODE_33 = frozenset({"\\u4e0a\\u6d77", "\\u5317\\u4eac", "\\u5929\\u6d25", "\\u5c71\\u4e1c", "\\u6d59\\u6c5f", "\\u6d77\\u5357"})',
))
PC.append((
    'MODE_312 = frozenset({\n    "广东", "江苏", "河北", "湖北", "湖南", "福建", "辽宁", "重庆", "甘肃",\n    "黑龙江", "吉林", "安徽", "江西", "贵州", "广西", "云南", "内蒙古",\n    "四川", "宁夏", "山西", "河南", "陕西", "青海",\n})',
    '# 3+1+2 mode: Guangdong, Jiangsu, Hebei, Hubei, Hunan, Fujian, Liaoning, Chongqing,\n'
    '# Gansu, Heilongjiang, Jilin, Anhui, Jiangxi, Guizhou, Guangxi, Yunnan, Inner Mongolia,\n'
    '# Sichuan, Ningxia, Shanxi, Henan, Shaanxi, Qinghai.\n'
    'MODE_312 = frozenset({\n'
    '    "\\u5e7f\\u4e1c", "\\u6c5f\\u82cf", "\\u6cb3\\u5317", "\\u6e56\\u5317", "\\u6e56\\u5357", "\\u798f\\u5efa", "\\u8fbd\\u5b81", "\\u91cd\\u5e86", "\\u7518\\u8083",\n'
    '    "\\u9ed1\\u9f99\\u6c5f", "\\u5409\\u6797", "\\u5b89\\u5fbd", "\\u6c5f\\u897f", "\\u8d35\\u5dde", "\\u5e7f\\u897f", "\\u4e91\\u5357", "\\u5185\\u8499\\u53e4",\n'
    '    "\\u56db\\u5ddd", "\\u5b81\\u590f", "\\u5c71\\u897f", "\\u6cb3\\u5357", "\\u9655\\u897f", "\\u9752\\u6d77",\n'
    '})',
))
PC.append((
    'MODE_OLD = frozenset({"新疆"})',
    '# Old gaokao system (liberal arts / science): Xinjiang.\nMODE_OLD = frozenset({"\\u65b0\\u7586"})',
))
PC.append((
    'VALID_CLASSIFY_BY_MODE: dict[str, frozenset[str]] = {\n    "33": frozenset({"综合"}),\n    "312": frozenset({"物理", "历史"}),\n    "老高考": frozenset({"文科", "理科"}),\n}',
    '# classify values: comprehensive / physics / history / liberal arts / science.\nVALID_CLASSIFY_BY_MODE: dict[str, frozenset[str]] = {\n    "33": frozenset({"\\u7efc\\u5408"}),\n    "312": frozenset({"\\u7269\\u7406", "\\u5386\\u53f2"}),\n    "old": frozenset({"\\u6587\\u79d1", "\\u7406\\u79d1"}),\n}',
))
PC.append((
    'MODE_LABELS: dict[str, str] = {\n    "33": "3+3",\n    "312": "3+1+2",\n    "老高考": "老高考",\n}',
    'MODE_LABELS: dict[str, str] = {\n    "33": "3+3",\n    "312": "3+1+2",\n    "old": "old system",\n}',
))
PC.append((
    'SUBJECTS_312_ELECTIVES = frozenset({"化学", "生物", "政治", "地理"})\nSUBJECTS_33_POOL = frozenset({"物理", "历史", "化学", "生物", "政治", "地理"})\nSUBJECTS_33_ZHEJIANG = SUBJECTS_33_POOL | frozenset({"技术"})',
    '# Subjects: chemistry, biology, politics, geography / physics, history, ...\nSUBJECTS_312_ELECTIVES = frozenset({"\\u5316\\u5b66", "\\u751f\\u7269", "\\u653f\\u6cbb", "\\u5730\\u7406"})\nSUBJECTS_33_POOL = frozenset({"\\u7269\\u7406", "\\u5386\\u53f2", "\\u5316\\u5b66", "\\u751f\\u7269", "\\u653f\\u6cbb", "\\u5730\\u7406"})\nSUBJECTS_33_ZHEJIANG = SUBJECTS_33_POOL | frozenset({"\\u6280\\u672f"})',
))
PC.append((
    '    if province in MODE_OLD:\n        return "老高考"',
    '    if province in MODE_OLD:\n        return "old"',
))
PC.append((
    'def validate_classify(province: str, classify: str | None) -> None:\n    """校验 classify 是否与省份选科模式匹配。"""',
    'def validate_classify(province: str, classify: str | None) -> None:\n    """Validate that classify matches the province\'s subject-combination mode."""',
))
PC.append((
    '        raise ValueError(\n            f"省份 {province} 在测试环境暂不支持志愿/批次接口（平台未接入该省数据）"\n        )',
    '        raise ValueError(\n            f"Province {province} is not supported by the test environment yet "\n            f"(the platform has not integrated this province\'s data)"\n        )',
))
PC.append((
    '        raise ValueError(\n            f"缺少 classify：{province} 为{MODE_LABELS[mode]}模式，应填 {\'/\'.join(sorted(valid))}"\n        )',
    '        raise ValueError(\n            f"Missing classify: {province} uses the {MODE_LABELS[mode]} mode; "\n            f"classify must be one of {\'/\'.join(sorted(valid))}"\n        )',
))
PC.append((
    '        raise ValueError(\n            f"classify 与省份不匹配：{province} 为{MODE_LABELS[mode]}模式，"\n            f"classify 应为 {\'/\'.join(sorted(valid))}，当前为 {classify!r}。"\n            f"错误 classify 会导致批次接口返回空列表。"\n        )',
    '        raise ValueError(\n            f"classify does not match the province: {province} uses the {MODE_LABELS[mode]} mode; "\n            f"classify should be {\'/\'.join(sorted(valid))}, got {classify!r}. "\n            f"A wrong classify makes the batch API return an empty list."\n        )',
))
PC.append((
    '    """京沪津推断本科/专科；其他省份返回 None。"""',
    '    """Infer undergraduate/vocational for Beijing/Shanghai/Tianjin; None for other provinces."""',
))
PC.append((
    '    if explicit in ("本科", "专科"):\n        return explicit\n    if batch_pref == "专科批":\n        return "专科"\n    if batch_pref == "本科批":\n        return "本科"\n    if score is not None and score <= 450:\n        return "专科"\n    return "本科"',
    '    # API values (escaped): "\\u672c\\u79d1" = undergraduate, "\\u4e13\\u79d1" = vocational,\n    # "\\u4e13\\u79d1\\u6279" = vocational batch, "\\u672c\\u79d1\\u6279" = undergraduate batch.\n    if explicit in ("\\u672c\\u79d1", "\\u4e13\\u79d1"):\n        return explicit\n    if batch_pref == "\\u4e13\\u79d1\\u6279":\n        return "\\u4e13\\u79d1"\n    if batch_pref == "\\u672c\\u79d1\\u6279":\n        return "\\u672c\\u79d1"\n    if score is not None and score <= 450:\n        return "\\u4e13\\u79d1"\n    return "\\u672c\\u79d1"',
))
PC.append((
    '    """从请求体构建 batch/list 查询参数。"""',
    '    """Build batch/list query parameters from the request payload."""',
))
PC.append((
    '        raise ValueError("批次接口需要 province、classify、score")',
    '        raise ValueError("batch/list requires province, classify, and score")',
))
PC.append((
    '    """按省份规则规范化 subjects 字段。"""',
    '    """Normalize the subjects field per province rules."""',
))
PC.append((
    '    if province == "新疆":\n        if subjects in (None, "", "null", "NULL"):\n            payload.pop("subjects", None)\n        return',
    '    if province == "\\u65b0\\u7586":  # Xinjiang: subjects must be absent\n        if subjects in (None, "", "null", "NULL"):\n            payload.pop("subjects", None)\n        return',
))
PC.append((
    '    if province in PROVINCES_REQUIRING_GRADE_TYPE and grade_type == "专科":',
    '    if province in PROVINCES_REQUIRING_GRADE_TYPE and grade_type == "\\u4e13\\u79d1":',
))
PC.append((
    '    """发志愿接口前按省份规则清理请求体。"""',
    '    """Clean up the request body per province rules before calling the volunteer API."""',
))
PC.append((
    '    """志愿接口前校验 subjects 是否满足省份要求。"""',
    '    """Validate that subjects satisfies the province requirements before the volunteer API."""',
))
PC.append((
    '    if province == "新疆":\n        return\n    if province in PROVINCES_REQUIRING_GRADE_TYPE and payload.get("gradeType") == "专科":\n        return',
    '    if province == "\\u65b0\\u7586":  # Xinjiang\n        return\n    if province in PROVINCES_REQUIRING_GRADE_TYPE and payload.get("gradeType") == "\\u4e13\\u79d1":\n        return',
))
PC.append((
    '        raise ValueError(\n            f"缺少 subjects：{province}（{label}）需传选科组合，如 物理,化学,生物"\n        )',
    '        raise ValueError(\n            f"Missing subjects: {province} ({label}) requires a subject combination, "\n            f"e.g. physics,chemistry,biology"\n        )',
))
PC.append((
    '        if len(parts) != 3:\n            raise ValueError(\n                f"subjects 格式错误：{province}（3+1+2）须传完整三科（首选科目+两门再选），"\n                f"逗号分隔，如 classify=物理 时 subjects=物理,化学,生物；"\n                f"不能只传两门再选科目。当前为 {subjects!r}（{len(parts)} 科）"\n            )',
    '        if len(parts) != 3:\n            raise ValueError(\n                f"Invalid subjects: {province} (3+1+2) requires all three subjects "\n                f"(primary subject + two electives), comma-separated, "\n                f"e.g. with classify=physics use subjects=physics,chemistry,biology; "\n                f"never send only the two electives. Got {subjects!r} ({len(parts)} subjects)"\n            )',
))
PC.append((
    '        if classify not in parts:\n            raise ValueError(\n                f"subjects 与 classify 不一致：{province} classify={classify!r}，"\n                f"subjects 须包含首选科目 {classify!r}，当前为 {subjects!r}"\n            )',
    '        if classify not in parts:\n            raise ValueError(\n                f"subjects inconsistent with classify: {province} classify={classify!r}; "\n                f"subjects must include the primary subject {classify!r}, got {subjects!r}"\n            )',
))
PC.append((
    '        if len(electives) != 2:\n            raise ValueError(\n                f"subjects 格式错误：{province}（3+1+2）除首选科目外还须两门再选"\n                f"（化学/生物/政治/地理），当前为 {subjects!r}"\n            )',
    '        if len(electives) != 2:\n            raise ValueError(\n                f"Invalid subjects: {province} (3+1+2) requires two electives besides the "\n                f"primary subject (chemistry/biology/politics/geography), got {subjects!r}"\n            )',
))
PC.append((
    '        if invalid:\n            raise ValueError(\n                f"subjects 含无效再选科目 {invalid}：3+1+2 再选仅限化学/生物/政治/地理"\n            )',
    '        if invalid:\n            raise ValueError(\n                f"subjects contains invalid electives {invalid}: "\n                f"3+1+2 electives are limited to chemistry/biology/politics/geography"\n            )',
))
PC.append((
    '        if len(parts) != 3:\n            raise ValueError(\n                f"subjects 格式错误：{province}（3+3）须传完整三科选考科目，"\n                f"逗号分隔，如 物理,化学,生物；当前为 {subjects!r}（{len(parts)} 科）"\n            )',
    '        if len(parts) != 3:\n            raise ValueError(\n                f"Invalid subjects: {province} (3+3) requires all three elective subjects, "\n                f"comma-separated, e.g. physics,chemistry,biology; "\n                f"got {subjects!r} ({len(parts)} subjects)"\n            )',
))
PC.append((
    '        pool = SUBJECTS_33_ZHEJIANG if province == "浙江" else SUBJECTS_33_POOL\n        invalid = [p for p in parts if p not in pool]\n        if invalid:\n            raise ValueError(f"subjects 含无效科目 {invalid}：{province} 选考范围见 reference.md")',
    '        pool = SUBJECTS_33_ZHEJIANG if province == "\\u6d59\\u6c5f" else SUBJECTS_33_POOL  # Zhejiang\n        invalid = [p for p in parts if p not in pool]\n        if invalid:\n            raise ValueError(f"subjects contains invalid subjects {invalid}: see reference.md for {province}\'s subject pool")',
))
PC.append((
    '        if payload.get("gradeType") == "本科" and len(parts) != 3:\n            raise ValueError(\n                f"subjects 格式错误：{province}（3+3 本科）须传完整三科，"\n                f"如 物理,化学,生物；当前为 {subjects!r}"\n            )',
    '        if payload.get("gradeType") == "\\u672c\\u79d1" and len(parts) != 3:\n            raise ValueError(\n                f"Invalid subjects: {province} (3+3 undergraduate) requires all three "\n                f"subjects, e.g. physics,chemistry,biology; got {subjects!r}"\n            )',
))
patch(BASE / "province_config.py", PC)
print("province_config.py patched")

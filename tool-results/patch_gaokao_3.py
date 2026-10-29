#!/usr/bin/env python3
"""One-off patcher: merge_analysis.py + generate_html.py localization."""
from pathlib import Path

BASE = Path("/home/z/my-project/skills/gaokao-generate-report/scripts")


def patch(path: Path, repls: list[tuple[str, str]]) -> None:
    src = path.read_text(encoding="utf-8")
    miss = 0
    for old, new in repls:
        n = src.count(old)
        if n == 0:
            print(f"MISS in {path.name}: {old[:70]!r}")
            miss += 1
            continue
        src = src.replace(old, new)
    path.write_text(src, encoding="utf-8")
    print(f"{path.name}: done, {miss} misses")


# ================= merge_analysis.py =================
MA = []
MA.append((
    '"""合并 major_recommendation.json 与 school_recommendation.json 为 analysis.json。"""',
    '"""Merge major_recommendation.json and school_recommendation.json into analysis.json."""',
))
MA.append((
    '        raise RuntimeError(f"无法读取 {path}: {e}") from e',
    '        raise RuntimeError(f"cannot read {path}: {e}") from e',
))
MA.append((
    '    parser = argparse.ArgumentParser(description="合并专业/院校推荐为 analysis.json")\n    parser.add_argument("--majors", type=Path, required=True, help="major_recommendation.json")\n    parser.add_argument("--schools", type=Path, required=True, help="school_recommendation.json")\n    parser.add_argument("-o", "--output", type=Path, required=True, help="输出 analysis.json")',
    '    parser = argparse.ArgumentParser(description="Merge major/school recommendations into analysis.json")\n    parser.add_argument("--majors", type=Path, required=True, help="major_recommendation.json")\n    parser.add_argument("--schools", type=Path, required=True, help="school_recommendation.json")\n    parser.add_argument("-o", "--output", type=Path, required=True, help="output analysis.json")',
))
MA.append((
    '        print(f"错误: {e}", file=sys.stderr)',
    '        print(f"Error: {e}", file=sys.stderr)',
))
MA.append((
    '    print(\n        f"已合并: {args.output}（专业 {len(result[\'recommended_majors\'])}，"\n        f"学校 {len(result[\'recommended_schools\'])}）"\n    )',
    '    print(\n        f"Merged: {args.output} ({len(result[\'recommended_majors\'])} majors, "\n        f"{len(result[\'recommended_schools\'])} schools)"\n    )',
))
patch(BASE / "merge_analysis.py", MA)

# ================= generate_html.py =================
GH = []
GH.append((
    '"""将解析后的志愿 JSON + 推荐分析套用 HTML 模板，生成可视化报告。"""',
    '"""Apply the HTML template to the parsed volunteer JSON + recommendation analysis\nto generate a visual report."""',
))
GH.append((
    'VOLUNTEER_TYPE_LABELS = {\n    "ACADEMY_MAJOR": "院校志愿",\n    "ACADEMY_GROUP": "专业组",\n    "MAJOR_GROUP": "专业平行志愿",\n}',
    'VOLUNTEER_TYPE_LABELS = {\n    "ACADEMY_MAJOR": "University-based volunteers",\n    "ACADEMY_GROUP": "Major group",\n    "MAJOR_GROUP": "Parallel major volunteers",\n}',
))
GH.append((
    'TYPE_CSS = {\n    "冲": "chong",\n    "稳": "wen",\n    "保": "bao",\n    "难": "nan",\n    "易": "yi",\n}\n\nSECTION_ORDER = ["冲", "稳", "保", "易", "难"]\nSECTION_TITLE_CLASS = {\n    "冲": "title-chong",\n    "稳": "title-wen",\n    "保": "title-bao",\n    "易": "title-wen",\n    "难": "title-chong",\n}',
    '# Section labels are the English tier labels produced by fetch_volunteers.py\n# (TYPE_LABELS); the CSS class names (chong/wen/bao/...) are kept for styling.\nTYPE_CSS = {\n    "Reach": "chong",\n    "Match": "wen",\n    "Safety": "bao",\n    "Difficult": "nan",\n    "Easy": "yi",\n}\n\nSECTION_ORDER = ["Reach", "Match", "Safety", "Easy", "Difficult"]\nSECTION_TITLE_CLASS = {\n    "Reach": "title-chong",\n    "Match": "title-wen",\n    "Safety": "title-bao",\n    "Easy": "title-wen",\n    "Difficult": "title-chong",\n}',
))
GH.append((
    '    parts = [p.strip() for p in re.split(r"[,，]", subjects) if p.strip()]',
    '    parts = [p.strip() for p in re.split(r"[,\\uFF0C]", subjects) if p.strip()]',
))
GH.append((
    '    items = [t.strip() for t in re.split(r"[,，]", tags) if t.strip()]',
    '    items = [t.strip() for t in re.split(r"[,\\uFF0C]", tags) if t.strip()]',
))
GH.append((
    '        primary_parts.append(f"代码{school[\'university_code\']}")',
    '        primary_parts.append(f"Code {school[\'university_code\']}")',
))
GH.append((
    '    if loc_parts:\n        tags.append("".join(loc_parts))',
    '    if loc_parts:\n        tags.append(" · ".join(loc_parts))',
))
GH.append((
    '    cost = major.get("study_cost")\n    if cost and not str(cost).endswith("元"):\n        major["study_cost_display"] = f"{cost}元"\n    else:\n        major["study_cost_display"] = cost or "—"',
    '    cost = major.get("study_cost")\n    # "\\u5143" is the Chinese currency suffix (yuan) used by the API data.\n    if cost and not str(cost).endswith("\\u5143"):\n        major["study_cost_display"] = f"{cost}\\u5143"\n    else:\n        major["study_cost_display"] = cost or "—"',
))
GH.append((
    'def sort_majors_by_rec(majors: list[dict]) -> list[dict]:\n    """推荐专业排在前面，其余保持相对顺序。"""',
    'def sort_majors_by_rec(majors: list[dict]) -> list[dict]:\n    """Recommended majors first; the rest keep their relative order."""',
))
GH.append((
    'def university_rec_rank(uni: dict) -> int:\n    """同档位院校排序：推荐学校+推荐专业 > 仅推荐学校 > 其他。"""',
    'def university_rec_rank(uni: dict) -> int:\n    """Rank within a tier: recommended school + major > school only > other."""',
))
GH.append((
    'def build_rec_maps(analysis: dict | None) -> tuple[dict[tuple, str], dict[tuple, str], dict[str, dict]]:\n    """返回 (school_rec_map, major_rec_map, rec_modals)。"""',
    'def build_rec_maps(analysis: dict | None) -> tuple[dict[tuple, str], dict[tuple, str], dict[str, dict]]:\n    """Return (school_rec_map, major_rec_map, rec_modals)."""',
))
GH.append((
    '        if len(major_groups) == 1:\n            group_subtitle = f"/ 专业组 {major_groups[0]}"\n        elif len(major_groups) > 1:\n            group_subtitle = f"/ {len(major_groups)}个专业组"',
    '        if len(major_groups) == 1:\n            group_subtitle = f"/ Major group {major_groups[0]}"\n        elif len(major_groups) > 1:\n            group_subtitle = f"/ {len(major_groups)} major groups"',
))
GH.append((
    '    score = profile.get("score")\n    score_display = f"{score} 分" if score is not None else "—"\n    if profile.get("rank"):\n        score_display += f" / 位次 {profile[\'rank\']}"',
    '    score = profile.get("score")\n    score_display = f"{score} pts" if score is not None else "—"\n    if profile.get("rank"):\n        score_display += f" / Rank {profile[\'rank\']}"',
))
GH.append((
    '        "title": "高考志愿智能推荐方案",',
    '        "title": "Gaokao Volunteer Recommendation Report",',
))
GH.append((
    '        "is_adjust_label": "服从" if profile.get("is_adjust") else "不服从",',
    '        "is_adjust_label": "Yes" if profile.get("is_adjust") else "No",',
))
GH.append((
    '        raise FileNotFoundError(f"模板不存在: {template_path}")',
    '        raise FileNotFoundError(f"template not found: {template_path}")',
))
GH.append((
    '    parser = argparse.ArgumentParser(description="生成志愿推荐 HTML 报告")\n    parser.add_argument("-i", "--input", type=Path, required=True, help="fetch_volunteers.py 输出的 JSON")\n    parser.add_argument("-o", "--output", type=Path, required=True, help="HTML 输出路径")\n    parser.add_argument("-a", "--analysis", type=Path, help="Agent 产出的 analysis.json")\n    parser.add_argument(\n        "-t",\n        "--template",\n        type=Path,\n        default=DEFAULT_TEMPLATE,\n        help=f"Jinja2 模板路径（默认 {DEFAULT_TEMPLATE}）",\n    )',
    '    parser = argparse.ArgumentParser(description="Generate the volunteer recommendation HTML report")\n    parser.add_argument("-i", "--input", type=Path, required=True, help="JSON produced by fetch_volunteers.py")\n    parser.add_argument("-o", "--output", type=Path, required=True, help="HTML output path")\n    parser.add_argument("-a", "--analysis", type=Path, help="analysis.json produced by the agent")\n    parser.add_argument(\n        "-t",\n        "--template",\n        type=Path,\n        default=DEFAULT_TEMPLATE,\n        help=f"Jinja2 template path (default {DEFAULT_TEMPLATE})",\n    )',
))
GH.append((
    '        print(f"错误: 输入文件不存在 {args.input}", file=sys.stderr)',
    '        print(f"Error: input file does not exist {args.input}", file=sys.stderr)',
))
GH.append((
    '        print(f"错误: JSON 解析失败 — {e}", file=sys.stderr)',
    '        print(f"Error: JSON parsing failed - {e}", file=sys.stderr)',
))
GH.append((
    '            print(f"错误: 分析文件不存在 {args.analysis}", file=sys.stderr)',
    '            print(f"Error: analysis file does not exist {args.analysis}", file=sys.stderr)',
))
GH.append((
    '            print(f"错误: analysis JSON 解析失败 — {e}", file=sys.stderr)',
    '            print(f"Error: failed to parse analysis JSON - {e}", file=sys.stderr)',
))
GH.append((
    '        print(f"错误: {e}", file=sys.stderr)\n        return 1\n\n    print(f"已生成 HTML 报告: {args.output}")',
    '        print(f"Error: {e}", file=sys.stderr)\n        return 1\n\n    print(f"HTML report generated: {args.output}")',
))
patch(BASE / "generate_html.py", GH)

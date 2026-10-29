#!/usr/bin/env python3
"""One-off patcher: build_api_request.py + fetch_volunteers.py + test_batch_api.py localization."""
from pathlib import Path

BASE = Path("/home/z/my-project/skills/gaokao-fetch-volunteers/scripts")


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


# ================= build_api_request.py =================
BR = []
BR.append((
    '"""从 student.json 构建 API 请求体，将考生倾向映射到选填参数。"""',
    '"""Build the API request body from student.json, mapping student preferences to\noptional API parameters.\n\nNOTE: city/province/tag/major-class values below are the gaokao API\'s Chinese string\nvalues, written as \\uXXXX escapes (Python decodes them identically) so this source\nstays ASCII.\n"""',
))
BR.append((
    '''# 意向城市 → API provinces（省份意向）
CITY_TO_PROVINCE: dict[str, str] = {
    "北京": "北京",
    "上海": "上海",
    "天津": "天津",
    "重庆": "重庆",
    "深圳": "广东",
    "广州": "广东",
    "东莞": "广东",
    "佛山": "广东",
    "武汉": "湖北",
    "成都": "四川",
    "杭州": "浙江",
    "宁波": "浙江",
    "南京": "江苏",
    "苏州": "江苏",
    "无锡": "江苏",
    "西安": "陕西",
    "长沙": "湖南",
    "郑州": "河南",
    "济南": "山东",
    "青岛": "山东",
    "合肥": "安徽",
    "厦门": "福建",
    "福州": "福建",
    "大连": "辽宁",
    "沈阳": "辽宁",
    "哈尔滨": "黑龙江",
    "长春": "吉林",
    "昆明": "云南",
    "南宁": "广西",
    "海口": "海南",
    "石家庄": "河北",
    "太原": "山西",
    "南昌": "江西",
    "兰州": "甘肃",
    "贵阳": "贵州",
    "呼和浩特": "内蒙古",
    "乌鲁木齐": "新疆",
    "银川": "宁夏",
    "西宁": "青海",
    "拉萨": "西藏",
}''',
    '''# Preferred city -> API provinces value (province preference). Keys and values are the
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
    "\\u5317\\u4eac": "\\u5317\\u4eac",  # Beijing
    "\\u4e0a\\u6d77": "\\u4e0a\\u6d77",  # Shanghai
    "\\u5929\\u6d25": "\\u5929\\u6d25",  # Tianjin
    "\\u91cd\\u5e86": "\\u91cd\\u5e86",  # Chongqing
    "\\u6df1\\u5733": "\\u5e7f\\u4e1c",  # Shenzhen -> Guangdong
    "\\u5e7f\\u5dde": "\\u5e7f\\u4e1c",  # Guangzhou -> Guangdong
    "\\u4e1c\\u839e": "\\u5e7f\\u4e1c",  # Dongguan -> Guangdong
    "\\u4f5b\\u5c71": "\\u5e7f\\u4e1c",  # Foshan -> Guangdong
    "\\u6b66\\u6c49": "\\u6e56\\u5317",  # Wuhan -> Hubei
    "\\u6210\\u90fd": "\\u56db\\u5ddd",  # Chengdu -> Sichuan
    "\\u676d\\u5dde": "\\u6d59\\u6c5f",  # Hangzhou -> Zhejiang
    "\\u5b81\\u6ce2": "\\u6d59\\u6c5f",  # Ningbo -> Zhejiang
    "\\u5357\\u4eac": "\\u6c5f\\u82cf",  # Nanjing -> Jiangsu
    "\\u82cf\\u5dde": "\\u6c5f\\u82cf",  # Suzhou -> Jiangsu
    "\\u65e0\\u9521": "\\u6c5f\\u82cf",  # Wuxi -> Jiangsu
    "\\u897f\\u5b89": "\\u9655\\u897f",  # Xi'an -> Shaanxi
    "\\u957f\\u6c99": "\\u6e56\\u5357",  # Changsha -> Hunan
    "\\u90d1\\u5dde": "\\u6cb3\\u5357",  # Zhengzhou -> Henan
    "\\u6d4e\\u5357": "\\u5c71\\u4e1c",  # Jinan -> Shandong
    "\\u9752\\u5c9b": "\\u5c71\\u4e1c",  # Qingdao -> Shandong
    "\\u5408\\u80a5": "\\u5b89\\u5fbd",  # Hefei -> Anhui
    "\\u53a6\\u95e8": "\\u798f\\u5efa",  # Xiamen -> Fujian
    "\\u798f\\u5dde": "\\u798f\\u5efa",  # Fuzhou -> Fujian
    "\\u5927\\u8fde": "\\u8fbd\\u5b81",  # Dalian -> Liaoning
    "\\u6c88\\u9633": "\\u8fbd\\u5b81",  # Shenyang -> Liaoning
    "\\u54c8\\u5c14\\u6ee8": "\\u9ed1\\u9f99\\u6c5f",  # Harbin -> Heilongjiang
    "\\u957f\\u6625": "\\u5409\\u6797",  # Changchun -> Jilin
    "\\u6606\\u660e": "\\u4e91\\u5357",  # Kunming -> Yunnan
    "\\u5357\\u5b81": "\\u5e7f\\u897f",  # Nanning -> Guangxi
    "\\u6d77\\u53e3": "\\u6d77\\u5357",  # Haikou -> Hainan
    "\\u77f3\\u5bb6\\u5e84": "\\u6cb3\\u5317",  # Shijiazhuang -> Hebei
    "\\u592a\\u539f": "\\u5c71\\u897f",  # Taiyuan -> Shanxi
    "\\u5357\\u660c": "\\u6c5f\\u897f",  # Nanchang -> Jiangxi
    "\\u5170\\u5dde": "\\u7518\\u8083",  # Lanzhou -> Gansu
    "\\u8d35\\u9633": "\\u8d35\\u5dde",  # Guiyang -> Guizhou
    "\\u547c\\u548c\\u6d69\\u7279": "\\u5185\\u8499\\u53e4",  # Hohhot -> Inner Mongolia
    "\\u4e4c\\u9c81\\u6728\\u9f50": "\\u65b0\\u7586",  # Urumqi -> Xinjiang
    "\\u94f6\\u5ddd": "\\u5b81\\u590f",  # Yinchuan -> Ningxia
    "\\u897f\\u5b81": "\\u9752\\u6d77",  # Xining -> Qinghai
    "\\u62c9\\u8428": "\\u897f\\u85cf",  # Lhasa -> Tibet
}''',
))
BR.append((
    'def cities_to_provinces(cities: list[str] | None) -> list[str]:\n    """意向城市去重映射为省份列表。"""',
    'def cities_to_provinces(cities: list[str] | None) -> list[str]:\n    """Map preferred cities (deduplicated) to the list of API province values."""',
))
BR.append((
    '        key = str(city).strip().replace("市", "").replace("省", "")',
    '        # Strip the Chinese suffixes for "city" and "province" (unicode-escaped).\n        key = str(city).strip().replace("\\u5e02", "").replace("\\u7701", "")',
))
BR.append((
    'def student_to_api_payload(student: dict[str, Any]) -> dict[str, Any]:\n    """将 student.json 转为 API 请求体。"""',
    'def student_to_api_payload(student: dict[str, Any]) -> dict[str, Any]:\n    """Convert student.json into the API request body."""',
))
BR.append((
    'def summarize_preferences(student: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:\n    """返回倾向映射摘要，便于 Agent 向用户说明。"""',
    'def summarize_preferences(student: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:\n    """Return a preference-mapping summary so the agent can explain it to the user."""',
))
BR.append((
    '    parser = argparse.ArgumentParser(description="从 student.json 构建 API 请求 JSON")\n    parser.add_argument("-i", "--input", type=Path, required=True, help="student.json 路径")\n    parser.add_argument("-o", "--output", type=Path, required=True, help="输出 api_request.json")\n    parser.add_argument(\n        "--summary",\n        type=Path,\n        help="可选：输出倾向映射摘要 JSON（供 Agent 核对）",\n    )',
    '    parser = argparse.ArgumentParser(description="Build the API request JSON from student.json")\n    parser.add_argument("-i", "--input", type=Path, required=True, help="path to student.json")\n    parser.add_argument("-o", "--output", type=Path, required=True, help="output api_request.json")\n    parser.add_argument(\n        "--summary",\n        type=Path,\n        help="optional: output a preference-mapping summary JSON (for the agent to verify)",\n    )',
))
BR.append((
    '        print(f"错误: 无法读取 student.json — {e}", file=sys.stderr)',
    '        print(f"Error: cannot read student.json - {e}", file=sys.stderr)',
))
BR.append((
    '        print(f"错误: {e}", file=sys.stderr)\n        return 1\n\n    required = ["province", "classify", "score"]\n    missing = [k for k in required if not payload.get(k)]\n    if missing:\n        print(f"错误: student.json 缺少 API 必填字段 {missing}", file=sys.stderr)\n        return 1',
    '        print(f"Error: {e}", file=sys.stderr)\n        return 1\n\n    required = ["province", "classify", "score"]\n    missing = [k for k in required if not payload.get(k)]\n    if missing:\n        print(f"Error: student.json is missing API-required fields {missing}", file=sys.stderr)\n        return 1',
))
BR.append((
    '    print(f"已生成 API 请求: {args.output}")',
    '    print(f"API request written: {args.output}")',
))
BR.append((
    '        print(f"已生成倾向映射摘要: {args.summary}")',
    '        print(f"Preference-mapping summary written: {args.summary}")',
))
patch(BASE / "build_api_request.py", BR)

# ================= fetch_volunteers.py =================
FV = []
FV.append((
    '"""调用智能推荐志愿表 API，解析响应并输出结构化 JSON。"""',
    '"""Call the smart volunteer recommendation API, parse the response, and output\nstructured JSON.\n\nNOTE: province/batch/gradeType string values below are the gaokao API\'s Chinese string\nvalues, written as \\uXXXX escapes (Python decodes them identically) so this source\nstays ASCII.\n"""',
))
FV.append((
    '# ========== 接口配置（修改此处即可切换环境）==========',
    '# ========== API configuration (edit here to switch environments) ==========',
))
FV.append((
    'TYPE_LABELS = {\n    "CHONG": "冲",\n    "WEN": "稳",\n    "BAO": "保",\n    "NAN": "难",\n    "YI": "易",\n}',
    'TYPE_LABELS = {\n    "CHONG": "Reach",\n    "WEN": "Match",\n    "BAO": "Safety",\n    "NAN": "Difficult",\n    "YI": "Easy",\n}',
))
FV.append((
    'PROVINCE_BATCH_FALLBACK: dict[str, str] = {\n    "天津": "本科批A段",\n    "浙江": "普通类一段",\n    "山东": "普通类一段",\n    "四川": "本科批B段",\n    "云南": "本科批B段",\n    "甘肃": "本科批",\n    "宁夏": "本科批B段",\n    "新疆": "本科一批",\n}',
    'PROVINCE_BATCH_FALLBACK: dict[str, str] = {\n    # Tianjin -> undergraduate batch segment A; Zhejiang/Shandong -> general category segment 1;\n    # Sichuan/Yunnan/Ningxia -> undergraduate batch segment B; Gansu -> undergraduate batch;\n    # Xinjiang -> undergraduate first batch.\n    "\\u5929\\u6d25": "\\u672c\\u79d1\\u6279A\\u6bb5",\n    "\\u6d59\\u6c5f": "\\u666e\\u901a\\u7c7b\\u4e00\\u6bb5",\n    "\\u5c71\\u4e1c": "\\u666e\\u901a\\u7c7b\\u4e00\\u6bb5",\n    "\\u56db\\u5ddd": "\\u672c\\u79d1\\u6279B\\u6bb5",\n    "\\u4e91\\u5357": "\\u672c\\u79d1\\u6279B\\u6bb5",\n    "\\u7518\\u8083": "\\u672c\\u79d1\\u6279",\n    "\\u5b81\\u590f": "\\u672c\\u79d1\\u6279B\\u6bb5",\n    "\\u65b0\\u7586": "\\u672c\\u79d1\\u4e00\\u6279",\n}',
))
FV.append((
    'def resolve_batch_fallback(province: str | None, batch: str | None) -> str | None:\n    """批次 API 失败时的省份静态兜底。"""',
    'def resolve_batch_fallback(province: str | None, batch: str | None) -> str | None:\n    """Static per-province fallback used when the batch API fails."""',
))
FV.append((
    '    if str(batch).strip() == "本科批":\n        return mapped',
    '    if str(batch).strip() == "\\u672c\\u79d1\\u6279":  # generic "undergraduate batch"\n        return mapped',
))
FV.append((
    '    """GET 批次列表，返回 result 数组。"""',
    '    """GET the batch list; return the result array."""',
))
FV.append((
    '        raise RuntimeError(f"批次接口 HTTP {e.code}: {detail}") from e\n    except URLError as e:\n        raise RuntimeError(f"批次接口网络失败: {e.reason}") from e',
    '        raise RuntimeError(f"batch API HTTP {e.code}: {detail}") from e\n    except URLError as e:\n        raise RuntimeError(f"batch API network failure: {e.reason}") from e',
))
FV.append((
    '        raise ValueError(f"批次接口异常: status={raw.get(\'status\')}, message={raw.get(\'message\')}")',
    '        raise ValueError(f"batch API error: status={raw.get(\'status\')}, message={raw.get(\'message\')}")',
))
FV.append((
    '        raise ValueError("批次接口返回格式异常：result 非数组")',
    '        raise ValueError("unexpected batch API response format: result is not an array")',
))
FV.append((
    '        raise ValueError(\n            f"批次列表为空（{province}，{hint}）。"\n            f"请确认 classify 与省份选科模式一致（见 reference.md）"\n        )',
    '        raise ValueError(\n            f"Batch list is empty (province={province}, {hint}). "\n            f"Confirm that classify matches the province\'s subject-combination mode "\n            f"(see reference.md)"\n        )',
))
FV.append((
    '    """从批次列表中选取与分数、层次最匹配的一项。"""\n    if not items:\n        raise ValueError("没有可填报的批次")\n\n    candidates = list(items)\n\n    # 1. 精确批次名（非泛称「本科批」）\n    if preferred_batch and preferred_batch.strip() not in ("本科批", "专科批"):',
    '    """Pick the batch entry that best matches the score and tier preference."""\n    if not items:\n        raise ValueError("no fillable batch available")\n\n    candidates = list(items)\n\n    # 1. Exact batch name (not the generic undergraduate/vocational batch labels,\n    #    unicode-escaped: "\\u672c\\u79d1\\u6279" / "\\u4e13\\u79d1\\u6279")\n    if preferred_batch and preferred_batch.strip() not in ("\\u672c\\u79d1\\u6279", "\\u4e13\\u79d1\\u6279"):',
))
FV.append((
    '    # 2. 按 gradeType / 泛称本科批·专科批 过滤\n    if grade_type:\n        filtered = [x for x in candidates if x.get("gradeType") == grade_type]\n        if filtered:\n            candidates = filtered\n    elif preferred_batch == "本科批":\n        filtered = [x for x in candidates if x.get("gradeType") == "本科"]\n        if filtered:\n            candidates = filtered\n    elif preferred_batch == "专科批":\n        filtered = [x for x in candidates if x.get("gradeType") == "专科"]\n        if filtered:\n            candidates = filtered',
    '    # 2. Filter by gradeType / the generic undergraduate-vocational batch labels\n    #    (escaped: "\\u672c\\u79d1" = undergraduate, "\\u4e13\\u79d1" = vocational)\n    if grade_type:\n        filtered = [x for x in candidates if x.get("gradeType") == grade_type]\n        if filtered:\n            candidates = filtered\n    elif preferred_batch == "\\u672c\\u79d1\\u6279":\n        filtered = [x for x in candidates if x.get("gradeType") == "\\u672c\\u79d1"]\n        if filtered:\n            candidates = filtered\n    elif preferred_batch == "\\u4e13\\u79d1\\u6279":\n        filtered = [x for x in candidates if x.get("gradeType") == "\\u4e13\\u79d1"]\n        if filtered:\n            candidates = filtered',
))
FV.append((
    '    # 3. 分数达线：取控制线下考生分数仍达标的批次中，控制线最高者（偏本科一段）',
    '    # 3. Score threshold: among qualified batches pick the one with the highest control line',
))
FV.append((
    'def apply_batch_item_to_payload(payload: dict[str, Any], batch_item: dict[str, Any]) -> None:\n    """将选中批次写入志愿请求体。"""',
    'def apply_batch_item_to_payload(payload: dict[str, Any], batch_item: dict[str, Any]) -> None:\n    """Write the selected batch into the volunteer request body."""',
))
FV.append((
    '    """调用批次接口并选定 batch，返回 (batch名, 选中项, 全部项)。"""',
    '    """Call the batch API and select a batch; return (batch name, selected item, all items)."""',
))
FV.append((
    '    """将 score / parityScore 字段解析为 [{year, score, rank, plan_num}, ...]。"""',
    '    """Parse the score / parityScore fields into [{year, score, rank, plan_num}, ...]."""',
))
FV.append((
    'def normalize_api_response(raw: dict[str, Any]) -> dict[str, Any]:\n    """兼容新旧两种响应信封：{code,msg,body} 与 {status,message,result}。"""',
    'def normalize_api_response(raw: dict[str, Any]) -> dict[str, Any]:\n    """Support both response envelopes: {code,msg,body} and {status,message,result}."""',
))
FV.append((
    '            raise ValueError(f"API 返回异常: status={status}, message={msg}")',
    '            raise ValueError(f"API error: status={status}, message={msg}")',
))
FV.append((
    '        raise ValueError(f"API 返回异常: code={code}, msg={msg}")',
    '        raise ValueError(f"API error: code={code}, msg={msg}")',
))
FV.append((
    '        raise RuntimeError(f"网络请求失败: {e.reason}") from e',
    '        raise RuntimeError(f"network request failed: {e.reason}") from e',
))
FV.append((
    '    parser = argparse.ArgumentParser(description="获取并解析智能推荐志愿表")\n    parser.add_argument(\n        "--student",\n        type=Path,\n        help="student.json 路径（自动映射倾向到 API 选填参数，优先于 --config）",\n    )\n    parser.add_argument(\n        "--config",\n        type=Path,\n        help="完整请求 JSON 文件路径",\n    )\n    parser.add_argument(\n        "--base-url",\n        default=os.environ.get("ZP_API_BASE_URL", BASE_URL),\n        help=f"API 根地址（默认脚本内 BASE_URL: {BASE_URL}）",\n    )\n    parser.add_argument("-o", "--output", type=Path, required=True, help="解析结果 JSON 输出路径")\n    parser.add_argument("--save-raw", type=Path, help="可选：保存 API 原始响应")\n\n    parser.add_argument("--province", help="高考省份")\n    parser.add_argument("--classify", help="选科模式：文科/理科/物理/历史/综合")\n    parser.add_argument("--subjects", help="选科组合，逗号分隔，如 物理,化学,生物")\n    parser.add_argument("--grade-type", dest="grade_type", help="成绩类型：本科/专科（京沪津专科批）")\n    parser.add_argument("--score", type=int, help="高考成绩")\n    parser.add_argument("--rank", type=int, help="高考位次")\n    parser.add_argument("--batch", help="填报批次，如 本科批")\n    parser.add_argument(\n        "--auto-batch",\n        action=argparse.BooleanOptionalAction,\n        default=True,\n        help="是否通过 batch/list 接口自动解析批次（默认开启）",\n    )\n    parser.add_argument("--universitys", help="心仪高校，逗号分隔")\n    parser.add_argument("--provinces", help="省份意向，逗号分隔")\n    parser.add_argument("--tags", help="院校属性意向，逗号分隔")\n    parser.add_argument("--major-class", dest="major_class", help="专业类意向，逗号分隔")',
    '    parser = argparse.ArgumentParser(description="Fetch and parse the smart volunteer recommendation")\n    parser.add_argument(\n        "--student",\n        type=Path,\n        help="path to student.json (auto-maps preferences to optional API parameters; takes priority over --config)",\n    )\n    parser.add_argument(\n        "--config",\n        type=Path,\n        help="path to a complete request JSON file",\n    )\n    parser.add_argument(\n        "--base-url",\n        default=os.environ.get("ZP_API_BASE_URL", BASE_URL),\n        help=f"API root URL (defaults to the in-script BASE_URL: {BASE_URL})",\n    )\n    parser.add_argument("-o", "--output", type=Path, required=True, help="output path for the parsed-result JSON")\n    parser.add_argument("--save-raw", type=Path, help="optional: save the raw API response")\n\n    parser.add_argument("--province", help="gaokao province (API expects its Chinese name, e.g. \\\\u5c71\\\\u4e1c = Shandong)")\n    parser.add_argument("--classify", help="subject mode: liberal arts/science/physics/history/comprehensive (Chinese API values)")\n    parser.add_argument("--subjects", help="subject combination, comma-separated, e.g. physics,chemistry,biology (Chinese API values)")\n    parser.add_argument("--grade-type", dest="grade_type", help="grade type: undergraduate/vocational (Chinese API values; Beijing/Shanghai/Tianjin vocational only)")\n    parser.add_argument("--score", type=int, help="gaokao score")\n    parser.add_argument("--rank", type=int, help="provincial rank")\n    parser.add_argument("--batch", help="application batch, e.g. the undergraduate batch (Chinese API value)")\n    parser.add_argument(\n        "--auto-batch",\n        action=argparse.BooleanOptionalAction,\n        default=True,\n        help="resolve the batch automatically via the batch/list API (default: on)",\n    )\n    parser.add_argument("--universitys", help="desired universities, comma-separated (Chinese names)")\n    parser.add_argument("--provinces", help="province preferences, comma-separated (Chinese names)")\n    parser.add_argument("--tags", help="university attribute preferences, comma-separated")\n    parser.add_argument("--major-class", dest="major_class", help="major-class preferences, comma-separated (Chinese MOE class names)")',
))
FV.append((
    '        print(f"错误: 无法读取请求配置 — {e}", file=sys.stderr)',
    '        print(f"Error: cannot read the request config - {e}", file=sys.stderr)',
))
FV.append((
    '            print(\n                f"错误: 缺少必填参数 {missing}，请使用 --student、--config 或补全命令行",\n                file=sys.stderr,\n            )',
    '            print(\n                f"Error: missing required parameters {missing}; use --student, --config, "\n                f"or complete the CLI arguments",\n                file=sys.stderr,\n            )',
))
FV.append((
    '    # CLI 中 null 用字符串 "null" 传入时转为 None（subjects 在 sanitize 阶段按省处理）',
    '    # CLI passes null as the string "null" -> convert to None (subjects is handled per province in sanitize)',
))
FV.append((
    '        print(f"错误: {e}", file=sys.stderr)\n        return 1\n\n    batch_resolution: dict[str, Any] | None = None',
    '        print(f"Error: {e}", file=sys.stderr)\n        return 1\n\n    batch_resolution: dict[str, Any] | None = None',
))
FV.append((
    '            print(\n                f"批次: {batch_name}（{selected.get(\'gradeType\', \'\')} / {selected.get(\'type\', \'\')}）",\n                file=sys.stderr,\n            )',
    '            print(\n                f"Batch: {batch_name} ({selected.get(\'gradeType\', \'\')} / {selected.get(\'type\', \'\')})",\n                file=sys.stderr,\n            )',
))
FV.append((
    '            print(f"警告: 批次接口失败，使用静态兜底 — {e}", file=sys.stderr)',
    '            print(f"Warning: batch API failed, using the static fallback - {e}", file=sys.stderr)',
))
FV.append((
    '        print("错误: 已关闭 --auto-batch 且未提供 batch", file=sys.stderr)',
    '        print("Error: --no-auto-batch is set and no batch was provided", file=sys.stderr)',
))
FV.append((
    '    print(f"请求: {api_url(args.base_url)}", file=sys.stderr)',
    '    print(f"Request: {api_url(args.base_url)}", file=sys.stderr)',
))
FV.append((
    '    print(f"已保存解析结果: {args.output}（共 {parsed[\'stats\'][\'total\']} 所院校）")',
    '    print(f"Parsed result saved: {args.output} ({parsed[\'stats\'][\'total\']} universities in total)")',
))
patch(BASE / "fetch_volunteers.py", FV)

# ================= test_batch_api.py =================
TB = []
TB.append((
    '"""批量测试 batch/list 接口：各省 × 正确/错误 classify × 高/低分。"""',
    '"""Bulk-test the batch/list API: provinces x correct/wrong classify x high/low scores."""',
))
TB.append((
    '# 允许从 scripts/ 目录直接运行',
    '# Allow running directly from the scripts/ directory',
))
TB.append((
    'for p in MODE_33:\n    PROVINCE_CLASSIFY[p] = ["综合"]\nfor p in MODE_312:\n    PROVINCE_CLASSIFY[p] = ["物理", "历史"]\nfor p in MODE_OLD:\n    PROVINCE_CLASSIFY[p] = ["文科", "理科"]\nfor p in UNSUPPORTED_PROVINCES:\n    PROVINCE_CLASSIFY[p] = ["综合"]',
    'for p in MODE_33:\n    PROVINCE_CLASSIFY[p] = ["\\u7efc\\u5408"]  # comprehensive\nfor p in MODE_312:\n    PROVINCE_CLASSIFY[p] = ["\\u7269\\u7406", "\\u5386\\u53f2"]  # physics / history\nfor p in MODE_OLD:\n    PROVINCE_CLASSIFY[p] = ["\\u6587\\u79d1", "\\u7406\\u79d1"]  # liberal arts / science\nfor p in UNSUPPORTED_PROVINCES:\n    PROVINCE_CLASSIFY[p] = ["\\u7efc\\u5408"]',
))
TB.append((
    'WRONG_CLASSIFY = {\n    "综合": "物理",\n    "物理": "综合",\n    "历史": "理科",\n    "文科": "物理",\n    "理科": "历史",\n}',
    'WRONG_CLASSIFY = {\n    "\\u7efc\\u5408": "\\u7269\\u7406",  # comprehensive -> physics (wrong on purpose)\n    "\\u7269\\u7406": "\\u7efc\\u5408",\n    "\\u5386\\u53f2": "\\u7406\\u79d1",\n    "\\u6587\\u79d1": "\\u7269\\u7406",\n    "\\u7406\\u79d1": "\\u5386\\u53f2",\n}',
))
TB.append((
    '    return f"OK:{len(result)}项 [{\', \'.join(batches)}{extra}]"',
    '    return f"OK:{len(result)} items [{\', \'.join(batches)}{extra}]"',
))
TB.append((
    '    print("=== 正确 classify × 高分/低分（京沪津含 gradeType）===")',
    '    print("=== Correct classify x high/low scores (Beijing/Shanghai/Tianjin include gradeType) ===")',
))
TB.append((
    '        for score_label, score in [("高", HIGH_SCORE), ("低", LOW_SCORE)]:',
    '        for score_label, score in [("high", HIGH_SCORE), ("low", LOW_SCORE)]:',
))
TB.append((
    '                "batch": "本科批",\n            }\n            if province in ("北京", "上海", "天津"):\n                payload["gradeType"] = infer_grade_type(province, score, batch_pref="本科批")',
    '                "batch": "\\u672c\\u79d1\\u6279",\n            }\n            if province in ("\\u5317\\u4eac", "\\u4e0a\\u6d77", "\\u5929\\u6d25"):\n                payload["gradeType"] = infer_grade_type(province, score, batch_pref="\\u672c\\u79d1\\u6279")',
))
TB.append((
    '            print(f"  {mark} {province:4s} {primary} {gt:2s} {score_label}分({score}) → {summary}")',
    '            print(f"  {mark} {province:4s} {primary} {gt:2s} {score_label} ({score}) -> {summary}")',
))
TB.append((
    '    print("\\n=== 错误 classify 探测（高分）===")',
    '    print("\\n=== Wrong-classify probe (high score) ===")',
))
TB.append((
    '        wrong = WRONG_CLASSIFY.get(primary, "综合" if primary != "综合" else "物理")\n        ok_payload = {"province": province, "classify": primary, "score": HIGH_SCORE, "batch": "本科批"}\n        wrong_payload = dict(ok_payload, classify=wrong)\n        if province in ("北京", "上海", "天津"):\n            ok_payload["gradeType"] = infer_grade_type(province, HIGH_SCORE, batch_pref="本科批")',
    '        wrong = WRONG_CLASSIFY.get(primary, "\\u7efc\\u5408" if primary != "\\u7efc\\u5408" else "\\u7269\\u7406")\n        ok_payload = {"province": province, "classify": primary, "score": HIGH_SCORE, "batch": "\\u672c\\u79d1\\u6279"}\n        wrong_payload = dict(ok_payload, classify=wrong)\n        if province in ("\\u5317\\u4eac", "\\u4e0a\\u6d77", "\\u5929\\u6d25"):\n            ok_payload["gradeType"] = infer_grade_type(province, HIGH_SCORE, batch_pref="\\u672c\\u79d1\\u6279")',
))
TB.append((
    '            print(f"  ! {province}: 正确({primary})={ok_s} vs 错误({wrong})={wrong_s}")',
    '            print(f"  ! {province}: correct({primary})={ok_s} vs wrong({wrong})={wrong_s}")',
))
TB.append((
    '    print(f"\\n详细结果已保存: {out}")',
    '    print(f"\\nDetailed results saved: {out}")',
))
TB.append((
    '    print(f"\\n=== 汇总: 正确参数异常 {len(fails)} 项 ===")',
    '    print(f"\\n=== Summary: {len(fails)} unexpected failures with correct parameters ===")',
))
TB.append((
    '        print(f"  {r[\'province\']} {r[\'classify\']} {r[\'score_label\']}分 → {r[\'summary\']} | {r.get(\'message\')}")',
    '        print(f"  {r[\'province\']} {r[\'classify\']} {r[\'score_label\']} -> {r[\'summary\']} | {r.get(\'message\')}")',
))
patch(BASE / "test_batch_api.py", TB)

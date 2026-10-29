#!/usr/bin/env python3
"""One-off patcher for aminer-daily-paper/scripts/handle_trigger.py."""
from pathlib import Path

P = Path("/home/z/my-project/skills/aminer-daily-paper/scripts/handle_trigger.py")
src = P.read_text(encoding="utf-8")

repls = [
    # quotes-stripping regex + filler prefixes/suffixes (lines ~224-226)
    (
        "    candidate = re.sub(r'^[\\'\"`“”‘’]+|[\\'\"`“”‘’]+$', \"\", candidate)\n"
        "    candidate = re.sub(r\"^(?:关于|研究(?:方向)?|方向|领域|做|关注|topic(?:s)?|about|on)\\s*\", \"\", candidate, flags=re.IGNORECASE)\n"
        "    candidate = re.sub(r\"\\s*(?:相关|方向|领域|论文|papers?|research)\\s*$\", \"\", candidate, flags=re.IGNORECASE)",
        "    # Strip CJK/typographic quotes and Chinese filler prefixes/suffixes such as\n"
        "    # \"about\", \"research (direction)\", \"direction\", \"field\", \"working on\", \"focused on\",\n"
        "    # and suffixes \"related\", \"direction\", \"field\", \"papers\".\n"
        "    candidate = re.sub(r'^[\\'\"`\\u201c\\u201d\\u2018\\u2019]+|[\\'\"`\\u201c\\u201d\\u2018\\u2019]+$', \"\", candidate)\n"
        "    candidate = re.sub(r\"^(?:\\u5173\\u4e8e|\\u7814\\u7a76(?:\\u65b9\\u5411)?|\\u65b9\\u5411|\\u9886\\u57df|\\u505a|\\u5173\\u6ce8|topic(?:s)?|about|on)\\s*\", \"\", candidate, flags=re.IGNORECASE)\n"
        "    candidate = re.sub(r\"\\s*(?:\\u76f8\\u5173|\\u65b9\\u5411|\\u9886\\u57df|\\u8bba\\u6587|papers?|research)\\s*$\", \"\", candidate, flags=re.IGNORECASE)",
    ),
    # politeness fillers
    (
        "    cleaned = re.sub(r\"(?:给我|帮我|请|想看|想要|推荐|看看)\\s*\", \" \", cleaned)",
        "    # Strip Chinese politeness/request fillers: \"give me\", \"help me\", \"please\",\n"
        "    # \"want to see\", \"would like\", \"recommend\", \"take a look\".\n"
        "    cleaned = re.sub(r\"(?:\\u7ed9\\u6211|\\u5e2e\\u6211|\\u8bf7|\\u60f3\\u770b|\\u60f3\\u8981|\\u63a8\\u8350|\\u770b\\u770b)\\s*\", \" \", cleaned)",
    ),
    # conjunction split
    (
        "    parts = re.split(r\"[,，;/；、\\n]+|\\s+(?:and|or|以及|和|与|及)\\s+\", cleaned, flags=re.IGNORECASE)",
        "    # Split on punctuation and Chinese/English conjunctions (\"and\", \"or\").\n"
        "    parts = re.split(r\"[,;\\uFF0C\\uFF1B\\u3001/\\n]+|\\s+(?:and|or|\\u4ee5\\u53ca|\\u548c|\\u4e0e|\\u53ca)\\s+\", cleaned, flags=re.IGNORECASE)",
    ),
    # scholar self-intro patterns
    (
        "    patterns = [\n"
        "        r\"^我(?:是|叫)\\s*(?P<name>[^，,。；;、\\s]{2,20})\\s*[，,、]\\s*(?P<org>[^。；;，,]{2,60})\",\n"
        "        r\"^本人(?:是)?\\s*(?P<name>[^，,。；;、\\s]{2,20})\\s*[，,、]\\s*(?P<org>[^。；;，,]{2,60})\",\n"
        "        r\"^我是\\s*(?P<org>[^，,。；;]{2,60})\\s*的\\s*(?P<name>[^，,。；;、\\s]{2,20})\",\n"
        "    ]",
        "    patterns = [\n"
        "        # Chinese self-introductions, e.g. \"I am <name>, <org>\",\n"
        "        # \"I am <org>'s <name>\".\n"
        "        r\"^\\u6211(?:\\u662f|\\u53eb)\\s*(?P<name>[^\\uFF0C,.\\u3002\\uFF1B;\\u3001\\s]{2,20})\\s*[\\uFF0C,\\u3001]\\s*(?P<org>[^\\u3002\\uFF1B;,\\uFF0C]{2,60})\",\n"
        "        r\"^\\u672c\\u4eba(?:\\u662f)?\\s*(?P<name>[^\\uFF0C,.\\u3002\\uFF1B;\\u3001\\s]{2,20})\\s*[\\uFF0C,\\u3001]\\s*(?P<org>[^\\u3002\\uFF1B;,\\uFF0C]{2,60})\",\n"
        "        r\"^\\u6211\\u662f\\s*(?P<org>[^\\uFF0C,.\\u3002\\uFF1B;]{2,60})\\s*\\u7684\\s*(?P<name>[^\\uFF0C,.\\u3002\\uFF1B;\\u3001\\s]{2,20})\",\n"
        "    ]",
    ),
    # sentence split (occurs twice)
    (
        "re.split(r\"[。！？!?.；;]\", scholar_org, maxsplit=1)",
        "re.split(r\"[.!\\u3002?\\uFF1F!\\uFF01;\\uFF1B]\", scholar_org, maxsplit=1)",
    ),
    # bare name/org match
    (
        "r\"^(?P<name>[A-Za-z][A-Za-z .'-]{1,60}|[\\u4e00-\\u9fff·]{2,20})\\s*[，,、]\\s*(?P<org>[^。；;，,\\n]{2,80})\"",
        "r\"^(?P<name>[A-Za-z][A-Za-z .'-]{1,60}|[\\u4e00-\\u9fff\\u00b7]{2,20})\\s*[\\uFF0C,\\u3001]\\s*(?P<org>[^\\u3002\\uFF1B;,\\uFF0C\\n]{2,80})\"",
    ),
    # reply messages
    (
        "reply_text = \"输入里的 `aminer_author_id` 不合法。请提供 24 位十六进制字符串，例如：`/aminer-dp aminer_author_id: 696259801cb939bc391d3a37 topics: 多模态, 智能体`。\"",
        "reply_text = \"The `aminer_author_id` in the input is invalid. Please provide a 24-character hexadecimal string, e.g. `/aminer-dp aminer_author_id: 696259801cb939bc391d3a37 topics: multimodal, agents`.\"",
    ),
    (
        "reply_text = \"出于安全限制，`papers_file` 只能指向当前 skill 目录内的 JSON 文件，不能引用目录外路径。\"",
        "reply_text = \"For security reasons, `papers_file` may only point to a JSON file inside the current skill directory; paths outside it are not allowed.\"",
    ),
    (
        "reply_text = \"`papers_file` 目前只支持 `.json` 文件。\"",
        "reply_text = \"Only `.json` files are currently supported for `papers_file`.\"",
    ),
    (
        "reply_text = f\"输入不符合接口约束：{detail}\"",
        "reply_text = f\"Input violates interface constraints: {detail}\"",
    ),
    (
        "\"reply_text\": \"请发送 `/aminer-dp`（直接推荐），或加上 `topics: 多模态, 智能体`、`scholar: Jie Tang` 等参数精确推荐，也可以直接描述研究方向。\",",
        "\"reply_text\": \"Send `/aminer-dp` for direct recommendations, or add parameters such as `topics: multimodal, agents` or `scholar: Jie Tang` for precise recommendations. You can also simply describe your research interests.\",",
    ),
    (
        "\"reply_text\": f\"我还没能从这个 `aminer_author_id` 归纳出稳定研究方向，请补充研究方向或代表论文，例如：`/aminer-dp aminer_author_id: {parsed['aminer_author_id']} topics: 多模态, 智能体`。\",",
        "\"reply_text\": f\"Could not infer stable research topics from this `aminer_author_id`. Please provide research topics or representative papers, e.g. `/aminer-dp aminer_author_id: {parsed['aminer_author_id']} topics: multimodal, agents`.\",",
    ),
    (
        "\"reply_text\": \"我查到了学者线索，但还没成功归纳出稳定研究方向。请补充 `topics`、代表论文标题，或直接描述方向，例如：`/aminer-dp 我是张帆进，清华大学，做多模态智能体和 tool-use`。\",",
        "\"reply_text\": \"Found the scholar, but could not infer stable research topics yet. Please add `topics`, representative paper titles, or describe your interests directly, e.g. `/aminer-dp scholar: Zhang Fanjin org: Tsinghua University topics: multimodal agents, tool-use`.\",",
    ),
    (
        "\"reply_text\": f\"推荐流程执行失败，出错阶段：{detail}\",",
        "\"reply_text\": f\"The recommendation pipeline failed at stage: {detail}\",",
    ),
]

count = 0
for old, new in repls:
    n = src.count(old)
    if n == 0:
        print(f"MISS: {old[:70]!r}")
        continue
    src = src.replace(old, new)
    count += n
    print(f"ok ({n}x): {old[:60]!r}")

P.write_text(src, encoding="utf-8")
print(f"total replacements: {count}")

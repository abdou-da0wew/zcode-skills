#!/usr/bin/env python3
"""One-off patcher: volunteer_report.html localization + de-branding."""
from pathlib import Path

P = Path("/home/z/my-project/skills/gaokao-generate-report/templates/volunteer_report.html")
src = P.read_text(encoding="utf-8")

repls = [
    # 1. lang attribute
    ('<html lang="zh-CN">', '<html lang="en">'),
    # 2. de-brand the header (Zhipu/ChatGLM "AgentMore" logo and links -> neutral DiveeOI badge)
    (
        '''      <div class="brand-bar">
        <a href="https://agentmore.chatglm.cn/" target="_blank" rel="noopener">
          <img src="https://sfile.chatglm.cn/workspace/image/ee/eefb29159a.png" alt="清言 · AgentMore" class="brand-logo" />
        </a>
      </div>
      <div class="hero-header">
        <h1><a href="https://agentmore.chatglm.cn/" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;">{{ title }}</a></h1>
        <div class="meta-time">{{ generated_at }} · 智能算法生成</div>
      </div>''',
        '''      <div class="brand-bar">
        <span class="brand-logo" style="height:auto;font-weight:800;font-size:20px;letter-spacing:0.04em;color:var(--text);">DiveeOI</span>
      </div>
      <div class="hero-header">
        <h1>{{ title }}</h1>
        <div class="meta-time">{{ generated_at }} · AI-generated</div>
      </div>''',
    ),
    # 3. profile labels
    ('<div class="profile-item"><span class="label">省份</span>', '<div class="profile-item"><span class="label">Province</span>'),
    ('<div class="profile-item"><span class="label">选科</span>', '<div class="profile-item"><span class="label">Subjects</span>'),
    ('<div class="profile-item"><span class="label">成绩</span>', '<div class="profile-item"><span class="label">Score</span>'),
    ('<div class="profile-item"><span class="label">批次</span>', '<div class="profile-item"><span class="label">Batch</span>'),
    ('<div class="profile-item"><span class="label">志愿类型</span>', '<div class="profile-item"><span class="label">Volunteer type</span>'),
    ('<div class="profile-item"><span class="label">调剂</span>', '<div class="profile-item"><span class="label">Adjustment</span>'),
    # 4. stats container
    ('<a class="stat-box stat-link" href="#top" aria-label="回到顶部概览">', '<a class="stat-box stat-link" href="#top" aria-label="Back to top overview">'),
    ('<span class="label">推荐志愿</span>', '<span class="label">Recommended</span>'),
    ('<div class="stat-dist" title="冲 {{ stats.chong }} · 稳 {{ stats.wen }} · 保 {{ stats.bao }}">', '<div class="stat-dist" title="Reach {{ stats.chong }} · Match {{ stats.wen }} · Safety {{ stats.bao }}">'),
    ('<a class="stat-box stat-link" href="#section-chong" aria-label="跳到冲档志愿">', '<a class="stat-box stat-link" href="#section-reach" aria-label="Jump to reach-tier volunteers">'),
    ('<span class="label">冲档</span>', '<span class="label">Reach</span>'),
    ('<a class="stat-box stat-link" href="#section-wen" aria-label="跳到稳档志愿">', '<a class="stat-box stat-link" href="#section-match" aria-label="Jump to match-tier volunteers">'),
    ('<span class="label">稳档</span>', '<span class="label">Match</span>'),
    ('<a class="stat-box stat-link" href="#section-bao" aria-label="跳到保档志愿">', '<a class="stat-box stat-link" href="#section-safety" aria-label="Jump to safety-tier volunteers">'),
    ('<span class="label">保档</span>', '<span class="label">Safety</span>'),
    # 5. sticky nav
    ('<nav class="sticky-progress" id="stickyProgress" aria-label="快速定位导航">', '<nav class="sticky-progress" id="stickyProgress" aria-label="Quick navigation">'),
    ('<button class="pill" data-target="#top" type="button" aria-label="回到顶部">', '<button class="pill" data-target="#top" type="button" aria-label="Back to top">'),
    ('<button class="pill advice" data-target="#section-analysis" type="button" aria-label="跳到综合建议">\n        <span class="k">综合建议</span>', '<button class="pill advice" data-target="#section-analysis" type="button" aria-label="Jump to overall advice">\n        <span class="k">Advice</span>'),
    ('<button class="pill chong" data-target="#section-chong" type="button" aria-label="跳到冲档志愿">\n        <span class="k">冲</span><span class="v">{{ stats.chong }}</span>', '<button class="pill chong" data-target="#section-reach" type="button" aria-label="Jump to reach-tier volunteers">\n        <span class="k">Reach</span><span class="v">{{ stats.chong }}</span>'),
    ('<button class="pill wen" data-target="#section-wen" type="button" aria-label="跳到稳档志愿">\n        <span class="k">稳</span><span class="v">{{ stats.wen }}</span>', '<button class="pill wen" data-target="#section-match" type="button" aria-label="Jump to match-tier volunteers">\n        <span class="k">Match</span><span class="v">{{ stats.wen }}</span>'),
    ('<button class="pill bao" data-target="#section-bao" type="button" aria-label="跳到保档志愿">\n        <span class="k">保</span><span class="v">{{ stats.bao }}</span>', '<button class="pill bao" data-target="#section-safety" type="button" aria-label="Jump to safety-tier volunteers">\n        <span class="k">Safety</span><span class="v">{{ stats.bao }}</span>'),
    # 6. analysis section
    ('<h2 class="page-module-title">一、 综合测评与建议</h2>', '<h2 class="page-module-title">1. Overall Assessment &amp; Advice</h2>'),
    ('<section class="analysis-section" id="section-analysis" data-tier="建议">', '<section class="analysis-section" id="section-analysis" data-tier="advice">'),
    ('<h3>1. 核心定位与策略</h3>', '<h3>1. Core positioning and strategy</h3>'),
    ('<h3>2. 推荐专业方向解析</h3>', '<h3>2. Recommended major directions</h3>'),
    ('<h3>3. 院校梯度布局建议</h3>', '<h3>3. School tier layout advice</h3>'),
    # 7. volunteer list heading + section ids
    ('<h2 class="page-module-title">{% if has_analysis %}二、 {% endif %}具体志愿推荐列表</h2>', '<h2 class="page-module-title">{% if has_analysis %}2. {% endif %}Volunteer Recommendation List</h2>'),
    (
        "id=\"{% if section.label == '冲' %}section-chong{% elif section.label == '稳' %}section-wen{% elif section.label == '保' %}section-bao{% else %}section-{{ section.label }}{% endif %}\"",
        "id=\"{% if section.label == 'Reach' %}section-reach{% elif section.label == 'Match' %}section-match{% elif section.label == 'Safety' %}section-safety{% else %}section-{{ section.label }}{% endif %}\"",
    ),
    ('<h2 class="section-title {{ section.title_class }}">{{ section.label }}档志愿 ({{ section.count }}所)</h2>', '<h2 class="section-title {{ section.title_class }}">{{ section.label }} choices ({{ section.count }})</h2>'),
    # 8. recommendation badges
    ('<span class="rec-school-btn" data-rec-id="{{ uni.rec_id }}">👍🏻 推荐学校</span>', '<span class="rec-school-btn" data-rec-id="{{ uni.rec_id }}">👍🏻 Recommended school</span>'),
    ('🔥 推荐专业</span>{% endif %}', '🔥 Recommended major</span>{% endif %}'),
    # 9. probability labels
    ('<div class="prob-label">{% if uni.prob_min != uni.prob_max %}预测录取率区间{% else %}预测录取率{% endif %}</div>', '<div class="prob-label">{% if uni.prob_min != uni.prob_max %}Predicted admission rate range{% else %}Predicted admission rate{% endif %}</div>'),
    # 10. details summaries
    ('{% if uni.group_count > 1 %}展开查看 {{ uni.group_count }} 个专业组的历年投档与专业详情{% else %}展开查看历年投档与专业详情{% endif %}', '{% if uni.group_count > 1 %}Show historical scores and major details for {{ uni.group_count }} major groups{% else %}Show historical scores and major details{% endif %}'),
    ('展开查看专业详情（{{ uni.flat_major_count }} 个专业）', 'Show major details ({{ uni.flat_major_count }} majors)'),
    # 11. table headers (appears twice for majors-table variants)
    ('<th>专业名称</th><th>选科要求</th><th>学制/学费</th><th>计划</th>\n                    <th>历年投档（分/位次）</th><th>专业录取率</th>', '<th>Major</th><th>Subject requirements</th><th>Duration/Tuition</th><th>Seats</th>\n                    <th>Score history (score/rank)</th><th>Admission rate</th>'),
    ('<th>专业名称</th><th>选科要求</th><th>学制/学费</th><th>计划</th><th>专业录取率</th>', '<th>Major</th><th>Subject requirements</th><th>Duration/Tuition</th><th>Seats</th><th>Admission rate</th>'),
    # 12. major meta + cells
    ('<div class="major-meta">{% if m.major_code %}代码: {{ m.major_code }}{% endif %}', '<div class="major-meta">{% if m.major_code %}Code: {{ m.major_code }}{% endif %}'),
    ("<td>{{ m.claim or '不限' }}</td>", "<td>{{ m.claim or 'None' }}</td>"),
    ("<td>{{ m.study_year or '—' }}年 / {{ m.study_cost_display }}</td>", "<td>{{ m.study_year or '—' }} yrs / {{ m.study_cost_display }}</td>"),
    ('{% for h in m.entry_score_history[:2] %}<span>{{ h.year }}：{{ h.score }}/{{ h.rank }}</span>{% endfor %}', '{% for h in m.entry_score_history[:2] %}<span>{{ h.year }}: {{ h.score }}/{{ h.rank }}</span>{% endfor %}'),
    # 13. major group blocks
    ('<h4 style="font-size:15px;font-weight:600;">专业组 {{ group.major_group or \'—\' }}</h4>', '<h4 style="font-size:15px;font-weight:600;">Major group {{ group.major_group or \'—\' }}</h4>'),
    ('<span style="font-size:14px;color:var(--text-mute);">专业组录取率 <strong>{{ group.enroll_probability }}%</strong></span>', '<span style="font-size:14px;color:var(--text-mute);">Group admission rate <strong>{{ group.enroll_probability }}%</strong></span>'),
    ('<div><div style="color:var(--text-mute);">{{ h.year }}年投档</div><div style="font-weight:500;">{{ h.score }}分 / 位次{{ h.rank }} / 计划{{ h.plan_num }}</div></div>', '<div><div style="color:var(--text-mute);">{{ h.year }} cutoff</div><div style="font-weight:500;">{{ h.score }} pts / rank {{ h.rank }} / {{ h.plan_num }} seats</div></div>'),
    # 14. empty state + footer
    ('<p style="text-align:center;color:var(--text-mute);padding:48px;">暂无推荐院校数据</p>', '<p style="text-align:center;color:var(--text-mute);padding:48px;">No recommended universities to display</p>'),
    ('<p>录取概率说明：冲档通常 ≤30%；稳档约 50%–70%；保档 ≥80%。历年分数缺失时请优先参考录取概率与同位分。</p>', '<p>Admission probability guide: Reach tiers are usually ≤30%; Match roughly 50%–70%; Safety ≥80%. When historical scores are missing, rely on the admission probability and the same-rank score first.</p>'),
    ('<p style="margin-top: 6px;">本报告基于智能算法生成仅供参考，最终填报请务必核对省教育考试院官方目录。</p>', '<p style="margin-top: 6px;">This report is AI-generated and for reference only. Always verify the final application against the official catalog published by your provincial education examination authority.</p>'),
    # 15. modal
    ('<div class="modal-title" id="recModalTitle">推荐详情</div>', '<div class="modal-title" id="recModalTitle">Recommendation details</div>'),
    ('<button class="modal-close" onclick="closeRecModal()" aria-label="关闭">&times;</button>', '<button class="modal-close" onclick="closeRecModal()" aria-label="Close">&times;</button>'),
    ("document.getElementById('recModalTitle').innerText = data.title || '推荐详情';", "document.getElementById('recModalTitle').innerText = data.title || 'Recommendation details';"),
    # 16. JS tier map
    (
        "var tierToTarget = { {% if has_analysis %}'建议': '#section-analysis', {% endif %}'冲': '#section-chong', '稳': '#section-wen', '保': '#section-bao' };",
        "var tierToTarget = { {% if has_analysis %}'advice': '#section-analysis', {% endif %}'Reach': '#section-reach', 'Match': '#section-match', 'Safety': '#section-safety' };",
    ),
]

miss = 0
for old, new in repls:
    n = src.count(old)
    if n == 0:
        print(f"MISS: {old[:70]!r}")
        miss += 1
        continue
    src = src.replace(old, new)
P.write_text(src, encoding="utf-8")
print(f"done, {miss} misses")

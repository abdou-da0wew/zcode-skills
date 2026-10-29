#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch exact-string replacements for guizang-ppt/assets/pattern-slides.html (chunk3 localization)."""
import io

path = "/home/z/my-project/skills/design/design-templates/ppt/guizang-ppt/assets/pattern-slides.html"
s = io.open(path, encoding="utf-8").read()

pairs = [
(r'''  Topic: "一人公司 · The Quiet Hardware" — a fictional but realistic 64-day
  case study, mirroring the rhythm and content arc of the original 歸藏
  guizang-ppt-skill demo.''',
 r'''  Topic: "One-Person Company · The Quiet Hardware" — a fictional but
  realistic 64-day case study, mirroring the rhythm and content arc of the
  original Guizang guizang-ppt-skill demo.'''),
(r'<div class="kicker">私享会 · 创作者 Demo Day</div>', r'<div class="kicker">Private salon · Creator Demo Day</div>'),
(r'<h1 class="h-hero">一人公司</h1>', r'<h1 class="h-hero">One-Person Company</h1>'),
(r'<h2 class="h-sub">被 AI 折叠的组织</h2>', r'<h2 class="h-sub">An organization folded by AI</h2>'),
(r'''      一个独立创作者 —— 在 64 天里完成 11 万行代码、覆盖 9 个平台、跨过 5 个时区，<br>
      生活节奏几乎没有被打扰。''',
 r'''      An independent creator — 110K lines of code in 64 days, across 9 platforms and 5 time zones, <br>
      with almost no disruption to daily life.'''),
(r'<span>歸藏 Guizang</span><span>·</span><span>独立创作者</span><span>·</span><span>CodePilot 作者</span>',
 r'<span>Guizang</span><span>·</span><span>independent creator</span><span>·</span><span>CodePilot author</span>'),
(r'<div>一场关于 AI · 组织 · 个体的分享</div>', r'<div>A talk about AI · organizations · individuals</div>'),
(r'<div>过去 64 天 · 开发篇</div>', r'<div>Last 64 days · build log</div>'),
(r'<div class="kicker">一个人，做了什么。</div>', r'<div class="kicker">One person. What got built.</div>'),
(r'<h2 class="h-xl">过去 64 天</h2>', r'<h2 class="h-xl">The last 64 days</h2>'),
(r'<p class="lead" style="margin-bottom:5vh">从 0 到开源 CodePilot。</p>', r'<p class="lead" style="margin-bottom:5vh">From zero to open-source CodePilot.</p>'),
(r'<div class="stat-nb">64 <span class="stat-unit">天</span></div>', r'<div class="stat-nb">64 <span class="stat-unit">days</span></div>'),
(r'<div class="stat-note">从立项到现在</div>', r'<div class="stat-note">from kickoff to now</div>'),
(r'<div class="stat-note">一行一行写到 11 万+</div>', r'<div class="stat-note">written line by line to 110K+</div>'),
(r'<div class="stat-note">单仓库 · 60 天破 5K</div>', r'<div class="stat-note">single repo · 5K in 60 days</div>'),
(r'<div class="stat-note">装进了几万台电脑里</div>', r'<div class="stat-note">installed on tens of thousands of machines</div>'),
(r'<div class="stat-note">跨平台模型接入</div>', r'<div class="stat-note">cross-platform model access</div>'),
(r'<div class="stat-note">没有协作者</div>', r'<div class="stat-note">no collaborators</div>'),
(r'<div>项目 · CodePilot　|　github.com/codepilot</div>', r'<div>Project · CodePilot　|　github.com/codepilot</div>'),
(r'<div>身份反差 · The Twist</div>', r'<div>Identity contrast · The Twist</div>'),
(r'''\n          我不是程序员。\n        ''', r'\n          I am not a programmer.\n        '),
(r'''\n          大学毕业之后再没写过一行生产代码。过去十年做的是 UI 设计 / AI 特效 / 自媒体内容。\n        ''',
 r'\n          Never wrote a line of production code after college. The last decade: UI design / AI VFX / creator content.\n        '),
(r'''        “这东西在三年前，<br>
        需要一个十人团队做一年。”
        <div class="callout-src">— 一个观察者的判断</div>''',
 r'''        "Three years ago this <br>
        would have taken a ten-person team a year."
        <div class="callout-src">— one observer's judgment</div>'''),
(r'<div>Page 03 · 我不是程序员</div>', r'<div>Page 03 · I am not a programmer</div>'),
(r'<div>我的工作流 · Workflow</div>', r'<div>My workflow · Workflow</div>'),
(r'<div class="kicker">Pipeline · 流水线</div>', r'<div class="kicker">Pipeline</div>'),
(r'<h2 class="h-xl">两条流水线</h2>', r'<h2 class="h-xl">Two pipelines</h2>'),
(r'<div class="pipeline-label">文本侧 · Text Pipeline</div>', r'<div class="pipeline-label">Text side · Text Pipeline</div>'),
(r'<div class="step-desc">AI 帮我起草初稿</div>', r'<div class="step-desc">AI drafts the first version</div>'),
(r'<div class="step-desc">AI 润色去 AI 味</div>', r'<div class="step-desc">AI polishes away the AI flavor</div>'),
(r'<div class="step-desc">AI 变形成推特 / 小红书</div>', r'<div class="step-desc">AI reshapes it for Twitter / XHS</div>'),
(r'<div class="step-desc">AI 生成信息图</div>', r'<div class="step-desc">AI generates infographics</div>'),
(r'<div class="step-desc">一键分发 9 平台</div>', r'<div class="step-desc">one-click publish to 9 platforms</div>'),
(r'<div class="pipeline-label">视觉 · 视频侧 · Video Pipeline</div>', r'<div class="pipeline-label">Visual · video side · Video Pipeline</div>'),
(r'<div class="step-desc">AI 剪辑 + 自动配字幕</div>', r'<div class="step-desc">AI edits + auto-captions</div>'),
(r'<div class="step-desc">AI 包装 + 配 BGM</div>', r'<div class="step-desc">AI packages + picks the BGM</div>'),
(r'<div class="step-desc">AI 生成封面图</div>', r'<div class="step-desc">AI generates the cover art</div>'),
(r'<div>Page 04 · 我的内容工厂</div>', r'<div>Page 04 · my content factory</div>'),
(r'<div>第二幕 · 折叠</div>', r'<div>Act Two · The Fold</div>'),
(r'<h1 class="h-hero" style="font-size:8.5vw">折叠</h1>', r'<h1 class="h-hero" style="font-size:8.5vw">The Fold</h1>'),
(r'''\n      从 “一个人做内容” 到 “一个人是组织”。<br>\n      AI 不是工具，是岗位的折叠器。\n    ''',
 r'\n      From "one person making content" to "one person as an organization". <br>\n      AI is not a tool — it is a role-folding machine.\n    '),
(r'<div>第二幕引子</div>', r'<div>Act Two opener</div>'),
(r'<div>The Takeaway · 核心金句</div>', r'<div>The Takeaway</div>'),
(r'<div class="kicker">Quote · 金句</div>', r'<div class="kicker">Quote</div>'),
(r'''\n      “没有交接,<br>所有人都在构建。”\n    ''', r'\n      "With no handoff,<br>everyone is building."\n    '),
(r'<div>Page 06 · 金句</div>', r'<div>Page 06 · quote</div>'),
(r'<div>留给你的问题</div>', r'<div>A question left with you</div>'),
(r'''      你的公司里，<br>
      哪些岗位本来就<br>
      不该由人来做？''',
 r'''      In your company, which roles<br>
      were never meant<br>
      to be done by humans?'''),
(r'\n      这不是技术问题，是架构问题。\n    ', r'\n      Not a technology question — an architecture question.\n    '),
(r'<div>旧 vs 新 · The Shift</div>', r'<div>Old vs new · The Shift</div>'),
(r'<div class="kicker">Before / After · 范式转变</div>', r'<div class="kicker">Before / After · paradigm shift</div>'),
(r'<h2 class="h-xl" style="margin-bottom:4vh">从交接到共建</h2>', r'<h2 class="h-xl" style="margin-bottom:4vh">From handoff to co-building</h2>'),
(r'<div class="kicker" style="opacity:.9">Before · 旧模式</div>', r'<div class="kicker" style="opacity:.9">Before · the old way</div>'),
(r'<h3 class="h-md" style="margin-top:2vh">设计 → 开发 → 交接</h3>', r'<h3 class="h-md" style="margin-top:2vh">Design → build → handoff</h3>'),
(r'<li>设计师在 Figma 做稿，反复对齐像素</li>', r'<li>Designers comp in Figma, endlessly aligning pixels</li>'),
(r'<li>开发盯着设计稿手动翻译</li>', r'<li>Developers manually translate from mockups</li>'),
(r'<li>反复 PR 沟通，文档遗失在 Slack</li>', r'<li>Endless PR loops, specs lost in Slack</li>'),
(r'<li>非技术成员无法触碰代码</li>', r'<li>Non-technical members cannot touch code</li>'),
(r'<div class="kicker" style="opacity:.9">After · 新模式</div>', r'<div class="kicker" style="opacity:.9">After · the new way</div>'),
(r'<h3 class="h-md" style="margin-top:2vh">同工具 · 并行 · 共建</h3>', r'<h3 class="h-md" style="margin-top:2vh">Same tools · parallel · co-building</h3>'),
(r'<li>三个角色同时在同一份 Intent 上工作</li>', r'<li>Three roles work on the same Intent simultaneously</li>'),
(r'<li>agents.md / SKILL.md 是共享上下文</li>', r'<li>agents.md / SKILL.md as the shared context</li>'),
(r'<li>代理处理对齐、冲突、动效</li>', r'<li>Agents handle alignment, conflicts, motion</li>'),
(r'<li>任何人都能安全贡献代码</li>', r'<li>Anyone can safely contribute code</li>'),
(r'<div>Page 08 · 范式转变</div>', r'<div>Page 08 · paradigm shift</div>'),
(r'<div>End · 致谢</div>', r'<div>End · thanks</div>'),
(r'<h1 class="h-hero" style="font-size:9vw">谢谢。</h1>', r'<h1 class="h-hero" style="font-size:9vw">Thank you.</h1>'),
]

missed = []
for old, new in pairs:
    if old in s:
        s = s.replace(old, new, 1)
    else:
        missed.append(old.replace("\n", "\\n")[:80])

io.open(path, "w", encoding="utf-8").write(s)
print("REPLACED OK" if not missed else "MISSED:\n" + "\n".join(missed))

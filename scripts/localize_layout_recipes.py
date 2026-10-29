#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Localize social-card-editorial/references/layout-recipes.md (chunk3)."""
import io

path = "/home/z/my-project/skills/design/design-templates/social-card-editorial/references/layout-recipes.md"
s = io.open(path, encoding="utf-8").read()

pairs = [
("BUT you must add (a) source/context row 18-20px mono ≤15% from bottom, (b) date-stamp or 章号 kicker at top, (c) hairline rule above the source row.",
 "BUT you must add (a) source/context row 18-20px mono ≤15% from bottom, (b) date-stamp or chapter-number kicker at top, (c) hairline rule above the source row."),
('<h1 class="h-display">实测结果</h1>', '<h1 class="h-display">Field results</h1>'),
("- Quiet kicker like `The Question` or `留给你的`.", '- Quiet kicker like `The Question` or `Left for you`.'),
('<p class="kicker">The Question · 留给你的</p>', '<p class="kicker">The Question</p>'),
("""      下一次<br>
      你会先<br>
      问 AI 还是问朋友?""",
 """      Next time<br>
      will you ask<br>
      AI first or a friend?"""),
('<p class="lead">在评论区告诉我你的答案。</p>', '<p class="lead">Tell me your answer in the comments.</p>'),
('<span>欢迎留言</span>', '<span>Comments welcome</span>'),
('<p class="kicker">Workflow · 4 步</p>', '<p class="kicker">Workflow · 4 steps</p>'),
('<h2 class="h-xl">我的写作流水线</h2>', '<h2 class="h-xl">My writing pipeline</h2>'),
('<p class="step-desc">用语音备忘录把想法说出来</p>', '<p class="step-desc">Speak ideas into voice memos</p>'),
('<p class="step-desc">用 AI 把段落顺序重新排</p>', '<p class="step-desc">Let AI reorder the paragraphs</p>'),
('<p class="step-desc">人工逐句去 AI 味</p>', '<p class="step-desc">Hand-edit each line to remove the AI flavor</p>'),
('<p class="step-desc">同时发小红书、推特、公众号</p>', '<p class="step-desc">Publish to XHS, Twitter, and the official account at once</p>'),
('<h2 class="h-xl">写作流的演变</h2>', '<h2 class="h-xl">How the writing flow evolved</h2>'),
('<p class="kicker">Before · 旧</p>', '<p class="kicker">Before · the old way</p>'),
('<h3 class="h-md">在 Notion 里反复修</h3>', '<h3 class="h-md">Endless polishing in Notion</h3>'),
('<li>开头改了 20 遍</li>', '<li>Rewrote the opening 20 times</li>'),
('<li>每个段落都想精雕</li>', '<li>Tried to sculpt every paragraph</li>'),
('<li>一周才发一条</li>', '<li>Shipped one post a week</li>'),
('<p class="kicker">After · 新</p>', '<p class="kicker">After · the new way</p>'),
('<h3 class="h-md">先发版,再迭代</h3>', '<h3 class="h-md">Ship first, iterate after</h3>'),
('<li>20 分钟出初稿</li>', '<li>First draft in 20 minutes</li>'),
('<li>评论区做精修</li>', '<li>Refine in the comments</li>'),
('<li>一天发三条</li>', '<li>Ship three posts a day</li>'),
("Best for **lifestyle, image-heavy** content where the user has 1+ excellent photos: 旅行目的地 / 户外场景 / 自家成菜 / 家居一角 / 情感场景照.",
 "Best for **lifestyle, image-heavy** content where the user has 1+ excellent photos: travel destinations / outdoor scenes / home cooking / interior corners / emotional candid shots."),
("| **A · 顶压底沉** (top kicker + bottom title) |", "| **A · Top-press bottom-sink** (top kicker + bottom title) |"),
("| **B · 侧栏立柱** (vertical column) |", "| **B · Side column** (vertical column) |"),
("| **C · 角落徽章** (corner badge) |", "| **C · Corner badge** (corner badge) |"),
("| **D · 下沉条带** (bottom ribbon) |", "| **D · Bottom ribbon** (bottom ribbon) |"),
("**HTML skeleton (Mode A — 顶压底沉 on 3:4, no mask)**:", "**HTML skeleton (Mode A — top-press bottom-sink on 3:4, no mask)**:"),
("      Vol. 04 — 2026 — 户外", "      Vol. 04 — 2026 — Outdoor"),
("      在稻城<br/>看见冬天", "      Winter, seen<br/>in Daocheng"),
("**HTML skeleton (Mode D — 下沉条带 on 21:9, for WeChat main cover)**:", "**HTML skeleton (Mode D — bottom ribbon on 21:9, for WeChat main cover)**:"),
("      在稻城看见冬天", "      Winter, seen in Daocheng"),
('<span class="t-cat">Release · 产品</span>', '<span class="t-cat">Release · Product</span>'),
('<p class="t-cat">Cover · 主封面</p>', '<p class="t-cat">Cover · Main cover</p>'),
('<h1 class="h-statement">下一代<br>写作工作流</h1>', '<h1 class="h-statement">The next<br>writing workflow</h1>'),
('<p class="t-cat">Data · 半年增长</p>', '<p class="t-cat">Data · Six-month growth</p>'),
('<h2 class="h-xl">六个月,四组数字</h2>', '<h2 class="h-xl">Six months, four sets of numbers</h2>'),
('<h2 class="h-xl">本月最受欢迎的工具</h2>', '<h2 class="h-xl">This month\u2019s most popular tools</h2>'),
('<p class="t-cat">Spend · 五月账单</p>', '<p class="t-cat">Spend · May statement</p>'),
('<h2 class="h-xl">这个月我把钱花在哪</h2>', '<h2 class="h-xl">Where my money went this month</h2>'),
("""        <div class="ledger-lbl">订阅 · Subscriptions""",
 """        <div class="ledger-lbl">Subscriptions"""),
("""        <div class="ledger-lbl">书 · Books
          <span class="sub">6 本中文 · 2 本英文</span>""",
 """        <div class="ledger-lbl">Books
          <span class="sub">6 in Chinese · 2 in English</span>"""),
("""        <div class="ledger-lbl">咖啡 · Coffee
          <span class="sub">主要在 Manner 和 Seesaw</span>""",
 """        <div class="ledger-lbl">Coffee
          <span class="sub">mostly Manner and Seesaw</span>"""),
("""        <div class="ledger-lbl">硬件 · Hardware
          <span class="sub">键盘配件 · 一根 USB-C</span>""",
 """        <div class="ledger-lbl">Hardware
          <span class="sub">keyboard accessories · one USB-C cable</span>"""),
('<p class="t-cat">Capabilities · 能力清单</p>', '<p class="t-cat">Capabilities</p>'),
('<h2 class="h-xl">一个 Agent,十二件事</h2>', '<h2 class="h-xl">One agent, twelve things</h2>'),
('<div class="matrix-cell"><p class="cell-nb">01</p><p class="cell-title">读取项目结构</p></div>', '<div class="matrix-cell"><p class="cell-nb">01</p><p class="cell-title">Read the project structure</p></div>'),
('<div class="matrix-cell"><p class="cell-nb">02</p><p class="cell-title">运行测试</p></div>', '<div class="matrix-cell"><p class="cell-nb">02</p><p class="cell-title">Run the tests</p></div>'),
('<div class="matrix-cell is-accent"><p class="cell-nb">03</p><p class="cell-title">起草 PR 描述</p></div>', '<div class="matrix-cell is-accent"><p class="cell-nb">03</p><p class="cell-title">Draft the PR description</p></div>'),
('<div class="matrix-cell"><p class="cell-nb">04</p><p class="cell-title">回滚错误改动</p></div>', '<div class="matrix-cell"><p class="cell-nb">04</p><p class="cell-title">Revert bad changes</p></div>'),
('<div class="matrix-cell"><p class="cell-nb">05</p><p class="cell-title">迁移 lockfile</p></div>', '<div class="matrix-cell"><p class="cell-nb">05</p><p class="cell-title">Migrate the lockfile</p></div>'),
('<div class="matrix-cell"><p class="cell-nb">06</p><p class="cell-title">检查类型</p></div>', '<div class="matrix-cell"><p class="cell-nb">06</p><p class="cell-title">Type-check</p></div>'),
('<div class="matrix-cell"><p class="cell-nb">07</p><p class="cell-title">追踪 issue</p></div>', '<div class="matrix-cell"><p class="cell-nb">07</p><p class="cell-title">Triage issues</p></div>'),
('<div class="matrix-cell"><p class="cell-nb">08</p><p class="cell-title">阅读日志</p></div>', '<div class="matrix-cell"><p class="cell-nb">08</p><p class="cell-title">Read the logs</p></div>'),
('<p class="t-cat">In total · 累计</p>', '<p class="t-cat">In total</p>'),
('<p class="lead">在 6 个仓库上,持续 4 周。</p>', '<p class="lead">Across 6 repos, over 4 weeks.</p>'),
]

missed = []
for old, new in pairs:
    if old in s:
        s = s.replace(old, new)
    else:
        missed.append(old.replace("\n", "\\n")[:80])

io.open(path, "w", encoding="utf-8").write(s)
print("OK" if not missed else "MISSED:\n" + "\n".join(missed))

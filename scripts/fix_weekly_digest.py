#!/usr/bin/env python3
"""Translate remaining CJK lines in weekly-digest-vol18-notebook.html by line number."""
import re

P = '/home/z/my-project/skills/design/design-templates/project-brief/weekly-digest-vol18-notebook.html'

R = {
9:   '<title>Product Update Digest · VOL.18</title>',
14:  '  /* FlyFlowerSong typeface — ZeoSeven Fonts CDN (pre-split packages, loaded on demand) */',
714: '        <span class="row">Digest</span>',
715: '        <span class="row row-2">Product Update Weekly</span>',
719: '      <p class="intro">5 new features, 14 experience improvements and 4 bug fixes this week.<br>The AgentMore skill marketplace is now live, covering local travel, AMiner, Eastmoney and other skill categories.</p>',
724: '          Digest Product Team',
725: '          <div class="addr">DiveeOI · Beijing · Zhongguancun Rongke Info Center</div>',
729: '        <dd>AgentMore Editorial Team</dd>',
733: '          May 22, 2025',
734: '          <div class="addr">This issue covers 05 / 18 — 05 / 22 · 23 updates in total</div>',
743: '      <div class="toc-label">EXPOSICIONES<span class="note">Three sections this issue</span></div>',
746: '          <div class="name">New Features</div>',
747: '          <div class="count"><span class="arrow">→</span>5 items / New Features</div>',
750: '          <div class="name">Improvements</div>',
751: '          <div class="count"><span class="arrow">→</span>14 items / Optimizations</div>',
754: '          <div class="name">Bug Fixes</div>',
755: '          <div class="count"><span class="arrow">→</span>4 items / Bug Fixes</div>',
763: '      <span class="section-name">Five new features this week</span>',
770: '        <div class="name">AgentMore skill marketplace<span class="badge">Major</span></div>',
771: '        <div class="desc"><span class="arrow">→</span>Officially launched, giving users a richer set of skills and experiences</div>',
778: '        <div class="name">New AgentMore skills<span class="badge alt">New</span></div>',
779: '        <div class="desc"><span class="arrow">→</span>Local travel, AMiner and Eastmoney skills enrich the platform catalog</div>',
786: '        <div class="name">Points ledger now shows next-month credit timing</div>',
787: '        <div class="desc"><span class="arrow">→</span>More transparency on point movements — know before credits land</div>',
794: '        <div class="name">Points ledger adds credit-issuance notices</div>',
795: '        <div class="desc"><span class="arrow">→</span>More detailed point-movement info with traceable issuance timing</div>',
802: '        <div class="name">Bulk gift-card purchase added</div>',
803: '        <div class="desc"><span class="arrow">→</span>Supports bulk purchase of SVIP and points-package gift cards</div>',
810: '      <span class="section-name">Fourteen experience improvements</span>',
816: '        <span class="k">RECEIPT · Experience</span>',
822: '        <div class="opt"><span class="o-i">01</span><span class="o-t">AgentMore page styling refined for sidebar and skill-avatar visual consistency</span></div>',
823: '        <div class="opt"><span class="o-i">02</span><span class="o-t">AgentMore onboarding dialog adapted for small screens</span></div>',
824: '        <div class="opt"><span class="o-i">03</span><span class="o-t">AgentMore domain-security related fixes improve system safety</span></div>',
825: '        <div class="opt"><span class="o-i">04</span><span class="o-t">Offline notice refined for better feedback when the network drops</span></div>',
826: '        <div class="opt"><span class="o-i">05</span><span class="o-t">Agent-mode usage and points display logic clarified — quota info is clearer</span></div>',
827: '        <div class="opt"><span class="o-i">06</span><span class="o-t">Main chat history switched to async conversation resume for smoother long chats</span></div>',
828: '        <div class="opt"><span class="o-i">07</span><span class="o-t">Upload limit raised to 50 files to support multi-file workflows</span></div>',
829: '        <div class="opt"><span class="o-i">08</span><span class="o-t">Page-jump links refined for smoother, more accurate navigation</span></div>',
830: '        <div class="opt"><span class="o-i">09</span><span class="o-t">Enterprise auto-renewal logic improved for a smoother renewal flow</span></div>',
831: '        <div class="opt"><span class="o-i">10</span><span class="o-t">PC membership purchase screen redesigned for a smoother checkout</span></div>',
832: '        <div class="opt"><span class="o-i">11</span><span class="o-t">Markdown horizontal rule rendering improved for better readability</span></div>',
833: '        <div class="opt"><span class="o-i">12</span><span class="o-t">Message timestamp format refined for clarity</span></div>',
834: '        <div class="opt"><span class="o-i">13</span><span class="o-t">Group-chat creation dialog layout refined for a friendlier flow</span></div>',
835: '        <div class="opt"><span class="o-i">14</span><span class="o-t">H5 heartbeat loading style polished for smoother load animations</span></div>',
843: '        <span class="section-name">Four bug fixes</span>',
850: '          <span class="b-t">AgentMore fixed an issue where agents shared skills, improving compatibility and stability</span>',
854: '          <span class="b-t">AgentMore fixed exceptions during skill uninstallation to keep things running</span>',
858: '          <span class="b-t">Fixed typewriter-effect glitches when opening history or switching back from background</span>',
862: '          <span class="b-t">Fixed image-generation stability issues so pictures load and display correctly</span>',
870: '        <div class="l1">Digest<span class="de">·</span>Weekly</div>',
871: '        <div class="l2">todo el día · updated all day long</div>',
879: '          <div class="qr-label">SCAN<br>Subscribe</div>',
923: '        <div class="qr-meta">SCAN TO SUBSCRIBE · Product Update Weekly</div>',
928: '        <div class="ticket-row"><span class="b">CHANNEL</span><span class="a">Newsletter · Digest Product</span></div>',
934: '      <div class="left">Digest Product Team · Product Weekly</div>',
}

lines = open(P, encoding='utf-8').readlines()
misses = [n for n in R if not re.search(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', lines[n-1])]
print('lines without CJK (skipped):', misses)
for n, new in R.items():
    nl = '\n' if lines[n-1].endswith('\n') else ''
    lines[n-1] = new + nl
open(P, 'w', encoding='utf-8').write(''.join(lines))

left = [i for i, l in enumerate(lines, 1) if re.search(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', l)]
print('remaining CJK lines:', left)
for i in left:
    print(i, lines[i-1].rstrip()[:160])

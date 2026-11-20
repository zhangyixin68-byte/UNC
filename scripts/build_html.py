# -*- coding: utf-8 -*-
"""把 stage1 final_draft.md 转成符合 html_rules.md 的完整 HTML（business-report 主题）。"""
import re, html, json, sys

SRC = r"C:\Users\dell\WorkBuddy\2026-11-20-20-22-28\output\20261120215817\stage1\final_draft.md"
OUT = r"C:\Users\dell\WorkBuddy\2026-11-20-20-22-28\output\20261120215817\stage2\formatted-企业产品一物一码追溯编码规范.html"

with open(SRC, encoding="utf-8") as f:
    lines = f.read().split("\n")

# token 值（来自 business-report.json 预编译产物）
CSS_VARS = """
    --typography-fontFamily-heading: "微软雅黑", "Microsoft YaHei", sans-serif;
    --typography-fontFamily-body: "微软雅黑", "Microsoft YaHei", sans-serif;
    --typography-fontFamily-mono: "Consolas", monospace;
    --typography-fontSize-coverTitle: 26pt;
    --typography-fontSize-coverCategory: 13pt;
    --typography-fontSize-h1: 16pt;
    --typography-fontSize-h2: 14pt;
    --typography-fontSize-h3: 12.5pt;
    --typography-fontSize-body: 12pt;
    --typography-fontSize-small: 10.5pt;
    --typography-lineHeight-body: 1.6;
    --typography-lineHeight-heading: 1.3;
    --typography-fontWeight-bold: 700;
    --typography-fontWeight-normal: 400;
    --color-primary: #1565C0;
    --color-secondary: #0288D1;
    --color-accent: #00897B;
    --color-text: #212121;
    --color-textSecondary: #616161;
    --color-heading: #1A237E;
    --color-divider: #E0E0E0;
    --color-background: #FFFFFF;
    --color-surface: #F5F7FA;
    --color-callout-bg: #EEF4FB;
    --fs-cover-title: var(--typography-fontSize-coverTitle);
    --fs-h1: var(--typography-fontSize-h1);
    --fs-h2: var(--typography-fontSize-h2);
    --fs-h3: var(--typography-fontSize-h3);
    --fs-body: var(--typography-fontSize-body);
    --fs-small: var(--typography-fontSize-small);
    --ff-heading: var(--typography-fontFamily-heading);
    --ff-body: var(--typography-fontFamily-body);
    --ff-mono: var(--typography-fontFamily-mono);
    --lh-body: var(--typography-lineHeight-body);
    --fw-bold: var(--typography-fontWeight-bold);
    --fw-normal: var(--typography-fontWeight-normal);
    --spacing-paragraph: 0.6em;
    --spacing-section: 1.6em;
    --margin-page: var(--layout-margin, 2.5cm);
    --page-content-width: var(--layout-contentWidth, 16cm);
    --fs-tiny: 9pt;
    --color-on-primary: #FFFFFF;
"""

STYLE = """
<style>
:root {
""" + CSS_VARS + """
}
@page { margin: 2.3cm 2.5cm 2.2cm 2.5cm; @bottom-center { content: "第 " counter(page) " 页"; font-size: var(--fs-tiny); color: var(--color-textSecondary); } }
@page cover { @bottom-center { content: none; } }
section[role="cover"] { page: cover; }
body { max-width: var(--page-content-width); margin-left: auto; margin-right: auto;
       font-family: var(--ff-body); font-size: var(--fs-body); color: var(--color-text);
       line-height: var(--lh-body); }
body p { text-align: justify; text-indent: 2em; font-family: var(--ff-body); font-size: var(--fs-body);
         line-height: var(--lh-body); margin: var(--spacing-paragraph) 0; color: var(--color-text); }
h1 { font-family: var(--ff-heading); font-size: var(--fs-h1); color: var(--color-heading);
     font-weight: var(--fw-bold); line-height: var(--typography-lineHeight-heading);
     margin: var(--spacing-section) 0 0.7em 0; text-align: left; text-indent: 0;
     border-bottom: 2px solid var(--color-primary); padding-bottom: 0.3em; }
h2 { font-family: var(--ff-heading); font-size: var(--fs-h2); color: var(--color-primary);
     font-weight: var(--fw-bold); line-height: var(--typography-lineHeight-heading);
     margin: 1.4em 0 0.5em 0; text-align: left; text-indent: 0; }
h3 { font-family: var(--ff-heading); font-size: var(--fs-h3); color: var(--color-secondary);
     font-weight: var(--fw-bold); margin: 1em 0 0.4em 0; text-align: left; text-indent: 0; }
ul, ol { margin: 0.5em 0 0.8em 2em; padding: 0; }
li { font-family: var(--ff-body); font-size: var(--fs-body); line-height: var(--lh-body);
     margin: 0.25em 0; text-align: justify; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0 1.2em 0; font-family: var(--ff-body); font-size: var(--fs-small); }
caption { font-family: var(--ff-heading); font-size: var(--fs-small); font-weight: var(--fw-bold);
          color: var(--color-heading); text-align: center; margin-bottom: 0.4em; }
th { background: var(--color-primary); color: var(--color-on-primary); font-weight: var(--fw-bold);
     padding: 7px 9px; border: 0.5px solid var(--color-primary); text-align: left; font-size: var(--fs-small); }
td { padding: 6px 9px; border: 0.5px solid var(--color-divider); vertical-align: top;
     text-align: left; font-size: var(--fs-small); line-height: 1.45; }
tbody tr:nth-child(even) td { background: var(--color-surface); }
code { font-family: var(--ff-mono); font-size: var(--fs-small); background: var(--color-surface);
       padding: 0 3px; color: var(--color-accent); }
.cover-kicker { font-family: var(--ff-heading); font-size: var(--typography-fontSize-coverCategory);
                color: var(--color-secondary); text-align: center; text-indent: 0; letter-spacing: 3px;
                margin-top: 3.5cm; }
.cover-brand { font-family: var(--ff-heading); font-size: var(--fs-h2); font-weight: var(--fw-bold);
               color: var(--color-heading); text-align: center; text-indent: 0; margin: 1cm 0 0 0;
               letter-spacing: 1px; }
.cover-brand span { font-size: var(--fs-body); font-weight: var(--fw-normal); color: var(--color-textSecondary); letter-spacing: 0; }
.cover-title { font-family: var(--ff-heading); font-size: var(--fs-cover-title); color: var(--color-heading);
               font-weight: var(--fw-bold); text-align: center; text-indent: 0; line-height: 1.4;
               margin: 1.2cm 0 0.6cm 0; }
.cover-sub { font-family: var(--ff-body); font-size: var(--fs-h2); color: var(--color-textSecondary);
             text-align: center; text-indent: 0; margin: 0.3em 0; }
.cover-meta { font-family: var(--ff-body); font-size: var(--fs-body); color: var(--color-textSecondary);
              text-align: center; text-indent: 0; margin-top: 2.5cm; }
.toc-title { font-family: var(--ff-heading); font-size: var(--fs-h1); font-weight: var(--fw-bold);
             color: var(--color-heading); text-align: center; text-indent: 0;
             margin: 0.6cm 0 1cm 0; }
.toc-list, .toc-list ol, .toc-list ul { list-style: none; }
.toc-list { margin: 0; padding: 0; }
.toc-list > li { font-family: var(--ff-heading); font-size: var(--fs-h3); font-weight: var(--fw-bold);
                 color: var(--color-heading); margin: 0.55em 0 0.2em 0; }
.toc-list ol { margin: 0 0 0 1.2em; padding: 0; }
.toc-list ol li { font-family: var(--ff-body); font-size: var(--fs-body); color: var(--color-textSecondary);
                  margin: 0.18em 0; }
.toc-list a { color: inherit; text-decoration: none; }
.callout-note { border-left: 3px solid var(--color-accent); background: var(--color-callout-bg);
                padding: 8px 12px; margin: 1em 0; text-indent: 0; font-size: var(--fs-body); }
.foot-note { font-size: var(--fs-small); color: var(--color-textSecondary); text-indent: 0;
             text-align: center; margin-top: 2em; }
.executive-summary { border-collapse: collapse; width: 100%; margin: 0.4em 0 1.6em 0; }
.executive-summary td { background: var(--color-callout-bg); border: 0.5px solid var(--color-divider);
                        padding: 14px 18px; text-align: left; }
.es-title { font-family: var(--ff-heading); font-size: var(--fs-h2); font-weight: var(--fw-bold);
            color: var(--color-heading); text-indent: 0; text-align: left; margin: 0 0 0.5em 0; }
.es-body { font-family: var(--ff-body); font-size: var(--fs-body); line-height: var(--lh-body);
           text-indent: 0; text-align: justify; color: var(--color-text); margin: 0.3em 0; }
</style>
"""

def inline(t):
    """处理行内 Markdown：加粗、行内代码，并转义 HTML。"""
    t = html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    return t

# ---------- 解析 ----------
out = []
i = 0
chapters = []      # (id, title, level)
h1_counter = 0
h2_map = {}

# 章节编号：把 md 的 "1 总则" -> "一、总则"；附录保持原样
CN = "一二三四五六七八九十"
def num_h1(title):
    m = re.match(r'^(\d+)\s+(.*)$', title)
    if m:
        n = int(m.group(1))
        if n <= 10:
            label = CN[n-1]
        elif n < 20:
            label = "十" + (CN[n-11] if n > 10 else "")
        else:
            label = CN[n//10-1] + "十" + (CN[n%10-1] if n%10 else "")
        return label + "、" + m.group(2)
    return title

while i < len(lines):
    line = lines[i]
    s = line.strip()
    if not s:
        i += 1
        continue
    # 文档 H1 标题 -> 跳过（封面承载）
    if s.startswith("# ") and not s.startswith("## "):
        i += 1
        continue
    # 表格
    if s.startswith("|") and i+1 < len(lines) and re.match(r'^\s*\|[\s:\-|]+\|\s*$', lines[i+1]):
        header = [c.strip() for c in s.strip("|").split("|")]
        i += 2
        rows = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
            i += 1
        thead = "".join("<th>"+inline(c)+"</th>" for c in header)
        tbody = ""
        for r in rows:
            tbody += "<tr>" + "".join("<td>"+inline(c)+"</td>" for c in r) + "</tr>"
        out.append("<table><thead><tr>"+thead+"</tr></thead><tbody>"+tbody+"</tbody></table>")
        continue
    # H2 (章)
    if s.startswith("## "):
        title = num_h1(s[3:].strip())
        h1_counter += 1
        cid = "section-%d" % h1_counter
        chapters.append((cid, title, 1))
        out.append('<h1 id="%s">%s</h1>' % (cid, inline(title)))
        i += 1
        continue
    # H3 (节)
    if s.startswith("### "):
        title = s[4:].strip()
        # 二级目录归属最近 h1
        pid = chapters[-1][0] if chapters else "section-1"
        chapters.append((pid, title, 2))
        out.append("<h2>%s</h2>" % inline(title))
        i += 1
        continue
    # 引用块 -> callout 提示框
    if s.startswith(">"):
        items = []
        while i < len(lines) and lines[i].strip().startswith(">"):
            items.append(inline(lines[i].strip().lstrip(">").strip()))
            i += 1
        out.append('<p class="callout-note">%s</p>' % " ".join(items))
        continue
    # 无序列表
    if s.startswith("- "):
        items = []
        while i < len(lines) and lines[i].strip().startswith("- "):
            items.append(inline(lines[i].strip()[2:]))
            i += 1
        out.append("<ul>" + "".join("<li>"+x+"</li>" for x in items) + "</ul>")
        continue
    # 有序列表
    if re.match(r'^\d+\.\s', s):
        items = []
        while i < len(lines) and re.match(r'^\s*\d+\.\s', lines[i]):
            items.append(inline(re.sub(r'^\s*\d+\.\s+', '', lines[i])))
            i += 1
        out.append("<ol>" + "".join("<li>"+x+"</li>" for x in items) + "</ol>")
        continue
    # 引用/强调脚注（末尾斜体行）
    if s.startswith("*") and s.endswith("*") and not s.startswith("**"):
        out.append('<p class="foot-note">%s</p>' % inline(s.strip("*")))
        i += 1
        continue
    # 普通段落
    out.append("<p>%s</p>" % inline(s))
    i += 1

body_html = "\n".join(out)

# 目录
toc_items = []
for cid, title, level in chapters:
    if level == 1:
        toc_items.append('      <li><a href="#%s">%s</a></li>' % (cid, inline(title)))
    else:
        toc_items.append('      <li style="margin-left:1.2em"><a href="#%s">%s</a></li>' % (cid, inline(title)))
# 目录需要嵌套结构：重建
toc_nested = []
cur = None
for cid, title, level in chapters:
    if level == 1:
        if cur is not None:
            toc_nested.append(cur)
        cur = [cid, title, []]
    else:
        if cur is not None:
            cur[2].append((cid, title))
if cur is not None:
    toc_nested.append(cur)

toc_html_lines = []
for cid, title, subs in toc_nested:
    toc_html_lines.append('    <li><a href="#%s">%s</a>' % (cid, inline(title)))
    if subs:
        toc_html_lines.append('      <ol>')
        for scid, stitle in subs:
            toc_html_lines.append('        <li><a href="#%s">%s</a></li>' % (scid, inline(stitle)))
        toc_html_lines.append('      </ol>')
    toc_html_lines.append('    </li>')
toc_html = "\n".join(toc_html_lines)

EXEC_SUMMARY = """
<table class="executive-summary"><tbody><tr><td>
<p class="es-title">执行摘要</p>
<p class="es-body">在手工编码时代，为便于记忆与分类，编码往往把品类、属性、序号等信息全部塞进一段定长字符串里。这类编码本质上是“分类码”，它回答的是“这是什么产品”，适合配料、统计与检索，却无法支撑“这是哪一件、经过谁的手、现在在哪”这样的追溯诉求。当企业推进一物一码追溯管理时，编码的角色必须从静态身份证升级为动态履历载体，设计重心随之重构。</p>
<p class="es-body">本规范提出“三层编码、两类用途”的通用框架：产品族码（SKU）作为后台主数据标识产品种类；单品码（UIN）作为核心，为每件产品赋予全局唯一、终身不变、不可推测的身份；追溯载体（明码 + 加密二维码或 RFID）将身份固化到实物上。三层之间经赋码与加密贯通，形成可采集、可验证的完整链路。</p>
<p class="es-body">规范同时给出产品族码七段结构、单品码双码并行方案、包装层级父子关联模型、全流程六大采集节点、防伪防窜货机制、追溯深度分级、行业适配建议、数据字典与落地步骤。企业实施时应以“通用框架 + 自有字典”方式落地：分类树与属性字典按行业定制，编码规则与关联逻辑跨企业复用。</p>
</td></tr></tbody></table>
"""

DOC = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="docx-page-size" content="A4">
<title>Snowlio Uncia 雪豹码 · 企业产品一物一码追溯编码规范</title>
""" + STYLE + """
</head>
<body>
<section role="cover">
  <p class="cover-kicker">SNOWLIO UNCIA · 雪豹码 · UNC</p>
  <p class="cover-brand">Snowlio Suite 雪豹云追溯平台家族<span> / 一物一码生成系统</span></p>
  <p class="cover-title">企业产品一物一码追溯编码规范</p>
  <p class="cover-sub">通用版 · 覆盖食品 / 药品 / 3C / 化妆品 / 服装鞋帽等行业</p>
  <p class="cover-sub">以单品级（L2）追溯为主线</p>
  <p class="cover-meta">文件类别：技术规范 &nbsp;|&nbsp; 版本：V1.1</p>
  <p class="cover-meta">适用对象：IT / 质量 / 供应链 / 合规部门</p>
  <p class="cover-meta">编制日期：2026 年 11 月</p>
</section>
<section role="cover">
<nav class="doc-toc" aria-label="文档目录">
  <p class="toc-title">目 录</p>
  <ol class="toc-list">
""" + toc_html + """
  </ol>
</nav>
</section>
<section role="body" data-page-restart="1">
""" + EXEC_SUMMARY + body_html + """
</section>
</body>
</html>
"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(DOC)

print("HTML written:", OUT)
print("chapters:", h1_counter, "toc entries:", len(chapters))

#!/usr/bin/env python3
"""Render the Jev dossier markdown into a self-contained styled HTML document."""
import html
import re
import sys
from pathlib import Path

SRC = (
    Path(sys.argv[1]).resolve()
    if len(sys.argv) > 1
    else Path(__file__).resolve().parent.parent / "docs" / "jev-launch-week-dossier.md"
)
OUT = SRC.with_suffix(".html")

md = SRC.read_text()

# ---------- minimal, purpose-built markdown renderer ----------
def inline(t: str) -> str:
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t

lines = md.split("\n")
out, i = [], 0
in_code = False

def close_list(stack):
    while stack:
        out.append(f"</{stack.pop()}>")

list_stack: list[str] = []

while i < len(lines):
    ln = lines[i]

    if ln.strip().startswith("```"):
        if in_code:
            out.append("</code></pre>"); in_code = False
        else:
            close_list(list_stack); out.append("<pre><code>"); in_code = True
        i += 1; continue
    if in_code:
        out.append(html.escape(ln)); i += 1; continue

    # tables
    if ln.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
        close_list(list_stack)
        hdr = [c.strip() for c in ln.strip().strip("|").split("|")]
        out.append('<div class="tw"><table><thead><tr>')
        out += [f"<th>{inline(h)}</th>" for h in hdr]
        out.append("</tr></thead><tbody>")
        i += 2
        while i < len(lines) and lines[i].startswith("|"):
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            out.append("<tr>")
            for idx, c in enumerate(cells):
                cls = ' class="num"' if re.fullmatch(r"[\$~]?[\d.,%×–\-]+", c) else ""
                out.append(f"<td{cls}>{inline(c)}</td>")
            out.append("</tr>")
            i += 1
        out.append("</tbody></table></div>")
        continue

    # headings
    m = re.match(r"^(#{1,6})\s+(.*)$", ln)
    if m:
        close_list(list_stack)
        lvl = len(m.group(1))
        out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
        i += 1; continue

    # hr
    if re.match(r"^---+\s*$", ln):
        close_list(list_stack); out.append("<hr>"); i += 1; continue

    # blockquote
    if ln.startswith(">"):
        close_list(list_stack)
        buf = []
        while i < len(lines) and lines[i].startswith(">"):
            buf.append(lines[i].lstrip(">").strip())
            i += 1
        out.append("<blockquote>" + "<br>".join(inline(b) for b in buf if b) + "</blockquote>")
        continue

    # lists
    ul = re.match(r"^(\s*)[-*]\s+(.*)$", ln)
    ol = re.match(r"^(\s*)\d+\.\s+(.*)$", ln)
    if ul or ol:
        want = "ul" if ul else "ol"
        if not list_stack or list_stack[-1] != want:
            close_list(list_stack); out.append(f"<{want}>"); list_stack.append(want)
        out.append(f"<li>{inline((ul or ol).group(2))}</li>")
        i += 1; continue

    if not ln.strip():
        close_list(list_stack); i += 1; continue

    close_list(list_stack)
    out.append(f"<p>{inline(ln)}</p>")
    i += 1

close_list(list_stack)
if in_code:
    out.append("</code></pre>")

body = "\n".join(out)

CSS = """
:root{--bg:#0d1117;--panel:#161b22;--panel2:#1c2128;--ink:#e6edf3;--dim:#9198a1;
--line:#30363d;--acc:#58a6ff;--acc2:#f0883e;--ok:#3fb950;--warn:#d29922;--bad:#f85149;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.72 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Helvetica,Arial,sans-serif;
-webkit-font-smoothing:antialiased}
.wrap{max-width:960px;margin:0 auto;padding:64px 32px 120px}
h1{font-size:2.5rem;line-height:1.15;letter-spacing:-.02em;margin:0 0 .3em;
background:linear-gradient(92deg,#79c0ff,#f0883e);-webkit-background-clip:text;
-webkit-text-fill-color:transparent;background-clip:text}
h2{font-size:1.65rem;margin:2.6em 0 .7em;padding-bottom:.35em;
border-bottom:1px solid var(--line);letter-spacing:-.01em}
h3{font-size:1.22rem;margin:2em 0 .5em;color:#79c0ff}
h4{font-size:1.02rem;margin:1.5em 0 .4em;color:var(--acc2)}
p{margin:.85em 0}
a{color:var(--acc);text-decoration:none;border-bottom:1px solid #1f6feb55}
a:hover{border-bottom-color:var(--acc)}
hr{border:0;border-top:1px solid var(--line);margin:2.5em 0}
strong{color:#fff;font-weight:650}
em{color:#c9d1d9}
code{background:#21262d;padding:.15em .42em;border-radius:5px;font-size:.87em;
font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:#ffa657;
border:1px solid #30363d}
pre{background:var(--panel);border:1px solid var(--line);border-radius:10px;
padding:1.1em 1.3em;overflow-x:auto}
pre code{background:none;border:0;padding:0;color:var(--ink)}
blockquote{margin:1.3em 0;padding:.85em 1.2em;border-left:3px solid var(--acc);
background:linear-gradient(90deg,#1f6feb1a,transparent);border-radius:0 8px 8px 0;
color:#c9d1d9;font-size:1.02em}
.tw{overflow-x:auto;margin:1.4em 0;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:.9rem}
th{background:var(--panel2);text-align:left;padding:11px 14px;font-weight:640;
color:#79c0ff;border-bottom:1px solid var(--line);white-space:nowrap;
letter-spacing:.02em;text-transform:uppercase;font-size:.76rem}
td{padding:10px 14px;border-bottom:1px solid #21262d;vertical-align:top}
tr:last-child td{border-bottom:0}
tbody tr:hover{background:#1c212866}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap;color:#7ee787}
ul,ol{margin:.9em 0;padding-left:1.5em}
li{margin:.38em 0}
li::marker{color:var(--acc)}
h1+blockquote{font-size:1.05em}
@media print{body{background:#fff;color:#111}.wrap{max-width:none;padding:0}
h1{-webkit-text-fill-color:#111;background:none;color:#111}
h2,h3,h4,th{color:#111}.tw{border-color:#ccc}th{background:#eee;color:#111}
td{border-color:#ddd}blockquote{background:#f7f7f7;color:#222}code{color:#b3540a}}
nav.vol{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 2.2em;padding-bottom:1.1em;
border-bottom:1px solid var(--line);font-size:.86rem}
nav.vol a,nav.vol span{padding:.4em .85em;border-radius:999px;border:1px solid var(--line);
border-bottom:1px solid var(--line);white-space:nowrap}
nav.vol a{background:var(--panel);transition:background .15s,border-color .15s}
nav.vol a:hover{background:#1f6feb22;border-color:var(--acc)}
nav.vol span.cur{background:linear-gradient(92deg,#1f6feb33,#f0883e22);border-color:var(--acc);
color:#fff;font-weight:600}
nav.vol .lbl{color:var(--dim);border:0;background:none;padding-left:0}
@media print{nav.vol{display:none}}
"""

# Per-document metadata: title + the nav bar shown at the top of the rendered page.
DOCS = {
    "jev-launch-week-dossier": {
        "title": "The Jev Launch Week Dossier — 10 Wild Builds &amp; 21 Design Patterns",
        "nav": [
            ("cur", "📕 Dossier"),
            ("a", "jev-design-patterns-handbook.html", "📘 Patterns"),
            ("a", "jev-benchmark-report.html", "📊 Benchmarks"),
            ("a", "jev-production-playbook.html", "🔧 Playbook"),
            ("a", "../", "🌐 Home"),
        ],
    },
    "jev-design-patterns-handbook": {
        "title": "The Jev Design Pattern Handbook — 3 Primitives, 10 Shapes, 4 Patterns",
        "nav": [
            ("a", "jev-launch-week-dossier.html", "📕 Dossier"),
            ("cur", "📘 Patterns"),
            ("a", "jev-benchmark-report.html", "📊 Benchmarks"),
            ("a", "jev-production-playbook.html", "🔧 Playbook"),
            ("a", "../", "🌐 Home"),
        ],
    },
    "jev-benchmark-report": {
        "title": "The Jev Benchmark Report — Jev vs 12 Local Decision Models",
        "nav": [
            ("a", "jev-launch-week-dossier.html", "📕 Dossier"),
            ("a", "jev-design-patterns-handbook.html", "📘 Patterns"),
            ("cur", "📊 Benchmarks"),
            ("a", "jev-production-playbook.html", "🔧 Playbook"),
            ("a", "../", "🌐 Home"),
        ],
    },
    "jev-production-playbook": {
        "title": "The Jev Production Playbook — Deployment Economics with Jev + Treg",
        "nav": [
            ("a", "jev-launch-week-dossier.html", "📕 Dossier"),
            ("a", "jev-design-patterns-handbook.html", "📘 Patterns"),
            ("a", "jev-benchmark-report.html", "📊 Benchmarks"),
            ("cur", "🔧 Playbook"),
            ("a", "../", "🌐 Home"),
        ],
    },
}

meta = DOCS.get(SRC.stem, {"title": SRC.stem, "nav": [("a", "../", "🌐 Home")]})
parts = ['<span class="lbl">Jev volumes:</span>']
for item in meta["nav"]:
    if item[0] == "cur":
        parts.append(f'<span class="cur">{item[1]}</span>')
    else:
        parts.append(f'<a href="{item[1]}">{item[2]}</a>')
nav = '<nav class="vol">' + "".join(parts) + "</nav>"

doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{meta["title"]}</title>
<style>{CSS}</style></head>
<body><div class="wrap">
{nav}
{body}
</div></body></html>"""
OUT.write_text(doc)
print(f"wrote {OUT}  ({len(doc):,} bytes)")

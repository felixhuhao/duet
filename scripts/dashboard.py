#!/usr/bin/env python3
"""态势板生成器：扫描工件的 YAML 状态头（templates/frontmatter.md），渲染静态 HTML。

纯渲染层——不写任何真源文件；页面可随时整页重生成。
用法：dashboard.py --repo ~/Workspace/byteme_mobile --out /tmp/盘面.html
"""
import argparse
import html
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCAN_DIRS = ["docs/plans", "docs/devlogs", "docs/handoffs", "docs/migration"]
LANE_ORDER = ["全局", "B钱", "D对话", "E分身", "C经营", "AGT", "跨仓"]
STATUS_RANK = {"pending-owner": 0, "open": 1, "in-progress": 1, "frozen": 2,
               "paused": 3, "draft": 4, "done": 5, "archived": 6}
STATUS_CLASS = {"done": "ok", "pending-owner": "warn", "paused": "idle",
                "archived": "idle", "in-progress": "info", "open": "info",
                "frozen": "info", "draft": "idle"}
STATUS_LABEL = {"pending-owner": "等 owner", "in-progress": "进行中", "done": "已完结",
                "paused": "悬置", "open": "在途", "frozen": "已冻结",
                "draft": "草稿", "archived": "已归档"}


def parse_frontmatter(text):
    """扁平 YAML：key: value；值可为带引号字符串或单层 [a, b] 列表。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            continue
        key, raw = m.group(1), m.group(2).strip()
        if raw.startswith("[") and raw.endswith("]"):
            items = [s.strip().strip('"').strip("'")
                     for s in raw[1:-1].split(",")]
            fields[key] = [s for s in items if s]
        else:
            fields[key] = raw.strip('"').strip("'")
    return None  # 没闭合


def collect(repo):
    cards = []
    for d in SCAN_DIRS:
        base = repo / d
        if not base.is_dir():
            continue
        for p in sorted(base.glob("*.md")):
            try:
                head = p.read_text(encoding="utf-8")[:2000]
            except OSError:
                continue
            fm = parse_frontmatter(head)
            if fm is None:
                continue
            title = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", p.stem)
            fm["_title"] = title
            fm["_path"] = str(p.relative_to(repo))
            cards.append(fm)
    return cards


def git_meta(repo):
    def run(*args):
        try:
            return subprocess.run(["git", "-C", str(repo), *args],
                                  capture_output=True, text=True,
                                  timeout=10).stdout.strip()
        except Exception:
            return ""
    return run("rev-parse", "--short", "HEAD"), run("rev-parse", "--abbrev-ref", "HEAD")


CSS = """
:root {
  --bg: #f2f4f6; --surface: #ffffff; --ink: #1f2a35; --muted: #5f6e7d;
  --line: #dce2e8; --accent: #0e7490;
  --ok: #2f7d4f; --ok-bg: #e6f1ea; --warn: #a8650b; --warn-bg: #f9efdd;
  --info: #2b5fc7; --info-bg: #e7edfb; --idle: #66707b; --idle-bg: #eceff1;
  --queue-bg: #faf3e3; --queue-line: #e8d5ac;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #131920; --surface: #1b242e; --ink: #e6ecf2; --muted: #93a1af;
    --line: #2c3742; --accent: #53c3d8;
    --ok: #6cc694; --ok-bg: #1d3227; --warn: #e2ac61; --warn-bg: #382b12;
    --info: #85aaf3; --info-bg: #1c2c4c; --idle: #909ba6; --idle-bg: #242d36;
    --queue-bg: #251f0f; --queue-line: #4a3c1c;
  }
}
:root[data-theme="dark"] {
  --bg: #131920; --surface: #1b242e; --ink: #e6ecf2; --muted: #93a1af;
  --line: #2c3742; --accent: #53c3d8;
  --ok: #6cc694; --ok-bg: #1d3227; --warn: #e2ac61; --warn-bg: #382b12;
  --info: #85aaf3; --info-bg: #1c2c4c; --idle: #909ba6; --idle-bg: #242d36;
  --queue-bg: #251f0f; --queue-line: #4a3c1c;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--ink);
  font: 15px/1.65 "PingFang SC", -apple-system, "Helvetica Neue", "Noto Sans CJK SC", sans-serif;
}
.mono { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: .82em;
        font-variant-numeric: tabular-nums; }
.wrap { max-width: 1080px; margin: 0 auto; padding: 28px 20px 64px; }
header { display: flex; align-items: baseline; gap: 16px; flex-wrap: wrap;
         border-bottom: 2px solid var(--ink); padding-bottom: 12px; }
header h1 { margin: 0; font-size: 26px; letter-spacing: .12em; }
header .meta { color: var(--muted); font-size: 13px; }
.queue { margin-top: 22px; background: var(--queue-bg); border: 1px solid var(--queue-line);
         border-radius: 3px; padding: 14px 18px; }
.queue h2 { margin: 0 0 8px; font-size: 13px; letter-spacing: .18em; color: var(--warn);
            text-transform: uppercase; }
.queue ol { margin: 0; padding-left: 1.3em; display: grid; gap: 6px; }
.queue .src { color: var(--muted); font-size: 12.5px; margin-left: .5em; }
section.lane { margin-top: 30px; }
.lane h2 { font-size: 15px; letter-spacing: .1em; margin: 0 0 10px;
           display: flex; align-items: baseline; gap: 10px; }
.lane h2 .count { color: var(--muted); font-weight: 400; font-size: 12.5px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 12px; }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: 3px;
        padding: 13px 15px 12px; display: flex; flex-direction: column; gap: 7px; }
.card .top { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.pill { font-size: 11.5px; padding: 1.5px 9px; border-radius: 999px; font-weight: 600;
        letter-spacing: .04em; }
.pill.ok   { color: var(--ok);   background: var(--ok-bg); }
.pill.warn { color: var(--warn); background: var(--warn-bg); }
.pill.info { color: var(--info); background: var(--info-bg); }
.pill.idle { color: var(--idle); background: var(--idle-bg); }
.kind { font-size: 11.5px; color: var(--muted); border: 1px solid var(--line);
        padding: 1px 7px; border-radius: 2px; }
.baton { font-size: 11.5px; color: var(--accent); margin-left: auto; }
.card h3 { margin: 0; font-size: 15.5px; line-height: 1.45; }
.card h3 .batch { color: var(--accent); }
.next { font-size: 13.5px; }
.next::before { content: "▸ "; color: var(--accent); }
.blocked { font-size: 13px; color: var(--muted); margin: 0; padding-left: 1.2em; }
.blocked li::marker { content: "⛔ "; font-size: .8em; }
.card .foot { margin-top: auto; padding-top: 6px; border-top: 1px dashed var(--line);
              color: var(--muted); font-size: 12px; display: flex; gap: 12px; flex-wrap: wrap; }
footer { margin-top: 44px; color: var(--muted); font-size: 12.5px;
         border-top: 1px solid var(--line); padding-top: 12px; }
a { color: var(--accent); }
@media (prefers-reduced-motion: no-preference) { .card { transition: border-color .15s; } }
.card:hover { border-color: var(--accent); }
"""


def esc(s):
    return html.escape(str(s), quote=True)


def render_card(c):
    status = c.get("status", "draft")
    cls = STATUS_CLASS.get(status, "idle")
    label = STATUS_LABEL.get(status, status)
    parts = ['<article class="card">', '<div class="top">']
    parts.append(f'<span class="pill {cls}">{esc(label)}</span>')
    parts.append(f'<span class="kind">{esc(c.get("doc", "?"))}</span>')
    baton = c.get("baton")
    if baton and baton != "none":
        parts.append(f'<span class="baton">⊙ 棒：{esc(baton)}</span>')
    parts.append("</div>")
    batch = c.get("batch")
    bt = f'<span class="batch">{esc(batch)}</span> · ' if batch else ""
    parts.append(f'<h3>{bt}{esc(c["_title"])}</h3>')
    if c.get("next"):
        parts.append(f'<div class="next">{esc(c["next"])}</div>')
    blocked = c.get("blocked_on") or []
    if blocked:
        items = "".join(f"<li>{esc(b)}</li>" for b in blocked)
        parts.append(f'<ul class="blocked">{items}</ul>')
    foot = []
    if c.get("round"):
        foot.append(f'round {esc(c["round"])}')
    for k in ("base", "covers"):
        if c.get(k):
            foot.append(f'{k} <span class="mono">{esc(c[k])}</span>')
    if c.get("as_of"):
        foot.append(f'as-of <span class="mono">{esc(c["as_of"])}</span>')
    if c.get("updated"):
        foot.append(f'✎ <span class="mono">{esc(c["updated"])}</span>')
    if foot:
        parts.append('<div class="foot">' + " · ".join(foot) + "</div>")
    parts.append("</article>")
    return "\n".join(parts)


def render(cards, repo, head, branch):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    owner_q = [c for c in cards
               if str(c.get("next", "")).startswith("owner:") or c.get("baton") == "owner"]
    lanes = {}
    for c in cards:
        lanes.setdefault(c.get("track", "未分轨"), []).append(c)
    for lane in lanes.values():
        lane.sort(key=lambda c: STATUS_RANK.get(c.get("status"), 9))
    lane_names = [t for t in LANE_ORDER if t in lanes] + \
                 [t for t in lanes if t not in LANE_ORDER]

    out = ["<title>盘面</title>", f"<style>{CSS}</style>", '<div class="wrap">']
    out.append(f'<header><h1>盘面</h1><span class="meta">生成 <span class="mono">{now}</span>'
               f' · 语料 {esc(repo.name)} <span class="mono">{esc(branch)}@{esc(head)}</span>'
               f' · {len(cards)} 件</span></header>')
    if owner_q:
        out.append('<div class="queue"><h2>等 owner</h2><ol>')
        for c in owner_q:
            nxt = re.sub(r"^owner:\s*", "", str(c.get("next", "")))
            out.append(f'<li>{esc(nxt)}<span class="src">← {esc(c.get("track", ""))}'
                       f' · {esc(c["_title"])}</span></li>')
        out.append("</ol></div>")
    for name in lane_names:
        cs = lanes[name]
        live = sum(1 for c in cs if c.get("status") not in ("done", "archived"))
        out.append(f'<section class="lane"><h2>{esc(name)}'
                   f'<span class="count">{live} 在途 / {len(cs)} 件</span></h2><div class="grid">')
        out.extend(render_card(c) for c in cs)
        out.append("</div></section>")
    out.append('<footer>真源：各工件 md 文件的状态头（duet templates/frontmatter.md）。'
               '本页为只读渲染层，与真源不一致时以文件为准并重新生成。</footer>')
    out.append("</div>")
    return "\n".join(out)


ANSI = {"ok": "\033[32m", "warn": "\033[33m", "info": "\033[36m",
        "idle": "\033[2m", "dim": "\033[2m", "b": "\033[1m", "r": "\033[0m"}


def render_text(cards, repo, head, branch, color=True):
    c_ = (lambda k, s: f"{ANSI[k]}{s}{ANSI['r']}") if color else (lambda k, s: s)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    out = [c_("b", "盘面") + f" · 生成 {now} · {repo.name} {branch}@{head} · {len(cards)} 件"]
    owner_q = [c for c in cards
               if str(c.get("next", "")).startswith("owner:") or c.get("baton") == "owner"]
    if owner_q:
        out.append("")
        out.append(c_("warn", "━━ 等 owner"))
        for i, c in enumerate(owner_q, 1):
            nxt = re.sub(r"^owner:\s*", "", str(c.get("next", "")))
            out.append(f" {i}. {nxt}" + c_("dim", f"  ← {c.get('track', '')} · {c['_title']}"))
    lanes = {}
    for c in cards:
        lanes.setdefault(c.get("track", "未分轨"), []).append(c)
    for lane in lanes.values():
        lane.sort(key=lambda c: STATUS_RANK.get(c.get("status"), 9))
    lane_names = [t for t in LANE_ORDER if t in lanes] + \
                 [t for t in lanes if t not in LANE_ORDER]
    for name in lane_names:
        cs = lanes[name]
        live = sum(1 for c in cs if c.get("status") not in ("done", "archived"))
        out.append("")
        out.append(c_("b", f"━━ {name}") + c_("dim", f"（{live} 在途 / {len(cs)} 件）"))
        for c in cs:
            status = c.get("status", "draft")
            cls = STATUS_CLASS.get(status, "idle")
            label = STATUS_LABEL.get(status, status)
            batch = f"{c['batch']} · " if c.get("batch") else ""
            out.append(f" {c_(cls, f'[{label}]'):<18} {batch}{c['_title']}"
                       + c_("dim", f"  ({c.get('doc', '?')})"))
            if c.get("next"):
                out.append(c_("info", f"    ▸ {c['next']}"))
            for b in c.get("blocked_on") or []:
                out.append(c_("dim", f"    ⛔ {b}"))
            foot = [f"round {c['round']}" if c.get("round") else "",
                    f"base {c['base']}" if c.get("base") else "",
                    f"covers {c['covers']}" if c.get("covers") else "",
                    f"as-of {c['as_of']}" if c.get("as_of") else ""]
            foot = " · ".join(f for f in foot if f)
            if foot:
                out.append(c_("dim", f"    {foot}"))
    return "\n".join(out) + "\n"


def serve(repo, port):
    """按需渲染：每个请求现读工件现渲，刷新即拉取。/ = HTML，/text = 终端版。"""
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            try:
                cards = collect(repo)
                head, branch = git_meta(repo)
                if self.path.startswith("/text"):
                    body = render_text(cards, repo, head, branch, color=False)
                    ctype = "text/plain; charset=utf-8"
                else:
                    body = ('<!doctype html><meta charset="utf-8">'
                            '<meta name="viewport" content="width=device-width,initial-scale=1">'
                            + render(cards, repo, head, branch))
                    ctype = "text/html; charset=utf-8"
                raw = body.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
            except Exception as e:  # 渲染失败也别让服务死
                self.send_error(500, str(e))

        def log_message(self, *args):
            pass

    HTTPServer(("127.0.0.1", port), Handler).serve_forever()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", help="输出文件；text 模式省略则打到 stdout")
    ap.add_argument("--format", choices=["html", "text"], default="html")
    ap.add_argument("--no-color", action="store_true")
    ap.add_argument("--serve", type=int, metavar="PORT",
                    help="按需渲染服务：绑 127.0.0.1，刷新即重渲")
    a = ap.parse_args()
    if a.serve:
        serve(Path(a.repo).expanduser().resolve(), a.serve)
        return
    repo = Path(a.repo).expanduser().resolve()
    cards = collect(repo)
    if not cards:
        sys.exit("没有找到带状态头的工件")
    head, branch = git_meta(repo)
    if a.format == "text":
        color = not a.no_color and (a.out is None and sys.stdout.isatty())
        text = render_text(cards, repo, head, branch, color=color)
        if a.out:
            Path(a.out).expanduser().write_text(text, encoding="utf-8")
            print(f"{len(cards)} 张卡 → {a.out}")
        else:
            sys.stdout.write(text)
        return
    if not a.out:
        sys.exit("html 模式需要 --out")
    Path(a.out).expanduser().write_text(
        render(cards, repo, head, branch), encoding="utf-8")
    print(f"{len(cards)} 张卡 → {a.out}")


if __name__ == "__main__":
    main()

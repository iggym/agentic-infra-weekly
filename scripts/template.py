"""Render an Agentic Infra Weekly issue per docs/master-prompt-v1.md's HTML contract."""
import html
import math
import re
from datetime import date

SITE = "https://iggym.github.io/agentic-infra-weekly"
NAV_LABELS = ["s1", "s2", "s3", "s4", "s5", "s6", "s7"]

CSS = r"""
:root{color-scheme:dark;--bg:#090b10;--bg-raised:#0e1119;--surface:#12161f;--surface-hover:#171c28;--border:#232a38;--border-strong:#33405a;--text:#eef1f6;--text-muted:#9aa4b8;--text-faint:#62697a;--accent:#4f8cff;--accent-strong:#7cabff;--accent-glow:rgba(79,140,255,.14);--signal:#f5a623;--ok:#34d399;--danger:#f26d6d;--font-sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;--font-mono:ui-monospace,"SF Mono","IBM Plex Mono",Menlo,Consolas,monospace;--radius:10px}
[data-theme="light"]{color-scheme:light;--bg:#f6f7fa;--bg-raised:#fff;--surface:#fff;--surface-hover:#f0f2f7;--border:#dde1ea;--border-strong:#c3cadb;--text:#10141d;--text-muted:#4b5468;--text-faint:#6b7489;--accent:#2f66d9;--accent-strong:#1e4fbf;--accent-glow:rgba(47,102,217,.09);--signal:#9a6008}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{transition:none!important;animation:none!important}}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font-sans);line-height:1.65;font-size:1.05rem}
a{color:var(--accent-strong)}
:focus-visible{outline:2px solid var(--accent-strong);outline-offset:2px;border-radius:4px}
.skip-link{position:absolute;left:-9999px;top:0;background:var(--accent);color:#06101f;font-weight:700;padding:.7rem 1.1rem;z-index:100;text-decoration:none}
.skip-link:focus{left:0}
.topbar{position:sticky;top:0;z-index:10;display:flex;align-items:center;gap:.75rem;padding:.7rem 1rem;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--border);font-family:var(--font-mono);font-size:.78rem;color:var(--text-muted)}
.topbar a{color:var(--text);text-decoration:none;font-weight:700}
.topbar .crumb{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0}
.topbar .spacer{flex:1}
.theme-toggle{font:inherit;background:var(--surface);color:var(--text-muted);border:1px solid var(--border);border-radius:8px;padding:.35rem .6rem;cursor:pointer;min-height:32px}
.theme-toggle:hover{color:var(--text)}
.layout{max-width:1080px;margin:0 auto;padding:0 1rem 4rem;display:grid;grid-template-columns:minmax(0,1fr);gap:2rem}
@media (min-width:980px){.layout{grid-template-columns:200px minmax(0,720px);justify-content:center}}
nav.toc{display:none}
@media (min-width:980px){nav.toc{display:block;position:sticky;top:4rem;align-self:start;margin-top:3.2rem;font-size:.85rem}}
nav.toc ol{list-style:none;padding:0;margin:0;border-left:1px solid var(--border)}
nav.toc a{display:block;padding:.3rem .8rem;color:var(--text-muted);text-decoration:none}
nav.toc a:hover{color:var(--text);background:var(--surface-hover)}
article{min-width:0}
.kicker{font-family:var(--font-mono);font-size:.75rem;letter-spacing:.06em;text-transform:uppercase;color:var(--signal);margin:3rem 0 .6rem}
h1{font-size:clamp(2rem,6vw,2.9rem);line-height:1.1;letter-spacing:-.025em;margin:0}
.byline{color:var(--text-muted);font-family:var(--font-mono);font-size:.8rem;margin:.9rem 0 2.2rem}
h2{font-size:1.45rem;letter-spacing:-.01em;margin:2.8rem 0 .8rem;scroll-margin-top:4rem}
section{scroll-margin-top:4rem}
p{margin:0 0 1.05rem}
blockquote.reframe{margin:1.5rem 0;padding:1.1rem 1.3rem;border-left:3px solid var(--accent);background:var(--accent-glow);border-radius:0 var(--radius) var(--radius) 0;font-size:1.2rem;font-weight:650;line-height:1.45}
.oneliner{font-family:var(--font-mono);font-size:.95rem;color:var(--signal);border:1px dashed var(--border-strong);border-radius:var(--radius);padding:.8rem 1rem;margin:1.4rem 0}
ol.steps{padding-left:1.3rem}
ol.steps li{margin-bottom:.8rem}
.challenge{border:1px solid var(--border-strong);background:var(--surface);border-radius:var(--radius);padding:1.1rem 1.3rem}
.challenge p:last-child{margin:0}
code{font-family:var(--font-mono);font-size:.88em;background:var(--surface);border:1px solid var(--border);border-radius:4px;padding:.05em .35em}
sup a{text-decoration:none;font-size:.75em}
.hint{color:var(--text-faint);font-size:.85rem;margin-top:-.4rem}
.layers{display:flex;flex-direction:column;gap:.5rem}
.layer{width:100%;text-align:left;font:inherit;color:var(--text);background:var(--surface);border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:8px;padding:.75rem 1rem;cursor:pointer}
.layer:hover{background:var(--surface-hover)}
.layer .lname{display:block;font-family:var(--font-mono);font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--text-muted)}
.layer .ltech{font-weight:650}
.layer .lrole{display:block;color:var(--text-muted);font-size:.92rem;margin-top:.35rem}
.layer[aria-expanded="false"] .lrole{display:none}
.layer:nth-child(2){border-left-color:var(--ok)}.layer:nth-child(3){border-left-color:var(--signal)}.layer:nth-child(4){border-left-color:#c084fc}.layer:nth-child(5){border-left-color:var(--danger)}.layer:nth-child(6){border-left-color:#22d3ee}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:.8rem}
.card{font:inherit;text-align:left;color:var(--text);background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1rem;cursor:pointer;min-height:130px}
.card:hover{border-color:var(--border-strong)}
.card .face{display:block;font-family:var(--font-mono);font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:var(--text-faint);margin-bottom:.4rem}
.card .a{display:none;color:var(--text-muted)}
.card[aria-expanded="true"]{border-color:var(--accent)}
.card[aria-expanded="true"] .q{display:none}
.card[aria-expanded="true"] .a{display:block}
.recall-count{font-family:var(--font-mono);font-size:.8rem;color:var(--text-muted)}
.map svg{width:100%;height:auto;display:block;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius)}
.map .edge{stroke:var(--border-strong);stroke-width:1.5;transition:opacity .15s,stroke .15s}
.map .node circle{fill:var(--bg-raised);stroke:var(--accent);stroke-width:1.5}
.map .node.core circle{fill:var(--accent-glow);stroke-width:2.5}
.map .node text{fill:var(--text);font-family:var(--font-sans);font-size:12px;text-anchor:middle;pointer-events:none}
.map .node{cursor:pointer;outline:none}
.map .node:focus-visible circle{stroke:var(--signal);stroke-width:3}
.map.active .edge{opacity:.15}
.map.active .edge.on{opacity:1;stroke:var(--accent)}
.map.active .node{opacity:.4}
.map.active .node.on{opacity:1}
#citations ol{padding-left:1.3rem;font-size:.9rem;color:var(--text-muted);overflow-wrap:anywhere}
#citations li{margin-bottom:.5rem;scroll-margin-top:4rem}
#citations li:target{color:var(--text)}
footer.site-footer{border-top:1px solid var(--border);margin-top:3rem;padding-top:1.2rem;display:flex;flex-wrap:wrap;gap:1rem;font-size:.9rem}
footer.site-footer a{color:var(--text-muted)}
"""

JS = r"""
(function(){
  'use strict';
  var KEY='aiw:theme', root=document.documentElement, btn=document.getElementById('theme-toggle');
  function sysLight(){return window.matchMedia&&window.matchMedia('(prefers-color-scheme: light)').matches;}
  function apply(choice){
    var t=choice==='system'?(sysLight()?'light':'dark'):(choice==='light'?'light':'dark');
    root.setAttribute('data-theme',t);
    btn.textContent=t==='light'?'Dark mode':'Light mode';
    btn.setAttribute('aria-label','Switch to '+(t==='light'?'dark':'light')+' theme');
  }
  var saved='system';
  try{saved=localStorage.getItem(KEY)||'system';}catch(e){}
  apply(saved);
  btn.addEventListener('click',function(){
    var next=root.getAttribute('data-theme')==='light'?'dark':'light';
    try{localStorage.setItem(KEY,next);}catch(e){}
    apply(next);
  });

  document.querySelectorAll('.layer').forEach(function(el){
    el.addEventListener('click',function(){el.setAttribute('aria-expanded',String(el.getAttribute('aria-expanded')!=='true'));});
  });

  var cards=document.querySelectorAll('.card'), count=document.getElementById('recall-count');
  function updateCount(){
    var n=document.querySelectorAll('.card[aria-expanded="true"]').length;
    count.textContent=n+' / '+cards.length+' revealed';
  }
  cards.forEach(function(el){
    el.addEventListener('click',function(){el.setAttribute('aria-expanded',String(el.getAttribute('aria-expanded')!=='true'));updateCount();});
  });
  updateCount();

  var map=document.querySelector('.map'), status=document.getElementById('map-status');
  if(map){
    var edges=map.querySelectorAll('.edge'), nodes=map.querySelectorAll('.node');
    function on(id,label){
      map.classList.add('active');
      var linked=[];
      edges.forEach(function(e){
        var hit=e.getAttribute('data-a')===id||e.getAttribute('data-b')===id;
        e.classList.toggle('on',hit);
        if(hit)linked.push(e.getAttribute('data-a')===id?e.getAttribute('data-b'):e.getAttribute('data-a'));
      });
      var names=[];
      nodes.forEach(function(n){
        var hit=n.getAttribute('data-id')===id||linked.indexOf(n.getAttribute('data-id'))!==-1;
        n.classList.toggle('on',hit);
        if(hit&&n.getAttribute('data-id')!==id)names.push(n.getAttribute('aria-label'));
      });
      status.textContent=label+' connects to: '+names.join(', ')+'.';
    }
    function off(){map.classList.remove('active');status.textContent='';}
    nodes.forEach(function(n){
      var id=n.getAttribute('data-id'), label=n.getAttribute('aria-label');
      n.addEventListener('mouseenter',function(){on(id,label);});
      n.addEventListener('mouseleave',off);
      n.addEventListener('focus',function(){on(id,label);});
      n.addEventListener('blur',off);
      n.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();on(id,label);}});
    });
  }
})();
"""


def esc(s):
    return html.escape(s, quote=True)


def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s)


def word_count(sections):
    text = " ".join(strip_tags(s["body"]) for s in sections)
    return len(re.findall(r"[A-Za-z0-9’'\-]+", text))


def concept_svg(core, nodes, edges):
    w, h, cx, cy, r = 640, 420, 320, 210, 160
    pos = {"core": (cx, cy)}
    for i, n in enumerate(nodes):
        ang = -math.pi / 2 + 2 * math.pi * i / len(nodes)
        pos[n["id"]] = (round(cx + r * 1.3 * math.cos(ang)), round(cy + r * math.sin(ang)))
    all_edges = [("core", n["id"]) for n in nodes] + list(edges)
    out = [f'<svg viewBox="0 0 {w} {h}" role="group" aria-label="Concept map: {esc(core)}">']
    for a, b in all_edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        out.append(f'<line class="edge" data-a="{a}" data-b="{b}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')

    def node(nid, label, core_cls=""):
        x, y = pos[nid]
        rad = 52 if core_cls else 44
        words = label.split()
        lines, cur = [], ""
        for wd in words:
            if len(cur) + len(wd) + 1 > 12 and cur:
                lines.append(cur)
                cur = wd
            else:
                cur = (cur + " " + wd).strip()
        lines.append(cur)
        start = y - (len(lines) - 1) * 7
        tspans = "".join(f'<tspan x="{x}" y="{start + i * 14 + 4}">{esc(l)}</tspan>' for i, l in enumerate(lines))
        return (f'<g class="node{core_cls}" data-id="{nid}" tabindex="0" role="button" aria-label="{esc(label)}">'
                f'<circle cx="{x}" cy="{y}" r="{rad}"/><text>{tspans}</text></g>')

    out.append(node("core", core, " core"))
    for n in nodes:
        out.append(node(n["id"], n["label"]))
    out.append("</svg>")
    return "".join(out)


def render(a):
    d = date.fromisoformat(a["date"])
    pretty = d.strftime("%b %-d, %Y")
    words = word_count(a["sections"])
    minutes = math.ceil(words / 230)
    url = f"{SITE}/articles/{a['slug']}.html"
    desc = a["reframe"] if len(a["reframe"]) <= 160 else a["reframe"][:157].rsplit(" ", 1)[0] + "…"
    og_desc = a["reframe"] if len(a["reframe"]) <= 200 else a["reframe"][:197].rsplit(" ", 1)[0] + "…"

    toc = "".join(f'<li><a href="#{s["id"]}">{esc(s["heading"])}</a></li>' for s in a["sections"])
    toc += '<li><a href="#architecture">Architecture</a></li><li><a href="#recall">Recall Cards</a></li><li><a href="#concept-map">Concept Map</a></li><li><a href="#citations">Citations</a></li>'

    secs = []
    for s in a["sections"]:
        secs.append(f'<section id="{s["id"]}" aria-labelledby="{s["id"]}-h"><h2 id="{s["id"]}-h">{esc(s["heading"])}</h2>{s["body"]}</section>')

    layers = "".join(
        f'<button type="button" class="layer" aria-expanded="false"><span class="lname">{esc(l[0])}</span>'
        f'<span class="ltech">{esc(l[1])}</span><span class="lrole">{esc(l[2])}</span></button>'
        for l in a["layers"])
    cards = "".join(
        f'<button type="button" class="card" aria-expanded="false"><span class="face">Question</span>'
        f'<span class="q">{esc(q)}</span><span class="a">{esc(ans)}</span></button>'
        for q, ans in a["cards"])
    cites = "".join(f'<li id="c{i}">{c[0]} <a href="{esc(c[1])}" target="_blank" rel="noopener">{esc(c[1])}</a></li>'
                    for i, c in enumerate(a["citations"], 1))
    share_text = esc(a["title"] + " — Agentic Infra Weekly")
    from urllib.parse import quote
    x_url = f"https://twitter.com/intent/tweet?text={quote(a['title'] + ' — Agentic Infra Weekly')}&amp;url={quote(url, safe='')}"
    li_url = f"https://www.linkedin.com/sharing/share-offsite/?url={quote(url, safe='')}"

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(a['title'])} — Agentic Infra Weekly</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Agentic Infra Weekly">
<meta property="og:title" content="{esc(a['title'])}">
<meta property="og:description" content="{esc(og_desc)}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<meta property="article:published_time" content="{a['date']}">
<meta property="article:section" content="{esc(a['topic'])}">
<style>{CSS}</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="topbar">
  <a href="../index.html">Agentic Infra Weekly</a><span class="crumb">/ {esc(a['title'])}</span>
  <span class="spacer"></span><span>{minutes} min read</span>
  <button type="button" class="theme-toggle" id="theme-toggle">Light mode</button>
</header>
<div class="layout">
<nav class="toc" aria-label="Sections"><ol>{toc}</ol></nav>
<main id="main">
<article>
<p class="kicker">{esc(a['topic'])} · Week {a['week']}</p>
<h1>{esc(a['title'])}</h1>
<p class="byline"><time datetime="{a['date']}">{pretty}</time> · {minutes} min read</p>
{''.join(secs)}
<section id="architecture" aria-labelledby="architecture-h"><h2 id="architecture-h">Architecture</h2>
<p class="hint">{esc(a['arch_caption'])} Select a layer to expand it.</p>
<div class="layers">{layers}</div></section>
<section id="recall" aria-labelledby="recall-h"><h2 id="recall-h">Recall Cards</h2>
<p class="recall-count" id="recall-count" aria-live="polite"></p>
<div class="cards">{cards}</div></section>
<section id="concept-map" aria-labelledby="concept-map-h"><h2 id="concept-map-h">Concept Map</h2>
<p class="hint">Hover or focus a node (Tab, then Enter) to highlight its connections.</p>
<div class="map">{concept_svg(a['map_core'], a['map_nodes'], a['map_edges'])}</div>
<p class="hint" id="map-status" aria-live="polite"></p></section>
<section id="citations" aria-labelledby="citations-h"><h2 id="citations-h">Citations</h2><ol>{cites}</ol></section>
</article>
<footer class="site-footer">
  <a href="#main">Back to top</a><a href="../index.html">All issues</a>
  <a href="{x_url}" target="_blank" rel="noopener">Share on X</a>
  <a href="{li_url}" target="_blank" rel="noopener">Share on LinkedIn</a>
</footer>
</main>
</div>
<script>{JS}</script>
</body>
</html>
""", words, minutes

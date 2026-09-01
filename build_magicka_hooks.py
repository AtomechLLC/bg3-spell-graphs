"""Magicka Hooks: elements and magicks wired through game-states -> magicka_hooks.html.

The third Magicka lens, in the suite's hook grammar (BG3's Combo
Chemistry): the central wheel holds the states a combo passes through -
WET, FROZEN, BURNING, GREASE, BARRIER, BEAM CLASH - with the elements
and magicks that create each state feeding it from outside, and the
ones that cash it striking out. Chain edges across the wheel show state
chemistry itself: wet + cold = frozen, grease + fire = burning.
"""
import json
import math
import os

W, H = 1500, 960
CX, CY = W / 2, 490
SURFACE = "#16161D"

ELEMS = {
    "water": ("Water", "Q", "#3D7BD9", "💧"),
    "life": ("Life", "W", "#4FC46F", "✚"),
    "shield": ("Shield", "E", "#E8D44D", "⬟"),
    "cold": ("Cold", "R", "#A8DCE8", "❄"),
    "lightning": ("Lightning", "A", "#9B7BE8", "⚡"),
    "arcane": ("Arcane", "S", "#D9463E", "✦"),
    "earth": ("Earth", "D", "#8C6844", "🪨"),
    "fire": ("Fire", "F", "#E87A2D", "🔥"),
    "steam": ("Steam", "QF", "#C8CBD9", "♨"),
    "ice": ("Ice", "QR", "#7FC4E8", "🧊"),
}
MAGICKS = {
    "rain": ("Rain", "#3D7BD9"),
    "thunderstorm": ("Thunderstorm", "#9B7BE8"),
    "blizzard": ("Blizzard", "#A8DCE8"),
    "grease-m": ("Grease", "#C9B458"),
    "conflagration": ("Conflagration", "#E87A2D"),
    "napalm": ("Napalm", "#E87A2D"),
    "meteor": ("Meteor Shower", "#E87A2D"),
    "phoenix": ("Summon Phoenix", "#E87A2D"),
    "chain-l": ("Chain Lightning", "#9B7BE8"),
    "thunderbolt": ("Thunder Bolt", "#9B7BE8"),
    "vortex": ("Vortex", "#7FC4E8"),
    "tornado": ("Tornado", "#8C6844"),
}

# hooks: (id, emoji, LABEL, color, description)
HOOKS = [
    ("wet", "💧", "WET", "#3D7BD9",
     "soaked — lightning doubles and chains, cold freezes solid, fire won't stick"),
    ("frozen", "🧊", "FROZEN", "#7FC4E8",
     "solid ice — helpless until it thaws, and physical force shatters for massive damage"),
    ("burning", "🔥", "BURNING", "#E87A2D",
     "fire over time — panic, damage, and spreading until doused"),
    ("grease", "🛢", "GREASE", "#C9B458",
     "a slick, flammable floor — enemies slip, and one spark makes it a firestorm"),
    ("barrier", "🛡", "BARRIER", "#E8D44D",
     "walls, domes, mines and wards — the arena itself becomes a spell"),
    ("clash", "✨", "BEAM CLASH", "#D9463E",
     "crossed beams detonate — the co-op hazard that defines the game's comedy"),
]

# edges: (hook, node, 'make'|'use'|'counter', color, verb)
EDGES_DEF = [
    ("wet", "water", "make", "#3D7BD9", "soaks with every spray"),
    ("wet", "rain", "make", "#3D7BD9", "wets the whole field"),
    ("wet", "thunderstorm", "make", "#3D7BD9", "rains while it strikes"),
    ("wet", "steam", "make", "#C8CBD9", "condenses onto targets"),
    ("wet", "lightning", "use", "#9B7BE8", "conducts — double damage, self-zap for wet casters"),
    ("wet", "chain-l", "use", "#9B7BE8", "chains harder through the soaked"),
    ("wet", "thunderbolt", "use", "#9B7BE8", "lands the big bolt"),
    ("wet", "cold", "use", "#A8DCE8", "freezes the soaked solid"),
    ("wet", "fire", "counter", "#8a879a", "dries — and wet refuses burning"),
    ("frozen", "cold", "make", "#A8DCE8", "freezes the wet"),
    ("frozen", "blizzard", "make", "#A8DCE8", "freezes everyone, caster included"),
    ("frozen", "vortex", "make", "#7FC4E8", "ice-cold pull"),
    ("frozen", "earth", "use", "#E3C377", "shatters — the boulder crit"),
    ("frozen", "tornado", "use", "#8C6844", "launches the helpless"),
    ("burning", "fire", "make", "#E87A2D", "ignites on touch"),
    ("burning", "conflagration", "make", "#E87A2D", "a rolling heat wave"),
    ("burning", "napalm", "make", "#E87A2D", "airstrike-grade ignition"),
    ("burning", "meteor", "make", "#E87A2D", "meteors ignite where they land"),
    ("burning", "phoenix", "make", "#E87A2D", "the bird burns as it heals"),
    ("burning", "water", "counter", "#8a879a", "douses"),
    ("burning", "rain", "counter", "#8a879a", "douses the whole field"),
    ("grease", "grease-m", "make", "#C9B458", "paints the floor"),
    ("grease", "fire", "use", "#E87A2D", "one spark, one firestorm"),
    ("barrier", "shield", "make", "#E8D44D", "walls and domes"),
    ("barrier", "earth", "use", "#8C6844", "stone walls (E + D)"),
    ("barrier", "fire", "use", "#E87A2D", "fire mines and storms (E + F)"),
    ("barrier", "lightning", "use", "#9B7BE8", "lightning storms (E + A)"),
    ("barrier", "arcane", "counter", "#8a879a", "the beam grinds barriers down"),
    ("clash", "arcane", "make", "#D9463E", "the red beam"),
    ("clash", "life", "make", "#4FC46F", "the heal beam — cross them and duck"),
]

# state chemistry across the wheel itself
CHAIN = [("wet", "frozen", "wet + cold = frozen"),
         ("grease", "burning", "grease + fire = burning")]

NODES = {}
for hid, nid, d, col, verb in EDGES_DEF:
    NODES[nid] = True
print(f"{len(HOOKS)} hooks, {len(NODES)} nodes, {len(EDGES_DEF)} spokes")

def ninfo(nid):
    if nid in ELEMS:
        n, k, c, g = ELEMS[nid]
        return dict(name=n, key=k, col=c, glyph=g, kind="elem")
    n, c = MAGICKS[nid]
    return dict(name=n, key="", col=c, glyph="", kind="magick")

HPOS = {}
for i, h in enumerate(HOOKS):
    a = 2 * math.pi * i / len(HOOKS) - math.pi / 2
    HPOS[h[0]] = (CX + 190 * math.cos(a), CY + 150 * math.sin(a), a)

NODE_HOOKS = {}
for hid, nid, d, col, verb in EDGES_DEF:
    NODE_HOOKS.setdefault(nid, set()).add(hid)

import random
rng = random.Random(5)
pos = {}
for nid in NODES:
    hs = NODE_HOOKS[nid]
    vx = sum(math.cos(HPOS[h][2]) for h in hs)
    vy = sum(math.sin(HPOS[h][2]) for h in hs)
    a = math.atan2(vy, vx) if (vx or vy) else rng.uniform(0, 2 * math.pi)
    a += rng.uniform(-0.22, 0.22)
    rad = 420 + rng.uniform(-45, 45)
    pos[nid] = [CX + rad * math.cos(a), CY + rad * 0.75 * math.sin(a)]

def clamp(p):
    p[0] = min(max(p[0], 70), W - 70)
    p[1] = min(max(p[1], 80), H - 70)
    dx, dy = p[0] - CX, (p[1] - CY) / 0.75
    d = math.sqrt(dx * dx + dy * dy) or 1
    if d < 310:
        p[0] = CX + dx / d * 310
        p[1] = CY + dy / d * 310 * 0.75

for it in range(220):
    t = 1 - it / 220
    disp = {i: [0.0, 0.0] for i in pos}
    items = list(pos.items())
    for i in range(len(items)):
        id1, p1 = items[i]
        for j in range(i + 1, len(items)):
            id2, p2 = items[j]
            dx, dy = p1[0] - p2[0], p1[1] - p2[1]
            d2 = dx * dx + dy * dy
            if d2 < 1:
                dx, dy, d2 = rng.uniform(-1, 1), rng.uniform(-1, 1), 1
            if d2 < 150 * 150:
                d = math.sqrt(d2)
                fr = 1100 / d2 * 60
                disp[id1][0] += dx / d * fr; disp[id1][1] += dy / d * fr
                disp[id2][0] -= dx / d * fr; disp[id2][1] -= dy / d * fr
    for nid in pos:
        hs = NODE_HOOKS[nid]
        for h in hs:
            hx, hy, _a = HPOS[h]
            dx, dy = hx - pos[nid][0], hy - pos[nid][1]
            d = math.sqrt(dx * dx + dy * dy) or 1
            k = 0.05 / len(hs) * (d - 250)
            disp[nid][0] += dx / d * k
            disp[nid][1] += dy / d * k
    step = 11 * t + 1
    for nid, p in pos.items():
        dx, dy = disp[nid]
        d = math.sqrt(dx * dx + dy * dy) or 1
        m = min(d, step)
        p[0] += dx / d * m; p[1] += dy / d * m
        clamp(p)
for _ in range(90):
    moved = False
    ids = list(pos)
    for i in range(len(ids)):
        p1 = pos[ids[i]]
        for j in range(i + 1, len(ids)):
            p2 = pos[ids[j]]
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            d = math.sqrt(dx * dx + dy * dy) or 0.5
            if d < 74:
                push = (74 - d) / 2
                ux, uy = dx / d, dy / d
                p1[0] -= ux * push; p1[1] -= uy * push
                p2[0] += ux * push; p2[1] += uy * push
                clamp(p1); clamp(p2)
                moved = True
    if not moved:
        break

# ---------------------------------------------------------------- svg
colors = sorted({e[3] for e in EDGES_DEF} | {"#E3C377"})
markers = "".join(
    f'<marker id="m{c.lstrip("#")}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5.5" '
    f'markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" fill="{c}"/></marker>'
    for c in colors)

sv = [f'<rect width="{W}" height="{H}" fill="{SURFACE}" rx="14"/>']
sv.append(f'<ellipse cx="{CX}" cy="{CY}" rx="190" ry="150" fill="none" stroke="#2A2734" stroke-width="1.5" stroke-dasharray="3 6"/>')
sv.append(f'<ellipse cx="{CX}" cy="{CY}" rx="190" ry="150" fill="#D4AF5E" opacity="0.04" filter="url(#blur)"/>')
sv.append(f'<text x="{CX}" y="{CY + 5:.0f}" text-anchor="middle" fill="#6b6880" '
          f'font-family="Cinzel,Georgia,serif" font-size="15" letter-spacing="3">THE STATES</text>')

def shrink(x1, y1, x2, y2, r1, r2):
    dx, dy = x2 - x1, y2 - y1
    d = math.sqrt(dx * dx + dy * dy) or 1
    ux, uy = dx / d, dy / d
    return x1 + ux * r1, y1 + uy * r1, x2 - ux * r2, y2 - uy * r2

for a, b, why in CHAIN:
    ax, ay, _ = HPOS[a]; bx, by, _ = HPOS[b]
    x1, y1, x2, y2 = shrink(ax, ay, bx, by, 34, 40)
    sv.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#E3C377" '
              f'stroke-opacity="0.55" stroke-width="2.2" marker-end="url(#mE3C377)" '
              f'class="e t-chain h-{a} h-{b}"><title>{why}</title></line>')

for hid, nid, d, col, verb in EDGES_DEF:
    hx, hy, _a = HPOS[hid]
    sx, sy = pos[nid]
    if d == "make":
        x1, y1, x2, y2 = shrink(sx, sy, hx, hy, 26, 36)
    else:
        x1, y1, x2, y2 = shrink(hx, hy, sx, sy, 36, 26)
    dash = ' stroke-dasharray="5 4"' if d == "counter" else ""
    sv.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{col}" '
              f'stroke-opacity="0.30" stroke-width="1.5"{dash} marker-end="url(#m{col.lstrip("#")})" '
              f'class="e t-{d} h-{hid} n-{nid}"/>')

for hid, em, lab, col, desc in HOOKS:
    hx, hy, _a = HPOS[hid]
    nmk = sum(1 for e in EDGES_DEF if e[0] == hid and e[2] == "make")
    nus = sum(1 for e in EDGES_DEF if e[0] == hid and e[2] != "make")
    sv.append(f'<g class="hook" data-h="{hid}" data-name="{lab.title()}" '
              f'data-sub="{desc} · {nmk} in → {nus} out">')
    sv.append(f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="28" fill="{SURFACE}" stroke="{col}" stroke-width="2.6"/>')
    sv.append(f'<text x="{hx:.0f}" y="{hy + 7:.0f}" text-anchor="middle" font-size="21" class="femoji">{em}</text>')
    ly = hy + 47 if hy >= CY else hy - 37
    sv.append(f'<text x="{hx:.0f}" y="{ly:.0f}" text-anchor="middle" fill="{col}" '
              f'font-family="IBM Plex Mono,monospace" font-size="11" font-weight="600" letter-spacing="1.6" '
              f'stroke="{SURFACE}" stroke-width="5" paint-order="stroke">{lab}</text>')
    sv.append('</g>')

for nid in NODES:
    inf = ninfo(nid)
    x, y = pos[nid]
    roles = [f"{'creates' if e[2] == 'make' else 'counters' if e[2] == 'counter' else 'exploits'} "
             f"{next(h[2].lower() for h in HOOKS if h[0] == e[0])}: {e[4]}"
             for e in EDGES_DEF if e[1] == nid]
    sub = " · ".join(roles)
    sv.append(f'<g class="n" data-id="{nid}" data-name="{inf["name"]}'
              f'{" (" + inf["key"] + ")" if inf["key"] else ""}" data-sub="{sub}">')
    if inf["kind"] == "elem":
        sv.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="24" fill="{SURFACE}" stroke="{inf["col"]}" stroke-width="2.6"/>')
        sv.append(f'<text x="{x:.0f}" y="{y + 6:.0f}" text-anchor="middle" font-size="17" class="femoji" '
                  f'fill="{inf["col"]}">{inf["glyph"]}</text>')
        ly = y + 41 if y >= CY else y - 32
        sv.append(f'<text x="{x:.0f}" y="{ly:.0f}" text-anchor="middle" fill="{inf["col"]}" '
                  f'font-family="IBM Plex Mono,monospace" font-size="10.5" font-weight="600" letter-spacing="1" '
                  f'stroke="{SURFACE}" stroke-width="4" paint-order="stroke">{inf["name"].upper()} '
                  f'<tspan fill="#6b6880">{inf["key"]}</tspan></text>')
    else:
        sv.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="16" fill="{SURFACE}" stroke="{inf["col"]}" '
                  f'stroke-width="2" stroke-dasharray="4 2.5"/>')
        sv.append(f'<text x="{x:.0f}" y="{y + 4:.0f}" text-anchor="middle" fill="{inf["col"]}" '
                  f'font-family="IBM Plex Mono,monospace" font-size="9" font-weight="600">MK</text>')
        ly = y + 33 if y >= CY else y - 25
        sv.append(f'<text x="{x:.0f}" y="{ly:.0f}" text-anchor="middle" fill="#C9C6D4" '
                  f'font-family="IBM Plex Mono,monospace" font-size="11" '
                  f'stroke="{SURFACE}" stroke-width="4" paint-order="stroke">{inf["name"]}</text>')
    sv.append('</g>')
SVG = "\n".join(sv)

legend = "".join(
    f'<button class="pchip lc on" data-h="{hid}"><span class="femoji">{em}</span>'
    f'<span class="dot" style="background:{col}"></span>{lab.lower()}</button>'
    for hid, em, lab, col, _d in HOOKS)

DISCORD = ('<svg viewBox="0 0 127.14 96.36" width="16" height="12" fill="currentColor" aria-hidden="true">'
           '<path d="M107.7,8.07A105.15,105.15,0,0,0,81.47,0a72.06,72.06,0,0,0-3.36,6.83A97.68,97.68,0,0,'
           '0,49,6.83,72.37,72.37,0,0,0,45.64,0,105.89,105.89,0,0,0,19.39,8.09C2.79,32.65-1.71,'
           '56.6.54,80.21h0A105.73,105.73,0,0,0,32.71,96.36,77.7,77.7,0,0,0,39.6,85.25a68.42,68.42,'
           '0,0,1-10.85-5.18c.91-.66,1.8-1.34,2.66-2a75.57,75.57,0,0,0,64.32,0c.87.71,1.76,1.39,'
           '2.66,2a68.68,68.68,0,0,1-10.87,5.19,77,77,0,0,0,6.89,11.1A105.25,105.25,0,0,0,126.6,'
           '80.22h0C129.24,52.84,122.09,29.11,107.7,8.07ZM42.45,65.69C36.18,65.69,31,60,31,53s5-12.74,'
           '11.43-12.74S54,46,53.89,53,48.84,65.69,42.45,65.69Zm42.24,0C78.41,65.69,73.25,60,73.25,'
           '53s5-12.74,11.44-12.74S96.23,46,96.12,53,91.08,65.69,84.69,65.69Z"/></svg>')
FSC = (f'<a class="fsc" href="http://funsmith.club" target="_blank" rel="noopener" '
       f'title="Funsmith Club — game design community on Discord">{DISCORD}funsmith.club</a>')

HTML = f"""<title>Magicka Hooks</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#101016;color:#E8E6EF;font:400 14px/1.5 "IBM Plex Mono",ui-monospace,monospace;
  min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:22px 18px 30px}}
header{{width:100%;max-width:1500px;display:flex;flex-direction:column;gap:10px;margin-bottom:12px}}
.topline{{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap}}
h1{{font:600 22px Cinzel,Georgia,serif;color:#E3C377;margin:0;letter-spacing:.06em}}
.sub{{color:#A7A4B3;font-size:11.5px}}
.legend{{display:flex;gap:7px;flex-wrap:wrap;align-items:center}}
.pchip{{background:transparent;border:1px solid #3a3647;border-radius:999px;color:#C9C6D4;
  font:500 11px "IBM Plex Mono",monospace;padding:3px 11px;cursor:pointer;letter-spacing:.05em;
  display:inline-flex;align-items:center;gap:6px}}
.pchip:hover{{border-color:#6b6880}}
.pchip.on{{background:#D4AF5E14;border-color:#6b6880;color:#E8E6EF}}
.pchip:focus-visible{{outline:2px solid #E3C377;outline-offset:1px}}
.dot{{width:10px;height:10px;border-radius:50%;display:inline-block}}
.femoji{{font-family:"Segoe UI Emoji","Apple Color Emoji","Noto Color Emoji",sans-serif;font-style:normal}}
.segrow{{margin-left:auto;display:flex;align-items:center;gap:10px}}
#copybtn.ok{{border-color:#5fbf83;color:#7fdfa3}}
#copybtn.err{{border-color:#e58a9b;color:#e58a9b}}
.wrap{{width:100%;max-width:1500px;position:relative}}
svg{{width:100%;height:auto;display:block}}
.n,.hook{{cursor:pointer}}
svg.hov .n,svg.hov .hook{{opacity:.15}}
svg.hov .n.hl,svg.hov .hook.hl{{opacity:1}}
svg.hov line.e{{opacity:.05}}
svg.hov line.e.hl{{stroke-opacity:.95;opacity:1;stroke-width:2.2}}
line.e.offch{{display:none}}
#tip{{position:absolute;pointer-events:none;background:#211E2Bee;border:1px solid #3a3647;
  border-radius:8px;padding:7px 11px;font-size:12.5px;display:none;z-index:2;max-width:360px;
  box-shadow:0 8px 28px #000A}}
#tip b{{color:#E3C377;display:block;font-size:13px}}
#tip span{{color:#A7A4B3}}
footer{{color:#8a879a;font-size:11px;margin-top:10px;max-width:1500px;text-align:center;line-height:1.8}}
footer a{{color:#D4AF5E;text-decoration:none}}
::selection{{background:#D4AF5E44}}
.fsc{{display:inline-flex;align-items:center;gap:7px;border:1px solid #3a3647;
  border-radius:999px;padding:4px 12px;font:500 11px "IBM Plex Mono",monospace;color:#C9C6D4;
  text-decoration:none;letter-spacing:.05em}}
.fsc:hover{{border-color:#D4AF5E;color:#E3C377}}
</style>
<header>
  <div class="topline">
    <div><h1>Magicka Hooks</h1>
    <div class="sub">{len(HOOKS)} states · {len(NODES)} elements &amp; magicks · {len(EDGES_DEF)} spokes —
what BG3 hides in status rows, Magicka wears as its whole combat system</div></div>
    <div class="segrow">
      {FSC}
      <button id="copybtn" class="pchip" title="Copy the current view as a PNG image">⧉ copy image</button>
    </div>
  </div>
  <div class="legend">{legend}
    <button class="pchip" id="allch">all</button></div>
</header>
<div class="wrap">
  <svg viewBox="0 0 {W} {H}" role="img" aria-label="Magicka's game-states with the elements and magicks that create and exploit them">
  <defs><filter id="blur"><feGaussianBlur stdDeviation="26"/></filter>{markers}</defs>
  {SVG}</svg>
  <div id="tip"></div>
</div>
<footer>hover a state to see its whole economy · hover an element or magick (dashed ring, MK) for its roles ·
arrows point the way the combo flows: in to create the state, out to spend it · dashed spokes are counters ·
the gold chords are the wheel's own chemistry: wet + cold = frozen, grease + fire = burning ·
companion views: the element wheel (Magicka Chemistry) and the recipe trie (Casting Tree) ·
Magicka © Arrowhead Game Studios / Paradox Interactive</footer>
<script>
const tip = document.getElementById('tip'), wrap = document.querySelector('.wrap');
const svg = document.querySelector('.wrap svg');
function moveTip(e) {{
  const r = wrap.getBoundingClientRect();
  tip.style.left = Math.min(e.clientX - r.left + 14, r.width - 370) + 'px';
  tip.style.top = (e.clientY - r.top + 14) + 'px';
}}
function clearHl() {{
  svg.classList.remove('hov');
  svg.querySelectorAll('.hl').forEach(x => x.classList.remove('hl'));
  tip.style.display = 'none';
}}
function showTip(el) {{
  tip.innerHTML = '<b></b><span></span>';
  tip.firstChild.textContent = el.dataset.name;
  tip.lastChild.textContent = el.dataset.sub;
  tip.style.display = 'block';
}}
document.querySelectorAll('.n').forEach(n => {{
  n.addEventListener('mouseenter', () => {{
    svg.classList.add('hov');
    n.classList.add('hl');
    svg.querySelectorAll('line.e.n-' + n.dataset.id).forEach(l => {{
      if (l.classList.contains('offch')) return;
      l.classList.add('hl');
      const h = [...l.classList].find(c => c.indexOf('h-') === 0).slice(2);
      const hk = svg.querySelector('.hook[data-h="' + h + '"]');
      if (hk) hk.classList.add('hl');
    }});
    showTip(n);
  }});
  n.addEventListener('mousemove', moveTip);
  n.addEventListener('mouseleave', clearHl);
}});
document.querySelectorAll('.hook').forEach(hk => {{
  hk.addEventListener('mouseenter', () => {{
    svg.classList.add('hov');
    hk.classList.add('hl');
    svg.querySelectorAll('line.e.h-' + hk.dataset.h).forEach(l => {{
      if (l.classList.contains('offch')) return;
      l.classList.add('hl');
      [...l.classList].forEach(c => {{
        if (c.indexOf('n-') === 0) {{
          const nn = svg.querySelector('.n[data-id="' + c.slice(2) + '"]');
          if (nn) nn.classList.add('hl');
        }}
        if (c.indexOf('h-') === 0 && c.slice(2) !== hk.dataset.h) {{
          const oh = svg.querySelector('.hook[data-h="' + c.slice(2) + '"]');
          if (oh) oh.classList.add('hl');
        }}
      }});
    }});
    showTip(hk);
  }});
  hk.addEventListener('mousemove', moveTip);
  hk.addEventListener('mouseleave', clearHl);
}});
const HKS = {json.dumps([h[0] for h in HOOKS])};
const chs = new Set(HKS);
function applyCh() {{
  svg.querySelectorAll('line.e').forEach(l => {{
    const hs = [...l.classList].filter(c => c.indexOf('h-') === 0).map(c => c.slice(2));
    l.classList.toggle('offch', !hs.some(h => chs.has(h)));
  }});
  svg.querySelectorAll('.hook').forEach(h =>
    h.style.opacity = chs.has(h.dataset.h) ? '' : '0.25');
  document.querySelectorAll('.lc').forEach(b => b.classList.toggle('on', chs.has(b.dataset.h)));
}}
document.querySelectorAll('.lc').forEach(b => b.addEventListener('click', () => {{
  if (chs.size === HKS.length) {{ chs.clear(); chs.add(b.dataset.h); }}
  else if (chs.has(b.dataset.h)) {{ chs.delete(b.dataset.h); if (!chs.size) HKS.forEach(k => chs.add(k)); }}
  else chs.add(b.dataset.h);
  applyCh();
}}));
document.getElementById('allch').addEventListener('click', () => {{
  HKS.forEach(k => chs.add(k));
  applyCh();
}});
async function exportPNG() {{
  const clone = svg.cloneNode(true);
  clone.querySelectorAll('line.e.offch').forEach(l => l.remove());
  clone.querySelectorAll('.hl').forEach(x => x.classList.remove('hl'));
  const xml = new XMLSerializer().serializeToString(clone);
  const url = URL.createObjectURL(new Blob([xml], {{type: 'image/svg+xml'}}));
  const img = new Image();
  await new Promise((res, rej) => {{ img.onload = res; img.onerror = rej; img.src = url; }});
  const c = document.createElement('canvas');
  c.width = 3000; c.height = 1920;
  const ctx = c.getContext('2d');
  ctx.fillStyle = '#101016';
  ctx.fillRect(0, 0, c.width, c.height);
  ctx.drawImage(img, 0, 0, c.width, c.height);
  URL.revokeObjectURL(url);
  return new Promise(res => c.toBlob(res, 'image/png'));
}}
const copybtn = document.getElementById('copybtn');
function flashCopy(cls, text) {{
  copybtn.classList.add(cls);
  copybtn.textContent = text;
  setTimeout(() => {{ copybtn.classList.remove(cls); copybtn.textContent = '⧉ copy image'; }}, 2200);
}}
copybtn.addEventListener('click', async () => {{
  copybtn.textContent = '… rendering';
  try {{
    const blob = await exportPNG();
    await navigator.clipboard.write([new ClipboardItem({{'image/png': blob}})]);
    flashCopy('ok', '✓ copied');
  }} catch (e) {{
    flashCopy('err', '✕ blocked');
  }}
}});
</script>
"""
with open("magicka_hooks.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"magicka_hooks.html: {os.path.getsize('magicka_hooks.html') / 1024:.0f} KB")

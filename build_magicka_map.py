"""Magicka Chemistry: the combo map of Magicka (2011) -> magicka_map.html.

The purest combo system ever shipped, drawn in the suite's hook grammar:
the eight elements (plus the two hybrids) form the central wheel; cancel
chords and combine arcs are the wheel's internal chemistry; the status
hooks (WET / BURNING / FROZEN) sit just outside; and the outer ring holds
every Magick, wired to the elements its recipe queues.

Sources: Magickapedia, StrategyWiki, kingtoko's Magicks guide (web).
"""
import json
import math
import os

W, H = 1500, 980
CX, CY = W / 2, 500
SURFACE = "#16161D"

# id, name, key, color, glyph — ring order puts hybrid parents adjacent
ELEMS = [
    ("life", "Life", "W", "#4FC46F", "✚"),
    ("shield", "Shield", "E", "#E8D44D", "⬟"),
    ("cold", "Cold", "R", "#A8DCE8", "❄"),
    ("ice", "Ice", "QR", "#7FC4E8", "🧊"),
    ("water", "Water", "Q", "#3D7BD9", "💧"),
    ("steam", "Steam", "QF", "#C8CBD9", "♨"),
    ("fire", "Fire", "F", "#E87A2D", "🔥"),
    ("earth", "Earth", "D", "#8C6844", "🪨"),
    ("lightning", "Lightning", "A", "#9B7BE8", "⚡"),
    ("arcane", "Arcane", "S", "#D9463E", "✦"),
]
E = {e[0]: dict(zip(("id", "name", "key", "color", "glyph"), e)) for e in ELEMS}
EANG = {e[0]: 2 * math.pi * i / len(ELEMS) - math.pi / 2 for i, e in enumerate(ELEMS)}
def epos(eid, rx=205, ry=165):
    a = EANG[eid]
    return CX + rx * math.cos(a), CY + ry * math.sin(a)

CANCELS = [("fire", "cold", "opposites — queuing one dispels the other"),
           ("water", "lightning", "opposites — lightning refuses a wet queue"),
           ("earth", "lightning", "opposites — earth grounds lightning"),
           ("life", "arcane", "opposites — the beam of life against the beam of death")]
DOWNGRADES = [("fire", "ice", "fire melts queued ice back to water"),
              ("cold", "steam", "cold condenses queued steam back to water")]
COMBINES = [("water", "cold", "ice", "water + cold freeze into ice"),
            ("water", "fire", "steam", "water + fire boil into steam")]

# status hooks: (id, label, color, anchor element, dy-side)
STATUSES = [("wet", "WET", "#3D7BD9", "water", "water soaks — doubled lightning, freezable, fire-proof"),
            ("burning", "BURNING", "#E87A2D", "fire", "fire ignites — damage over time until doused"),
            ("frozen", "FROZEN", "#A8DCE8", "ice", "solid ice — shattered by physical hits for massive damage")]
STATUS_EDGES = [
    ("water", "wet", "make", "#3D7BD9", False),
    ("wet", "lightning", "use", "#9B7BE8", False),      # conduct (and self-zap!)
    ("wet", "frozen", "use", "#A8DCE8", False),
    ("cold", "frozen", "make", "#A8DCE8", False),
    ("frozen", "earth", "use", "#E3C377", False),       # shatter
    ("fire", "burning", "make", "#E87A2D", False),
    ("wet", "burning", "use", "#8a879a", True),         # douse (counter)
]

MAGICKS = [
    ("Revive", ["life", "lightning"], "revives fallen wizards", False),
    ("Grease", ["water", "earth", "life"], "slippery, flammable floor", False),
    ("Haste", ["lightning", "arcane", "fire"], "run much faster", False),
    ("Rain", ["water", "steam"], "rain that wets everyone", False),
    ("Nullify", ["arcane", "shield"], "strips status effects", False),
    ("Thunder Bolt", ["steam", "lightning", "arcane", "lightning"], "one heavy bolt", False),
    ("Tornado", ["earth", "steam", "water", "steam"], "launches everyone skyward", False),
    ("Conflagration", ["steam", "fire", "steam", "fire", "steam"], "a rolling heat wave", False),
    ("Time Warp", ["cold", "shield"], "slows time itself", False),
    ("Blizzard", ["cold", "ice", "cold"], "freezes the whole field", False),
    ("Teleport", ["lightning", "arcane", "lightning"], "blink to the cursor", False),
    ("Thunderstorm", ["steam", "steam", "lightning", "arcane", "lightning"], "random rain and thunder", False),
    ("Summon Phoenix", ["life", "lightning", "fire"], "fire bird; revives the fallen", False),
    ("Raise Dead", ["ice", "earth", "arcane", "cold"], "undead fighters", False),
    ("Fear", ["cold", "arcane", "shield"], "enemies flee", False),
    ("Charm", ["life", "shield", "earth"], "turns an enemy friendly", False),
    ("Summon Death", ["arcane", "cold", "ice", "cold", "arcane"], "reaps the weakest nearby", False),
    ("Invisibility", ["arcane", "shield", "steam", "arcane"], "untargetable", False),
    ("Summon Elemental", ["arcane", "shield", "earth", "steam", "arcane"], "an elemental ally", False),
    ("Corporealise", ["arcane", "steam", "lightning", "shield", "arcane"], "makes Assatur touchable", False),
    ("Vortex", ["ice", "arcane", "ice", "shield", "ice"], "a hungry vortex", False),
    ("Meteor Shower", ["fire", "earth", "steam", "earth", "fire"], "meteors, everywhere", True),
    ("Crash To Desktop", ["lightning", "lightning", "fire", "life"], "the instant-kill joke", True),
    ("Napalm", ["steam", "earth", "life", "fire", "fire"], "phantom airstrike", True),
    ("Portal", ["steam", "lightning", "shield"], "a blue and an orange portal", True),
    ("Tractor Pull", ["earth", "arcane"], "pulls instead of pushes", True),
    ("Propp's Party Plasma", ["fire", "steam", "arcane"], "arcane fire spray", True),
    ("Levitation", ["steam", "arcane", "steam"], "float over ground and water", True),
    ("Chain Lightning", ["lightning", "lightning", "lightning"], "longer, meaner lightning", True),
]
print(f"{len(ELEMS)} elements, {len(MAGICKS)} magicks "
      f"({sum(1 for m in MAGICKS if not m[3])} vanilla + {sum(1 for m in MAGICKS if m[3])} dlc)")

def keys_of(seq):
    return "-".join(E[s]["key"] for s in seq)

# magick placement: even ring order, ranked by recipe centroid angle
prefs = []
for i, (name, seq, eff, dlc) in enumerate(MAGICKS):
    vx = sum(math.cos(EANG[s]) for s in set(seq))
    vy = sum(math.sin(EANG[s]) for s in set(seq))
    prefs.append((math.atan2(vy, vx), i))
prefs.sort()
MPOS = {}
for rank, (_a, i) in enumerate(prefs):
    a = 2 * math.pi * rank / len(MAGICKS) - math.pi / 2
    MPOS[i] = (CX + 585 * math.cos(a), CY + 400 * math.sin(a), a)

def spos(sid):
    anchor = next(s[3] for s in STATUSES if s[0] == sid)
    a = EANG[anchor]
    return CX + 330 * math.cos(a) + (40 if sid == "frozen" else 0), CY + 258 * math.sin(a)

# ---------------------------------------------------------------- svg
sv = [f'<rect width="{W}" height="{H}" fill="{SURFACE}" rx="14"/>']
sv.append(f'<ellipse cx="{CX}" cy="{CY}" rx="205" ry="165" fill="none" stroke="#2A2734" stroke-width="1.5" stroke-dasharray="3 6"/>')
sv.append(f'<ellipse cx="{CX}" cy="{CY}" rx="205" ry="165" fill="#9B7BE8" opacity="0.04" filter="url(#blur)"/>')
sv.append(f'<text x="{CX}" y="{CY - 8:.0f}" text-anchor="middle" fill="#6b6880" '
          f'font-family="Cinzel,Georgia,serif" font-size="15" letter-spacing="3">THE ELEMENTS</text>')
sv.append(f'<text x="{CX}" y="{CY + 14:.0f}" text-anchor="middle" fill="#4a4758" '
          f'font-family="IBM Plex Mono,monospace" font-size="10.5" letter-spacing="1">queue five · cast · repeat</text>')

def line(x1, y1, x2, y2, col, cls, dash=False, op=0.30, wd=1.5, marker=None):
    d = ' stroke-dasharray="5 4"' if dash else ""
    m = f' marker-end="url(#m{col.lstrip("#")})"' if marker else ""
    return (f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{col}" '
            f'stroke-opacity="{op}" stroke-width="{wd}"{d}{m} class="{cls}"/>')

def shrink(x1, y1, x2, y2, r1, r2):
    dx, dy = x2 - x1, y2 - y1
    d = math.sqrt(dx * dx + dy * dy) or 1
    ux, uy = dx / d, dy / d
    return x1 + ux * r1, y1 + uy * r1, x2 - ux * r2, y2 - uy * r2

# magick -> element edges (under everything)
for i, (name, seq, eff, dlc) in enumerate(MAGICKS):
    mx, my, _a = MPOS[i]
    for eid in dict.fromkeys(seq):
        ex, ey = epos(eid)
        x1, y1, x2, y2 = shrink(mx, my, ex, ey, 14, 30)
        sv.append(line(x1, y1, x2, y2, E[eid]["color"],
                       f'e t-magick{" t-dlc" if dlc else ""} mk{i} el-{eid}', op=0.10, wd=1.2))

# cancel chords / downgrades / combines
for a, b, why in CANCELS:
    ax, ay = epos(a); bx, by = epos(b)
    x1, y1, x2, y2 = shrink(ax, ay, bx, by, 30, 30)
    sv.append(line(x1, y1, x2, y2, "#D9463E", f'e t-cancel el-{a} el-{b}', dash=True, op=0.35, wd=1.6))
for a, b, why in DOWNGRADES:
    ax, ay = epos(a); bx, by = epos(b)
    x1, y1, x2, y2 = shrink(ax, ay, bx, by, 30, 30)
    sv.append(line(x1, y1, x2, y2, "#8a879a", f'e t-cancel el-{a} el-{b}', dash=True, op=0.30, wd=1.3))
for a, b, hyb, why in COMBINES:
    for src in (a, b):
        ax, ay = epos(src); hx, hy = epos(hyb)
        x1, y1, x2, y2 = shrink(ax, ay, hx, hy, 30, 30)
        sv.append(line(x1, y1, x2, y2, E[hyb]["color"], f'e t-combine el-{src} el-{hyb}',
                       op=0.55, wd=2.2, marker=True))

# status hook edges
for a, b, d, col, dash in STATUS_EDGES:
    ax, ay = spos(a) if a in ("wet", "burning", "frozen") else epos(a)
    bx, by = spos(b) if b in ("wet", "burning", "frozen") else epos(b)
    r1 = 24 if a in ("wet", "burning", "frozen") else 30
    r2 = 24 if b in ("wet", "burning", "frozen") else 30
    x1, y1, x2, y2 = shrink(ax, ay, bx, by, r1, r2)
    sv.append(line(x1, y1, x2, y2, col, f'e t-status el-{a} el-{b}', dash=dash, op=0.5, wd=1.8, marker=True))

# element nodes
for eid, name, key, col, glyph in ELEMS:
    x, y = epos(eid)
    hyb = eid in ("steam", "ice")
    sub = {"water": "wets targets · combines up and down the ring",
           "life": "heals — the co-op beam; cancels arcane",
           "shield": "walls, mines, storms — never stacks",
           "cold": "chills and freezes the wet",
           "ice": "hybrid (Q+R): shard projectiles; melts to water under fire",
           "steam": "hybrid (Q+F): scalds — and carries lightning where water can't",
           "fire": "ignites; dries the wet; melts the frozen",
           "earth": "boulders — shatters the frozen",
           "lightning": "arcs and chains; loves wet targets, hates wet casters",
           "arcane": "the red beam; cancels life"}[eid]
    sv.append(f'<g class="n el" data-id="{eid}" data-name="{name} ({key})" data-sub="{sub}">')
    sv.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="27" fill="{SURFACE}" stroke="{col}" '
              f'stroke-width="{2.2 if hyb else 3}"{" stroke-dasharray=" + chr(34) + "5 3" + chr(34) if hyb else ""}/>')
    sv.append(f'<text x="{x:.0f}" y="{y + 7:.0f}" text-anchor="middle" font-size="20" class="femoji" '
              f'fill="{col}">{glyph}</text>')
    ly = y + 46 if y >= CY else y - 36
    sv.append(f'<text x="{x:.0f}" y="{ly:.0f}" text-anchor="middle" fill="{col}" '
              f'font-family="IBM Plex Mono,monospace" font-size="11.5" font-weight="600" letter-spacing="1.5" '
              f'stroke="{SURFACE}" stroke-width="5" paint-order="stroke">{name.upper()} <tspan '
              f'fill="#6b6880">{key}</tspan></text>')
    sv.append('</g>')

# status nodes (diamonds)
for sid, lab, col, anchor, sub in STATUSES:
    x, y = spos(sid)
    sv.append(f'<g class="n st" data-id="{sid}" data-name="{lab.title()}" data-sub="{sub}">')
    sv.append(f'<rect x="{x - 17:.0f}" y="{y - 17:.0f}" width="34" height="34" rx="6" '
              f'transform="rotate(45 {x:.0f} {y:.0f})" fill="{SURFACE}" stroke="{col}" stroke-width="2.4"/>')
    sv.append(f'<text x="{x:.0f}" y="{y + 4:.0f}" text-anchor="middle" fill="{col}" '
              f'font-family="IBM Plex Mono,monospace" font-size="9.5" font-weight="600" letter-spacing="1">{lab}</text>')
    sv.append('</g>')

# magick nodes: sequence dots on the ring point, label pushed outward
for i, (name, seq, eff, dlc) in enumerate(MAGICKS):
    mx, my, a = MPOS[i]
    ca = math.cos(a)
    anchor = "start" if ca > 0.30 else ("end" if ca < -0.30 else "middle")
    lx = mx + (14 if anchor == "start" else -14 if anchor == "end" else 0)
    ly = my + (24 if abs(ca) <= 0.30 and math.sin(a) > 0 else -16 if abs(ca) <= 0.30 else 4)
    dots = ""
    dw = 11
    x0 = mx - dw * (len(seq) - 1) / 2
    for k, eid in enumerate(seq):
        dots += (f'<circle cx="{x0 + k * dw:.0f}" cy="{my:.0f}" r="4.2" fill="{E[eid]["color"]}" '
                 f'stroke="{SURFACE}" stroke-width="1"/>')
    sv.append(f'<g class="n mk{" dlcn" if dlc else ""}" data-i="{i}" data-name="{name}" '
              f'data-sub="{keys_of(seq)} · {" + ".join(E[s]["name"] for s in seq)} — {eff}'
              f'{" · DLC" if dlc else ""}">')
    sv.append(dots)
    sv.append(f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anchor}" fill="#C9C6D4" '
              f'font-family="IBM Plex Mono,monospace" font-size="11.5"'
              f'{" font-style=" + chr(34) + "italic" + chr(34) if dlc else ""} '
              f'stroke="{SURFACE}" stroke-width="4" paint-order="stroke">{name}</text>')
    sv.append('</g>')
SVG = "\n".join(sv)

colors = sorted({E[c[2]]["color"] for c in COMBINES} | {e[3] for e in STATUS_EDGES})
markers = "".join(
    f'<marker id="m{c.lstrip("#")}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5.5" '
    f'markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" fill="{c}"/></marker>'
    for c in colors)

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

legend = (
    '<button class="pchip lc on" data-k="combine"><span class="dot" style="background:#C8CBD9"></span>combines</button>'
    '<button class="pchip lc on" data-k="cancel"><span class="dot" style="background:#D9463E"></span>cancels</button>'
    '<button class="pchip lc on" data-k="status"><span class="dot" style="background:#3D7BD9"></span>statuses</button>'
    '<button class="pchip lc on" data-k="magick"><span class="dot" style="background:#E3C377"></span>magick recipes</button>'
    '<button class="pchip lc on" data-k="dlc"><span class="dot" style="background:#6b6880"></span>dlc</button>')

HTML = f"""<title>Magicka Chemistry</title>
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
.n{{cursor:pointer}}
svg.hov .n{{opacity:.14}}
svg.hov .n.hl{{opacity:1}}
svg.hov line.e{{opacity:.04}}
svg.hov line.e.hl{{stroke-opacity:.95;opacity:1;stroke-width:2.2}}
line.e.offch{{display:none}}
.n.offn{{display:none}}
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
    <div><h1>Magicka Chemistry</h1>
    <div class="sub">{len(ELEMS)} elements · {len(MAGICKS)} magicks · the whole combat system is the
combo system — queue elements, and the chemistry <em>is</em> the spell</div></div>
    <div class="segrow">
      {FSC}
      <button id="copybtn" class="pchip" title="Copy the current view as a PNG image">⧉ copy image</button>
    </div>
  </div>
  <div class="legend">{legend}
    <button class="pchip" id="allch">all</button></div>
</header>
<div class="wrap">
  <svg viewBox="0 0 {W} {H}" role="img" aria-label="Magicka's element wheel, status chemistry, and magick recipes">
  <defs><filter id="blur"><feGaussianBlur stdDeviation="26"/></filter>{markers}</defs>
  {SVG}</svg>
  <div id="tip"></div>
</div>
<footer>hover an element to light every recipe and reaction it joins · hover a magick to read its queue ·
sequence dots on each magick <em>are</em> the recipe, in casting order · dashed red chords cancel ·
solid arrows combine (water+cold=ice, water+fire=steam) · diamonds are the statuses: wet doubles
lightning and freezes under cold; frozen shatters to earth; wet douses burning — and a wet wizard
casting lightning zaps themself · sources:
<a href="https://magicka.fandom.com/wiki/Magicks_(Magicka_1)">Magickapedia</a> ·
<a href="https://strategywiki.org/wiki/Magicka/Elements">StrategyWiki</a> ·
<a href="https://kingtoko.com/2011/01/29/magicka-magicks-guide/">kingtoko's guide</a> ·
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
svg.querySelectorAll('.n').forEach(n => {{
  n.addEventListener('mouseenter', () => {{
    svg.classList.add('hov');
    n.classList.add('hl');
    if (n.dataset.i !== undefined) {{
      svg.querySelectorAll('line.e.mk' + n.dataset.i).forEach(l => {{
        if (l.classList.contains('offch')) return;
        l.classList.add('hl');
        [...l.classList].filter(c => c.indexOf('el-') === 0).forEach(c => {{
          const en = svg.querySelector('.n[data-id="' + c.slice(3) + '"]');
          if (en) en.classList.add('hl');
        }});
      }});
    }} else {{
      svg.querySelectorAll('line.e.el-' + n.dataset.id).forEach(l => {{
        if (l.classList.contains('offch')) return;
        l.classList.add('hl');
        [...l.classList].forEach(c => {{
          if (c.indexOf('el-') === 0 && c.slice(3) !== n.dataset.id) {{
            const en = svg.querySelector('.n[data-id="' + c.slice(3) + '"]');
            if (en) en.classList.add('hl');
          }}
          if (c.indexOf('mk') === 0 && c !== 'mk') {{
            const mn = svg.querySelector('.n[data-i="' + c.slice(2) + '"]');
            if (mn) mn.classList.add('hl');
          }}
        }});
      }});
    }}
    showTip(n);
  }});
  n.addEventListener('mousemove', moveTip);
  n.addEventListener('mouseleave', clearHl);
}});
const KINDS = ['combine', 'cancel', 'status', 'magick', 'dlc'];
const chs = new Set(KINDS);
function applyCh() {{
  svg.querySelectorAll('line.e').forEach(l => {{
    const kinds = [...l.classList].filter(c => c.indexOf('t-') === 0).map(c => c.slice(2));
    let off = !kinds.some(k => chs.has(k));
    if (kinds.includes('dlc') && !chs.has('dlc')) off = true;
    if (kinds.includes('magick') && !chs.has('magick')) off = true;
    l.classList.toggle('offch', off);
  }});
  svg.querySelectorAll('.n.dlcn').forEach(n => n.classList.toggle('offn', !chs.has('dlc') || !chs.has('magick')));
  svg.querySelectorAll('.n.mk:not(.dlcn)').forEach(n => n.classList.toggle('offn', !chs.has('magick')));
  document.querySelectorAll('.lc').forEach(b => b.classList.toggle('on', chs.has(b.dataset.k)));
}}
document.querySelectorAll('.lc').forEach(b => b.addEventListener('click', () => {{
  if (chs.size === KINDS.length) {{ chs.clear(); chs.add(b.dataset.k);
    if (b.dataset.k === 'dlc') chs.add('magick'); }}
  else if (chs.has(b.dataset.k)) {{ chs.delete(b.dataset.k); if (!chs.size) KINDS.forEach(k => chs.add(k)); }}
  else chs.add(b.dataset.k);
  applyCh();
}}));
document.getElementById('allch').addEventListener('click', () => {{
  KINDS.forEach(k => chs.add(k));
  applyCh();
}});
async function exportPNG() {{
  const clone = svg.cloneNode(true);
  clone.querySelectorAll('line.e.offch,.n.offn').forEach(l => l.remove());
  clone.querySelectorAll('.hl').forEach(x => x.classList.remove('hl'));
  const xml = new XMLSerializer().serializeToString(clone);
  const url = URL.createObjectURL(new Blob([xml], {{type: 'image/svg+xml'}}));
  const img = new Image();
  await new Promise((res, rej) => {{ img.onload = res; img.onerror = rej; img.src = url; }});
  const c = document.createElement('canvas');
  c.width = 3000; c.height = 1960;
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
MTABS = '<style>\n.mtabs{display:flex;border:1px solid #3a3647;border-radius:7px;overflow:hidden;align-self:flex-start}\n.mtabs a{color:#A7A4B3;font:500 11px "IBM Plex Mono",monospace;letter-spacing:.08em;\n  padding:5px 12px;text-decoration:none;cursor:pointer}\n.mtabs a + a{border-left:1px solid #3a3647}\n.mtabs a.on{background:#D4AF5E1f;color:#E3C377;cursor:default}\n.mtabs a:not(.on):hover{color:#E8E6EF}\n.mtabs a:focus-visible{outline:2px solid #E3C377;outline-offset:-2px}\n</style>\n<div class="mtabs" role="navigation" aria-label="Magicka views">\n  <a data-p="wheel">ELEMENT WHEEL</a>\n  <a data-p="tree">CASTING TREE</a>\n  <a data-p="hooks">HOOKS</a>\n</div>\n'
MTABS_JS = "\n<script>\n(function () {\n  var CUR = 'wheel';\n  var ART = {wheel: 'https://claude.ai/code/artifact/7d834068-95da-4943-b7d7-36d02a28f3f5',\n             tree: 'https://claude.ai/code/artifact/d453af2e-2023-45f0-917e-07a3c016d68a',\n             hooks: 'https://claude.ai/code/artifact/2b477318-74aa-4c89-92fd-5b8371d0da51'};\n  var DOCS = {wheel: 'magicka-chemistry.html', tree: 'magicka-casting-tree.html', hooks: 'magicka-hooks.html'};\n  var LOCAL = {wheel: 'magicka_map.html', tree: 'magicka_tree.html', hooks: 'magicka_hooks.html'};\n  var path = location.pathname.split('/').pop();\n  var map = location.hostname.indexOf('claude') !== -1 ? ART\n          : (path.indexOf('_') !== -1 ? LOCAL : DOCS);\n  document.querySelectorAll('.mtabs a').forEach(function (a) {\n    var p = a.getAttribute('data-p');\n    if (p === CUR) { a.classList.add('on'); return; }\n    a.href = map[p];\n  });\n})();\n</script>\n"
_mt_style, _mt_div = MTABS.split('</style>\n', 1)
_mt_style += '</style>\n'
HTML = HTML.replace('<div class="segrow">', _mt_style + '<div class="segrow">' + _mt_div, 1)
HTML += MTABS_JS
with open("magicka_map.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"magicka_map.html: {os.path.getsize('magicka_map.html') / 1024:.0f} KB")

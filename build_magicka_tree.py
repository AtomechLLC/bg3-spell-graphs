"""Magicka Casting Tree: recipes traversed in casting order -> magicka_tree.html.

A radial prefix tree of every magick recipe: the center is the empty
queue, each ring is one more queued element, and recipes that share an
opening share a path (Nullify S-E is literally the trunk Invisibility
and Summon Elemental grow from). Repeats read as straight radial runs -
Chain Lightning is A-A-A in a line.
"""
import json
import math
import os

W, H = 1500, 1010
CX, CY = W / 2, 505
SURFACE = "#16161D"

ELEMS = [
    ("life", "Life", "W", "#4FC46F"),
    ("shield", "Shield", "E", "#E8D44D"),
    ("cold", "Cold", "R", "#A8DCE8"),
    ("ice", "Ice", "QR", "#7FC4E8"),
    ("water", "Water", "Q", "#3D7BD9"),
    ("steam", "Steam", "QF", "#C8CBD9"),
    ("fire", "Fire", "F", "#E87A2D"),
    ("earth", "Earth", "D", "#8C6844"),
    ("lightning", "Lightning", "A", "#9B7BE8"),
    ("arcane", "Arcane", "S", "#D9463E"),
]
E = {e[0]: dict(zip(("id", "name", "key", "color"), e)) for e in ELEMS}
ORDER = {e[0]: i for i, e in enumerate(ELEMS)}

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

# mono-element stacks: (element, max repeats, what the full stack casts)
STACKS = [
    ("water", 5, "a fire-hose that soaks and shoves"),
    ("life", 5, "the heal beam at full strength"),
    ("shield", 1, "one barrier — a second E cancels the first"),
    ("cold", 5, "a wide, deep chill"),
    ("ice", 2, "a heavy shard volley (two hybrids fill four slots)"),
    ("steam", 2, "a scalding blast (two hybrids fill four slots)"),
    ("fire", 5, "a broad flamethrower"),
    ("earth", 5, "the boulder — one rock, maximum caliber"),
    ("lightning", 5, "the hardest arc (never while wet)"),
    ("arcane", 5, "the disintegrating beam at full power"),
]

# ---------------------------------------------------------------- trie
NODES = [dict(id=0, elem=None, depth=0, parent=None, children=[], magick=None, dlc=False, stack=False)]
def insert(seq, name, eff, dlc, stack=False):
    cur = 0
    for eid in seq:
        nxt = next((c for c in NODES[cur]["children"] if NODES[c]["elem"] == eid), None)
        if nxt is None:
            nxt = len(NODES)
            NODES.append(dict(id=nxt, elem=eid, depth=NODES[cur]["depth"] + 1,
                              parent=cur, children=[], magick=None, dlc=False, stack=False))
            NODES[cur]["children"].append(nxt)
        cur = nxt
    NODES[cur]["magick"] = (name, eff)
    NODES[cur]["dlc"] = dlc
    NODES[cur]["stack"] = stack

for name, seq, eff, dlc in MAGICKS:
    insert(seq, name, eff, dlc)
for eid, mx, eff in STACKS:
    insert([eid] * mx, f"{E[eid]['name']} ×{mx}", eff, False, stack=True)

def sort_rec(nid):
    NODES[nid]["children"].sort(key=lambda c: ORDER[NODES[c]["elem"]])
    for c in NODES[nid]["children"]:
        sort_rec(c)
sort_rec(0)

print(f"{len(MAGICKS)} recipes + {len(STACKS)} element stacks -> {len(NODES) - 1} trie nodes "
      f"(vs {sum(len(m[1]) for m in MAGICKS) + sum(s[1] for s in STACKS)} raw steps: shared openings merge)")

# leaf slots: terminals count as leaves for spacing when childless
leaves = [n["id"] for n in NODES[1:] if not n["children"]]
ANG = {}
for i, nid in enumerate(leaves):
    ANG[nid] = 2 * math.pi * i / len(leaves) - math.pi / 2
def set_ang(nid):
    n = NODES[nid]
    if nid in ANG:
        return ANG[nid]
    a = [set_ang(c) for c in n["children"]]
    # circular mean is safe here: children of one parent stay in one sector
    ANG[nid] = math.atan2(sum(math.sin(x) for x in a), sum(math.cos(x) for x in a))
    return ANG[nid]
set_ang(0)

RX = [0, 120, 216, 312, 408, 504]

# per-ring minimum angular separation so nodes never overlap
for d in range(1, 6):
    ring = sorted((n["id"] for n in NODES[1:] if n["depth"] == d), key=lambda i: ANG[i])
    if len(ring) < 2:
        continue
    mingap = 40 / (RX[d] * 0.88)
    base = ANG[ring[0]]
    xs = [(ANG[i] - base) % (2 * math.pi) for i in ring]
    for i in range(1, len(xs)):
        xs[i] = max(xs[i], xs[i - 1] + mingap)
    span = 2 * math.pi - mingap
    if xs[-1] > span:
        xs = [x * span / xs[-1] for x in xs]
    for i, nid in enumerate(ring):
        ANG[nid] = base + xs[i]
def pos(nid):
    n = NODES[nid]
    if n["depth"] == 0:
        return CX, CY
    a = ANG[nid]
    return CX + RX[n["depth"]] * math.cos(a), CY + RX[n["depth"]] * 0.80 * math.sin(a)

def desc(nid):
    out = [nid]
    for c in NODES[nid]["children"]:
        out += desc(c)
    return out
def anc(nid):
    out = []
    while nid is not None:
        out.append(nid)
        nid = NODES[nid]["parent"]
    return out
def prefix_keys(nid):
    ks = []
    for a in reversed(anc(nid)):
        if NODES[a]["elem"]:
            ks.append(E[NODES[a]["elem"]]["key"])
    return "-".join(ks)
def magicks_below(nid):
    return [NODES[d]["magick"][0] for d in desc(nid) if NODES[d]["magick"]]

# ---------------------------------------------------------------- svg
sv = [f'<rect width="{W}" height="{H}" fill="{SURFACE}" rx="14"/>']
for d in range(1, 6):
    sv.append(f'<ellipse cx="{CX}" cy="{CY}" rx="{RX[d]}" ry="{RX[d] * 0.80:.0f}" fill="none" '
              f'stroke="#23202C" stroke-width="1" stroke-dasharray="2 7"/>')
    sv.append(f'<text x="{CX + 6:.0f}" y="{CY - RX[d] * 0.80 + 14:.0f}" fill="#4a4758" '
              f'font-family="IBM Plex Mono,monospace" font-size="10">{d}{"st" if d == 1 else "nd" if d == 2 else "rd" if d == 3 else "th"}</text>')

for n in NODES[1:]:
    px, py = pos(n["parent"])
    x, y = pos(n["id"])
    col = E[n["elem"]]["color"]
    sv.append(f'<line x1="{px:.0f}" y1="{py:.0f}" x2="{x:.0f}" y2="{y:.0f}" stroke="{col}" '
              f'stroke-opacity="0.35" stroke-width="2" class="e c{n["id"]}"/>')

sv.append(f'<circle cx="{CX}" cy="{CY}" r="26" fill="{SURFACE}" stroke="#6b6880" stroke-width="2"/>')
sv.append(f'<text x="{CX}" y="{CY + 4:.0f}" text-anchor="middle" fill="#8a879a" '
          f'font-family="Cinzel,Georgia,serif" font-size="12" letter-spacing="1">CAST</text>')

for n in NODES[1:]:
    x, y = pos(n["id"])
    col = E[n["elem"]]["color"]
    term = n["magick"] is not None
    mags = magicks_below(n["id"])
    sub = (f'{prefix_keys(n["id"])} · ' +
           (f'{n["magick"][0]} — {n["magick"][1]}' if term and not n["children"] else
            f'{n["magick"][0]} casts here; ' + str(len(mags) - 1) + " more continue" if term else
            f'{len(mags)} magick{"s" if len(mags) != 1 else ""} pass through: ' + ", ".join(mags[:5]) +
            ("…" if len(mags) > 5 else "")))
    sv.append(f'<g class="n" data-id="{n["id"]}" data-anc="|{"|".join(map(str, anc(n["id"])))}|" '
              f'data-desc="|{"|".join(map(str, desc(n["id"])))}|" '
              f'data-name="{E[n["elem"]]["name"]}" data-sub="{sub}">')
    r = 12 if len(E[n["elem"]]["key"]) == 1 else 13.5
    ring = ' stroke-dasharray="4 2.5"' if len(E[n["elem"]]["key"]) > 1 else ""
    sv.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{SURFACE}" stroke="{col}" stroke-width="2.4"{ring}/>')
    if term:
        sv.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r + 5}" fill="none" stroke="{col}" '
                  f'stroke-width="1" stroke-opacity="0.7"/>')
    sv.append(f'<text x="{x:.0f}" y="{y + 4:.0f}" text-anchor="middle" fill="{col}" '
              f'font-family="IBM Plex Mono,monospace" font-size="{11 if r == 12 else 9.5}" '
              f'font-weight="600">{E[n["elem"]]["key"]}</text>')
    sv.append('</g>')

placed = []
def label_box(lx, ly, anchor, text):
    w = 7.2 * len(text)
    x0 = lx - (w if anchor == "end" else w / 2 if anchor == "middle" else 0)
    return (x0, ly - 12, x0 + w, ly + 3)

def collides(box):
    return any(box[0] < p[2] and p[0] < box[2] and box[1] < p[3] and p[1] < box[3]
               for p in placed)

for n in NODES[1:]:
    if not n["magick"]:
        continue
    x, y = pos(n["id"])
    a = ANG[n["id"]]
    ca = math.cos(a)
    if n["children"]:                     # terminal with continuations: tag beside the node
        lx, ly, anchor = x, y - 22, "middle"
    else:
        lx = x + 24 * ca * 1.35
        ly = y + 24 * 0.85 * math.sin(a) + 4
        anchor = "start" if ca > 0.30 else ("end" if ca < -0.30 else "middle")
        if anchor == "middle":
            ly = y + (30 if math.sin(a) > 0 else -24)
    for _try in range(4):                 # push outward along the ray until clear
        if not collides(label_box(lx, ly, anchor, n["magick"][0])):
            break
        lx += 16 * ca
        ly += 15 * (1 if math.sin(a) >= 0 else -1) * abs(math.sin(a)) + (14 if abs(ca) < 0.3 and math.sin(a) >= 0 else -14 if abs(ca) < 0.3 else 0)
    placed.append(label_box(lx, ly, anchor, n["magick"][0]))
    lcol = E[n["elem"]]["color"] if n["stack"] else "#C9C6D4"
    sv.append(f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anchor}" fill="{lcol}" '
              f'font-family="IBM Plex Mono,monospace" font-size="12"'
              f'{" font-style=" + chr(34) + "italic" + chr(34) if n["dlc"] else ""} '
              f'stroke="{SURFACE}" stroke-width="4" paint-order="stroke" class="ml m{n["id"]}" '
              f'data-for="{n["id"]}">{n["magick"][0]}</text>')
SVG = "\n".join(sv)

legend = "".join(
    f'<span class="pchip lk"><span class="dot" style="background:{c}"></span>{k} {nm.lower()}</span>'
    for _i, nm, k, c in ELEMS)

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

HTML = f"""<title>Magicka Casting Tree</title>
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
.legend{{display:flex;gap:6px;flex-wrap:wrap;align-items:center}}
.pchip{{background:transparent;border:1px solid #3a3647;border-radius:999px;color:#C9C6D4;
  font:500 11px "IBM Plex Mono",monospace;padding:3px 11px;letter-spacing:.05em;
  display:inline-flex;align-items:center;gap:6px}}
.pchip.lk{{cursor:default;padding:2px 9px}}
button.pchip{{cursor:pointer}}
button.pchip:hover{{border-color:#6b6880}}
.dot{{width:10px;height:10px;border-radius:50%;display:inline-block}}
.segrow{{margin-left:auto;display:flex;align-items:center;gap:10px}}
#copybtn.ok{{border-color:#5fbf83;color:#7fdfa3}}
#copybtn.err{{border-color:#e58a9b;color:#e58a9b}}
.wrap{{width:100%;max-width:1500px;position:relative}}
svg{{width:100%;height:auto;display:block}}
.n,.ml{{cursor:pointer}}
svg.hov .n,svg.hov .ml{{opacity:.13}}
svg.hov .n.hl,svg.hov .ml.hl{{opacity:1}}
svg.hov line.e{{opacity:.05}}
svg.hov line.e.hl{{stroke-opacity:.95;opacity:1;stroke-width:3}}
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
    <div><h1>Magicka Casting Tree</h1>
    <div class="sub">every magick traversed in casting order — the centre is the empty queue, each ring
one more element · magicks share trunks with each other and with the plain element stacks · type below to test a queue</div></div>
    <div class="segrow">
      {FSC}
      <button id="copybtn" class="pchip" title="Copy the tree as a PNG image">⧉ copy image</button>
    </div>
  </div>
  <div class="legend">{legend}</div>
</header>
<div class="wrap">
  <svg viewBox="0 0 {W} {H}" role="img" aria-label="Radial prefix tree of Magicka recipes in casting order">
  {SVG}</svg>
  <div id="tip"></div>
</div>
<footer>hover any step to light the path in from CAST and everything that grows out of it ·
hover a name to trace its whole recipe · a double ring marks a spot where a magick casts mid-branch (release at S-E for Nullify, keep queuing for Invisibility; Chain Lightning sits three steps down the Lightning ×5 run) · colored end-labels are the mono-element stacks — Shield stops at one because a second E cancels the first ·
dashed rings are the hybrids (QF steam, QR ice) · read the trunks: S-E is the ritual opening three
magicks share, A-S forks into Haste and Teleport, and Chain Lightning is A-A-A straight out ·
recipes from <a href="https://magicka.fandom.com/wiki/Magicks_(Magicka_1)">Magickapedia</a> and
<a href="https://kingtoko.com/2011/01/29/magicka-magicks-guide/">kingtoko's guide</a>, roster
cross-checked against a local install's Magick effect data (which also lists item- and boss-granted
magicks — Earthquake, Polymorph, Grow, Shrink, Etherealize — that have no element queue and so no
branch here) · Magicka © Arrowhead Game Studios / Paradox Interactive</footer>
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
function light(ids) {{
  svg.classList.add('hov');
  ids.forEach(id => {{
    const nn = svg.querySelector('.n[data-id="' + id + '"]');
    if (nn) nn.classList.add('hl');
    svg.querySelectorAll('line.e.c' + id).forEach(l => l.classList.add('hl'));
    const ml = svg.querySelector('.ml.m' + id);
    if (ml) ml.classList.add('hl');
  }});
}}
svg.querySelectorAll('.n').forEach(n => {{
  n.addEventListener('mouseenter', () => {{
    const ids = (n.dataset.anc + n.dataset.desc).split('|').filter(Boolean);
    light([...new Set(ids)]);
    tip.innerHTML = '<b></b><span></span>';
    tip.firstChild.textContent = n.dataset.name;
    tip.lastChild.textContent = n.dataset.sub;
    tip.style.display = 'block';
  }});
  n.addEventListener('mousemove', moveTip);
  n.addEventListener('mouseleave', clearHl);
}});
svg.querySelectorAll('.ml').forEach(ml => {{
  ml.addEventListener('mouseenter', () => {{
    const n = svg.querySelector('.n[data-id="' + ml.dataset.for + '"]');
    light(n.dataset.anc.split('|').filter(Boolean));
    tip.innerHTML = '<b></b><span></span>';
    tip.firstChild.textContent = ml.textContent;
    tip.lastChild.textContent = n.dataset.sub;
    tip.style.display = 'block';
  }});
  ml.addEventListener('mousemove', moveTip);
  ml.addEventListener('mouseleave', clearHl);
}});
async function exportPNG() {{
  const clone = svg.cloneNode(true);
  clone.querySelectorAll('.hl').forEach(x => x.classList.remove('hl'));
  const xml = new XMLSerializer().serializeToString(clone);
  const url = URL.createObjectURL(new Blob([xml], {{type: 'image/svg+xml'}}));
  const img = new Image();
  await new Promise((res, rej) => {{ img.onload = res; img.onerror = rej; img.src = url; }});
  const c = document.createElement('canvas');
  c.width = 3000; c.height = 2020;
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


# ---------------------------------------------------------------- sequence builder
TRIE_JS = {str(n["id"]): {"e": n["elem"],
                          "c": {NODES[c]["elem"]: c for c in n["children"]},
                          "m": list(n["magick"]) if n["magick"] else None,
                          "s": n["stack"], "d": n["dlc"]}
           for n in NODES}
EINFO_JS = {e[0]: {"n": e[1], "k": e[2], "col": e[3]} for e in ELEMS}
KEYMAP_JS = {"q": "water", "w": "life", "e": "shield", "r": "cold",
             "a": "lightning", "s": "arcane", "d": "earth", "f": "fire"}

BUILDER_CSS = """
<style>
#builder{width:100%;max-width:1500px;margin:12px 0 0;background:#15131C;border:1px solid #2A2734;
  border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:10px}
.brow1{display:flex;gap:16px;align-items:center;flex-wrap:wrap}
#slots{display:flex;gap:7px}
.slot{width:46px;height:46px;border-radius:9px;border:1.5px dashed #3a3647;display:flex;
  align-items:center;justify-content:center;font:600 15px "IBM Plex Mono",monospace;color:#6b6880;
  background:#101016}
.slot.f{border-style:solid;color:var(--sc);border-color:var(--sc);
  box-shadow:inset 0 0 10px color-mix(in srgb,var(--sc) 22%,transparent)}
#rline{font-size:12px;color:#A7A4B3;line-height:1.7;min-height:20px}
#rline b{color:#E3C377}
#rline .cast{color:#7fdfa3;font-weight:600}
#rline .stackr{font-weight:600}
#rline kbd{border:1px solid #3a3647;border-bottom-width:2px;border-radius:4px;padding:0 5px;
  font:500 10.5px "IBM Plex Mono",monospace;background:#211E2B;margin:0 1px}
.brow2{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.eb{border:1px solid #3a3647;border-radius:8px;background:#101016;color:var(--sc);cursor:pointer;
  font:500 11.5px "IBM Plex Mono",monospace;padding:5px 10px;display:inline-flex;gap:7px;
  align-items:center;letter-spacing:.04em}
.eb:hover{border-color:var(--sc)}
.eb b{font-size:13px}
.eb:focus-visible{outline:2px solid #E3C377;outline-offset:1px}
#bclear{border:1px solid #3a3647;border-radius:8px;background:transparent;color:#C9C6D4;
  cursor:pointer;font:500 11px "IBM Plex Mono",monospace;padding:6px 11px;margin-left:auto}
#bclear:hover{border-color:#e58a9b;color:#e58a9b}
#builder.flash{animation:bfl .5s}
@keyframes bfl{0%{border-color:#7fdfa3}100%{border-color:#2A2734}}
@media (prefers-reduced-motion: reduce){#builder.flash{animation:none}}
svg.q .n{opacity:.13}
svg.q .n.ql{opacity:1}
svg.q .ml{opacity:.13}
svg.q .ml.ql{opacity:1}
svg.q line.e{opacity:.05}
svg.q line.e.ql{stroke-opacity:.95;opacity:1;stroke-width:3}
svg.q .n.qf{opacity:.55}
svg.q .ml.qf{opacity:.55}
svg.q line.e.qf{opacity:1;stroke-opacity:.42;stroke-width:2.2}
</style>
<div id="builder">
  <div class="brow1">
    <div id="slots"></div>
    <div id="rline"></div>
  </div>
  <div class="brow2" id="ebtns"><button id="bclear">&#10005; clear</button></div>
</div>
"""

BUILDER_JS = """
<script>
const TRIE = __TRIE__;
const EINFO = __EINFO__;
const KEYMAP = __KEYMAP__;
const OPP = {water: ['lightning'], lightning: ['water', 'earth'], earth: ['lightning'],
             fire: ['cold'], cold: ['fire'], life: ['arcane'], arcane: ['life'], shield: ['shield']};
const COMB = {'water|fire': 'steam', 'fire|water': 'steam', 'water|cold': 'ice', 'cold|water': 'ice'};
const DOWN = {'fire|ice': 'water', 'cold|steam': 'water'};
const Q = [];
const slotsEl = document.getElementById('slots');
const rline = document.getElementById('rline');
const builder = document.getElementById('builder');

const btnbar = document.getElementById('ebtns');
for (const k of ['q', 'w', 'e', 'r', 'a', 's', 'd', 'f']) {
  const eid = KEYMAP[k];
  const b = document.createElement('button');
  b.className = 'eb';
  b.style.setProperty('--sc', EINFO[eid].col);
  b.innerHTML = '<b>' + k.toUpperCase() + '</b>' + EINFO[eid].n.toLowerCase();
  b.addEventListener('click', () => { push(eid); b.blur(); });
  btnbar.insertBefore(b, document.getElementById('bclear'));
}
for (const h of ['steam', 'ice']) {
  const seq = h === 'steam' ? ['water', 'fire'] : ['water', 'cold'];
  const b = document.createElement('button');
  b.className = 'eb';
  b.style.setProperty('--sc', EINFO[h].col);
  b.innerHTML = '<b>' + EINFO[h].k + '</b>' + EINFO[h].n.toLowerCase();
  b.title = EINFO[h].n + ' = ' + seq.map(e => EINFO[e].k).join(' then ') + ' (two real presses)';
  b.addEventListener('click', () => { seq.forEach(e => pushInto(Q, e)); refresh(); b.blur(); });
  btnbar.insertBefore(b, document.getElementById('bclear'));
}
document.getElementById('bclear').addEventListener('click', () => { Q.length = 0; refresh(); });

function pushInto(arr, eid) {
  for (let i = arr.length - 1; i >= 0; i--) {
    const s = arr[i];
    if (DOWN[eid + '|' + s]) { arr[i] = DOWN[eid + '|' + s]; return arr; }
    if ((OPP[eid] || []).includes(s)) { arr.splice(i, 1); return arr; }
    if (COMB[eid + '|' + s]) { arr[i] = COMB[eid + '|' + s]; return arr; }
  }
  if (arr.length < 5) arr.push(eid);
  return arr;
}
function push(eid) { pushInto(Q, eid); refresh(); }

function walk(arr) {
  arr = arr || Q;
  let cur = '0';
  let ok = 0;
  for (const eid of arr) {
    const nxt = TRIE[cur].c[eid];
    if (nxt === undefined) return {node: cur, depth: ok, off: true};
    cur = String(nxt);
    ok++;
  }
  return {node: cur, depth: ok, off: false};
}

function refresh() {
  slotsEl.innerHTML = '';
  for (let i = 0; i < 5; i++) {
    const d = document.createElement('div');
    d.className = 'slot' + (Q[i] ? ' f' : '');
    if (Q[i]) { d.style.setProperty('--sc', EINFO[Q[i]].col); d.textContent = EINFO[Q[i]].k; }
    slotsEl.appendChild(d);
  }
  svg.querySelectorAll('.ql, .qf').forEach(x => x.classList.remove('ql', 'qf'));
  svg.classList.toggle('q', Q.length > 0);
  if (!Q.length) {
    rline.innerHTML = 'queue elements &mdash; <kbd>Q</kbd><kbd>W</kbd><kbd>E</kbd><kbd>R</kbd> ' +
      '<kbd>A</kbd><kbd>S</kbd><kbd>D</kbd><kbd>F</kbd> &middot; <kbd>&#9003;</kbd> undo &middot; ' +
      '<kbd>esc</kbd> clear &middot; opposites cancel, water mixes, and the tree lights your path';
    return;
  }
  const w = walk();
  let cur = w.node;
  const ids = [];
  let c2 = cur;
  while (c2 !== null && c2 !== undefined && c2 !== '0') {
    ids.push(c2);
    const p = [...Object.keys(TRIE)].find(k => Object.values(TRIE[k].c).map(String).includes(String(c2)));
    c2 = p === '0' ? null : p;
  }
  ids.forEach(id => {
    const nn = svg.querySelector('.n[data-id="' + id + '"]');
    if (nn) nn.classList.add('ql');
    svg.querySelectorAll('line.e.c' + id).forEach(l => l.classList.add('ql'));
    const ml = svg.querySelector('.ml.m' + id);
    if (ml) ml.classList.add('ql');
  });
  if (!w.off) {                       // half-light every still-viable continuation
    const fut = [];
    (function rec(k) {
      Object.values(TRIE[k].c).forEach(c => { fut.push(String(c)); rec(String(c)); });
    })(String(w.node));
    fut.forEach(id => {
      const nn = svg.querySelector('.n[data-id="' + id + '"]');
      if (nn && !nn.classList.contains('ql')) nn.classList.add('qf');
      svg.querySelectorAll('line.e.c' + id).forEach(l => {
        if (!l.classList.contains('ql')) l.classList.add('qf');
      });
      const ml = svg.querySelector('.ml.m' + id);
      if (ml && !ml.classList.contains('ql')) ml.classList.add('qf');
    });
  }
  const keys = Q.map(e => EINFO[e].k).join('-');
  const node = TRIE[w.node];
  let html = '<b>' + keys + '</b> &middot; ';
  if (w.off) {
    const recov = [];
    for (const k of ['q', 'w', 'e', 'r', 'a', 's', 'd', 'f']) {
      const tw = walk(pushInto(Q.slice(), KEYMAP[k]));
      if (!tw.off && (TRIE[tw.node].m || magicksBelow(tw.node).length)) recov.push(k);
    }
    html += 'freeform spell &mdash; off the recipe map';
    if (recov.length) {
      html += ' &middot; recover with ' + recov.map(k => '<kbd>' + k.toUpperCase() + '</kbd>').join(' ') +
        ' (a cancel or mix puts you back on a path)';
    }
  } else {
    const below = magicksBelow(w.node).filter(m => m !== (node.m && node.m[0]));
    if (node.m) {
      html += '<span class="' + (node.s ? 'stackr' : 'cast') + '"' +
        (node.s ? ' style="color:' + EINFO[node.e].col + '"' : '') + '>' +
        (node.s ? node.m[0] : '&#9889; SPACE casts ' + node.m[0]) + '</span> &mdash; ' + node.m[1];
      if (below.length) html += ' &middot; or keep queuing: ' + below.slice(0, 4).join(', ');
    } else if (below.length) {
      html += 'on the path to: ' + below.slice(0, 5).join(', ') + (below.length > 5 ? '&hellip;' : '');
    } else {
      html += 'a freeform mix &mdash; nothing named down this branch';
    }
  }
  rline.innerHTML = html;
}
function magicksBelow(id) {
  const out = [];
  (function rec(k) {
    if (TRIE[k].m) out.push(TRIE[k].m[0]);
    Object.values(TRIE[k].c).forEach(c => rec(String(c)));
  })(String(id));
  return out;
}
document.addEventListener('keydown', e => {
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  const k = e.key.toLowerCase();
  if (KEYMAP[k]) { push(KEYMAP[k]); e.preventDefault(); }
  else if (e.key === 'Backspace') { Q.pop(); refresh(); e.preventDefault(); }
  else if (e.key === 'Escape') { Q.length = 0; refresh(); }
  else if (e.key === ' ') {
    e.preventDefault();
    const w = walk();
    if (!w.off && TRIE[w.node].m) {
      builder.classList.remove('flash');
      void builder.offsetWidth;
      builder.classList.add('flash');
      Q.length = 0;
      refresh();
    }
  }
});
refresh();
</script>
"""

HTML = HTML.replace('<footer>', BUILDER_CSS + '<footer>')
HTML += (BUILDER_JS
         .replace('__TRIE__', json.dumps(TRIE_JS))
         .replace('__EINFO__', json.dumps(EINFO_JS))
         .replace('__KEYMAP__', json.dumps(KEYMAP_JS)))

with open("magicka_tree.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"magicka_tree.html: {os.path.getsize('magicka_tree.html') / 1024:.0f} KB")

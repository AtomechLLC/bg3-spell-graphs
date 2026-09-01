"""Combo Chemistry: the interlocking-design map of BG3 -> combo_map.html.

Nodes are spells; edges are *combos*, not similarity: surface ignition,
wet conduction, deep freeze, shove-into-hazard, mark procs, crit set-ups,
and the counter-chemistry that undoes them. Same nodes as the
constellation, a completely different graph.
"""
import base64
import io
import json
import math
import os
import random
import re

from PIL import Image

rows = json.load(open("bg3_spells.json", encoding="utf-8"))
rows = rows if isinstance(rows, list) else list(rows.values())
ROOTS = [r for r in rows if not r.get("container") and r.get("classes")]
BYNAME = {}
for r in ROOTS:
    BYNAME.setdefault(r["name"], r)

def blob(r):
    return " ".join(str(r.get(k) or "") for k in
                    ("properties", "spell_success", "spell_fail", "status_apply", "desc"))

def deals(r, dtype):
    return dtype.lower() in (r.get("damage_type") or "").lower() or \
           dtype in (r.get("tooltip_damage") or "")

def surfaces_of(r):
    return set(re.findall(r"CreateSurface\(\s*[\d.]*\s*,?\s*[\d.]*\s*,?\s*([A-Za-z]+)", blob(r)))

# ---------------------------------------------------------------- rosters
def names(*ns):
    out = []
    for n in ns:
        if n in BYNAME:
            out.append(BYNAME[n])
    return out

FIRE = [r for r in ROOTS if deals(r, "Fire") and r["name"] not in ("Fire Shield",)]
LIGHTNING = [r for r in ROOTS if deals(r, "Lightning")]
COLD = [r for r in ROOTS if deals(r, "Cold")]

FLAMMABLE_MAKERS = [r for r in ROOTS if surfaces_of(r) & {"Grease", "Web", "Poison"}]
WET_MAKERS = [r for r in ROOTS if "WET" in blob(r) or surfaces_of(r) & {"Water"}]
ICE_MAKERS = [r for r in ROOTS if surfaces_of(r) & {"WaterFrozen"}]
CLOUD_MAKERS = [r for r in ROOTS if surfaces_of(r) & {"FogCloud", "CloudkillCloud", "StinkingCloud", "DarknessCloud"}]

PARALYZERS = names("Hold Person", "Hold Monster", "Sleep", "Flesh to Stone")
MELEE_CRITTERS = names("Searing Smite", "Thunderous Smite", "Wrathful Smite", "Staggering Smite",
                       "Inflict Wounds", "Vampiric Touch", "Flame Blade", "Shadow Blade")
ADV_MAKERS = names("Faerie Fire", "Guiding Bolt", "Blindness", "Greater Invisibility")
MARKS = names("Hex", "Hunter's Mark")
MULTI_HIT = names("Scorching Ray", "Eldritch Blast", "Magic Missile")
MOVERS = names("Telekinesis", "Gust of Wind", "Grasping Vine", "Thunderwave", "Destructive Wave")
HAZARDS = names("Spike Growth", "Cloud of Daggers", "Wall of Fire", "Hunger of Hadar",
                "Moonbeam", "Insect Plague", "Flaming Sphere", "Black Tentacles")
DOUSERS = names("Create or Destroy Water")
CLEARERS = names("Gust of Wind")

CHEM = [
    ("ignite", "#E06A3A", "ignite", "fire lit on a flammable surface",
     [(a, b) for a in FLAMMABLE_MAKERS for b in FIRE]),
    ("conduct", "#5A9BF0", "conduct", "lightning doubled through wet targets",
     [(a, b) for a in WET_MAKERS for b in LIGHTNING]),
    ("freeze", "#7FD4E8", "deep-freeze", "cold freezes wet targets solid",
     [(a, b) for a in WET_MAKERS for b in COLD]),
    ("slip", "#9BD47F", "slip", "ice surfaces knock walkers prone",
     [(a, b) for a in ICE_MAKERS for b in MELEE_CRITTERS[:4]]),
    ("crit", "#E3C377", "crit set-up", "paralysed and sleeping targets take melee crits",
     [(a, b) for a in PARALYZERS for b in MELEE_CRITTERS]),
    ("adv", "#D4AF5E", "advantage", "the tag that makes the next attack land",
     [(a, b) for a in ADV_MAKERS for b in MELEE_CRITTERS[:4] + MULTI_HIT[:1]]),
    ("mark", "#E58A9B", "mark proc", "per-hit riders multiplied by multi-hit spells",
     [(a, b) for a in MARKS for b in MULTI_HIT]),
    ("shove", "#B67AF0", "shove into", "forced movement priced in hazard zones",
     [(a, b) for a in MOVERS for b in HAZARDS]),
    ("counter", "#8a879a", "counter", "water douses fire · wind clears clouds",
     [(a, b) for a in DOUSERS for b in FIRE[:6]] + [(a, b) for a in CLEARERS for b in CLOUD_MAKERS]),
]

ENGINES = [
    ("kitchen", "THE FIRE KITCHEN", ["ignite"]),
    ("stormlab", "THE STORM LAB", ["conduct", "freeze", "slip"]),
    ("critmill", "THE CRIT MILL", ["crit", "adv"]),
    ("refinery", "THE MARK REFINERY", ["mark"]),
    ("chasm", "THE CHASM ECONOMY", ["shove"]),
    ("fireman", "THE COUNTER DESK", ["counter"]),
]

# ---------------------------------------------------------------- graph
NODES = {}
EDGES = []
for key, col, lab, desc, pairs in CHEM:
    for a, b in pairs:
        if a["id"] == b["id"]:
            continue
        NODES[a["id"]] = a
        NODES[b["id"]] = b
        EDGES.append((key, col, a["id"], b["id"]))
print(f"{len(NODES)} nodes, {len(EDGES)} combo edges")

ENGINE_OF = {}
for ek, _, chems in ENGINES:
    for ckey, _c, _l, _d, pairs in CHEM:
        if ckey in chems:
            for a, b in pairs:
                ENGINE_OF.setdefault(a["id"], set()).add(ek)
                ENGINE_OF.setdefault(b["id"], set()).add(ek)

W, H = 1500, 950
CX, CY = W / 2, H / 2
SURFACE = "#16161D"
EANCHOR = {}
for i, (ek, _t, _c) in enumerate(ENGINES):
    a = 2 * math.pi * i / len(ENGINES) - math.pi / 2
    EANCHOR[ek] = (CX + 470 * math.cos(a), CY + 20 + 330 * math.sin(a))

rng = random.Random(7)
pos = {}
for nid in NODES:
    eng = ENGINE_OF.get(nid, set())
    xs = [EANCHOR[e][0] for e in eng] or [CX]
    ys = [EANCHOR[e][1] for e in eng] or [CY]
    pos[nid] = [sum(xs) / len(xs) + rng.uniform(-60, 60),
                sum(ys) / len(ys) + rng.uniform(-50, 50)]

def clamp(p):
    p[0] = min(max(p[0], 60), W - 60)
    p[1] = min(max(p[1], 90), H - 60)

for it in range(240):
    t = 1 - it / 240
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
            if d2 < 120 * 120:
                d = math.sqrt(d2)
                fr = 900 / d2 * 60
                disp[id1][0] += dx / d * fr; disp[id1][1] += dy / d * fr
                disp[id2][0] -= dx / d * fr; disp[id2][1] -= dy / d * fr
    for nid in pos:
        eng = ENGINE_OF.get(nid, set())
        for e in eng:
            ax, ay = EANCHOR[e]
            disp[nid][0] += (ax - pos[nid][0]) * 0.10 / len(eng)
            disp[nid][1] += (ay - pos[nid][1]) * 0.10 / len(eng)
    step = 12 * t + 1
    for nid, p in pos.items():
        dx, dy = disp[nid]
        d = math.sqrt(dx * dx + dy * dy) or 1
        m = min(d, step)
        p[0] += dx / d * m; p[1] += dy / d * m
        clamp(p)
for _ in range(80):
    moved = False
    ids = list(pos)
    for i in range(len(ids)):
        p1 = pos[ids[i]]
        for j in range(i + 1, len(ids)):
            p2 = pos[ids[j]]
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            d = math.sqrt(dx * dx + dy * dy) or 0.5
            if d < 44:
                push = (44 - d) / 2
                ux, uy = dx / d, dy / d
                p1[0] -= ux * push; p1[1] -= uy * push
                p2[0] += ux * push; p2[1] += uy * push
                clamp(p1); clamp(p2)
                moved = True
    if not moved:
        break

# ---------------------------------------------------------------- icons + svg
ICONS = {}
def icon_uri(sid):
    if sid in ICONS:
        return sid
    p = os.path.join("bg3_codex_icons", sid + ".png")
    if not os.path.exists(p):
        return None
    buf = io.BytesIO()
    Image.open(p).save(buf, "WEBP", quality=80)
    ICONS[sid] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    return sid

CHEM_BY_KEY = {c[0]: c for c in CHEM}
role_of = {}
for key, col, lab, desc, pairs in CHEM:
    for a, b in pairs:
        role_of.setdefault(a["id"], set()).add(key + ":make")
        role_of.setdefault(b["id"], set()).add(key + ":use")

sv = [f'<rect width="{W}" height="{H}" fill="{SURFACE}" rx="14"/>']
for ek, title, chems in ENGINES:
    ax, ay = EANCHOR[ek]
    col = CHEM_BY_KEY[chems[0]][1]
    sv.append(f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="170" fill="{col}" opacity="0.05" filter="url(#blur)"/>')
    ly = ay - 150 if ay < CY else ay + 165
    sv.append(f'<text x="{min(max(ax, 130), W - 130):.0f}" y="{ly:.0f}" text-anchor="middle" '
              f'fill="#E3C377" font-family="Cinzel,Georgia,serif" font-size="17" font-weight="600" '
              f'letter-spacing="2" stroke="{SURFACE}" stroke-width="6" paint-order="stroke" '
              f'class="anchor">{title}</text>')
for k, (key, col, lab, desc, _p) in enumerate(CHEM):
    pass
for ei, (key, col, a, b) in enumerate(EDGES):
    pa, pb = pos[a], pos[b]
    dash = ' stroke-dasharray="5 4"' if key == "counter" else ""
    sv.append(f'<line x1="{pa[0]:.0f}" y1="{pa[1]:.0f}" x2="{pb[0]:.0f}" y2="{pb[1]:.0f}" '
              f'stroke="{col}" stroke-opacity="0.16" stroke-width="1.3"{dash} '
              f'class="e t-{key} n{a} n{b}"/>')
for nid, r in NODES.items():
    x, y = pos[nid]
    iid = icon_uri(nid)
    roles = sorted(role_of.get(nid, []))
    chems = "|" + "|".join(sorted({q.split(":")[0] for q in roles})) + "|"
    sub = " · ".join(
        ("creates" if q.endswith(":make") else "exploits") + " " + CHEM_BY_KEY[q.split(":")[0]][2]
        for q in roles)
    sv.append(f'<g class="n" data-id="{nid}" data-name="{r["name"]}" data-ch="{chems}" data-sub="{sub}">')
    sv.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="16" fill="{SURFACE}" stroke="#6b6880" stroke-width="2"/>')
    if iid:
        sv.append(f'<image class="sic" data-i="{iid}" x="{x - 12:.0f}" y="{y - 12:.0f}" '
                  f'width="24" height="24" clip-path="inset(0 round 50%)"/>')
    else:
        sv.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="#6b6880"/>')
    sv.append('</g>')
SVG = "\n".join(sv)

legend = "".join(
    f'<button class="pchip lc on" data-ch="{key}"><span class="dot" style="background:{col}"></span>'
    f'{lab}</button>' for key, col, lab, desc, _p in CHEM)

HTML = f"""<title>Combo Chemistry</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=IBM+Plex+Mono:wght@400;500&display=swap">
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
.dot{{width:11px;height:11px;border-radius:50%;display:inline-block}}
.wrap{{width:100%;max-width:1500px;position:relative}}
svg{{width:100%;height:auto;display:block}}
.n{{cursor:pointer}}
svg.hov .n{{opacity:.16}}
svg.hov .n.hl{{opacity:1}}
svg.hov line.e{{opacity:.04}}
svg.hov line.e.hl{{stroke-opacity:.9;opacity:1;stroke-width:2}}
line.e.offch{{display:none}}
#tip{{position:absolute;pointer-events:none;background:#211E2Bee;border:1px solid #3a3647;
  border-radius:8px;padding:7px 11px;font-size:12.5px;display:none;z-index:2;max-width:320px;
  box-shadow:0 8px 28px #000A}}
#tip b{{color:#E3C377;display:block;font-size:13px}}
#tip span{{color:#A7A4B3}}
footer{{color:#8a879a;font-size:11px;margin-top:10px;max-width:1500px;text-align:center;line-height:1.8}}
::selection{{background:#D4AF5E44}}
</style>
<header>
  <div class="topline">
    <div><h1>Combo Chemistry</h1>
    <div class="sub">{len(NODES)} spells · {len(EDGES)} interlocks · edges are combos, not similarity — the same
constellation, wired by what plays together</div></div>
  </div>
  <div class="legend">{legend}
    <button class="pchip" id="allch">all</button></div>
</header>
<div class="wrap">
  <svg viewBox="0 0 {W} {H}" role="img" aria-label="BG3 spells connected by combo interactions">
  <defs><filter id="blur"><feGaussianBlur stdDeviation="26"/></filter></defs>
  {SVG}</svg>
  <div id="tip"></div>
</div>
<footer>hover a spell to light its combos · toggle a chemistry to isolate it ·
🔥 ignite: grease and webs are fuel · ⚡ conduct: wet targets take double lightning ·
❄ deep-freeze: wet + cold = frozen solid · ⛓ crit: paralysed targets take auto-crits in melee ·
🏷 mark procs: Hex pays out once per beam · 🕳 shove: forced movement priced in hazard zones and ledges ·
counters (dashed): water douses, wind disperses · data: spell effect rows from a local BG3 install ·
© Larian Studios &amp; Wizards of the Coast</footer>
<script>
const ICONS = {json.dumps(ICONS)};
document.querySelectorAll('image.sic').forEach(el => {{
  const d = ICONS[el.dataset.i];
  if (d) el.setAttribute('href', d); else el.remove();
}});
const tip = document.getElementById('tip'), wrap = document.querySelector('.wrap');
const svg = document.querySelector('svg');
document.querySelectorAll('.n').forEach(n => {{
  n.addEventListener('mouseenter', () => {{
    svg.classList.add('hov');
    n.classList.add('hl');
    svg.querySelectorAll('line.e.n' + CSS.escape(n.dataset.id)).forEach(l => {{
      if (l.classList.contains('offch')) return;
      l.classList.add('hl');
      [...l.classList].filter(c => c.indexOf('n') === 0 && c !== 'n' + n.dataset.id)
        .forEach(c => {{
          const on = svg.querySelector('.n[data-id="' + c.slice(1) + '"]');
          if (on) on.classList.add('hl');
        }});
    }});
    tip.innerHTML = '<b></b><span></span>';
    tip.firstChild.textContent = n.dataset.name;
    tip.lastChild.textContent = n.dataset.sub;
    tip.style.display = 'block';
  }});
  n.addEventListener('mousemove', e => {{
    const r = wrap.getBoundingClientRect();
    tip.style.left = Math.min(e.clientX - r.left + 14, r.width - 330) + 'px';
    tip.style.top = (e.clientY - r.top + 14) + 'px';
  }});
  n.addEventListener('mouseleave', () => {{
    svg.classList.remove('hov');
    svg.querySelectorAll('.hl').forEach(x => x.classList.remove('hl'));
    tip.style.display = 'none';
  }});
}});
const chs = new Set({json.dumps([c[0] for c in CHEM])});
function applyCh() {{
  svg.querySelectorAll('line.e').forEach(l => {{
    const key = [...l.classList].find(c => c.indexOf('t-') === 0).slice(2);
    l.classList.toggle('offch', !chs.has(key));
  }});
  document.querySelectorAll('.lc').forEach(b => b.classList.toggle('on', chs.has(b.dataset.ch)));
}}
document.querySelectorAll('.lc').forEach(b => b.addEventListener('click', () => {{
  if (chs.size === {len(CHEM)}) {{ chs.clear(); chs.add(b.dataset.ch); }}
  else if (chs.has(b.dataset.ch)) {{ chs.delete(b.dataset.ch); if (!chs.size) {json.dumps([c[0] for c in CHEM])}.forEach(k => chs.add(k)); }}
  else chs.add(b.dataset.ch);
  applyCh();
}}));
document.getElementById('allch').addEventListener('click', () => {{
  {json.dumps([c[0] for c in CHEM])}.forEach(k => chs.add(k));
  applyCh();
}});
</script>
"""
with open("combo_map.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"combo_map.html: {os.path.getsize('combo_map.html') / 1024:.0f} KB")

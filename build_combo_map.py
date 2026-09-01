"""Combo Chemistry: the interlocking-design map of BG3 -> combo_map.html.

The central wheel holds the HOOKS - the game-state tokens a combo passes
through (fuel, wet, helpless, marked...). Creator spells feed a hook from
outside; exploiter spells cash it. Every combo is spell -> hook -> spell,
so the wheel is the grammar and the edges stay linear, not quadratic.
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

def names(*ns):
    return [BYNAME[n] for n in ns if n in BYNAME]

FIRE = [r for r in ROOTS if deals(r, "Fire") and r["name"] not in ("Fire Shield",)]
LIGHTNING = [r for r in ROOTS if deals(r, "Lightning")]
COLD = [r for r in ROOTS if deals(r, "Cold")]
FLAMMABLE_MAKERS = [r for r in ROOTS if surfaces_of(r) & {"Grease", "Web", "Poison"}]
WET_MAKERS = [r for r in ROOTS if "WET" in blob(r) or surfaces_of(r) & {"Water"}]
ICE_MAKERS = [r for r in ROOTS if surfaces_of(r) & {"WaterFrozen"}]
CLOUD_MAKERS = [r for r in ROOTS if surfaces_of(r) & {"FogCloud", "CloudkillCloud", "StinkingCloud", "DarknessCloud"}]
PARALYZERS = names("Hold Person", "Hold Monster", "Sleep", "Flesh to Stone")
MELEE = names("Searing Smite", "Thunderous Smite", "Wrathful Smite", "Staggering Smite",
              "Inflict Wounds", "Vampiric Touch", "Flame Blade", "Shadow Blade")
ADV_MAKERS = names("Faerie Fire", "Guiding Bolt", "Blindness", "Greater Invisibility")
MARKS = names("Hex", "Hunter's Mark")
MULTI_HIT = names("Scorching Ray", "Eldritch Blast", "Magic Missile")
MOVERS = names("Telekinesis", "Gust of Wind", "Grasping Vine", "Thunderwave", "Destructive Wave")
HAZARDS = names("Spike Growth", "Cloud of Daggers", "Wall of Fire", "Hunger of Hadar",
                "Moonbeam", "Insect Plague", "Flaming Sphere", "Black Tentacles")
CLEARERS = names("Gust of Wind")

# hook = (id, emoji, LABEL, color, state-description, makers, [(edge-color, verb, users)])
HOOKS = [
    ("fuel", "🛢", "FUEL", "#E06A3A", "a flammable surface waiting for a spark",
     FLAMMABLE_MAKERS, [("#E06A3A", "ignites", FIRE)]),
    ("wet", "💧", "WET", "#5A9BF0", "soaked targets take double lightning and cold",
     WET_MAKERS, [("#5A9BF0", "conducts through", LIGHTNING),
                  ("#7FD4E8", "deep-freezes", COLD)]),
    ("ice", "🧊", "ICE", "#7FD4E8", "a frozen floor that drops walkers prone",
     ICE_MAKERS, [("#9BD47F", "crits the slipped", MELEE[:4])]),
    ("helpless", "⛓", "HELPLESS", "#E3C377", "paralysed and sleeping targets take melee auto-crits",
     PARALYZERS, [("#E3C377", "auto-crits", MELEE)]),
    ("adv", "🎯", "ADVANTAGE", "#D4AF5E", "the tag that makes the next attack land",
     ADV_MAKERS, [("#D4AF5E", "lands with advantage", MELEE[:4] + MULTI_HIT[:1])]),
    ("mark", "🏷", "MARKED", "#E58A9B", "+1d6 riding every single hit",
     MARKS, [("#E58A9B", "procs per beam", MULTI_HIT)]),
    ("hazard", "🕳", "HAZARD", "#B67AF0", "zones and ledges that price forced movement",
     HAZARDS, [("#B67AF0", "shoves victims in", MOVERS)]),
    ("cloud", "💨", "CLOUD", "#8a879a", "lingering clouds - and the wind that cancels them",
     CLOUD_MAKERS, [("#8a879a", "disperses", CLEARERS)]),
]

NODES = {}
EDGES = []       # (hook_id, color, spell_id, direction 'make'|'use', dashed)
ROLES = {}
for hid, em, lab, col, desc, makers, uses in HOOKS:
    for r in makers:
        NODES[r["id"]] = r
        EDGES.append((hid, col, r["id"], "make", hid == "cloud" and False))
        ROLES.setdefault(r["id"], []).append(f"creates {lab.lower()}")
    for ecol, verb, users in uses:
        for r in users:
            NODES[r["id"]] = r
            EDGES.append((hid, ecol, r["id"], "use", hid == "cloud"))
            ROLES.setdefault(r["id"], []).append(f"{verb} {lab.lower()}")
print(f"{len(NODES)} spells, {len(HOOKS)} hooks, {len(EDGES)} spokes")

# ---------------------------------------------------------------- layout
W, H = 1500, 950
CX, CY = W / 2, 480
SURFACE = "#16161D"
HOOK_ANGLE = {}
HOOK_POS = {}
for i, h in enumerate(HOOKS):
    a = 2 * math.pi * i / len(HOOKS) - math.pi / 2
    HOOK_ANGLE[h[0]] = a
    HOOK_POS[h[0]] = (CX + 185 * math.cos(a), CY + 150 * math.sin(a))

SPELL_HOOKS = {}
for hid, col, sid, d, dash in EDGES:
    SPELL_HOOKS.setdefault(sid, set()).add(hid)

rng = random.Random(11)
pos = {}
for sid in NODES:
    vx = sum(math.cos(HOOK_ANGLE[h]) for h in SPELL_HOOKS[sid])
    vy = sum(math.sin(HOOK_ANGLE[h]) for h in SPELL_HOOKS[sid])
    a = math.atan2(vy, vx) if (vx or vy) else rng.uniform(0, 2 * math.pi)
    a += rng.uniform(-0.28, 0.28)
    rad = 400 + rng.uniform(-55, 55)
    pos[sid] = [CX + rad * math.cos(a), CY + rad * 0.82 * math.sin(a)]

def clamp(p):
    p[0] = min(max(p[0], 60), W - 60)
    p[1] = min(max(p[1], 60), H - 60)
    dx, dy = p[0] - CX, (p[1] - CY) / 0.82
    d = math.sqrt(dx * dx + dy * dy) or 1
    if d < 300:                       # keep the wheel clear
        p[0] = CX + dx / d * 300
        p[1] = CY + dy / d * 300 * 0.82

for it in range(200):
    t = 1 - it / 200
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
            if d2 < 110 * 110:
                d = math.sqrt(d2)
                fr = 800 / d2 * 60
                disp[id1][0] += dx / d * fr; disp[id1][1] += dy / d * fr
                disp[id2][0] -= dx / d * fr; disp[id2][1] -= dy / d * fr
    for sid in pos:
        hooks = SPELL_HOOKS[sid]
        for h in hooks:
            hx, hy = HOOK_POS[h]
            dx, dy = hx - pos[sid][0], hy - pos[sid][1]
            d = math.sqrt(dx * dx + dy * dy) or 1
            k = 0.045 / len(hooks) * (d - 240)
            disp[sid][0] += dx / d * k
            disp[sid][1] += dy / d * k
    step = 11 * t + 1
    for sid, p in pos.items():
        dx, dy = disp[sid]
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
            if d < 45:
                push = (45 - d) / 2
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

colors = sorted({c for _h, c, *_ in [(e[0], e[1]) for e in EDGES]} | {h[3] for h in HOOKS})
markers = "".join(
    f'<marker id="m{c.lstrip("#")}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5.5" '
    f'markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" fill="{c}"/></marker>'
    for c in colors)

sv = [f'<rect width="{W}" height="{H}" fill="{SURFACE}" rx="14"/>']
sv.append(f'<ellipse cx="{CX}" cy="{CY}" rx="185" ry="150" fill="none" stroke="#2A2734" stroke-width="1.5" stroke-dasharray="3 6"/>')
sv.append(f'<ellipse cx="{CX}" cy="{CY}" rx="185" ry="150" fill="#D4AF5E" opacity="0.04" filter="url(#blur)"/>')
sv.append(f'<text x="{CX}" y="{CY + 5:.0f}" text-anchor="middle" fill="#6b6880" '
          f'font-family="Cinzel,Georgia,serif" font-size="15" letter-spacing="3">THE HOOKS</text>')

for hid, col, sid, d, dash in EDGES:
    hx, hy = HOOK_POS[hid]
    sx, sy = pos[sid]
    dx, dy = hx - sx, hy - sy
    dist = math.sqrt(dx * dx + dy * dy) or 1
    ux, uy = dx / dist, dy / dist
    if d == "make":     # spell feeds the hook: arrow points inward
        x1, y1 = sx + ux * 20, sy + uy * 20
        x2, y2 = hx - ux * 36, hy - uy * 36
    else:               # hook feeds the spell: arrow points outward
        x1, y1 = hx - ux * 36, hy - uy * 36
        x2, y2 = sx + ux * 20, sy + uy * 20
    dsh = ' stroke-dasharray="5 4"' if dash else ""
    sv.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{col}" '
              f'stroke-opacity="0.28" stroke-width="1.4"{dsh} marker-end="url(#m{col.lstrip("#")})" '
              f'class="e h-{hid} n{sid}"/>')

for hid, em, lab, col, desc, makers, uses in HOOKS:
    hx, hy = HOOK_POS[hid]
    nmk = len(makers)
    nus = sum(len(u[2]) for u in uses)
    sv.append(f'<g class="hook" data-h="{hid}" data-name="{lab.title()}" '
              f'data-sub="{desc} · {nmk} creators → {nus} exploiters">')
    sv.append(f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="27" fill="{SURFACE}" stroke="{col}" stroke-width="2.6"/>')
    sv.append(f'<text x="{hx:.0f}" y="{hy + 7:.0f}" text-anchor="middle" font-size="21" class="femoji">{em}</text>')
    ly = hy + 45 if hy >= CY else hy - 36
    sv.append(f'<text x="{hx:.0f}" y="{ly:.0f}" text-anchor="middle" fill="{col}" '
              f'font-family="IBM Plex Mono,monospace" font-size="11.5" font-weight="600" letter-spacing="2" '
              f'stroke="{SURFACE}" stroke-width="5" paint-order="stroke">{lab}</text>')
    sv.append('</g>')

for sid, r in NODES.items():
    x, y = pos[sid]
    iid = icon_uri(sid)
    sub = " · ".join(dict.fromkeys(ROLES[sid]))
    hooks = "|" + "|".join(sorted(SPELL_HOOKS[sid])) + "|"
    sv.append(f'<g class="n" data-id="{sid}" data-name="{r["name"]}" data-hk="{hooks}" data-sub="{sub}">')
    sv.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="16" fill="{SURFACE}" stroke="#6b6880" stroke-width="2"/>')
    if iid:
        sv.append(f'<image class="sic" data-i="{iid}" x="{x - 12:.0f}" y="{y - 12:.0f}" '
                  f'width="24" height="24" clip-path="inset(0 round 50%)"/>')
    else:
        sv.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="#6b6880"/>')
    sv.append('</g>')
SVG = "\n".join(sv)

legend = "".join(
    f'<button class="pchip lc on" data-h="{hid}"><span class="femoji">{em}</span>'
    f'<span class="dot" style="background:{col}"></span>{lab.lower()}</button>'
    for hid, em, lab, col, *_ in HOOKS)

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

HTML = f"""<title>Combo Chemistry</title>
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
.wrap{{width:100%;max-width:1500px;position:relative}}
svg{{width:100%;height:auto;display:block}}
.n,.hook{{cursor:pointer}}
svg.hov .n,svg.hov .hook{{opacity:.15}}
svg.hov .n.hl,svg.hov .hook.hl{{opacity:1}}
svg.hov line.e{{opacity:.05}}
svg.hov line.e.hl{{stroke-opacity:.95;opacity:1;stroke-width:2}}
line.e.offch{{display:none}}
#tip{{position:absolute;pointer-events:none;background:#211E2Bee;border:1px solid #3a3647;
  border-radius:8px;padding:7px 11px;font-size:12.5px;display:none;z-index:2;max-width:330px;
  box-shadow:0 8px 28px #000A}}
#tip b{{color:#E3C377;display:block;font-size:13px}}
#tip span{{color:#A7A4B3}}
footer{{color:#8a879a;font-size:11px;margin-top:10px;max-width:1500px;text-align:center;line-height:1.8}}
::selection{{background:#D4AF5E44}}
.fsc{{display:inline-flex;align-items:center;gap:7px;border:1px solid #3a3647;
  border-radius:999px;padding:4px 12px;font:500 11px "IBM Plex Mono",monospace;color:#C9C6D4;
  text-decoration:none;letter-spacing:.05em;align-self:flex-start}}
.fsc:hover{{border-color:#D4AF5E;color:#E3C377}}
</style>
<header>
  <div class="topline">
    <div><h1>Combo Chemistry</h1>
    <div class="sub">{len(NODES)} spells · {len(HOOKS)} hooks · {len(EDGES)} spokes — every combo is
spell → <b>hook</b> → spell: creators feed the wheel, exploiters cash it</div></div>
    {FSC}
  </div>
  <div class="legend">{legend}
    <button class="pchip" id="allch">all</button></div>
</header>
<div class="wrap">
  <svg viewBox="0 0 {W} {H}" role="img" aria-label="BG3 combo hooks: creators feed each hook, exploiters cash it">
  <defs><filter id="blur"><feGaussianBlur stdDeviation="26"/></filter>{markers}</defs>
  {SVG}</svg>
  <div id="tip"></div>
</div>
<footer>hover a hook to see its whole economy · hover a spell to see what it feeds or cashes ·
arrows point the way the combo flows: into the wheel to create the state, out of it to spend it ·
🛢 fuel: grease and webs wait for a spark · 💧 wet: double lightning and cold · ⛓ helpless: melee auto-crits ·
🏷 marked: Hex pays per beam · 🕳 hazard: forced movement priced in zones and ledges · 💨 dashed = counterplay ·
data: spell effect rows from a local BG3 install · © Larian Studios &amp; Wizards of the Coast</footer>
<script>
const ICONS = {json.dumps(ICONS)};
document.querySelectorAll('image.sic').forEach(el => {{
  const d = ICONS[el.dataset.i];
  if (d) el.setAttribute('href', d); else el.remove();
}});
const tip = document.getElementById('tip'), wrap = document.querySelector('.wrap');
const svg = document.querySelector('.wrap svg');
function moveTip(e) {{
  const r = wrap.getBoundingClientRect();
  tip.style.left = Math.min(e.clientX - r.left + 14, r.width - 340) + 'px';
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
    svg.querySelectorAll('line.e.n' + CSS.escape(n.dataset.id)).forEach(l => {{
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
      const sn = [...l.classList].filter(c => c !== 'e' && c !== 'hl' && c.indexOf('h-') !== 0);
      sn.forEach(c => {{
        const nn = svg.querySelector('.n[data-id="' + c.slice(1) + '"]');
        if (nn) nn.classList.add('hl');
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
    const key = [...l.classList].find(c => c.indexOf('h-') === 0).slice(2);
    l.classList.toggle('offch', !chs.has(key));
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
</script>
"""
with open("combo_map.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"combo_map.html: {os.path.getsize('combo_map.html') / 1024:.0f} KB")

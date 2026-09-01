"""Spell Constellations with switchable clustering methods -> cluster_map.html.

Three layouts of the same BG3 spells: BY FAMILY (similarity force layout,
container satellites), BY CLASS (anchor layout, share-count rings), BY SCHOOL
(anchor layout, family-tier rings). Icons stored once, shared by all views.
Supersedes build_cluster_viz.py / build_class_map.py.
"""
import base64
import io
import json
import math
import os
import random
from itertools import combinations

from PIL import Image

import build_bg3_codex as C
from bg3_analyze import pair_score

BY = C.BY
POP = C.POP            # 213 roots (duplicate SKUs kept)
DPOP = sorted(C.DPOP, key=lambda r: r["id"])   # 211 deduped
FAMILY_OF = C.FAMILY_OF
SURFACE = "#16161D"
W, H = 1500, 980
CX, CY = W / 2, H / 2

TIER_COLOR = {"clone": "#d95926", "template": "#3987e5", "engine": "#199e70"}
NEUTRAL = "#7c7c88"
RAMP = [("1 class", "#2e5286"), ("2 classes", "#3987e5"),
        ("3–4 classes", "#7db4f0"), ("5+ classes", "#cfe3fb")]

def ramp_color(n):
    return RAMP[0][1] if n <= 1 else RAMP[1][1] if n == 2 else RAMP[2][1] if n <= 4 else RAMP[3][1]

from purpose_defs import load_purposes, PEMOJI as PUR_EMOJI, PSHORT as PUR_SHORT, PLABEL as PUR_LABEL
BG3_PUR = load_purposes("Baldur's Gate 3")

def pur_of(r):
    return BG3_PUR.get(r["name"].lower(), "utility")

def fam_of(r):
    fm = FAMILY_OF.get(r["id"])
    if not fm:
        for x in POP:
            if x["name"] == r["name"] and x["level"] == r["level"] and x["id"] in FAMILY_OF:
                fm = FAMILY_OF[x["id"]]
                break
    return fm

def tier_color(r):
    fm = fam_of(r)
    return TIER_COLOR[fm["tier"]] if fm else NEUTRAL, (fm["icon"] + " " + fm["title"]) if fm else "no family"

def uni_attrs(r):
    """Filter attributes carried by every node in every view."""
    fm = fam_of(r)
    return {"cl": "|" + "|".join(r["classes"]) + "|",
            "sc": r.get("school") or "",
            "fs": fm["slug"] if fm else "",
            "tier": fm["tier"] if fm else "",
            "pur": pur_of(r)}

# ---------------------------------------------------------------- icons (shared)
ICON_URIS = {}
def icon_uri(spell_id):
    if spell_id in ICON_URIS:
        return spell_id
    p = os.path.join("bg3_codex_icons", spell_id + ".png")
    if not os.path.exists(p):
        return None
    buf = io.BytesIO()
    Image.open(p).save(buf, "WEBP", quality=80)
    ICON_URIS[spell_id] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    return spell_id

def clamp(p, top=70):
    p[0] = min(max(p[0], 50), W - 50)
    p[1] = min(max(p[1], top), H - 55)

# ================================================================ view 1: family
sims = {tuple(k.split("|")): v for k, v in json.load(open("cluster_sims.json")).items()}
for r in POP:
    pass

rng = random.Random(42)
fams = list(C.F)
fam_angle = {f["slug"]: 2 * math.pi * i / len(fams) for i, f in enumerate(fams)}
fpos = {}
for r in POP:
    f = FAMILY_OF.get(r["id"])
    if f:
        a = fam_angle[f["slug"]]
        rad = 310 + 50 * rng.random()
        fpos[r["id"]] = [CX + rad * math.cos(a) + rng.uniform(-25, 25),
                         CY + 10 + rad * math.sin(a) * 0.60 + rng.uniform(-25, 25)]
    else:
        a = rng.uniform(0, 2 * math.pi)
        rad = 470 + 70 * rng.random()
        fpos[r["id"]] = [CX + rad * math.cos(a), CY + 10 + rad * math.sin(a) * 0.72]

springs = [(a, b, s) for (a, b), s in sims.items() if s >= 0.80]
for it in range(320):
    t = 1 - it / 320
    disp = {i: [0.0, 0.0] for i in fpos}
    items = list(fpos.items())
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
                fr = 1500 / d2 * 60
                disp[id1][0] += dx / d * fr; disp[id1][1] += dy / d * fr
                disp[id2][0] -= dx / d * fr; disp[id2][1] -= dy / d * fr
    for a, b, s in springs:
        pa, pb = fpos[a], fpos[b]
        dx, dy = pb[0] - pa[0], pb[1] - pa[1]
        d = math.sqrt(dx * dx + dy * dy) or 1
        fa, fb = FAMILY_OF.get(a), FAMILY_OF.get(b)
        k = (s - 0.80) * (0.50 if fa is not None and fa is fb else 0.03)
        fr = k * (d - 46)
        disp[a][0] += dx / d * fr; disp[a][1] += dy / d * fr
        disp[b][0] -= dx / d * fr; disp[b][1] -= dy / d * fr
    cent = {}
    for f in fams:
        pts = [fpos[m] for m in f["members"]]
        cent[f["slug"]] = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
    for r in POP:
        p = fpos[r["id"]]
        fm = FAMILY_OF.get(r["id"])
        if fm:
            cx, cy = cent[fm["slug"]]
            disp[r["id"]][0] += (cx - p[0]) * 0.12 + (CX - p[0]) * 0.004
            disp[r["id"]][1] += (cy - p[1]) * 0.12 + (CY - p[1]) * 0.004
        else:
            disp[r["id"]][0] += (CX - p[0]) * 0.0008
            disp[r["id"]][1] += (CY - p[1]) * 0.0008
    step = 14 * t + 1
    for i, p in fpos.items():
        dx, dy = disp[i]
        d = math.sqrt(dx * dx + dy * dy) or 1
        m = min(d, step)
        p[0] += dx / d * m; p[1] += dy / d * m
        clamp(p)

def fam_radius(r):
    return 40 if r["children"] else 21

for _ in range(90):
    moved = False
    items = [(r, fpos[r["id"]]) for r in POP]
    for i in range(len(items)):
        r1, p1 = items[i]
        for j in range(i + 1, len(items)):
            r2, p2 = items[j]
            need = fam_radius(r1) + fam_radius(r2)
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            d = math.sqrt(dx * dx + dy * dy) or 0.5
            if d < need:
                push = (need - d) / 2
                ux, uy = dx / d, dy / d
                p1[0] -= ux * push; p1[1] -= uy * push
                p2[0] += ux * push; p2[1] += uy * push
                clamp(p1); clamp(p2)
                moved = True
    if not moved:
        break

# ---------------------------------------------------------------- anchor layouts
def anchor_layout(nodes, anchors_of, anchors, seed, pull_solo=0.16, pull_multi=0.09):
    rng2 = random.Random(seed)
    pos = {}
    for r in nodes:
        cls = anchors_of(r)
        ax = sum(anchors[c][0] for c in cls) / len(cls)
        ay = sum(anchors[c][1] for c in cls) / len(cls)
        pos[r["id"]] = [ax + rng2.uniform(-40, 40), ay + rng2.uniform(-40, 40)]
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
                    dx, dy, d2 = rng2.uniform(-1, 1), rng2.uniform(-1, 1), 1
                if d2 < 140 * 140:
                    d = math.sqrt(d2)
                    fr = 850 / d2 * 60
                    disp[id1][0] += dx / d * fr; disp[id1][1] += dy / d * fr
                    disp[id2][0] -= dx / d * fr; disp[id2][1] -= dy / d * fr
        for r in nodes:
            p = pos[r["id"]]
            cls = anchors_of(r)
            pull = pull_solo if len(cls) == 1 else pull_multi
            for c in cls:
                ax, ay = anchors[c]
                disp[r["id"]][0] += (ax - p[0]) * pull / len(cls)
                disp[r["id"]][1] += (ay - p[1]) * pull / len(cls)
        step = 13 * t + 1
        for i, p in pos.items():
            dx, dy = disp[i]
            d = math.sqrt(dx * dx + dy * dy) or 1
            m = min(d, step)
            p[0] += dx / d * m; p[1] += dy / d * m
            clamp(p)
    for _ in range(90):
        moved = False
        ids = [r["id"] for r in nodes]
        for i in range(len(ids)):
            p1 = pos[ids[i]]
            for j in range(i + 1, len(ids)):
                p2 = pos[ids[j]]
                dx, dy = p2[0] - p1[0], p2[1] - p1[1]
                d = math.sqrt(dx * dx + dy * dy) or 0.5
                if d < 38:
                    push = (38 - d) / 2
                    ux, uy = dx / d, dy / d
                    p1[0] -= ux * push; p1[1] -= uy * push
                    p2[0] += ux * push; p2[1] += uy * push
                    clamp(p1); clamp(p2)
                    moved = True
        if not moved:
            break
    return pos

CLASSES = ["Druid", "Ranger", "Cleric", "Paladin", "Bard", "Sorcerer",
           "Wizard", "Fighter", "Rogue", "Warlock"]
CANCHOR = {c: (CX + 555 * math.cos(2 * math.pi * i / len(CLASSES) - math.pi / 2),
               CY + 368 * math.sin(2 * math.pi * i / len(CLASSES) - math.pi / 2))
           for i, c in enumerate(CLASSES)}
cpos = anchor_layout(DPOP, lambda r: [c for c in r["classes"] if c in CANCHOR] or ["Wizard"],
                     CANCHOR, seed=7)

PURS = [p for p in PUR_SHORT if any(pur_of(r) == p for r in DPOP)]
PANCHOR = {p: (CX + 585 * math.cos(2 * math.pi * i / len(PURS) - math.pi / 2),
               CY + 390 * math.sin(2 * math.pi * i / len(PURS) - math.pi / 2))
           for i, p in enumerate(PURS)}
ppos = anchor_layout(DPOP, lambda r: [pur_of(r)], PANCHOR, seed=13, pull_solo=0.11)

SCHOOLS = sorted({r["school"] for r in DPOP if r["school"] and r["school"] != "None"})
SANCHOR = {s: (CX + 545 * math.cos(2 * math.pi * i / len(SCHOOLS) - math.pi / 2),
               CY + 360 * math.sin(2 * math.pi * i / len(SCHOOLS) - math.pi / 2))
           for i, s in enumerate(SCHOOLS)}
def school_of(r):
    return [r["school"]] if r["school"] in SANCHOR else [SCHOOLS[0]]
spos = anchor_layout(DPOP, school_of, SANCHOR, seed=11, pull_solo=0.11)

# ---------------------------------------------------------------- svg builders
TIER_DASH = {TIER_COLOR["template"]: "7 3", TIER_COLOR["engine"]: "2.5 2.5"}

def node_svg(r, p, col, extra_data, k=None, satellites=False):
    x, y = p
    iid = icon_uri(r["id"])
    data = " ".join(f'data-{a}="{v}"' for a, v in extra_data.items())
    g = [f'<g class="n" data-name="{r["name"]}" {data}>']
    if satellites and r["children"]:
        kids = r["children"][:8]
        ring = 32
        g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{ring}" fill="none" stroke="{col}" '
                 f'stroke-opacity="0.55" stroke-width="1.2" stroke-dasharray="3 4"/>')
        for kk, ch in enumerate(kids):
            a = 2 * math.pi * kk / len(kids) - math.pi / 2
            sx, sy = x + ring * math.cos(a), y + ring * math.sin(a)
            cid = icon_uri(ch)
            if cid:
                g.append(f'<image class="sic" data-i="{cid}" x="{sx - 7:.0f}" y="{sy - 7:.0f}" '
                         f'width="14" height="14" opacity="0.9"/>')
    dash = TIER_DASH.get(col, "")
    g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="16.5" fill="{SURFACE}" stroke="{col}" stroke-width="2.6"'
             + (f' stroke-dasharray="{dash}"' if dash else "") + '/>')
    if iid:
        g.append(f'<image class="sic" data-i="{iid}" x="{x - 13:.0f}" y="{y - 13:.0f}" '
                 f'width="26" height="26" clip-path="inset(0 round 50%)"/>')
    else:
        g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="{col}"/>')
    g.append('</g>')
    return "".join(g)

def anchor_labels(anchors, counts):
    out = []
    for c, (ax, ay) in anchors.items():
        lx = min(max(ax, 90), W - 90)
        dy = -16 if ay < CY else 30
        out.append(f'<text x="{lx:.0f}" y="{ay + dy:.0f}" text-anchor="middle" fill="#E3C377" '
                   f'font-family="Cinzel,Georgia,serif" font-size="19" font-weight="600" '
                   f'letter-spacing="2" stroke="{SURFACE}" stroke-width="6" paint-order="stroke" '
                   f'class="anchor" data-c="{c}">{c.upper()}</text>')
        out.append(f'<text x="{lx:.0f}" y="{ay + dy + 17:.0f}" text-anchor="middle" fill="#a8a4b5" '
                   f'font-family="IBM Plex Mono,monospace" font-size="11.5" stroke="{SURFACE}" '
                   f'stroke-width="5" paint-order="stroke">{counts[c]}</text>')
    return out

# --- families svg
sv1 = [f'<rect width="{W}" height="{H}" fill="{SURFACE}" rx="14"/>']
for f in fams:
    pts = [fpos[m] for m in f["members"]]
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    spread = max(max(math.dist((cx, cy), p) for p in pts) + 46, 60)
    col = TIER_COLOR[f["tier"]]
    sv1.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{spread:.0f}" fill="{col}" opacity="0.08" filter="url(#blur)"/>')
    sv1.append(f'<text x="{cx:.0f}" y="{cy + spread - 8:.0f}" text-anchor="middle" font-size="20" '
               f'opacity="0.65" class="fmark" data-f="{f["slug"]}">{f["icon"]}</text>')
sv1.append('<g stroke="#8d89a6" fill="none">')
IDX = {r["id"]: i for i, r in enumerate(POP)}
for (a, b), s in sims.items():
    if s < 0.88:
        continue
    pa, pb = fpos[a], fpos[b]
    sv1.append(f'<line x1="{pa[0]:.0f}" y1="{pa[1]:.0f}" x2="{pb[0]:.0f}" y2="{pb[1]:.0f}" '
               f'stroke-opacity="{min(0.45, (s - 0.86) * 3):.2f}" stroke-width="{1 + (s - 0.88) * 8:.1f}" '
               f'class="e e{IDX[a]} e{IDX[b]}"/>')
sv1.append('</g>')
for r in POP:
    col, famname = tier_color(r)
    sv1.append(node_svg(r, fpos[r["id"]], col,
                        {**uni_attrs(r), "sub": famname, "i": str(IDX[r["id"]])},
                        satellites=True))
SVG_FAM = "\n".join(sv1)

# --- classes svg
counts_c = {c: sum(1 for r in DPOP if c in r["classes"]) for c in CLASSES}
sv2 = [f'<rect width="{W}" height="{H}" fill="{SURFACE}" rx="14"/>']
for c in CLASSES:
    ax, ay = CANCHOR[c]
    sv2.append(f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="150" fill="#D4AF5E" opacity="0.05" filter="url(#blur)"/>')
sv2.append('<g id="spokes" stroke="#E3C377" fill="none">')
for k, r in enumerate(DPOP):
    p = cpos[r["id"]]
    for c in r["classes"]:
        if c in CANCHOR:
            ax, ay = CANCHOR[c]
            sv2.append(f'<line x1="{p[0]:.0f}" y1="{p[1]:.0f}" x2="{ax:.0f}" y2="{ay:.0f}" '
                       f'stroke-opacity="0" class="sp sp{k}" data-c="{c}"/>')
sv2.append('</g>')
for k, r in enumerate(DPOP):
    sv2.append(node_svg(r, cpos[r["id"]], ramp_color(len(r["classes"])),
                        {**uni_attrs(r), "sub": " · ".join(r["classes"]) or "—", "k": str(k)}))
sv2 += anchor_labels(CANCHOR, counts_c)
SVG_CLS = "\n".join(sv2)

# --- schools svg
counts_s = {s: sum(1 for r in DPOP if school_of(r)[0] == s) for s in SCHOOLS}
sv3 = [f'<rect width="{W}" height="{H}" fill="{SURFACE}" rx="14"/>']
for s in SCHOOLS:
    ax, ay = SANCHOR[s]
    sv3.append(f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="150" fill="#D4AF5E" opacity="0.05" filter="url(#blur)"/>')
for r in DPOP:
    col, famname = tier_color(r)
    sv3.append(node_svg(r, spos[r["id"]], col,
                        {**uni_attrs(r), "sub": r["school"] + " · " + famname}))
sv3 += anchor_labels(SANCHOR, counts_s)
SVG_SCH = "\n".join(sv3)

# --- purposes svg
counts_p = {p: sum(1 for r in DPOP if pur_of(r) == p) for p in PURS}
sv4 = [f'<rect width="{W}" height="{H}" fill="{SURFACE}" rx="14"/>']
for p in PURS:
    ax, ay = PANCHOR[p]
    sv4.append(f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="130" fill="#D4AF5E" opacity="0.05" filter="url(#blur)"/>')
for r in DPOP:
    col, famname = tier_color(r)
    pk = pur_of(r)
    sv4.append(node_svg(r, ppos[r["id"]], col,
                        {**uni_attrs(r), "sub": PUR_EMOJI[pk] + " " + PUR_LABEL[pk] + " · " + famname}))
for p in PURS:
    ax, ay = PANCHOR[p]
    lx = min(max(ax, 100), W - 100)
    dy = -16 if ay < CY else 30
    sv4.append(f'<text x="{lx:.0f}" y="{ay + dy:.0f}" text-anchor="middle" fill="#E3C377" '
               f'font-family="Cinzel,Georgia,serif" font-size="15" font-weight="600" '
               f'letter-spacing="1.5" stroke="{SURFACE}" stroke-width="6" paint-order="stroke" '
               f'class="anchor" data-c="{p}"><tspan class="femoji">{PUR_EMOJI[p]}</tspan> {PUR_SHORT[p]}</text>')
    sv4.append(f'<text x="{lx:.0f}" y="{ay + dy + 16:.0f}" text-anchor="middle" fill="#a8a4b5" '
               f'font-family="IBM Plex Mono,monospace" font-size="11" stroke="{SURFACE}" '
               f'stroke-width="5" paint-order="stroke">{counts_p[p]}</text>')
SVG_PUR = "\n".join(sv4)

tier_chips = "".join(
    f'<span class="chip"><span class="dot" style="background:{c}"></span>{l}</span>'
    for l, c in [("clone family", TIER_COLOR["clone"]), ("template family", TIER_COLOR["template"]),
                 ("engine family", TIER_COLOR["engine"]), ("singleton", NEUTRAL)])
ramp_chips = "".join(
    f'<span class="chip"><span class="dot" style="background:{c}"></span>{l}</span>' for l, c in RAMP)

pick_cls = "".join(f'<button class="pchip" data-g="cls" data-val="{c}">{c}</button>' for c in CLASSES)
pick_sch = "".join(f'<button class="pchip" data-g="sch" data-val="{s}">{s}</button>' for s in SCHOOLS)
pick_tier = "".join(
    f'<button class="pchip" data-g="tier" data-val="{t}"><span class="dot" '
    f'style="background:{TIER_COLOR[t]}"></span>{lab}</button>'
    for t, lab in [("clone", "clones"), ("template", "templates"), ("engine", "engines")])
pick_fam = "".join(
    f'<button class="pchip pfam" data-g="fam" data-val="{f["slug"]}" title="{f["title"]}" '
    f'aria-label="{f["title"]}">{f["icon"]}<span class="pl">{f["title"].removeprefix("The ").lower()}</span></button>' for f in C.F)
pick_pur = "".join(
    f'<button class="pchip" data-g="pur" data-val="{p}" title="{PUR_LABEL[p]}">'
    f'<span class="femoji">{PUR_EMOJI[p]}</span>{PUR_SHORT[p].lower()}</button>' for p in PURS)

HTML = f"""<title>Spell Constellations</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#101016;color:#E8E6EF;font:400 14px/1.5 "IBM Plex Mono",ui-monospace,monospace;
  min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:22px 18px 30px}}
header{{width:100%;max-width:1500px;display:flex;flex-direction:column;gap:10px;margin-bottom:12px}}
.topline{{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap}}
.segrow{{margin-left:auto;display:flex;align-items:center;gap:10px}}
#copybtn.ok{{border-color:#5fbf83;color:#7fdfa3}}
#copybtn.err{{border-color:#e58a9b;color:#e58a9b}}
h1{{font:600 22px Cinzel,Georgia,serif;color:#E3C377;margin:0;letter-spacing:.04em}}
.sub{{color:#A7A4B3;font-size:11.5px}}
.seg{{display:flex;border:1px solid #3a3647;border-radius:7px;overflow:hidden}}
.seg button{{background:transparent;border:0;color:#A7A4B3;font:500 12px "IBM Plex Mono",monospace;
  letter-spacing:.08em;padding:8px 16px;cursor:pointer}}
.seg button + button{{border-left:1px solid #3a3647}}
.seg button.on{{background:#D4AF5E1f;color:#E3C377}}
.seg button:focus-visible{{outline:2px solid #E3C377;outline-offset:-2px}}
.legend{{display:flex;gap:14px;flex-wrap:wrap;align-items:center;font-size:11.5px;color:#C9C6D4}}
.chip{{display:inline-flex;align-items:center;gap:6px}}
.dot{{width:11px;height:11px;border-radius:50%;display:inline-block}}
.ringchip{{width:15px;height:15px;border-radius:50%;border:1.4px dashed #A7A4B3;display:inline-block}}
.wrap{{width:100%;max-width:1500px;position:relative}}
.view{{display:none}}
.view.on{{display:block}}
svg{{width:100%;height:auto;display:block}}
.n{{cursor:pointer}}
.sp{{stroke-width:1.1}}
svg.hov .n{{opacity:.16;transition:opacity .15s}}
svg.hov .n.hl{{opacity:1}}
svg.hov line.e{{opacity:.06}}
svg.hov line.e.hl{{opacity:1;stroke:#E3C377}}
svg.hov .sp.hl{{stroke-opacity:.85}}
svg.hov text.anchor{{opacity:.3}}
svg.hov text.anchor.hl{{opacity:1}}
text.anchor,.fmark{{cursor:pointer}}
svg.hov .fmark{{opacity:.25}}
svg.hov .fmark.hl{{opacity:1}}
@media (prefers-reduced-motion: reduce){{svg.hov .n{{transition:none}}}}
#tip{{position:absolute;pointer-events:none;background:#211E2Bee;border:1px solid #3a3647;
  border-radius:6px;padding:7px 11px;font-size:12.5px;display:none;z-index:2;max-width:300px}}
#tip b{{color:#E3C377;display:block;font-size:13px}}
#tip span{{color:#A7A4B3}}
.filtered .n{{opacity:.10}}
.filtered .n.lit{{opacity:1}}
.filtered line.e{{opacity:.05}}
.filtered line.e.lit2{{opacity:.65;stroke:#E3C377}}
.filtered .fmark{{opacity:.3}}
.bar{{width:100%;max-width:1500px;margin-top:14px;display:flex;flex-direction:column;gap:7px}}
.bgroup{{display:flex;align-items:center;gap:6px;flex-wrap:wrap}}
.blabel{{font-size:10.5px;color:#8a879a;letter-spacing:.14em;flex:0 0 80px;text-transform:uppercase}}
.pchip{{background:transparent;border:1px solid #3a3647;border-radius:999px;color:#C9C6D4;
  font:500 11px "IBM Plex Mono",monospace;padding:4px 11px;cursor:pointer;letter-spacing:.05em;
  display:inline-flex;align-items:center;gap:6px}}
.pchip:hover{{border-color:#6b6880}}
.pchip.on{{background:#D4AF5E22;border-color:#D4AF5E;color:#E3C377}}
.pchip:focus-visible{{outline:2px solid #E3C377;outline-offset:1px}}
.pfam{{font-size:15px;padding:2px 8px;font-family:"Segoe UI Emoji","Apple Color Emoji","Noto Color Emoji",sans-serif}}
#fcount{{color:#E3C377;font-size:11.5px;margin-left:6px}}
footer{{color:#8a879a;font-size:11px;margin-top:10px;max-width:1500px;text-align:center}}
.bar{{background:#15131C;border:1px solid #2A2734;border-radius:12px;padding:12px 14px;gap:8px}}
.pchip{{padding:3px 10px}}
.pfam{{padding:2px 7px}}
#tip{{border-radius:8px;box-shadow:0 8px 28px #000A}}
h1{{letter-spacing:.06em}}
footer{{line-height:1.8}}
::selection{{background:#D4AF5E44}}
.pchip .pl{{font:500 10px "IBM Plex Mono",monospace;letter-spacing:.04em}}
.pfam{{font-size:14px;padding:2px 9px 2px 6px;gap:4px;font-family:inherit}}
#tip.pinned{{pointer-events:auto;border-color:#D4AF5E}}
#tip a{{color:#E3C377;display:inline-block;margin-top:4px;font-size:11.5px}}
#helpov{{position:fixed;inset:0;background:#000A;display:none;z-index:20;align-items:center;justify-content:center;padding:20px}}
#helpov.on{{display:flex}}
#helpov .card{{background:#1B1822;border:1px solid #3a3647;border-radius:12px;padding:20px 26px;max-width:430px;font-size:12.5px;line-height:2.1}}
#helpov b{{color:#E3C377;display:block;margin-bottom:4px}}
#helpov kbd{{border:1px solid #3a3647;border-bottom-width:2px;border-radius:4px;padding:0 6px;font:500 11px "IBM Plex Mono",monospace;background:#211E2B}}
svg.filtered.hov .n.lit{{opacity:.45}}
#fpanel{{position:absolute;top:14px;display:none;z-index:3;background:#1B1822F2;
  border:1px solid #3a3647;border-radius:10px;padding:10px 12px;width:230px;
  max-height:calc(100% - 28px);overflow-y:auto;font-size:12px;scrollbar-width:thin;
  scrollbar-color:#3a3647 transparent}}
.fph{{font:600 11px "IBM Plex Mono",monospace;color:#E3C377;text-transform:uppercase;
  letter-spacing:.08em;margin:10px 0 5px}}
.fph:first-child{{margin-top:0}}
.fph em{{color:#8a879a;font-style:normal;margin-left:4px}}
.fpr{{display:flex;align-items:center;gap:8px;padding:2.5px 4px;border-radius:5px;cursor:default}}
.fpr:hover{{background:#D4AF5E1f}}
.fpr img{{width:20px;height:20px;border-radius:4px;flex:0 0 20px}}
.fpr .fpn{{width:20px;height:20px;border-radius:4px;background:#322D3B;flex:0 0 20px;display:inline-block}}
</style>
<header>
  <div class="topline">
    <div><h1>Spell Constellations</h1><div class="sub" id="sub"></div></div>
    <div class="segrow">
      <div class="seg">
        <button data-v="fam">BY FAMILY</button>
        <button data-v="cls">BY CLASS</button>
        <button data-v="sch">BY SCHOOL</button>
        <button data-v="pur">BY PURPOSE</button>
      </div>
      <button id="copybtn" class="pchip" title="Copy the current view (with active filters) as a PNG image">⧉ copy image</button>
      <button id="helpbtn" class="pchip" title="Keyboard shortcuts">?</button>
    </div>
  </div>
  <div class="legend" id="leg"></div>
</header>
<div class="wrap">
  <div class="view" data-v="fam"><svg viewBox="0 0 {W} {H}" role="img" aria-label="Spells clustered by template family">
    <defs><filter id="blur"><feGaussianBlur stdDeviation="26"/></filter></defs>{SVG_FAM}</svg></div>
  <div class="view" data-v="cls"><svg viewBox="0 0 {W} {H}" role="img" aria-label="Spells clustered by class ownership">
    <defs><filter id="blur2"><feGaussianBlur stdDeviation="30"/></filter></defs>{SVG_CLS}</svg></div>
  <div class="view" data-v="sch"><svg viewBox="0 0 {W} {H}" role="img" aria-label="Spells clustered by school of magic">
    <defs><filter id="blur3"><feGaussianBlur stdDeviation="30"/></filter></defs>{SVG_SCH}</svg></div>
  <div class="view" data-v="pur"><svg viewBox="0 0 {W} {H}" role="img" aria-label="Spells clustered by functional purpose">
    <defs><filter id="blur4"><feGaussianBlur stdDeviation="30"/></filter></defs>{SVG_PUR}</svg></div>
  <div id="tip"></div>
  <div id="fpanel"></div>
</div>
<div class="bar">
  <div class="bgroup"><span class="blabel">Classes</span>{pick_cls}</div>
  <div class="bgroup"><span class="blabel">Schools</span>{pick_sch}</div>
  <div class="bgroup"><span class="blabel">Families</span>{pick_tier}{pick_fam}</div>
  <div class="bgroup"><span class="blabel">Purposes</span>{pick_pur}</div>
  <div class="bgroup"><span class="blabel"></span>
    <button class="pchip" id="clear">✕ clear</button><span id="fcount" aria-live="polite"></span></div>
</div>
<footer>⌨ press ? for all shortcuts · ←/→ cycles through the active layout's groups · ↑/↓ or 1–4 switches layouts · esc clears ·
pick a clustering method above · toggle the pickers below to light up overlaps in any layout —
classes intersect (Cleric + Wizard = spells on both lists), schools and families add ·
lines (family view) connect mechanics ≥ 0.88 similar · hover any spell, class name, or family mark ·
icons © Larian Studios &amp; Wizards of the Coast</footer>
<div id="helpov" role="dialog" aria-label="Keyboard shortcuts"><div class="card">
<b>Keyboard &amp; mouse</b>
<kbd>&larr;</kbd> <kbd>&rarr;</kbd> cycle the active layout's groups<br>
<kbd>&uarr;</kbd> <kbd>&darr;</kbd> or <kbd>1</kbd>&ndash;<kbd>4</kbd> switch layouts<br>
<kbd>esc</kbd> close &middot; unpin &middot; clear filters<br>
<kbd>?</kbd> this overlay<br>
click a spell to pin its card; click again to release<br>
<kbd>ctrl</kbd>+scroll zooms &middot; drag pans when zoomed &middot; double-click resets
</div></div>
<script>
const ICONS = {json.dumps(ICON_URIS)};
const SUBS = {{fam: "{len(POP)} spells · similar mechanics attract · variants orbit their container",
  cls: "{len(DPOP)} spells drawn toward every class that learns them · brighter = more shared",
  sch: "{len(DPOP)} spells grouped by school of magic · rings colored by family tier",
  pur: "{len(DPOP)} spells grouped by what they are for · rings colored by family tier"}};
const LEGS = {{fam: `{tier_chips}<span class="chip"><span class="ringchip"></span>variants orbit</span>`,
  cls: `{ramp_chips}`, sch: `{tier_chips}`, pur: `{tier_chips}`}};
document.querySelectorAll('image.sic').forEach(el => {{
  const d = ICONS[el.dataset.i];
  if (d) el.setAttribute('href', d); else el.remove();
}});
const FAMTITLE = {json.dumps({f["slug"]: f["title"] for f in C.F})};
const PURSHORT = {json.dumps({p: PUR_SHORT[p] for p in PURS})};
const FAMMEM = {json.dumps({f["slug"]: [[icon_uri(m) or "", BY[m]["name"]] for m in f["members"]] for f in C.F})};
const tip = document.getElementById('tip'), wrap = document.querySelector('.wrap');
function show(v) {{
  document.querySelectorAll('.view').forEach(x => x.classList.toggle('on', x.dataset.v === v));
  document.querySelectorAll('.seg button').forEach(b => {{ b.classList.toggle('on', b.dataset.v === v); b.setAttribute('aria-pressed', b.dataset.v === v ? 'true' : 'false'); }});
  document.getElementById('sub').textContent = SUBS[v];
  document.getElementById('leg').innerHTML = LEGS[v];
  try {{ localStorage.setItem('constellation-view', v); }} catch (e) {{}}
  updateCount();
}}

// ---- overlap pickers -------------------------------------------------
const state = {{cls: new Set(), sch: new Set(), tier: new Set(), fam: new Set(), pur: new Set()}};
function matches(n) {{
  const d = n.dataset;
  for (const c of state.cls) if (!(d.cl || '').includes('|' + c + '|')) return false;
  if (state.sch.size && !state.sch.has(d.sc)) return false;
  if (state.pur.size && !state.pur.has(d.pur)) return false;
  if ((state.tier.size + state.fam.size) &&
      !(state.tier.has(d.tier) || state.fam.has(d.fs))) return false;
  return true;
}}
function anySel() {{
  return state.cls.size + state.sch.size + state.tier.size + state.fam.size + state.pur.size > 0;
}}
function updateCount() {{
  const any = anySel();
  const el = document.getElementById('fcount');
  if (!any) {{ el.textContent = ''; saveState(); updatePanel(); return; }}
  const act = document.querySelector('.view.on svg');
  const litN = act.querySelectorAll('.n.lit').length;
  const parts = [];
  if (state.cls.size) parts.push([...state.cls].join(' \u2229 '));
  if (state.sch.size) parts.push([...state.sch].join(' + '));
  const tf = [...state.tier].concat([...state.fam].map(s => FAMTITLE[s] || s));
  if (tf.length) parts.push(tf.join(' + '));
  if (state.pur.size) parts.push([...state.pur].map(p => PURSHORT[p] || p).join(' + '));
  el.textContent = litN + ' spells lit' + (parts.length ? ' \u2014 ' + parts.join(' \u00b7 ') : '');
  saveState();
  updatePanel();
}}
function applyFilter() {{
  const any = anySel();
  document.querySelectorAll('.view svg').forEach(svg => {{
    svg.classList.toggle('filtered', any);
    const lit = new Set();
    svg.querySelectorAll('.n').forEach(n => {{
      const ok = any && matches(n);
      n.classList.toggle('lit', ok);
      if (ok && n.dataset.i !== undefined) lit.add(n.dataset.i);
    }});
    svg.querySelectorAll('line.e').forEach(l => {{
      const ids = [...l.classList].filter(c => /^e\\d+$/.test(c)).map(c => c.slice(1));
      l.classList.toggle('lit2', any && ids.length === 2 && ids.every(i => lit.has(i)));
    }});
  }});
  updateCount();
}}
document.querySelectorAll('.pchip[data-g]').forEach(b => {{
  b.addEventListener('click', () => {{
    const set = state[b.dataset.g];
    if (set.has(b.dataset.val)) set.delete(b.dataset.val); else set.add(b.dataset.val);
    b.classList.toggle('on');
    applyFilter();
  }});
}});
document.getElementById('clear').addEventListener('click', () => {{
  Object.values(state).forEach(s => s.clear());
  document.querySelectorAll('.pchip.on').forEach(b => b.classList.remove('on'));
  applyFilter();
}});
document.querySelectorAll('.seg button').forEach(b =>
  b.addEventListener('click', () => show(b.dataset.v)));
function updatePanel() {{
  document.querySelectorAll('.view svg').forEach(s => {{
    s.classList.remove('hov');
    s.querySelectorAll('.hl').forEach(x => x.classList.remove('hl'));
  }});
  const fp = document.getElementById('fpanel');
  const sel = [...state.fam];
  if (!sel.length) {{ fp.style.display = 'none'; return; }}
  let html = '';
  for (const s of sel) {{
    const mem = FAMMEM[s] || [];
    html += '<div class="fph">' + (FAMTITLE[s] || s) + '<em>' + mem.length + '</em></div>';
    for (const m of mem) {{
      const ic = ICONS[m[0]];
      html += '<div class="fpr" data-n="' + m[1].split('"').join('&quot;') + '">' +
        (ic ? '<img src="' + ic + '" alt="">' : '<span class="fpn"></span>') +
        '<span>' + m[1] + '</span></div>';
    }}
  }}
  fp.innerHTML = html;
  const svg = document.querySelector('.view.on svg');
  const wr = wrap.getBoundingClientRect();
  let sx = 0, cnt = 0;
  svg.querySelectorAll('.n.lit').forEach(nd => {{
    const r = nd.getBoundingClientRect();
    sx += r.left + r.width / 2; cnt++;
  }});
  const mid = cnt ? (sx / cnt - wr.left) : wr.width / 2;
  if (mid < wr.width / 2) {{ fp.style.right = '14px'; fp.style.left = 'auto'; }}
  else {{ fp.style.left = '14px'; fp.style.right = 'auto'; }}
  fp.style.display = 'block';
}}
document.getElementById('fpanel').addEventListener('mouseover', e => {{
  const row = e.target.closest('.fpr'); if (!row) return;
  const svg = document.querySelector('.view.on svg');
  svg.classList.add('hov');
  svg.querySelectorAll('.n').forEach(nd => nd.classList.toggle('hl', nd.dataset.name === row.dataset.n));
}});
document.getElementById('fpanel').addEventListener('mouseout', e => {{
  if (!e.target.closest('.fpr')) return;
  const svg = document.querySelector('.view.on svg');
  svg.classList.remove('hov');
  svg.querySelectorAll('.n.hl').forEach(x => x.classList.remove('hl'));
}});
function saveState() {{
  try {{ localStorage.setItem('constellation-filters', JSON.stringify({{cls: [...state.cls], sch: [...state.sch], tier: [...state.tier], fam: [...state.fam], pur: [...state.pur]}})); }} catch (e) {{}}
}}
try {{
  const fs = JSON.parse(localStorage.getItem('constellation-filters') || '{{}}');
  for (const g of ['cls', 'sch', 'tier', 'fam', 'pur']) (fs[g] || []).forEach(v => state[g].add(v));
  document.querySelectorAll('.pchip[data-g]').forEach(b => {{
    if (state[b.dataset.g].has(b.dataset.val)) b.classList.add('on');
  }});
  if (Object.values(state).some(s => s.size)) applyFilter();
}} catch (e) {{}}
let v0 = 'fam';
try {{ v0 = localStorage.getItem('constellation-view') || 'fam'; }} catch (e) {{}}
if (!['fam','cls','sch','pur'].includes(v0)) v0 = 'fam';
show(v0);
let pinned = null, suppressClick = false;
function tipLink(n) {{
  if (!n.dataset.fs || location.hostname.indexOf('claude') !== -1) return '';
  return '<br><a href="larian-codex.html#/families/' + n.dataset.fs + '">open family page \u2192</a>';
}}
function fillTip(n, withLink) {{
  tip.innerHTML = '<b>' + n.dataset.name + '</b><span>' + (n.dataset.sub || '') + '</span>' + (withLink ? tipLink(n) : '');
}}
function unpin() {{ pinned = null; tip.classList.remove('pinned'); tip.style.display = 'none'; }}
document.addEventListener('click', e => {{
  if (pinned && !e.target.closest('.n') && !e.target.closest('#tip')) unpin();
}});
document.querySelectorAll('.n').forEach(n => {{
  const svg = n.closest('svg');
  n.addEventListener('click', e => {{
    if (suppressClick) return;
    e.stopPropagation();
    if (pinned === n) {{ unpin(); return; }}
    pinned = n;
    fillTip(n, true);
    tip.classList.add('pinned');
    tip.style.display = 'block';
  }});
  n.addEventListener('mouseenter', () => {{
    svg.classList.add('hov');
    n.classList.add('hl');
    if (n.dataset.i !== undefined) {{
      svg.querySelectorAll('line.e' + n.dataset.i).forEach(l => {{
        l.classList.add('hl');
        const other = [...l.classList].find(c => /^e\\d+$/.test(c) && c !== 'e' + n.dataset.i);
        if (other) {{
          const on = svg.querySelector('.n[data-i="' + other.slice(1) + '"]');
          if (on) on.classList.add('hl');
        }}
      }});
    }}
    if (n.dataset.k !== undefined) {{
      svg.querySelectorAll('.sp' + n.dataset.k).forEach(l => {{
        l.classList.add('hl');
        svg.querySelectorAll('text.anchor[data-c="' + l.dataset.c + '"]').forEach(t => t.classList.add('hl'));
      }});
    }}
    if (!pinned) fillTip(n, false);
    tip.style.display = 'block';
  }});
  n.addEventListener('mousemove', e => {{
    if (pinned) return;
    const r = wrap.getBoundingClientRect();
    tip.style.left = Math.min(e.clientX - r.left + 14, r.width - 310) + 'px';
    tip.style.top = (e.clientY - r.top + 14) + 'px';
  }});
  n.addEventListener('mouseleave', () => {{
    svg.classList.remove('hov');
    svg.querySelectorAll('.hl').forEach(x => x.classList.remove('hl'));
    if (pinned) {{ fillTip(pinned, true); }} else {{ tip.style.display = 'none'; }}
  }});
}});
// ---- keyboard: arrows cycle groups/layouts, digits jump, esc clears ---
const VIEWS = ['fam', 'cls', 'sch', 'pur'];
const CYCLE = {{fam: {json.dumps([f["slug"] for f in C.F])},
  cls: {json.dumps(CLASSES)}, sch: {json.dumps(SCHOOLS)}, pur: {json.dumps(PURS)}}};
const CYCLE_GROUP = {{fam: 'fam', cls: 'cls', sch: 'sch', pur: 'pur'}};
function selectOnly(g, val) {{
  state[g].clear();
  if (val !== null) state[g].add(val);
  document.querySelectorAll('.pchip[data-g="' + g + '"]').forEach(b =>
    b.classList.toggle('on', b.dataset.val === val));
  applyFilter();
}}
function cycleGroup(dir) {{
  const v = document.querySelector('.view.on').dataset.v;
  const g = CYCLE_GROUP[v], vals = CYCLE[v];
  const cur = state[g].size === 1 ? vals.indexOf([...state[g]][0]) : -1;
  const next = ((cur + dir) % (vals.length + 1) + vals.length + 1) % (vals.length + 1);
  selectOnly(g, next === vals.length ? null : vals[next]);
}}
document.addEventListener('keydown', e => {{
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  if (e.key === 'ArrowRight') {{ cycleGroup(1); e.preventDefault(); }}
  else if (e.key === 'ArrowLeft') {{ cycleGroup(-1); e.preventDefault(); }}
  else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {{
    const i = VIEWS.indexOf(document.querySelector('.view.on').dataset.v);
    show(VIEWS[(i + (e.key === 'ArrowDown' ? 1 : -1) + VIEWS.length) % VIEWS.length]);
    e.preventDefault();
  }}
  else if (e.key >= '1' && e.key <= '4') show(VIEWS[+e.key - 1]);
  else if (e.key === 'Escape') {{
    const ov = document.getElementById('helpov');
    if (ov.classList.contains('on')) ov.classList.remove('on');
    else if (pinned) unpin();
    else document.getElementById('clear').click();
  }}
  else if (e.key === '?') document.getElementById('helpov').classList.toggle('on');
}});

// hover a class/school name -> highlight every spell it owns
document.querySelectorAll('text.anchor').forEach(a => {{
  const svg = a.closest('svg');
  const view = a.closest('.view').dataset.v;
  const c = a.dataset.c;
  const sel = view === 'cls' ? '.n[data-cl*="|' + c + '|"]'
    : view === 'pur' ? '.n[data-pur="' + c + '"]' : '.n[data-sc="' + c + '"]';
  a.addEventListener('mouseenter', () => {{
    svg.classList.add('hov');
    a.classList.add('hl');
    svg.querySelectorAll(sel).forEach(n => n.classList.add('hl'));
    svg.querySelectorAll('.sp[data-c="' + c + '"]').forEach(l => l.classList.add('hl'));
  }});
  a.addEventListener('mouseleave', () => {{
    svg.classList.remove('hov');
    svg.querySelectorAll('.hl').forEach(x => x.classList.remove('hl'));
  }});
}});
// ---- copy the active view as a PNG image -----------------------------
async function exportPNG() {{
  const live = document.querySelector('.view.on svg');
  const clone = live.cloneNode(true);
  if (live.classList.contains('filtered')) {{     // bake CSS filter state into attributes
    clone.querySelectorAll('.n').forEach(n =>
      n.setAttribute('opacity', n.classList.contains('lit') ? '1' : '0.10'));
    clone.querySelectorAll('line.e').forEach(l => {{
      if (l.classList.contains('lit2')) {{
        l.setAttribute('stroke', '#E3C377');
        l.setAttribute('stroke-opacity', '0.65');
      }} else {{
        l.setAttribute('opacity', '0.05');
      }}
    }});
    clone.querySelectorAll('.fmark').forEach(t => t.setAttribute('opacity', '0.3'));
  }}
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

// hover a family mark -> highlight its members
document.querySelectorAll('.fmark').forEach(a => {{
  const svg = a.closest('svg');
  a.addEventListener('mouseenter', () => {{
    svg.classList.add('hov');
    a.classList.add('hl');
    svg.querySelectorAll('.n[data-fs="' + a.dataset.f + '"]').forEach(n => n.classList.add('hl'));
  }});
  a.addEventListener('mouseleave', () => {{
    svg.classList.remove('hov');
    svg.querySelectorAll('.hl').forEach(x => x.classList.remove('hl'));
  }});
}});

document.getElementById('helpbtn').addEventListener('click', () =>
  document.getElementById('helpov').classList.toggle('on'));
document.getElementById('helpov').addEventListener('click', e => {{
  if (e.target.id === 'helpov') e.target.classList.remove('on');
}});
document.querySelectorAll('.view svg').forEach(svg => {{
  const vb0 = svg.getAttribute('viewBox').split(' ').map(Number);
  const base = {{x: vb0[0], y: vb0[1], w: vb0[2], h: vb0[3]}};
  const st = {{x: base.x, y: base.y, w: base.w, h: base.h}};
  const apply = () => svg.setAttribute('viewBox', st.x + ' ' + st.y + ' ' + st.w + ' ' + st.h);
  svg.addEventListener('wheel', e => {{
    if (!e.ctrlKey && !e.metaKey) return;
    e.preventDefault();
    const f = e.deltaY < 0 ? 0.85 : 1 / 0.85;
    const nw = Math.min(base.w, Math.max(base.w / 8, st.w * f));
    const sc = nw / st.w;
    const r = svg.getBoundingClientRect();
    const mx = st.x + (e.clientX - r.left) / r.width * st.w;
    const my = st.y + (e.clientY - r.top) / r.height * st.h;
    st.x = mx - (mx - st.x) * sc;
    st.y = my - (my - st.y) * sc;
    st.w = nw; st.h = nw * base.h / base.w;
    st.x = Math.min(Math.max(st.x, base.x), base.x + base.w - st.w);
    st.y = Math.min(Math.max(st.y, base.y), base.y + base.h - st.h);
    svg.style.cursor = st.w < base.w ? 'grab' : '';
    apply();
  }}, {{passive: false}});
  let drag = null;
  svg.addEventListener('pointerdown', e => {{
    if (st.w >= base.w) return;
    drag = {{px: e.clientX, py: e.clientY, x: st.x, y: st.y, moved: false}};
  }});
  svg.addEventListener('pointermove', e => {{
    if (!drag) return;
    const r = svg.getBoundingClientRect();
    if (Math.abs(e.clientX - drag.px) + Math.abs(e.clientY - drag.py) > 4) drag.moved = true;
    st.x = Math.min(Math.max(drag.x - (e.clientX - drag.px) / r.width * st.w, base.x), base.x + base.w - st.w);
    st.y = Math.min(Math.max(drag.y - (e.clientY - drag.py) / r.height * st.h, base.y), base.y + base.h - st.h);
    apply();
  }});
  ['pointerup', 'pointerleave'].forEach(ev => svg.addEventListener(ev, () => {{
    if (drag && drag.moved) {{ suppressClick = true; setTimeout(() => {{ suppressClick = false; }}, 60); }}
    drag = null;
  }}));
  svg.addEventListener('dblclick', () => {{
    st.x = base.x; st.y = base.y; st.w = base.w; st.h = base.h;
    svg.style.cursor = ''; apply();
  }});
}});
</script>
"""
with open("cluster_map.html", "w", encoding="utf-8") as fh:
    fh.write(HTML)
print(f"cluster_map.html: {os.path.getsize('cluster_map.html') / 1024:.0f} KB, "
      f"{len(ICON_URIS)} shared icons, schools: {', '.join(SCHOOLS)}")

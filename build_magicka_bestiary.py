"""Magicka Bestiary: real combat values from the install -> magicka_bestiary.html.

Renders magicka_bestiary.json (extracted from the game's LZX-compressed
CharacterTemplate XNBs): per enemy - hit points, elemental resistance
multipliers, and the AI's scripted casts as key sequences with their
trigger expressions. Run magicka_bestiary_extract.py first.
"""
import html as H
import json
import os
import re

rows = json.load(open("magicka_bestiary.json", encoding="utf-8"))
rows = [r for r in rows if r.get("hp")]
rows.sort(key=lambda r: -r["hp"])

ECOL = {"earth": "#8C6844", "water": "#3D7BD9", "cold": "#A8DCE8", "fire": "#E87A2D",
        "lightning": "#9B7BE8", "arcane": "#D9463E", "life": "#4FC46F",
        "shield": "#E8D44D", "ice": "#7FC4E8", "steam": "#C8CBD9"}
KEYCOL = {"D": "#8C6844", "Q": "#3D7BD9", "R": "#A8DCE8", "F": "#E87A2D",
          "A": "#9B7BE8", "S": "#D9463E", "W": "#4FC46F", "E": "#E8D44D",
          "QR": "#7FC4E8", "QF": "#C8CBD9"}

def pretty(fid):
    return re.sub(r"[_]+", " ", fid).strip().title()

body = []
n_res = n_cast = 0
for r in rows:
    res = ""
    for e in r["resist"]:
        col = ECOL[e["elem"]]
        lab = "IMMUNE" if e["imm"] or e["mult"] == 0 else f'×{e["mult"]:g}'
        if e["mult"] < 0:
            lab = f'HEALS ×{abs(e["mult"]):g}'
        extra = f' {e["mod"]:+g}' if e["mod"] else ""
        res += (f'<span class="rc" style="--c:{col}" title="{e["elem"]}">'
                f'{e["elem"][:2].upper()} {lab}{extra}</span>')
    if r["resist"]:
        n_res += 1
    casts = ""
    for c in r["casts"][:6]:
        seq = "".join(f'<b style="color:{KEYCOL[k]}">{k}</b>' for k in c["seq"])
        casts += (f'<span class="cs" title="{H.escape(c["cond"] or "always")} '
                  f'[{c["mode"]}]">{seq}</span>')
    if r["casts"]:
        n_cast += 1
    body.append(
        f'<tr><td class="nm">{H.escape(pretty(r["file"]))}</td>'
        f'<td class="hp">{r["hp"]:,}</td>'
        f'<td>{res or "<span class=mut>—</span>"}</td>'
        f'<td>{casts or "<span class=mut>—</span>"}</td></tr>')

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

HTML = f"""<title>Magicka Bestiary</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#101016;color:#E8E6EF;font:400 13px/1.55 "IBM Plex Mono",ui-monospace,monospace;
  min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:22px 18px 30px}}
header{{width:100%;max-width:1180px;display:flex;flex-direction:column;gap:10px;margin-bottom:12px}}
.topline{{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap}}
h1{{font:600 22px Cinzel,Georgia,serif;color:#E3C377;margin:0;letter-spacing:.06em}}
.sub{{color:#A7A4B3;font-size:11.5px}}
.segrow{{margin-left:auto;display:flex;align-items:center;gap:10px}}
.fsc{{display:inline-flex;align-items:center;gap:7px;border:1px solid #3a3647;
  border-radius:999px;padding:4px 12px;font:500 11px "IBM Plex Mono",monospace;color:#C9C6D4;
  text-decoration:none;letter-spacing:.05em}}
.fsc:hover{{border-color:#D4AF5E;color:#E3C377}}
#q{{width:100%;max-width:340px;padding:7px 12px;font:400 12.5px "IBM Plex Mono",monospace;
  color:#E8E6EF;background:#15131C;border:1px solid #3a3647;border-radius:8px}}
#q:focus{{outline:2px solid #E3C377;outline-offset:1px}}
.tw{{width:100%;max-width:1180px;overflow-x:auto;border:1px solid #2A2734;border-radius:12px;
  background:#15131C}}
table{{border-collapse:collapse;width:100%;font-size:12.5px}}
th{{font:600 10.5px "IBM Plex Mono",monospace;text-transform:uppercase;letter-spacing:.1em;
  color:#8a879a;text-align:left;padding:10px 12px;border-bottom:1px solid #2A2734;
  position:sticky;top:0;background:#15131C;cursor:pointer;user-select:none}}
th:hover{{color:#E3C377}}
td{{padding:6px 12px;border-bottom:1px solid #221F2B;vertical-align:top}}
tr:hover td{{background:#D4AF5E0d}}
td.nm{{white-space:nowrap;color:#E8E6EF}}
td.hp{{font-variant-numeric:tabular-nums;color:#E3C377;text-align:right;white-space:nowrap}}
.rc{{display:inline-block;border:1px solid color-mix(in srgb,var(--c) 55%,transparent);
  border-left:4px solid var(--c);border-radius:5px;padding:0 6px;margin:1px 3px 1px 0;
  font-size:11px;color:#C9C6D4;white-space:nowrap}}
.cs{{display:inline-block;border:1px solid #3a3647;border-radius:5px;padding:0 6px;
  margin:1px 3px 1px 0;font-size:11.5px;letter-spacing:.1em;cursor:help}}
.mut{{color:#4a4758}}
footer{{color:#8a879a;font-size:11px;margin-top:12px;max-width:1180px;text-align:center;line-height:1.8}}
::selection{{background:#D4AF5E44}}
</style>
<header>
  <div class="topline">
    <div><h1>Magicka Bestiary</h1>
    <div class="sub">real combat values from the install — the spell damage table decompiled from
Magicka.Defines (damage = base × √share of queue), then {len(rows)} enemies with
{n_res} resistance tables and {n_cast} scripted AI casts</div></div>
    <div class="segrow">{FSC}</div>
  </div>
  <input id="q" type="search" placeholder="filter {len(rows)} enemies…">
</header>
<div class="tw" style="margin-bottom:14px"><table>
<tr><th>Element</th><th>Forward cast</th><th>Self cast</th><th>Shield mine/ward</th><th>Notes (all from Magicka.Defines)</th></tr>
<tr><td class="nm" style="color:#9B7BE8">Lightning A</td><td class="hp">250</td><td class="hp">80</td><td class="hp">130</td><td>doubled on WET targets</td></tr>
<tr><td class="nm" style="color:#C8CBD9">Steam QF</td><td class="hp">280</td><td class="hp">80</td><td class="hp">225</td><td>the hardest forward base in the game — and it wets</td></tr>
<tr><td class="nm" style="color:#D9463E">Arcane S</td><td class="hp">225</td><td class="hp">200</td><td class="hp">225</td><td>beam; steady per tick</td></tr>
<tr><td class="nm" style="color:#7FC4E8">Ice QR</td><td class="hp">180</td><td class="hp">120</td><td class="hp">275</td><td>with Earth in the mix the pair jumps to 275</td></tr>
<tr><td class="nm" style="color:#8C6844">Earth D</td><td class="hp">150</td><td class="hp">100</td><td class="hp">—</td><td>physical — ×10 against FROZEN targets</td></tr>
<tr><td class="nm" style="color:#E87A2D">Fire F</td><td class="hp">60</td><td class="hp">60</td><td class="hp">225</td><td>+ BURNING: 60 status damage on a 0.2s tick</td></tr>
<tr><td class="nm" style="color:#A8DCE8">Cold R</td><td class="hp">25</td><td class="hp">—</td><td class="hp">—</td><td>the damage is a decoy — chill and FREEZE are the product</td></tr>
<tr><td class="nm" style="color:#3D7BD9">Water Q</td><td class="hp">0</td><td class="hp">—</td><td class="hp">—</td><td>push strength 70 · applies WET</td></tr>
<tr><td class="nm" style="color:#4FC46F">Life W</td><td class="hp">−180</td><td class="hp">−180</td><td class="hp">−600</td><td>negative = healing; the Life ward is a 600-point fountain</td></tr>
<tr><td class="nm" style="color:#E8D44D">Shield E</td><td class="hp">—</td><td class="hp">—</td><td class="hp">—</td><td>barrier HP 500 (elemental walls 100)</td></tr>
</table></div>
<div class="tw"><table id="t">
<tr><th data-k="0">Enemy</th><th data-k="1">HP</th><th>Resistances (damage ×)</th>
<th>AI casts (hover for trigger)</th></tr>
{chr(10).join(body)}
</table></div>
<footer>×0.5 = takes half damage from that element · IMMUNE = no damage · a negative multiplier heals ·
cast chips show the AI's queued element keys; hover shows the scripting condition — the cold cultist
self-casts F when wet and R when burning · extracted with an LZX decompressor from the local install's
Content/Data/Characters (heuristic parse of the binary CharacterTemplate; sequences and fields verified
on sampled enemies, but treat single odd rows with suspicion) ·
Magicka © Arrowhead Game Studios / Paradox Interactive</footer>
<script>
const q = document.getElementById('q');
const rows = [...document.querySelectorAll('#t tr')].slice(1);
q.addEventListener('input', () => {{
  const v = q.value.toLowerCase();
  rows.forEach(r => r.style.display = r.textContent.toLowerCase().includes(v) ? '' : 'none');
}});
document.querySelectorAll('th[data-k]').forEach(th => th.addEventListener('click', () => {{
  const k = +th.dataset.k;
  const dir = th.dataset.d === 'a' ? -1 : 1;
  document.querySelectorAll('th').forEach(x => delete x.dataset.d);
  th.dataset.d = dir === 1 ? 'a' : 'd';
  const body = rows[0].parentElement;
  rows.slice().sort((a, b) => {{
    const va = a.cells[k].textContent.trim(), vb = b.cells[k].textContent.trim();
    if (k === 1) return dir * ((+vb.replace(/,/g, '') || 0) - (+va.replace(/,/g, '') || 0));
    return dir * va.localeCompare(vb);
  }}).forEach(r => body.appendChild(r));
}}));
</script>
"""
with open("magicka_bestiary.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"magicka_bestiary.html: {os.path.getsize('magicka_bestiary.html') / 1024:.0f} KB "
      f"({len(rows)} enemies)")

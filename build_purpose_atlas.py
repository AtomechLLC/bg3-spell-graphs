"""Build the cross-game purpose taxonomy report -> purpose_atlas.html."""
import csv
import html as H
import os
from collections import defaultdict

from purpose_classify import PURPOSES

GAMES = ["D&D 5e SRD", "Baldur's Gate 3", "WoW Classic"]
GKEY = {"D&D 5e SRD": "srd", "Baldur's Gate 3": "bg3", "WoW Classic": "wow"}

rows = list(csv.DictReader(open("purpose_tagged.csv", encoding="utf-8")))
mat = defaultdict(lambda: defaultdict(list))
tot = defaultdict(int)
for r in rows:
    mat[r["purpose"]][r["game"]].append(r["ability"])
    tot[r["game"]] += 1

PEMOJI = {"damage": "💥", "offboost": "⚔️", "defboost": "🛡️", "negation": "🧯",
          "create": "🧞", "remove": "🕳️", "disable": "⛓️", "degrade": "🩸",
          "heal": "❤️‍🩹", "mobility": "🌀", "zone": "🕸️", "info": "👁️",
          "stealth": "🎭", "provision": "🧺", "threat": "😡", "roleshift": "🐻",
          "utility": "🔧"}

maxpct = max(100 * len(mat[p][g]) / tot[g] for p, *_ in PURPOSES for g in GAMES)

def bar_rows(user_flag):
    out = []
    for pk, label, user, defn in PURPOSES:
        if user != user_flag:
            continue
        cells = []
        for g in GAMES:
            n = len(mat[pk][g])
            pct = 100 * n / tot[g]
            w = 100 * pct / maxpct
            cells.append(
                f'<div class="brow"><span class="bar {GKEY[g]}" style="width:{w:.1f}%"></span>'
                f'<span class="bval">{pct:.1f}% <em>({n})</em></span></div>')
        out.append(f'''<div class="prow">
<div class="plabel"><span class="femoji">{PEMOJI[pk]}</span> <strong>{label}</strong>
<span class="pdef">{defn}</span></div>
<div class="pbars">{''.join(cells)}</div></div>''')
    return "\n".join(out)

def detail_sections():
    out = []
    for pk, label, user, defn in PURPOSES:
        total_n = sum(len(mat[pk][g]) for g in GAMES)
        chips = []
        for g in GAMES:
            for a in sorted(mat[pk][g]):
                chips.append(f'<span class="chip {GKEY[g]}">{H.escape(a)}</span>')
        out.append(f'''<details><summary><span class="femoji">{PEMOJI[pk]}</span>
<strong>{label}</strong> — {total_n} abilities <span class="pdef">{defn}</span></summary>
<div class="chips">{''.join(chips)}</div></details>''')
    return "\n".join(out)

HTML = f"""<title>The Purpose Atlas</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:wght@500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{
  --bg:#F4F5F2; --panel:#ECEEE9; --ink:#22262B; --muted:#5C645F; --line:#D6DAD2;
  --accent:#5A4FB0; --srd:#2a78d6; --bg3:#eb6834; --wow:#1baf7a; --code-bg:#E4E7E0;
}}
@media (prefers-color-scheme: dark){{
  :root:not([data-theme="light"]){{
    --bg:#191B1E; --panel:#22252A; --ink:#D6D8D2; --muted:#9AA29C; --line:#33373C;
    --accent:#A79BF0; --srd:#3987e5; --bg3:#d95926; --wow:#199e70; --code-bg:#2A2E33;
  }}
}}
:root[data-theme="dark"]{{
  --bg:#191B1E; --panel:#22252A; --ink:#D6D8D2; --muted:#9AA29C; --line:#33373C;
  --accent:#A79BF0; --srd:#3987e5; --bg3:#d95926; --wow:#199e70; --code-bg:#2A2E33;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);
  font:400 16.5px/1.62 "Source Serif 4",Georgia,serif;display:flex;justify-content:center;
  padding:40px 18px 70px}}
main{{max-width:860px;width:100%}}
h1{{font:600 34px/1.15 Spectral,Georgia,serif;margin:0 0 8px;text-wrap:balance}}
h2{{font:600 22px Spectral,Georgia,serif;margin:38px 0 12px}}
p{{margin:0 0 14px;max-width:70ch}}
.sub{{color:var(--muted);font:400 13px "IBM Plex Mono",monospace;margin-bottom:26px}}
.legend{{display:flex;gap:18px;flex-wrap:wrap;font:400 12.5px "IBM Plex Mono",monospace;
  color:var(--muted);margin:14px 0 6px}}
.dot{{width:11px;height:11px;border-radius:3px;display:inline-block;vertical-align:-1px;margin-right:6px}}
.prow{{display:grid;grid-template-columns:250px 1fr;gap:14px;padding:10px 0;
  border-bottom:1px solid var(--line);align-items:center}}
.plabel{{font-size:15px;line-height:1.35}}
.pdef{{display:block;color:var(--muted);font-size:12.5px;font-style:italic}}
.pbars{{display:flex;flex-direction:column;gap:3px}}
.brow{{display:flex;align-items:center;gap:8px;height:15px}}
.bar{{display:inline-block;height:11px;border-radius:2px;min-width:2px}}
.bar.srd{{background:var(--srd)}}
.bar.bg3{{background:var(--bg3)}}
.bar.wow{{background:var(--wow)}}
.bval{{font:400 11.5px "IBM Plex Mono",monospace;color:var(--muted);white-space:nowrap;
  font-variant-numeric:tabular-nums}}
.bval em{{font-style:normal;opacity:.7}}
details{{border:1px solid var(--line);border-radius:6px;margin:8px 0;background:var(--panel)}}
summary{{padding:10px 14px;cursor:pointer;font-size:15px}}
summary .pdef{{display:inline;margin-left:8px}}
.chips{{padding:4px 14px 14px;display:flex;flex-wrap:wrap;gap:5px}}
.chip{{font:400 12px "IBM Plex Mono",monospace;padding:2px 8px;border-radius:999px;
  border:1px solid var(--line);border-left-width:4px}}
.chip.srd{{border-left-color:var(--srd)}}
.chip.bg3{{border-left-color:var(--bg3)}}
.chip.wow{{border-left-color:var(--wow)}}
.femoji{{font-family:"Segoe UI Emoji","Apple Color Emoji","Noto Color Emoji",sans-serif;font-style:normal}}
ul{{margin:0 0 14px;padding-left:22px;max-width:75ch}}
li{{margin-bottom:8px}}
code{{font:500 13px "IBM Plex Mono",monospace;background:var(--code-bg);padding:1px 5px;border-radius:3px}}
footer{{margin-top:44px;padding-top:14px;border-top:1px solid var(--line);
  font-size:12.5px;color:var(--muted)}}
@media (max-width:640px){{.prow{{grid-template-columns:1fr}}}}
</style>
<main>
<h1>The Purpose Atlas</h1>
<div class="sub">what every spell is <em>for</em> — 953 abilities · three games · one functional taxonomy</div>

<p>The third axis of the homogeneity study. Families ask <em>how is it built</em>; class lists ask
<em>who owns it</em>; purpose asks <em>what is it for</em>. Every ability in the three datasets —
{tot['D&D 5e SRD']} D&amp;D SRD spells, {tot["Baldur's Gate 3"]} Baldur's Gate 3 spells,
{tot['WoW Classic']} WoW Classic abilities — classified into seventeen functional purposes:
seven requested, ten more that the data itself argues for.</p>

<div class="legend">
<span><span class="dot" style="background:var(--srd)"></span>D&amp;D 5e SRD</span>
<span><span class="dot" style="background:var(--bg3)"></span>Baldur's Gate 3</span>
<span><span class="dot" style="background:var(--wow)"></span>WoW Classic</span>
<span>share of each game's kit</span>
</div>

<h2>The seven requested purposes</h2>
{bar_rows(True)}

<h2>Ten more the data argues for</h2>
{bar_rows(False)}

<h2>What the divergences say</h2>
<ul>
<li><strong>💥 Damage share doubles from table to screen.</strong> 12.5% of the tabletop kit → 25.6%
of BG3's → 20.1% of WoW's. Real-time and encounter-driven games spend far more of their design
budget on hurting things.</li>
<li><strong>⛓️ Disables travel the opposite direction</strong> (17.9% → 13.3% → 9.0%). Tabletop
D&amp;D is a crowd-control game wearing a damage game's clothes; the MMO inverts it.</li>
<li><strong>😡 Threat control is the MMO's invention</strong> — 0% of the SRD, 2.6% of classic WoW
(taunts, feints, aggro dumps, Blessing of Salvation). BG3 carries a single tabletop-shaped echo
(Compelled Duel). This is the clearest case of a whole purpose being <em>born</em> in one medium.</li>
<li><strong>🕸️ Zone control is BG3's signature</strong> (8.5%, on the surface engine) and almost
absent from classic WoW (0.2%) — persistent ground effects don't fit a game about not standing still.</li>
<li><strong>🎭👁️ The tabletop pillars got gutted.</strong> Deception &amp; stealth (8.5% → ~3%) and
information (6.0% → 0.9% in BG3) shrink drastically on screen — the UI, camera, and quest log do
the jobs that illusion and divination spells did at the table.</li>
<li><strong>🐻 Role shift is WoW's quiet fourth pillar</strong> (4.0%: forms, stances, auras,
aspects) — exclusive-mode kit-swapping barely exists in the other two games.</li>
<li><strong>🧺 Provisioning follows the economy.</strong> WoW manufactures resources (5.9%: gems,
stones, food, water) because consumables are its economy; BG3 cut nearly all of it (0.5%) because
camp supplies made it redundant.</li>
</ul>

<h2>Every ability, by purpose</h2>
{detail_sections()}

<footer>Method: manual overrides &gt; reskin-family mapping &gt; ordered keyword rules on
tooltips/descriptions &gt; utility fallback ({sum(1 for r in rows if r['assigned_by']=='family')} by family,
{sum(1 for r in rows if r['assigned_by']=='rule')} by rule, {sum(1 for r in rows if r['assigned_by']=='override')} by
override, {sum(1 for r in rows if r['assigned_by']=='fallback')} fallback). Full tags in
<code>purpose_tagged.csv</code>. Part of the spell-homogeneity study: the Reskin Codex (SRD),
the Larian Codex (BG3), the Azeroth Codex (WoW Classic), and Spell Constellations.
Game content © Wizards of the Coast / Larian Studios / Blizzard Entertainment; research reference.</footer>
</main>
"""
with open("purpose_atlas.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"purpose_atlas.html: {os.path.getsize('purpose_atlas.html') / 1024:.0f} KB")

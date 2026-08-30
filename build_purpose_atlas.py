"""Build the cross-game purpose taxonomy report -> purpose_atlas.html."""
import csv
import html as H
import json
import os
from collections import defaultdict

from purpose_defs import PURPOSES

HOM = json.load(open("homogeneity.json", encoding="utf-8"))
COMP = json.load(open("class_comp.json", encoding="utf-8"))

GAMES = ["D&D 5e SRD", "Baldur's Gate 3", "WoW Classic"]
GKEY = {"D&D 5e SRD": "srd", "Baldur's Gate 3": "bg3", "WoW Classic": "wow"}

rows = list(csv.DictReader(open("purpose_tagged.csv", encoding="utf-8")))
mat = defaultdict(lambda: defaultdict(list))
tot = defaultdict(int)
for r in rows:
    mat[r["purpose"]][r["game"]].append(r["ability"])
    tot[r["game"]] += 1

from purpose_defs import PEMOJI

maxpct = max(100 * len(mat[p][g]) / tot[g] for p, *_ in PURPOSES for g in GAMES)

def bar_rows(user_flag):
    out = []
    for idx, (pk, label, user, defn) in enumerate(PURPOSES):
        if user != user_flag:
            continue
        cells = []
        pcts = {}
        for g in GAMES:
            n = len(mat[pk][g])
            pct = 100 * n / tot[g]
            pcts[GKEY[g]] = pct
            w = 100 * pct / maxpct
            cells.append(
                f'<div class="brow {GKEY[g]}"><span class="bar {GKEY[g]}" style="width:{w:.1f}%"></span>'
                f'<span class="bval">{pct:.1f}% <em>({n})</em></span></div>')
        out.append(f'''<div class="prow" data-idx="{idx}" data-srd="{pcts['srd']:.1f}" \
data-bg3="{pcts['bg3']:.1f}" data-wow="{pcts['wow']:.1f}">
<div class="plabel"><span class="femoji">{PEMOJI[pk]}</span> <strong>{label}</strong>
<span class="pdef">{defn}</span></div>
<div class="pbars">{''.join(cells)}</div></div>''')
    return "\n".join(out)

PKEYS = [p[0] for p in PURPOSES]
PLBL = {p[0]: p[1] for p in PURPOSES}

def hom_tiles():
    tiles = []
    for g in GAMES:
        h = HOM[g]
        tiles.append(f'''<div class="htile {GKEY[g]}">
<div class="hbig">{h['twin']}%</div>
<div class="hlab">{H.escape(g)}</div>
<div class="hsub">{h['rel']}% within 0.75 · n={h['n']}<br>measure: {h['measure']}</div></div>''')
    return "".join(tiles)

def comp_table(g):
    comp = COMP[g]
    gk = GKEY[g]
    classes = sorted(comp, key=lambda c: -sum(comp[c].values()))
    head = "".join(f'<th class="ph" title="{PLBL[p]}"><span class="femoji">{PEMOJI[p]}</span></th>'
                   for p in PKEYS)
    mx = max(100 * v / sum(comp[c].values()) for c in classes for v in comp[c].values())
    rws = []
    for c in classes:
        tot_c = sum(comp[c].values())
        cells = []
        for p in PKEYS:
            n = comp[c].get(p, 0)
            if n:
                pct = 100 * n / tot_c
                a = 0.10 + 0.90 * pct / mx
                lab = f"{pct:.0f}" if pct >= 8 else ""
                cells.append(f'<td class="hm {gk}" style="--a:{a:.2f}" '
                             f'title="{H.escape(c)} — {PLBL[p]}: {n} of {tot_c} ({pct:.0f}%)">{lab}</td>')
            else:
                cells.append('<td class="hm"></td>')
        rws.append(f'<tr><th class="cl">{H.escape(c)} <span class="cn">{tot_c}</span></th>'
                   f'{"".join(cells)}</tr>')
    return (f'<h3><span class="gdot" style="background:var(--{gk})"></span>{H.escape(g)}</h3>'
            f'<div class="tw"><table class="hmt"><tr><th></th>{head}</tr>{"".join(rws)}</table></div>')

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
::selection{{background:color-mix(in srgb,var(--accent) 24%,transparent)}}
h2{{text-wrap:balance}}
.prow{{transition:background .12s}}
.prow:hover{{background:color-mix(in srgb,var(--accent) 5%,transparent)}}
.chip{{background:var(--panel)}}
a{{color:var(--accent)}}
a:focus-visible,summary:focus-visible{{outline:2px solid var(--accent);outline-offset:2px;border-radius:3px}}
@media (prefers-reduced-motion: reduce){{.prow{{transition:none}}}}
h3{{font:600 16px Spectral,Georgia,serif;margin:24px 0 8px}}
.gdot{{width:11px;height:11px;border-radius:3px;display:inline-block;vertical-align:-1px;margin-right:7px}}
.htiles{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin:18px 0 8px}}
.htile{{border:1px solid var(--line);border-radius:10px;padding:16px 18px;background:var(--panel)}}
.htile.srd{{border-top:3px solid var(--srd)}}
.htile.bg3{{border-top:3px solid var(--bg3)}}
.htile.wow{{border-top:3px solid var(--wow)}}
.hbig{{font:600 36px/1 Spectral,Georgia,serif;font-variant-numeric:tabular-nums;margin-bottom:6px}}
.hlab{{font-size:14.5px;margin-bottom:4px}}
.hsub{{font:400 11px/1.6 "IBM Plex Mono",monospace;color:var(--muted)}}
.legend button{{all:unset;cursor:pointer;display:inline-flex;align-items:center;
  font:inherit;color:inherit;padding:2px 6px;border-radius:5px}}
.legend button:hover{{background:color-mix(in srgb,var(--accent) 8%,transparent)}}
.legend button:focus-visible{{outline:2px solid var(--accent);outline-offset:1px}}
.legend button[aria-pressed="false"]{{opacity:.38;text-decoration:line-through}}
body.hide-srd .brow.srd,body.hide-srd .chip.srd{{display:none}}
body.hide-bg3 .brow.bg3,body.hide-bg3 .chip.bg3{{display:none}}
body.hide-wow .brow.wow,body.hide-wow .chip.wow{{display:none}}
.sortbar{{display:flex;gap:6px;align-items:center;margin:8px 0 4px;flex-wrap:wrap;
  font:400 11.5px "IBM Plex Mono",monospace;color:var(--muted)}}
.sortbar button{{all:unset;cursor:pointer;font:500 11px "IBM Plex Mono",monospace;color:var(--muted);
  border:1px solid var(--line);border-radius:999px;padding:3px 11px}}
.sortbar button:hover{{border-color:var(--accent)}}
.sortbar button.on{{color:var(--accent);border-color:var(--accent);
  background:color-mix(in srgb,var(--accent) 10%,transparent)}}
.sortbar button:focus-visible{{outline:2px solid var(--accent);outline-offset:1px}}
.tw{{overflow-x:auto;border:1px solid var(--line);border-radius:8px;margin:6px 0 16px}}
.hmt{{border-collapse:collapse;font:400 10.5px "IBM Plex Mono",monospace;
  font-variant-numeric:tabular-nums;width:100%}}
.hmt th{{padding:5px 4px;font-weight:500;color:var(--muted)}}
.hmt th.ph{{font-size:13px;text-align:center;min-width:27px}}
.hmt th.cl{{text-align:left;white-space:nowrap;padding:3px 10px 3px 8px;font-size:11.5px;color:var(--ink)}}
.hmt .cn{{color:var(--muted);margin-left:4px;font-size:10px}}
.hmt td.hm{{width:27px;height:23px;text-align:center;border:1px solid var(--bg);border-radius:3px;
  color:var(--ink)}}
.hmt td.hm.srd{{background:color-mix(in srgb,var(--srd) calc(var(--a)*62%),transparent)}}
.hmt td.hm.bg3{{background:color-mix(in srgb,var(--bg3) calc(var(--a)*62%),transparent)}}
.hmt td.hm.wow{{background:color-mix(in srgb,var(--wow) calc(var(--a)*62%),transparent)}}
</style>
<main>
<h1>The Purpose Atlas</h1>
<div class="sub">what every spell is <em>for</em> — 953 abilities · three games · one functional taxonomy</div>

<p>The third axis of the homogeneity study. Families ask <em>how is it built</em>; class lists ask
<em>who owns it</em>; purpose asks <em>what is it for</em>. Every ability in the three datasets —
{tot['D&D 5e SRD']} D&amp;D SRD spells, {tot["Baldur's Gate 3"]} Baldur's Gate 3 spells,
{tot['WoW Classic']} WoW Classic abilities — classified into nineteen functional purposes:
seven requested, twelve more that the data itself argues for (including two the WoW remap
proposed: resource warfare and companion upkeep).</p>

<h2>The homogeneity index</h2>
<p>One number per game: the share of the kit whose <strong>nearest neighbour scores ≥ 0.85</strong>
on that game's own mechanical-similarity measure — abilities that have at least one near-twin
somewhere in the same game.</p>
<div class="htiles">{hom_tiles()}</div>
<p class="pdef" style="display:block;max-width:70ch">Caveat: each game is measured on its own
instrument. The SRD's masked-text ratio is far stricter than the stat-signature measures — text
must match, not just mechanics — so read the SRD tile as a floor, not a peer. The BG3 and WoW
numbers are directly comparable in spirit: both score decoded effect data.</p>

<div class="legend" role="group" aria-label="Toggle games">
<button data-g="srd" aria-pressed="true"><span class="dot" style="background:var(--srd)"></span>D&amp;D 5e SRD</button>
<button data-g="bg3" aria-pressed="true"><span class="dot" style="background:var(--bg3)"></span>Baldur's Gate 3</button>
<button data-g="wow" aria-pressed="true"><span class="dot" style="background:var(--wow)"></span>WoW Classic</button>
<span>share of each game's kit · click a game to hide it</span>
</div>
<div class="sortbar" role="group" aria-label="Sort purposes">sort:
<button data-k="idx" class="on">default</button>
<button data-k="srd">by SRD</button>
<button data-k="bg3">by BG3</button>
<button data-k="wow">by WoW</button>
</div>

<h2>The seven requested purposes</h2>
<div class="psec">
{bar_rows(True)}
</div>

<h2>Ten more the data argues for</h2>
<div class="psec">
{bar_rows(False)}
</div>

<h2>The WoW remap</h2>
<p>Applying the D&amp;D-derived map to WoW Classic and letting the ability data push back produced
two <strong>new major purposes</strong> and two <strong>culls</strong>. New: 🧛 <em>Resource
warfare</em> — mana burns, drains, and life taps that attack the resource system itself, a WoW
pillar with no real tabletop analog — and 🐕 <em>Companion upkeep</em>, the pet-lifecycle verbs
(call, tame, feed, mend, revive) that manage a summon rather than create one. Culled from the
WoW view: 🕸️ zone control and 🕳️ removing entities, each nearly empty there — Banish and Turn
Undead are re-read as what they play as in an MMO: disables. Classification for WoW leans on
<code>SpellEffect</code> mechanics (effect types and aura codes) rather than tooltip language.</p>

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

<h2>What is a class made of?</h2>
<p>Class composition profiles: each row is a class, each column a purpose, cell shading is the
purpose's share of that class's kit (numbers shown at ≥ 8%; hover any cell for exact counts).
Multi-list spells count once per class that owns them; classes sort by kit size.</p>
{comp_table("D&D 5e SRD")}
{comp_table("Baldur's Gate 3")}
{comp_table("WoW Classic")}

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
<script>
document.querySelectorAll('.legend button[data-g]').forEach(b => b.addEventListener('click', () => {{
  const g = b.dataset.g;
  document.body.classList.toggle('hide-' + g);
  b.setAttribute('aria-pressed', document.body.classList.contains('hide-' + g) ? 'false' : 'true');
}}));
document.querySelectorAll('.sortbar button').forEach(b => b.addEventListener('click', () => {{
  document.querySelectorAll('.sortbar button').forEach(x => x.classList.toggle('on', x === b));
  const k = b.dataset.k;
  document.querySelectorAll('.psec').forEach(sec => {{
    [...sec.querySelectorAll('.prow')]
      .sort((a, c) => k === 'idx' ? (+a.dataset.idx - +c.dataset.idx)
                                  : (+c.dataset[k] - +a.dataset[k]))
      .forEach(r => sec.appendChild(r));
  }});
}}));
</script>
"""
with open("purpose_atlas.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"purpose_atlas.html: {os.path.getsize('purpose_atlas.html') / 1024:.0f} KB")

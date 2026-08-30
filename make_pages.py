"""Wrap the artifact-style HTML fragments into standalone pages under docs/
for GitHub Pages, plus a landing page."""
import os
import re

PAGES = [
    ("wiki.html", "reskin-codex.html", "🧬"),
    ("bg3_codex.html", "larian-codex.html", "🦑"),
    ("wow_codex.html", "azeroth-codex.html", "🐉"),
    ("cluster_map.html", "constellations.html", "🌌"),
    ("wow_map.html", "azeroth-constellations.html", "🌠"),
    ("purpose_atlas.html", "purpose-atlas.html", "🎯"),
]
os.makedirs("docs", exist_ok=True)


def favicon(emoji):
    return ('<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 '
            f'viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>{emoji}</text></svg>">')


def wrap(src, dst, emoji):
    frag = open(src, encoding="utf-8").read()
    m = re.search(r"<title>(.*?)</title>\s*", frag)
    title = m.group(1) if m else dst
    frag = frag.replace(m.group(0), "", 1) if m else frag
    html = (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{title}</title>\n{favicon(emoji)}\n</head>\n<body>\n{frag}\n</body>\n</html>\n')
    with open(os.path.join("docs", dst), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"docs/{dst}: {os.path.getsize(os.path.join('docs', dst)) // 1024} KB — {title}")


for src, dst, emoji in PAGES:
    wrap(src, dst, emoji)

INDEX = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BG3 Spell Graphs</title>
{favicon("✨")}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Alegreya:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono&display=swap">
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#101016;color:#DCD3BF;font:400 16.5px/1.6 Alegreya,Georgia,serif;
  min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:60px 20px 40px}}
h1{{font:700 34px Cinzel,Georgia,serif;color:#E3C377;margin:0 0 6px;letter-spacing:.05em;
  text-align:center;text-wrap:balance}}
.sub{{color:#9A907B;font:400 12.5px "IBM Plex Mono",monospace;margin-bottom:44px;text-align:center}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;
  width:100%;max-width:980px}}
a.card{{display:block;background:#1D1A23;border:1px solid #322D3B;border-radius:10px;
  padding:26px 24px;color:inherit;text-decoration:none;transition:border-color .15s}}
a.card:hover{{border-color:#D4AF5E}}
.card .em{{font-size:30px;display:block;margin-bottom:10px}}
.card h2{{font:600 19px Cinzel,Georgia,serif;color:#E3C377;margin:0 0 8px}}
.card p{{margin:0;font-size:14.5px;color:#B4AC99}}
footer{{margin-top:52px;color:#8a879a;font-size:12px;max-width:760px;text-align:center;line-height:1.7}}
footer a{{color:#D4AF5E;text-decoration:none}}
</style>
</head>
<body>
<h1>BG3 Spell Graphs</h1>
<div class="sub">how often a game re-sells the same spell design — d&amp;d 5e srd vs. baldur's gate 3</div>
<div class="cards">
<a class="card" href="constellations.html"><span class="em">🌌</span><h2>Spell Constellations</h2>
<p>Interactive cluster map of all 213 BG3 class spells — switch between family, class, and school
layouts; toggle picker chips to light up overlaps.</p></a>
<a class="card" href="azeroth-constellations.html"><span class="em">🌠</span><h2>Azeroth Constellations</h2>
<p>The WoW twin of the cluster map: 423 classic abilities in four layouts — family, class, school,
and the WoW-remapped purpose taxonomy — with the same overlap pickers.</p></a>
<a class="card" href="larian-codex.html"><span class="em">🦑</span><h2>The Larian Codex</h2>
<p>The homogeneity analysis on BG3's own game data: 19 template families, 28 container spells,
duplicate SKUs, the surface engine, and the upcast clone farm.</p></a>
<a class="card" href="reskin-codex.html"><span class="em">🧬</span><h2>The Reskin Codex</h2>
<p>The tabletop companion: all 319 D&amp;D 5e SRD spells — 24 families of near-identical design,
per-class lists, and the cross-class overlap matrix.</p></a>
<a class="card" href="azeroth-codex.html"><span class="em">🐉</span><h2>The Azeroth Codex</h2>
<p>WoW Classic's 423 trainer abilities from the game's own data: 25 families, the cross-class
copy shop, and the rank clone farm — 69% of the spellbook is the same spell again.</p></a>
<a class="card" href="purpose-atlas.html"><span class="em">🎯</span><h2>The Purpose Atlas</h2>
<p>What every spell is <em>for</em>: 953 abilities across all three games in one functional
taxonomy — and the divergences that reveal each medium's design priorities.</p></a>
</div>
<footer>Includes content from the SRD 5.1 by Wizards of the Coast (CC-BY-4.0).
Baldur's Gate 3 data and icons © Larian Studios &amp; Wizards of the Coast, shown for research
reference. Pipeline and sources: <a href="https://github.com/AtomechLLC/bg3-spell-graphs">github.com/AtomechLLC/bg3-spell-graphs</a></footer>
</body>
</html>
"""
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(INDEX)
print("docs/index.html written")

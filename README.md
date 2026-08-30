# BG3 Spell Graphs

Research into **RPG skill homogeneity**: how often a game re-sells the same
ability design with a new coat of paint. Three datasets, one method — the D&D
5e SRD (tabletop), Baldur's Gate 3 (read from the game's pak files), and WoW
Classic Era (read from the client database, with wowhead cross-checks).

Live site: https://atomechllc.github.io/bg3-spell-graphs/

## Deliverables

| File | What it is |
|---|---|
| `wiki.html` | **The Reskin Codex** — 319 SRD spells: 24 reskin families, per-class lists, cross-class overlap matrix, missile index |
| `bg3_codex.html` | **The Larian Codex** — 211 BG3 class spells: 19 families, 28 container spells, the surface engine, the upcast clone farm (22% of the spell database) |
| `wow_codex.html` | **The Azeroth Codex** — 423 WoW Classic trainer abilities: 32 function-primary families at **100% coverage**, the mechanical-twin class matrix, the rank clone farm (~70% of the spellbook), and the Effects Ledger (per-ability effect boxes in wowhead vocabulary) |
| `cluster_map.html` | **Spell Constellations** — interactive BG3 cluster map: four layouts (family / class / school / purpose), overlap picker chips, keyboard cycling, copy-as-image |
| `wow_map.html` | **Azeroth Constellations** — the WoW twin of the cluster map, same features |
| `purpose_atlas.html` | **The Purpose Atlas** — all 953 abilities across the three games in one 19-purpose functional taxonomy, with per-game divergences and the WoW remap |
| `wiki/`, `bg3_wiki/`, `wow_wiki/` | Markdown sources for the codices (Karpathy-wiki pattern, `[[wikilinks]]`) |
| `*.csv`, `*_spells.json`, `purpose_tagged.csv`, `wow_effects.csv` | Machine-readable outputs |

Headline findings: reskin-family coverage runs 25% (SRD) → 39% (BG3) → 100%
(WoW, function-primary). Damage's share of the kit doubles from table to
screen while disables halve; threat control is a purpose born in the MMO;
zone control is BG3's invention; deception and information — tabletop
pillars — are gutted on screen. WoW's homogeneity is chiefly *cross-class*
(nine heals that are one heal; a druid whose feral kit photocopies the Rogue
and Warrior), BG3's is *explicit* (container spells), and the SRD's is
*editorial* (template families).

## Pipeline

**SRD:** `analyze_spells.py` (masked-text similarity) → `class_stats.py` →
`build_wiki.py`.

**BG3:** `bg3pak.py` (LSPK v18 reader) → `extract_bg3_data.py` →
`bg3_dataset.py` (stats + localization + progressions) → `bg3_analyze.py`
(mechanical signatures) → `build_bg3_codex.py` → `build_constellations.py`.
Icons via `extract_bg3_codex_icons.py` from an owned install.

**WoW:** wago.tools CSVs of the Classic Era client tables → `wow_dataset.py`
→ `wow_analyze.py` (0.6 × `SpellEffect` signature + 0.4 × masked tooltip) →
`wow_icons.py` / `wow_icons_fill.py` (warcraft.wiki.gg, CDN fallback) →
`wow_wowhead_pull.py` + `wow_effects_decode.py` (effect boxes, validated 78%
label-exact against wowhead pages) → `build_wow_codex.py` → `build_wow_map.py`.

**Cross-game:** `purpose_defs.py` + `purpose_classify.py` (overrides >
curated families > effect data > tooltip keywords) → `build_purpose_atlas.py`.

**Site:** `make_pages.py` wraps the deliverables into `docs/`; GitHub Pages
deploys `docs/` on push.

## Licensing

- SRD spell data: [5e-bits database](https://github.com/5e-bits/5e-database);
  includes content from the SRD 5.1 by Wizards of the Coast, **CC-BY-4.0**.
- Baldur's Gate 3 data and icons: **© Larian Studios & Wizards of the Coast**.
- WoW Classic data and icons: **© Blizzard Entertainment** (client tables via
  wago.tools; icons via warcraft.wiki.gg; effect boxes cross-checked against
  wowhead.com/classic).
- Raw extracted game files are deliberately not committed (`.gitignore`); the
  scripts regenerate them from owned installs and public tools. Built pages
  embed downscaled icons and short rules text for research reference, in the
  spirit of community wikis — not for commercial use.
- Analysis code and text: MIT-style, use freely.

# BG3 Spell Graphs

Research into **RPG skill homogeneity**: how often a game re-sells the same
spell design with a new coat of paint. Two datasets, one method — the D&D 5e
SRD (tabletop) and Baldur's Gate 3 (read directly from the game's pak files).

## Deliverables

| File | What it is |
|---|---|
| `wiki.html` | **The Reskin Codex** — interlinked wiki over the 319 SRD spells: 23 template families, per-class lists, cross-class overlap matrix |
| `bg3_codex.html` | **The Larian Codex** — the same analysis on BG3's own data: 211 class spells, 19 families, 28 container spells, the surface engine, the upcast clone farm |
| `cluster_map.html` | **Spell Constellations** — interactive cluster map with three switchable layouts (by family / by class / by school) and overlap picker chips |
| `wiki/`, `bg3_wiki/` | Markdown sources for both codices (Karpathy-wiki pattern, `[[wikilinks]]`) |
| `*.csv`, `clusters.json`, `bg3_spells.json` | Machine-readable analysis outputs |

Headline numbers: 23% of SRD spells sit in a reskin family; BG3 raises that to
37% and adds explicit reskin machinery — 28 container spells wrapping 136
variant children, duplicate per-class SKUs of the same spell (Shield ×3,
similarity 1.000), and 1,012 of 4,614 SpellData entries (22%) that exist only
to implement upcasting as cloned entries.

## Pipeline

SRD side: `analyze_spells.py` (masked-text similarity over all spell pairs) →
`class_stats.py` (overlap matrix) → `build_wiki.py`.

BG3 side: `bg3pak.py` (minimal LSPK v18 pak reader) → `extract_bg3_data.py`
(stats txt, SpellLists.lsx, Progressions.lsx, english.loca) →
`bg3_dataset.py` (inheritance-resolved spell records + class attribution) →
`bg3_analyze.py` (mechanical-signature similarity) → `build_bg3_codex.py` →
`build_constellations.py` (force layouts + the cluster maps).
`extract_bg3_codex_icons.py` pulls each spell's icon (BC7 DDS → 64px PNG).

To regenerate the BG3 half, point the `BG3` path constants at your own
install and run the scripts in that order. Requires Python 3.12+ with
`pillow`, `lz4`, `zstandard`.

## Licensing

- SRD spell data: from the [5e-bits database](https://github.com/5e-bits/5e-database);
  includes content from the SRD 5.1 by Wizards of the Coast, **CC-BY-4.0**.
- Baldur's Gate 3 spell data and icons: **© Larian Studios & Wizards of the
  Coast**. Raw extracted game files are deliberately not committed
  (`.gitignore`); the extraction scripts regenerate them from an owned copy of
  the game. The built HTML pages embed downscaled icons and short rules text
  for research reference, in the spirit of community wikis — not for
  commercial use.
- Analysis code and text: MIT-style, use freely.

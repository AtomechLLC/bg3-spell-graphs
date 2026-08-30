# Methodology

**Source.** The [SRD 5.1 spell database](https://github.com/5e-bits/5e-database) (the dataset behind dnd5eapi.co) — all **319 spells** of the 2014 System Reference Document with full rules text and per-class lists. Includes content from the SRD 5.1 by Wizards of the Coast, CC-BY-4.0. D&D Beyond was not scraped: its terms block automated access, and its spell content beyond the SRD is paywalled licensed material.

**Pipeline.**

1. **Mask the flavor.** Lowercase each spell description, then replace surface variables with tokens: damage types → `DMG`, element words (flame, frost, shock…) → `ELEM`, creature words (beast, humanoid, fey…) → `CRT`, ability names → `ABL`, dice expressions → `DICE`, all numbers → `N`.
2. **Compare structure.** Token-level `difflib.SequenceMatcher` ratio (autojunk off) over every pair of masked descriptions — 50,721 pairs.
3. **Cluster.** Union-find over pairs above 0.72 seeds the clone groups; the 0.60–0.72 band plus mechanical judgment fills out the template and engine tiers.

After masking, two spells that differ only in damage type, dice, or target creature become near-identical strings — which is precisely the definition of a reskin.

**What the score misses.** It reads *wording*, not *rules*. A copied spell with one extra sentence loses several points ([[families/hold|Hold Person/Monster]], 0.69); two spells with the same mechanic written by different hands score low ([[families/speak-with|the Speak-With series]]). Tier calls on [[findings|the list]] therefore combine the metric with a mechanical read.

**Known limits.** The SRD is a subset of the 2014 Player's Handbook (319 of 361 spells — no Chromatic Orb, no subclass-expansion lists), and excludes later books entirely; notably Tasha's *Summon X* series, the most aggressively templated spell family in 5e, cannot be measured here. The 2024 revision is also out of scope.

**Icons.** Spell rows carry the spell's *Baldur's Gate 3* icon where the spell exists in BG3 (184 of 319 — itself a rough measure of which SRD spells survived into the video-game adaptation, which caps at 6th-level slots). Icons were extracted from a locally owned BG3 install (`Game.pak` controller-UI DDS assets, downscaled to 64 px); © Larian Studios & Wizards of the Coast, embedded for private research reference.

**Reproduce.** `analyze_spells.py` builds `similar_pairs.csv`, `clusters.json`, and `spell_lists_per_class.csv`; `class_stats.py` prints the overlap matrix; `build_wiki.py` renders this wiki.

---
*Linked from: [[families/attack-cantrips|The Damage Cantrip Engine]] · [[families/bane-bless|Bane & Bless]] · [[families/blast|The Elemental Blast Template]] · [[families/conjure-single|Conjure a Champion]] · [[families/conjure-table|Conjure by Menu]] · [[families/cure|The Cure Family]] · [[families/darkness-daylight|Darkness & Daylight]] · [[families/detect|The Detect Series]] · [[families/disguise-seeming|The Disguise Ladder]] · [[families/dispel|The Dispel Engine]] · [[families/dominate|The Dominate Chain]] · [[families/guidance-resistance|Guidance & Resistance]] · [[families/hold|The Hold Pair]] · [[families/hp-pool|The Hit-Point Pool Engine]] · [[families/image|The Image Ladder]] · [[families/invisibility|The Invisibility Ladder]] · [[families/locate|The Locate Series]] · [[families/polymorph|The Polymorph Ladder]] · [[families/protection|The Protection Series]] · [[families/speak-with|The Speak-With Series]] · [[families/suggestion|The Suggestion Pair]] · [[families/touch-buffs|The Touch-Buff Skeleton]] · [[families/undead|The Undead Workshop]] · [[findings|The Identical-Spell List]] · [[missiles|Missile Spells]] · [[overview|Overview]] · [[spells|All Spells, Tagged]]*

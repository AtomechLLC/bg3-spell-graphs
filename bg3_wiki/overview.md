# How Homogeneous Are Baldur's Gate 3 Spells?

The companion codex to the tabletop study: the same homogeneity analysis, run on **Baldur's Gate 3's actual game data** — every spell reachable through class progressions, read straight from the install's pak files. The result: the video game is *more* homogeneous than the book, and honest about it.

## Axis 1 — the same spell, on many class lists

211 distinct spells fill 755 class-list slots (3.6 lists per spell). The most-shared spells sit on 8 of 11 lists: Bone Chill, Charm Person, Hold Person. Bard's Magical Secrets and the half-caster subclasses (Eldritch Knight, Arcane Trickster) import other classes' lists wholesale:

| ↓ list · shared with → | [[classes/bard|Bard]] | [[classes/cleric|Cleric]] | [[classes/druid|Druid]] | [[classes/fighter|Fighter]] | [[classes/monk|Monk]] | [[classes/paladin|Paladin]] | [[classes/ranger|Ranger]] | [[classes/rogue|Rogue]] | [[classes/sorcerer|Sorcerer]] | [[classes/warlock|Warlock]] | [[classes/wizard|Wizard]] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [[classes/bard|Bard]] (122) | — | 56% | 33% | 32% | 0% | 13% | 12% | 32% | 52% | 31% | 61% |
| [[classes/cleric|Cleric]] (111) | 61% | — | 46% | 22% | 0% | 15% | 14% | 22% | 40% | 17% | 47% |
| [[classes/druid|Druid]] (68) | 59% | 75% | — | 21% | 0% | 7% | 24% | 21% | 44% | 10% | 46% |
| [[classes/fighter|Fighter]] (64) | 61% | 38% | 22% | — | 0% | 6% | 9% | 100% | 83% | 39% | 100% |
| [[classes/monk|Monk]] (0) |  |  |  |  | — |  |  |  |  |  |  |
| [[classes/paladin|Paladin]] (29) | 55% | 59% | 17% | 14% | 0% | — | 14% | 14% | 10% | 28% | 24% |
| [[classes/ranger|Ranger]] (25) | 60% | 60% | 64% | 24% | 0% | 16% | — | 24% | 32% | 8% | 32% |
| [[classes/rogue|Rogue]] (64) | 61% | 38% | 22% | 100% | 0% | 6% | 9% | — | 83% | 39% | 100% |
| [[classes/sorcerer|Sorcerer]] (96) | 67% | 46% | 31% | 55% | 0% | 3% | 8% | 55% | — | 40% | 93% |
| [[classes/warlock|Warlock]] (58) | 66% | 33% | 12% | 43% | 0% | 14% | 3% | 43% | 66% | — | 78% |
| [[classes/wizard|Wizard]] (118) | 63% | 44% | 26% | 54% | 0% | 6% | 7% | 54% | 75% | 38% | — |

## Axis 2 — different spells, same design

**83 of 211 spells sit in 19 template families** — see [[findings|The Identical-Spell List]]. Beyond the tabletop-inherited families, BG3 adds four homogenizers of its own:

- **[[containers|Container spells]]** — 28 spells whose cast button opens a menu of 136 variant children. The reskin as a shipped feature.
- **[[families/duplicate-skus|Duplicate SKUs]]** — Shield exists three times in the data, once per class that learns it. Similarity: 1.000.
- **[[families/surfaces|The surface engine]]** — Larian rebuilt tabletop's area spells on one ground-surface system; ten spells measure 0.88–0.96 on mechanics.
- **The upcast clone farm** — 22% of the entire spell database is numbered upcast copies ([[methodology|Methodology]]).

## Browse

- **Classes:** [[classes/bard|Bard]] · [[classes/cleric|Cleric]] · [[classes/druid|Druid]] · [[classes/fighter|Fighter]] · [[classes/monk|Monk]] · [[classes/paladin|Paladin]] · [[classes/ranger|Ranger]] · [[classes/rogue|Rogue]] · [[classes/sorcerer|Sorcerer]] · [[classes/warlock|Warlock]] · [[classes/wizard|Wizard]]
- **The list:** [[findings|The Identical-Spell List]] · **Containers:** [[containers|Container Spells]]
- **Every spell, tagged:** [[spells|All Spells, Tagged]] · **How:** [[methodology|Methodology]]

---
*Linked from: [[classes/bard|Bard]] · [[classes/cleric|Cleric]] · [[classes/druid|Druid]] · [[classes/fighter|Fighter]] · [[classes/monk|Monk]] · [[classes/paladin|Paladin]] · [[classes/ranger|Ranger]] · [[classes/rogue|Rogue]] · [[classes/sorcerer|Sorcerer]] · [[classes/warlock|Warlock]] · [[classes/wizard|Wizard]] · [[containers|Container Spells]] · [[spells|All Spells, Tagged]]*

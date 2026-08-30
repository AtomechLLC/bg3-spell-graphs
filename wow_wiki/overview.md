# How Homogeneous Are WoW Classic Spells?

The third dataset in the homogeneity study — and the most homogeneous of the three. Everything below is read from WoW Classic Era's own client database (423 trainer-taught class abilities), with icons from the community wiki. See [[findings|The Identical-Spell List]] for the full family catalogue and [[methodology|Methodology]] for the pipeline.

## Axis 0 — the rank clone farm

Before any reskin analysis: **70% of the classic spellbook is rank duplicates** (1388 entries for 423 abilities). BG3 hides its upcast clones in the data files; classic sells them at the trainer.

## Axis 1 — the same ability in several class books

Unlike D&D (where classes share one spell list) or BG3 (where lists overlap), classic WoW ships **the same design as separate class-branded spells**: nine heals that are [[families/heals|one heal]], five [[families/interrupts|interrupts]], the [[families/rez|resurrection franchise]], one [[families/protection|protection effect]] wearing armor, ward, and shield vocabularies across four classes, Cure Poison printed verbatim in two books, and the Feral Druid — a licensed photocopy of the Rogue and Warrior kits, now filed by function (its openers with [[families/melee-enhance|the strikes]], its roars in [[families/threat|the Aggro Ledger]], its prowl in [[families/concealment|the Vanishing Act]]). Because the *names* are the reskin, name sharing is near zero and useless as a measure — so the matrix below measures **mechanics**: the share of the row class's kit that has an effect-twin in the column class's book (a *different* ability with blended `SpellEffect`-signature similarity ≥ 0.75). Standouts: **20%** of the Rogue book has a twin in Druid's; **13%** of the Hunter book has a twin in Warlock's; **13%** of the Hunter book has a twin in Druid's.

| ↓ has effect-twins in → | [[classes/druid|Drui]] | [[classes/hunter|Hunt]] | [[classes/mage|Mage]] | [[classes/paladin|Pala]] | [[classes/priest|Prie]] | [[classes/rogue|Rogu]] | [[classes/shaman|Sham]] | [[classes/warlock|Warl]] | [[classes/warrior|Warr]] |
|---|---|---|---|---|---|---|---|---|---|
| [[classes/druid|Druid]] (53) | — | 4% | 2% | 8% | 8% | 11% | 6% | 2% | 6% |
| [[classes/hunter|Hunter]] (54) | 13% | — | 0% | 4% | 0% | 0% | 0% | 13% | 2% |
| [[classes/mage|Mage]] (51) | 2% | 0% | — | 0% | 10% | 0% | 2% | 8% | 0% |
| [[classes/paladin|Paladin]] (47) | 9% | 4% | 0% | — | 9% | 0% | 6% | 9% | 0% |
| [[classes/priest|Priest]] (44) | 9% | 0% | 11% | 7% | — | 0% | 7% | 5% | 0% |
| [[classes/rogue|Rogue]] (30) | 20% | 0% | 0% | 0% | 0% | — | 0% | 0% | 3% |
| [[classes/shaman|Shaman]] (45) | 11% | 0% | 2% | 4% | 9% | 0% | — | 2% | 2% |
| [[classes/warlock|Warlock]] (65) | 2% | 3% | 3% | 6% | 3% | 0% | 2% | — | 2% |
| [[classes/warrior|Warrior]] (34) | 9% | 3% | 0% | 0% | 0% | 3% | 3% | 3% | — |

**Internal redundancy** — the same measure pointed at each class's *own* book (how much of the kit has a different in-book twin): [[classes/mage|Mage]] **59%** · [[classes/warlock|Warlock]] **58%** · [[classes/shaman|Shaman]] **58%** · [[classes/paladin|Paladin]] **49%** · [[classes/hunter|Hunter]] **31%** · [[classes/druid|Druid]] **25%** · [[classes/priest|Priest]] **20%** · [[classes/rogue|Rogue]] **17%** · [[classes/warrior|Warrior]] **0%**. The teleport matrix, the totem foundry, and the conjured-stone commissary are why the top three look the way they do.

## Axis 2 — one chassis, many payloads

Classic's signature template shape is the **payload rack**: [[families/totems|21 totems]], [[families/status-boosts|24 status boosts]] (blessings, prayers, and auras), [[families/curses|8 curses]], [[families/tracking|10 tracking dials]], [[families/teleports|a 6×2 teleport matrix]], [[families/conjured|23 conjured consumables]], [[families/seals|6 seals]], [[families/poisons|5 poisons]], [[families/aspects|6 aspects]]. **387 of 423 abilities (91%) sit in 34 families.**

## Browse

- **Classes:** [[classes/druid|Druid]] · [[classes/hunter|Hunter]] · [[classes/mage|Mage]] · [[classes/paladin|Paladin]] · [[classes/priest|Priest]] · [[classes/rogue|Rogue]] · [[classes/shaman|Shaman]] · [[classes/warlock|Warlock]] · [[classes/warrior|Warrior]]
- **The list:** [[findings|The Identical-Spell List]] · **Every ability, tagged:** [[spells|All Abilities, Tagged]]
- **How:** [[methodology|Methodology]]

---
*Linked from: [[classes/druid|Druid]] · [[classes/hunter|Hunter]] · [[classes/mage|Mage]] · [[classes/paladin|Paladin]] · [[classes/priest|Priest]] · [[classes/rogue|Rogue]] · [[classes/shaman|Shaman]] · [[classes/warlock|Warlock]] · [[classes/warrior|Warrior]] · [[effects|The Effects Ledger]] · [[spells|All Abilities, Tagged]]*

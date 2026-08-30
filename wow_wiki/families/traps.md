# <span class="femoji">🪤</span> The Trap Line

<span class="plate"><span class="tier tier-template">Shared template</span><span class="pv"><b>4</b> abilities</span><span class="pv">similarity <b>0.77–0.91</b></span><span class="pv"><b>1</b> classes</span><span class="pv pvc">Hunter</span></span>

| Ability | Class | Level | School | Ranks | Tooltip |
|---|---|---|---|---|---|
| <img class="sic" data-i="frost-trap" alt=""> **Frost Trap** | Hunter | 28 | Frost | 1 | Place a frost trap that creates an ice slick around itself for X when the first enemy approaches it.  All enem |
| <img class="sic" data-i="explosive-trap" alt=""> **Explosive Trap** | Hunter | 54 | Fire | 3 | Place a fire trap that explodes when an enemy approaches, causing X Fire damage and X additional Fire damage o |
| <img class="sic" data-i="immolation-trap" alt=""> **Immolation Trap** | Hunter | 56 | Fire | 5 | Place a fire trap that will burn the first enemy to approach for X Fire damage over X.  Trap will exist for X. |
| <img class="sic" data-i="freezing-trap" alt=""> **Freezing Trap** | Hunter | 60 | Frost | 3 | Place a frost trap that freezes the first enemy that approaches, preventing all action for up to X.  Any damag |

**Shared skeleton.** All four run the identical `Summon Trap` effect (id 320 in the game data) — one buried trigger object, four payloads: burst fire, freeze, frost slow, immolation DoT. An effect-revealed family: the tooltips read differently, the machinery is one line.

**What varies.** The payload and its school; arming time and cooldown are shared.

**Design read.** The Hunter's [[families/totems|totem foundry]] inverted — instead of a standing object that helps allies, a buried object that ambushes enemies, stamped four times.

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/hunter|Hunter]] · [[findings|The Identical-Spell List]] · [[spells|All Abilities, Tagged]]*

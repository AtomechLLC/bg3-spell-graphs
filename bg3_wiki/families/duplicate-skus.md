# <span class="femoji">🛍️</span> The Duplicate SKUs

<span class="tier tier-clone">Verbatim clone</span><span class="pv"><b>5</b> spells</span><span class="pv">similarity <b>0.69–1.00</b></span><span class="pv"><b>7</b> classes</span><span class="pv pvc">Bard, Fighter, Paladin, Rogue, Sorcerer, Warlock, Wizard</span>

| Spell | Lv | School | Type | Cost | Damage | Save / Attack | Classes |
|---|---|---|---|---|---|---|---|
| <img class="sic" data-i="Shout_Shield_Sorcerer" alt=""> **Shield** | 1 | Abjuration | Shout | Reaction + L1 slot |  |  | [[classes/sorcerer|Sorcerer]] |
| <img class="sic" data-i="Shout_Shield_Warlock" alt=""> **Shield** | 1 | Abjuration | Shout | Reaction + L1 slot |  |  | [[classes/warlock|Warlock]] |
| <img class="sic" data-i="Shout_Shield_Wizard" alt=""> **Shield** | 1 | Abjuration | Shout | Reaction + L1 slot |  |  | [[classes/fighter|Fighter]], [[classes/rogue|Rogue]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Target_Darkness" alt=""> **Darkness** | 2 | Evocation | Target | Action + L2 slot |  |  | [[classes/bard|Bard]], [[classes/fighter|Fighter]], [[classes/paladin|Paladin]], [[classes/rogue|Rogue]], [[classes/sorcerer|Sorcerer]], [[classes/warlock|Warlock]], [[classes/wizard|Wizard]] |
| **Eyes of the Dark: Darkness** | 2 | Evocation | Target | Action |  |  | [[classes/sorcerer|Sorcerer]] |

**Shared skeleton.** Shield exists three times in the game data — `Shout_Shield_Sorcerer`, `Shout_Shield_Warlock`, `Shout_Shield_Wizard` — with measured similarity **1.000**: byte-identical mechanics, one entry per class that learns it. Darkness ships twice: once as the spell, once as the Shadow Magic sorcerer's 'Eyes of the Dark' feature grant (0.91 on mechanics).

**What varies.** The id string and which list references it. Nothing else.

**Design read.** The purest homogeneity in the game: not a reskin but a re-SKU. Larian duplicates entries so each grantor can own its copy — the same spell as three products. (Spirit Guardians pulls the same trick inside a [[containers|container]], with radiant/necrotic twins.)

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/bard|Bard]] · [[classes/fighter|Fighter]] · [[classes/paladin|Paladin]] · [[classes/rogue|Rogue]] · [[classes/sorcerer|Sorcerer]] · [[classes/warlock|Warlock]] · [[classes/wizard|Wizard]] · [[findings|The Identical-Spell List]] · [[overview|Overview]] · [[spells|All Spells, Tagged]]*

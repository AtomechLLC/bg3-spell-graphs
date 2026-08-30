# <span class="femoji">🩹</span> The Temp-HP Ledger

<span class="plate"><span class="tier tier-engine">Shared engine</span><span class="pv"><b>4</b> spells</span><span class="pv">similarity <b>0.76–0.85</b></span><span class="pv"><b>8</b> classes</span><span class="pv pvc">Bard, Cleric, Fighter, Paladin, Rogue, Sorcerer, Warlock, Wizard</span></span>

| Spell | Lv | School | Type | Cost | Damage | Save / Attack | Classes |
|---|---|---|---|---|---|---|---|
| <img class="sic" data-i="Shout_ArmorOfAgathys" alt=""> **Armour of Agathys** | 1 | Abjuration | Shout | Action + L1 slot |  |  | [[classes/bard|Bard]], [[classes/warlock|Warlock]] |
| <img class="sic" data-i="Shout_FalseLife" alt=""> **False Life** | 1 | Necromancy | Shout | Action + L1 slot |  |  | [[classes/bard|Bard]], [[classes/cleric|Cleric]], [[classes/fighter|Fighter]], [[classes/rogue|Rogue]], [[classes/sorcerer|Sorcerer]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Target_Heroism" alt=""> **Heroism** | 1 | Enchantment | Target | Action + L1 slot |  |  | [[classes/bard|Bard]], [[classes/paladin|Paladin]] |
| <img class="sic" data-i="Shout_Aid" alt=""> **Aid** | 2 | Abjuration | Shout | Action + L2 slot | heal `5` |  | [[classes/cleric|Cleric]], [[classes/paladin|Paladin]] |

**Shared skeleton.** One hidden engine, verified in the game data: temporary hit points share a single cap-and-pool system, so these spells literally overwrite each other's ledgers. False Life is the plain buffer, Armour of Agathys the buffer with cold-damage spikes, Heroism the per-turn refill, Aid the max-HP variant that sidesteps the ledger entirely.

**What varies.** The buffer size, the refill schedule, and the rider (retaliation damage, fear immunity, party-wide).

**Design read.** A shared engine invisible in tooltips and visible in the data — the same lesson WoW's absorb shields taught: one accountant, many product names.

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/bard|Bard]] · [[classes/cleric|Cleric]] · [[classes/fighter|Fighter]] · [[classes/paladin|Paladin]] · [[classes/rogue|Rogue]] · [[classes/sorcerer|Sorcerer]] · [[classes/warlock|Warlock]] · [[classes/wizard|Wizard]] · [[findings|The Identical-Spell List]] · [[spells|All Spells, Tagged]]*

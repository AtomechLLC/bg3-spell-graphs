# <span class="femoji">🧼</span> The Cleanse Counter

<span class="plate"><span class="tier tier-engine">Shared engine</span><span class="pv"><b>5</b> spells</span><span class="pv">similarity <b>0.66–0.89</b></span><span class="pv"><b>7</b> classes</span><span class="pv pvc">Bard, Cleric, Druid, Paladin, Ranger, Warlock, Wizard</span></span>

| Spell | Lv | School | Type | Cost | Damage | Save / Attack | Classes |
|---|---|---|---|---|---|---|---|
| <img class="sic" data-i="Target_LesserRestoration" alt=""> **Lesser Restoration** | 2 | Abjuration | Target | Action + L2 slot |  |  | [[classes/bard|Bard]], [[classes/cleric|Cleric]], [[classes/druid|Druid]], [[classes/paladin|Paladin]], [[classes/ranger|Ranger]] |
| <img class="sic" data-i="Target_ProtectionFromPoison" alt=""> **Protection from Poison** | 2 | Abjuration | Target | Action + L2 slot |  |  | [[classes/cleric|Cleric]], [[classes/druid|Druid]], [[classes/paladin|Paladin]], [[classes/ranger|Ranger]] |
| <img class="sic" data-i="Target_RemoveCurse" alt=""> **Remove Curse** | 3 | Abjuration | Target | Action + L3 slot |  |  | [[classes/bard|Bard]], [[classes/cleric|Cleric]], [[classes/paladin|Paladin]], [[classes/warlock|Warlock]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Shout_DispelEvilAndGood" alt=""> **Dispel Evil And Good** | 5 | Abjuration | Shout | Action + L5 slot |  |  | [[classes/cleric|Cleric]] |
| <img class="sic" data-i="Target_GreaterRestoration" alt=""> **Greater Restoration** | 5 | Abjuration | Target | Action + L5 slot |  |  | [[classes/bard|Bard]], [[classes/cleric|Cleric]], [[classes/druid|Druid]] |

**Shared skeleton.** Touch a creature, remove conditions from a named list; signatures measure 0.83–0.89 — one RemoveStatus() engine with different shopping lists. Dispel Evil And Good is the planar edition: its list is charm, fright, and possession inflicted by celestials, fiends, and undead.

**What varies.** The list (disease/poison vs. curses vs. planar afflictions vs. everything) and the level.

**Design read.** A vertical ladder of the same verb: pay more, cleanse more.

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/bard|Bard]] · [[classes/cleric|Cleric]] · [[classes/druid|Druid]] · [[classes/paladin|Paladin]] · [[classes/ranger|Ranger]] · [[classes/warlock|Warlock]] · [[classes/wizard|Wizard]] · [[families/counters|The Cancel Desk]] · [[findings|The Identical-Spell List]] · [[spells|All Spells, Tagged]]*

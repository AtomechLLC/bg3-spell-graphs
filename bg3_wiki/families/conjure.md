# <span class="femoji">🧞</span> The Summoning Contract

<span class="tier tier-template">Shared template</span> · 10 spells · mechanical similarity 0.45–0.97

| Spell | Lv | School | Type | Cost | Damage | Save / Attack | Classes |
|---|---|---|---|---|---|---|---|
| <img class="sic" data-i="Target_FindFamiliar" alt=""> **Find Familiar** *(+6 variants)* | 1 | Conjuration | Target | Action + L1 slot |  |  | [[classes/fighter|Fighter]], [[classes/rogue|Rogue]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Target_FlamingSphere" alt=""> **Flaming Sphere** | 2 | Conjuration | Target | Action + L2 slot | `2d6` fire | DEX save | [[classes/cleric|Cleric]], [[classes/druid|Druid]], [[classes/fighter|Fighter]], [[classes/rogue|Rogue]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Target_SpiritualWeapon" alt=""> **Spiritual Weapon** *(+6 variants)* | 2 | Evocation | Target | Bonus + L2 slot | `1d8+SpellCastingAbilityModifier` force |  | [[classes/bard|Bard]], [[classes/cleric|Cleric]] |
| <img class="sic" data-i="Target_AnimateDead" alt=""> **Animate Dead** *(+2 variants)* | 3 | Necromancy | Target | Action + L3 slot |  |  | [[classes/bard|Bard]], [[classes/cleric|Cleric]], [[classes/druid|Druid]], [[classes/paladin|Paladin]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Target_ConjureElementals_Minor_Container" alt=""> **Conjure Minor Elemental** *(+3 variants)* | 4 | Conjuration | Target | Action + L4 slot |  |  | [[classes/druid|Druid]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Target_ConjureWoodlandBeings" alt=""> **Conjure Woodland Being** | 4 | Conjuration | Target | Action + L4 slot |  |  | [[classes/druid|Druid]] |
| <img class="sic" data-i="Target_GuardianOfFaith" alt=""> **Guardian of Faith** | 4 | Conjuration | Target | Action + L4 slot |  |  | [[classes/bard|Bard]], [[classes/cleric|Cleric]] |
| <img class="sic" data-i="Target_ConjureElemental_Container" alt=""> **Conjure Elemental** *(+4 variants)* | 5 | Conjuration | Target | Action + L5  slot |  |  | [[classes/bard|Bard]], [[classes/druid|Druid]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Target_CreateUndead" alt=""> **Create Undead** | 6 | Necromancy | Target | Action + L6 slot |  |  | [[classes/cleric|Cleric]], [[classes/warlock|Warlock]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Target_PlanarAlly_Container" alt=""> **Planar Ally** *(+3 variants)* | 6 | Conjuration | Target | Action + L6 slot |  |  | [[classes/cleric|Cleric]] |

**Shared skeleton.** Summon a persistent ally that fights and acts under your command: a creature chosen from a menu (Conjure Elemental/Minor Elemental, 0.94 signature similarity; Conjure Woodland Being's dryad), a familiar, a raised corpse (Animate Dead and its senior product Create Undead), a planar servant, a stationary sentinel (Guardian of Faith) — or an *object* on the same contract: Spiritual Weapon and Flaming Sphere are summons whose 'creature' is a floating weapon or rolling fireball with its own place in your action economy.

**What varies.** The summoned thing (elemental, dryad, familiar, undead, celestial, sentinel, weapon, sphere), its control verbs, and duration. Most are [[containers|containers]], their menus implemented as child spells.

**Design read.** One summoning engine spanning units, creatures, and conjured objects — the whole conjuration aisle runs on a single contract, and Larian's container system makes each menu literal.

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/bard|Bard]] · [[classes/cleric|Cleric]] · [[classes/druid|Druid]] · [[classes/fighter|Fighter]] · [[classes/paladin|Paladin]] · [[classes/rogue|Rogue]] · [[classes/warlock|Warlock]] · [[classes/wizard|Wizard]] · [[findings|The Identical-Spell List]] · [[spells|All Spells, Tagged]]*

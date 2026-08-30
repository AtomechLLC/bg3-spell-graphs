# <span class="femoji">🏹</span> The Bolt Rack

<span class="tier tier-template">Shared template</span> · 8 spells · mechanical similarity 0.59–0.88

| Spell | Lv | School | Type | Cost | Damage | Save / Attack | Classes |
|---|---|---|---|---|---|---|---|
| <img class="sic" data-i="Projectile_ChromaticOrb" alt=""> **Chromatic Orb** *(+6 variants)* | 1 | Evocation | Projectile | Action + L1 slot | `3d8` thunder | ranged atk | [[classes/bard|Bard]], [[classes/fighter|Fighter]], [[classes/rogue|Rogue]], [[classes/sorcerer|Sorcerer]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Projectile_GuidingBolt" alt=""> **Guiding Bolt** | 1 | Evocation | Projectile | Action + L1 slot | `4d6` radiant | ranged atk | [[classes/bard|Bard]], [[classes/cleric|Cleric]] |
| <img class="sic" data-i="Projectile_IceKnife" alt=""> **Ice Knife** | 1 | Conjuration | Projectile | Action + L1 slot | `1d10` piercing, `2d6` cold | RangedSpellAttack;Dexterity | [[classes/bard|Bard]], [[classes/druid|Druid]], [[classes/fighter|Fighter]], [[classes/rogue|Rogue]], [[classes/sorcerer|Sorcerer]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Projectile_MagicMissile" alt=""> **Magic Missile** | 1 | Evocation | Projectile | Action + L1 slot | `3d4+3` force |  | [[classes/bard|Bard]], [[classes/fighter|Fighter]], [[classes/rogue|Rogue]], [[classes/sorcerer|Sorcerer]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Projectile_RayOfSickness" alt=""> **Ray of Sickness** | 1 | Necromancy | Projectile | Action + L1 slot | `2d8` poison | RangedSpellAttack;Constitution | [[classes/cleric|Cleric]], [[classes/fighter|Fighter]], [[classes/rogue|Rogue]], [[classes/sorcerer|Sorcerer]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Projectile_WitchBolt" alt=""> **Witch Bolt** | 1 | Evocation | Projectile | Action + L1 slot | `1d12` lightning | ranged atk | [[classes/fighter|Fighter]], [[classes/rogue|Rogue]], [[classes/sorcerer|Sorcerer]], [[classes/warlock|Warlock]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Projectile_AcidArrow" alt=""> **Melf's Acid Arrow** | 2 | Evocation | Projectile | Action + L2 slot | `4d4` acid, `2d4` acid | ranged atk | [[classes/fighter|Fighter]], [[classes/rogue|Rogue]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Projectile_ScorchingRay" alt=""> **Scorching Ray** | 2 | Evocation | Projectile | Action + L2 slot | `6d6` fire | ranged atk | [[classes/bard|Bard]], [[classes/cleric|Cleric]], [[classes/fighter|Fighter]], [[classes/rogue|Rogue]], [[classes/sorcerer|Sorcerer]], [[classes/wizard|Wizard]] |

**Shared skeleton.** WoW's bolt engine — the family that started this whole study — found in BG3's leveled single-target projectiles. Chromatic Orb is the element menu (a six-way [[containers|container]]), Guiding Bolt sells advantage-on-next-hit, Witch Bolt a re-zap channel, Scorching Ray splits into three rolls, Melf's Acid Arrow a lingering tick, Ice Knife a shrapnel burst, Magic Missile the auto-hit, Ray of Sickness the poison rider. The cantrip tier lives in the [[families/attack-cantrips|Damage Cantrip Engine]]; the AoE tier in the [[families/blast|Elemental Blast Template]].

**What varies.** Element, dice, attack roll vs. auto-hit, and the rider (advantage, repeat damage, lingering tick, poison).

**Design read.** Single-target projectile damage is the most homogeneous shelf in every game studied — BG3's version was hiding in plain sight among the unfamilied.

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/bard|Bard]] · [[classes/cleric|Cleric]] · [[classes/druid|Druid]] · [[classes/fighter|Fighter]] · [[classes/rogue|Rogue]] · [[classes/sorcerer|Sorcerer]] · [[classes/warlock|Warlock]] · [[classes/wizard|Wizard]] · [[findings|The Identical-Spell List]] · [[spells|All Spells, Tagged]]*

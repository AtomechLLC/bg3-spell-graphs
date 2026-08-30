# <span class="femoji">🔨</span> The Smite Armoury

<span class="tier tier-template">Shared template</span><span class="pv"><b>11</b> spells</span><span class="pv">similarity <b>0.32–0.94</b></span><span class="pv"><b>8</b> classes</span><span class="pv pvc">Bard, Fighter, Paladin, Ranger, Rogue, Sorcerer, Warlock, Wizard</span>

| Spell | Lv | School | Type | Cost | Damage | Save / Attack | Classes |
|---|---|---|---|---|---|---|---|
| **Booming Blade** | Cantrip | Evocation | Target | Action | `MainMeleeWeapon` mainmeleeweapondamagetype | melee wpn | [[classes/fighter|Fighter]], [[classes/rogue|Rogue]], [[classes/sorcerer|Sorcerer]], [[classes/warlock|Warlock]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="Projectile_EnsnaringStrike_Container" alt=""> **Ensnaring Strike** *(+2 variants)* | 1 | Conjuration | Projectile | Action | `MainRangedWeapon` mainrangedweapondamagetype | STR save | [[classes/ranger|Ranger]] |
| <img class="sic" data-i="Projectile_HailOfThorns" alt=""> **Hail of Thorns** | 1 | Conjuration | Projectile | Action + L1 slot + Bonus | `MainRangedWeapon` mainrangedweapondamagetype, `1d10` piercing | RangedWeaponAttack;Dexterity | [[classes/ranger|Ranger]] |
| <img class="sic" data-i="Target_Smite_Searing" alt=""> **Searing Smite** | 1 | Evocation | Target | Action | `MainMeleeWeapon` mainmeleeweapondamagetype, `1d6` fire | melee wpn | [[classes/paladin|Paladin]] |
| <img class="sic" data-i="Target_Smite_Thunderous" alt=""> **Thunderous Smite** | 1 | Evocation | Target | Action | `MainMeleeWeapon` mainmeleeweapondamagetype, `2d6` thunder | MeleeWeaponAttack;Strength | [[classes/bard|Bard]], [[classes/paladin|Paladin]] |
| <img class="sic" data-i="Target_Smite_Wrathful" alt=""> **Wrathful Smite** | 1 | Evocation | Target | Action | `MainMeleeWeapon` mainmeleeweapondamagetype, `1d6` psychic | MeleeWeaponAttack;Wisdom | [[classes/paladin|Paladin]], [[classes/warlock|Warlock]] |
| <img class="sic" data-i="Target_Smite_Branding_Container" alt=""> **Branding Smite** *(+2 variants)* | 2 | Evocation | Target | Action | `MainMeleeWeapon` mainmeleeweapondamagetype, `2d6` radiant | MeleeWeaponAttack;Constitution | [[classes/paladin|Paladin]], [[classes/warlock|Warlock]] |
| <img class="sic" data-i="Target_Smite_Blinding" alt=""> **Blinding Smite** | 3 | Evocation | Target | Action | `MainMeleeWeapon` mainmeleeweapondamagetype, `3d8` radiant | MeleeWeaponAttack;Constitution | [[classes/paladin|Paladin]] |
| <img class="sic" data-i="Projectile_LightningArrow" alt=""> **Lightning Arrow** | 3 | Transmutation | Projectile | Action + L3 slot | `4d8` lightning, `2d8` lightning | RangedWeaponAttack;Dexterity | [[classes/ranger|Ranger]] |
| <img class="sic" data-i="Target_StaggeringSmite" alt=""> **Staggering Smite** | 4 | Evocation | Target | Action | `MainMeleeWeapon` mainmeleeweapondamagetype, `4d6` psychic | MeleeWeaponAttack;Wisdom | [[classes/warlock|Warlock]] |
| <img class="sic" data-i="Projectile_Smite_Banishing_Container" alt=""> **Banishing Smite** *(+2 variants)* | 5 | Abjuration | Projectile | Action | `MainRangedWeapon` mainrangedweapondamagetype, `5d10` force | ranged wpn | [[classes/bard|Bard]], [[classes/warlock|Warlock]] |

**Shared skeleton.** Weapon strike + XdY typed damage + a rider on hit; measured 0.92–0.94 signature similarity between smites. The ranger wing runs the same engine at action cost: Ensnaring Strike (weapon hit + vines), Hail of Thorns (weapon hit + thorn burst), Lightning Arrow (weapon hit + lightning splash) — players literally petition for them to get the smites' interface. Booming Blade is the cantrip tier of the same engine: weapon hit + a thunder rider that detonates if the target moves.

**What varies.** The rider (burning, prone, frightened, branded, blinded, staggered, banished, ensnared, thorned, shocked, booming), the element, the action cost (bonus vs. action), and the price (cantrip to 4th). Branding, Banishing, and Ensnaring are themselves [[containers|containers]] with melee/ranged children.

**Design read.** Eleven products from one on-hit engine — a pricing table for conditions, with the smite name as the flavor knob, the ranger versions as the same knob in a different aisle, and Booming Blade as the free sample.

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/bard|Bard]] · [[classes/fighter|Fighter]] · [[classes/paladin|Paladin]] · [[classes/ranger|Ranger]] · [[classes/rogue|Rogue]] · [[classes/sorcerer|Sorcerer]] · [[classes/warlock|Warlock]] · [[classes/wizard|Wizard]] · [[containers|Container Spells]] · [[families/attack-cantrips|The Damage Cantrip Engine]] · [[families/imbues|The Imbue Shelf]] · [[findings|The Identical-Spell List]] · [[spells|All Spells, Tagged]]*

# <span class="femoji">📦</span> Container Spells

Larian's answer to the reskin: make it a **feature**. A container spell is one spell whose cast button opens a menu of variant child spells — **28 containers wrap 136 variant spells**, every child a separate `SpellData` entry inheriting from its parent.

Where tabletop publishes Chromatic Orb as one paragraph with a damage-type clause, BG3 ships **six sibling entries** differing in one damage row. Where the SRD's [[families/smites|smites]] are seven spells, two of them here are containers *again* (melee/ranged) — reskins inside reskins.

| Container | Lv | Variant axis | Variants |
|---|---|---|---|
| <img class="sic" data-i="Projectile_ChromaticOrb" alt=""> **Chromatic Orb** | 1 | damage type (6) | Acid, Cold, Fire, Lightning, Poison, Thunder |
| <img class="sic" data-i="Target_Command_Container" alt=""> **Command** | 1 | verb (5) | Halt, Approach, Drop, Flee, Grovel |
| <img class="sic" data-i="Target_CreateDestroyWater" alt=""> **Create or Destroy Water** | 1 | create / destroy | Create Water, Destroy Water |
| <img class="sic" data-i="Shout_DisguiseSelf" alt=""> **Disguise Self** | 1 | race × build × gender (32) | Masc Tiefling, Femme Tiefling, Masc Drow, Femme Drow, Masc Human, Femme Human, Masc Githyanki, Femme Githyanki, … (32 total) |
| <img class="sic" data-i="Projectile_EnsnaringStrike_Container" alt=""> **Ensnaring Strike** | 1 | melee / ranged | Ensnaring Strike (Ranged), Ensnaring Strike (Melee) |
| <img class="sic" data-i="Target_FindFamiliar" alt=""> **Find Familiar** | 1 | creature (6) | Cat, Crab, Frog, Rat, Raven, Spider |
| <img class="sic" data-i="Target_Hex" alt=""> **Hex** | 1 | ability (6) | Hex (Strength), Hex (Dexterity), Hex (Constitution), Hex (Intelligence), Hex (Wisdom), Hex (Charisma) |
| <img class="sic" data-i="Target_Smite_Branding_Container" alt=""> **Branding Smite** | 2 | melee / ranged | Branding Smite (Ranged), Branding Smite (Melee) |
| <img class="sic" data-i="Target_EnhanceAbility" alt=""> **Enhance Ability** | 2 | ability (6) | Bear's Endurance, Bull's Strength, Cat's Grace, Eagle's Splendour, Fox's Cunning, Owl's Wisdom |
| <img class="sic" data-i="Target_EnlargeReduce" alt=""> **Enlarge/Reduce** | 2 | enlarge / reduce | Enlarge, Reduce |
| <img class="sic" data-i="Target_SpiritualWeapon" alt=""> **Spiritual Weapon** | 2 | weapon form (6) | Greataxe, Greatsword, Halberd, Maul, Spear, Trident |
| <img class="sic" data-i="Target_AnimateDead" alt=""> **Animate Dead** | 3 | undead form | Skeleton, Zombie |
| <img class="sic" data-i="Target_BestowCurse" alt=""> **Bestow Curse** | 3 | curse choice (9) | Strength Disadvantage, Dexterity Disadvantage, Constitution Disadvantage, Intelligence Disadvantage, Wisdom Disadvantage, Charisma Disadvantage, Attack Disadvantage, Additional Damage, … (9 total) |
| <img class="sic" data-i="Zone_ConjureBarrage" alt=""> **Conjure Barrage** | 3 | weapon held | Melee Weapon, Ranged Weapon |
| <img class="sic" data-i="Target_Daylight_Container" alt=""> **Daylight** | 3 | sphere / enchant item | Sphere, Enchant Item |
| <img class="sic" data-i="Target_ElementalWeapon" alt=""> **Elemental Weapon** | 3 | damage type (5) | Acid, Cold, Fire, Lightning, Thunder |
| <img class="sic" data-i="Target_GlyphOfWarding" alt=""> **Glyph of Warding** | 3 | glyph effect (7) | Acid, Cold, Fire, Lightning, Thunder, Detonation, Sleep |
| <img class="sic" data-i="Target_ProtectionFromEnergy" alt=""> **Protection from Energy** | 3 | damage type (5) | Acid, Cold, Fire, Lightning, Thunder |
| <img class="sic" data-i="Shout_SpiritGuardians" alt=""> **Spirit Guardians** | 3 | radiant / necrotic | Spirit Guardians, Spirit Guardians |
| <img class="sic" data-i="Target_ConjureElementals_Minor_Container" alt=""> **Conjure Minor Elemental** | 4 | creature (3) | Azer, Ice Mephits, Mud Mephits |
| <img class="sic" data-i="Shout_FireShield" alt=""> **Fire Shield** | 4 | chill / warm | Chill, Warm |
| <img class="sic" data-i="Projectile_Smite_Banishing_Container" alt=""> **Banishing Smite** | 5 | melee / ranged | Banishing Smite (Melee), Banishing Smite (Ranged) |
| <img class="sic" data-i="Target_ConjureElemental_Container" alt=""> **Conjure Elemental** | 5 | element (4) | Air Elemental, Earth Elemental, Fire Elemental, Water Elemental |
| <img class="sic" data-i="Target_Contagion" alt=""> **Contagion** | 5 | disease (6) | Blinding Sickness, Filth Fever, Flesh Rot, Mindfire, Seizure, Slimy Doom |
| <img class="sic" data-i="Shout_DestructiveWave" alt=""> **Destructive Wave** | 5 | necrotic / radiant | Necrotic, Radiant |
| <img class="sic" data-i="Target_Eyebite" alt=""> **Eyebite** | 6 | condition (3) | Asleep, Panicked, Sickened |
| <img class="sic" data-i="Target_FreezingSphere" alt=""> **Otiluke's Freezing Sphere** | 6 | throw now / pocket it | Otiluke's Conveniently Portable Freezing Sphere, Otiluke's Freezing Sphere |
| <img class="sic" data-i="Target_PlanarAlly_Container" alt=""> **Planar Ally** | 6 | creature (3) | Djinni, Deva, Cambion |

The variant axes tell the design story: **damage type** (Chromatic Orb, Elemental Weapon, Glyph, Protection), **ability** (Hex, Enhance Ability — six children each, one per ability score), **weapon form** (Spiritual Weapon's six cosmetic weapons), and pure presentation (Disguise Self's 32 race/build/gender bodies — one mechanical effect, thirty-two costumes).

Back to [[overview|Overview]] · [[findings|The Identical-Spell List]]

---
*Linked from: [[classes/bard|Bard]] · [[classes/cleric|Cleric]] · [[classes/druid|Druid]] · [[classes/fighter|Fighter]] · [[classes/paladin|Paladin]] · [[classes/ranger|Ranger]] · [[classes/rogue|Rogue]] · [[classes/sorcerer|Sorcerer]] · [[classes/warlock|Warlock]] · [[classes/wizard|Wizard]] · [[families/conjure|The Summoning Contract]] · [[families/duplicate-skus|The Duplicate SKUs]] · [[families/smites|The Smite Armoury]] · [[findings|The Identical-Spell List]] · [[overview|Overview]] · [[spells|All Spells, Tagged]]*

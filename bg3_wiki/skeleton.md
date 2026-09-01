# 🧩 The Parameterized Skeleton

Every one of the 211 spells in this codex compiles from **one parameterized definition** —
the skeleton below. A "spell" is a point in this parameter space; a [[overview|family]] is a
neighbourhood of points that differ in one or two slots; a [[containers|container]] is a spell whose
menu axis is exposed to the player.

```
Spell :=
  Chassis    ( Target | Projectile | Shout | Zone | Wall | Teleportation | Throw )
  x Cost     ( action | bonus | reaction | free ,  slot level 0-6 ,  concentration? )
  x Delivery ( range , area shape , legal targets )
  x Gate     ( AttackRoll(melee|ranged, weapon|spell) | Save(ability, negate|half) | Auto )
  x Payload  ( Damage(dice, type)* + ApplyStatus(name, duration, save)* +
               CreateSurface(type, radius)? + Summon(stats)? + RemoveStatus(list)? )
  x Scaling  ( +dice per slot | +targets per slot | children per menu choice )
  x Rider    ( on-hit condition | on-move detonation | proc per hit )
```

The rest of this page is the skeleton's actual value inventory, mined from the game data.

## Chassis — Larian's own delivery taxonomy

The engine's spell-type prefix *is* a delivery chassis. Two chassis carry
81% of the entire game.

| Chassis (`stype` in the data) | Spells |
|---|---|
| Target | 138 |
| Shout | 36 |
| Projectile | 21 |
| Zone | 9 |
| Wall | 5 |
| Teleportation | 3 |
| Throw | 1 |

## Gate — how the effect is allowed to land

| Gate | Spells |
|---|---|
| none (auto-hit or pure effect) | 107 |
| Dexterity save | 26 |
| Wisdom save | 24 |
| Constitution save | 20 |
| RangedSpellAttack | 12 |
| Strength save | 7 |
| MeleeWeaponAttack | 7 |
| MeleeSpellAttack | 4 |
| RangedWeaponAttack | 3 |
| Charisma save | 2 |

## Cost signature

| Action x slot | Spells |
|---|---|
| action · slot | 158 |
| action · no slot | 33 |
| bonus action · slot | 16 |
| reaction · slot | 4 |
| free · slot | 1 |
| bonus action · no slot | 1 |

## Damage types in the payload slot

| Damage type | Spells |
|---|---|
| Fire | 10 |
| Necrotic | 9 |
| Radiant | 8 |
| Psychic | 7 |
| Lightning | 6 |
| Force | 5 |
| Cold | 5 |
| Acid | 4 |
| Piercing | 4 |
| Poison | 4 |
| Thunder | 3 |
| None | 1 |
| Slashing | 1 |
| Bludgeoning | 1 |

## Surfaces the payload can print

| Surface | Spells |
|---|---|
| Acid | 2 |
| WaterFrozen | 2 |
| DarknessCloud | 2 |
| Vines | 2 |
| BlackTentacles | 1 |
| CloudkillCloud | 1 |
| Water | 1 |
| FogCloud | 1 |
| Grease | 1 |
| Overgrowth | 1 |
| SpikeGrowth | 1 |
| StinkingCloud | 1 |
| Web | 1 |

## Five spells, written as parameter tuples

| Spell | Chassis | Cost | Gate | Payload | Scaling |
|---|---|---|---|---|---|
| **Fireball** | Projectile | action · slot 3 | Dex save, half | 8d6 Fire + ignite surfaces | +1d6/slot |
| **Hold Person** | Target | action · slot 2 · conc. | Wis save, negate | ApplyStatus(PARALYZED) | +1 target/slot |
| **Searing Smite** | Target (on-hit) | bonus · slot 1 | weapon attack | weapon + 1d6 Fire + ApplyStatus(BURNING) | +1d6/slot |
| **Misty Step** | Teleportation | bonus · slot 2 | auto | relocate self | — |
| **Cloud of Daggers** | Target (zone) | action · slot 2 · conc. | auto (enter/turn) | 4d4 Slashing per tick | +2d4/slot |

## The design read

Larian's data model makes the SRD's implicit skeleton *explicit*: chassis is a field, the gate is a
field, the payload is a call list. That is why the [[methodology|signature similarity]] works — and
why the families are so tight: **the game was compiled from this skeleton, so reading spells back
into it is lossless.** A designer building a new spell system could start from this table of slots
and the value inventories above; the three-game comparison suggests every RPG fills the same slots
with different vocabularies.

See it interactive: the Combo Chemistry map draws the *edges between* payload outputs (surfaces,
statuses) and the gates that consume them.

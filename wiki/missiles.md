# <span class="femoji">🏹</span> Missile Spells

Every SRD spell that fires a **single-target projectile** — a bolt, ray, dart, orb, or hurled missile — with what it does on impact. Beam-and-blast spells whose projectile explodes into an area ([[families/blast|Fireball's]] "bright streak" is flavor text for an AoE) are excluded, as are melee touch spells (Shocking Grasp, Inflict Wounds, Vampiric Touch) and effects that descend from above (Sacred Flame, Call Lightning).

| Spell | Lv | To-hit | Damage | Range | Effect / rider | Scaling | Classes |
|---|---|---|---|---|---|---|---|
| <img class="sic" data-i="fire-bolt" alt=""> **Fire Bolt** | Cantrip | ranged atk | `1d10` fire | 120 feet | Ignites unattended flammable objects. | `2d10`/`3d10`/`4d10` at char lv 5/11/17 | [[classes/sorcerer|Sorcerer]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="ray-of-frost" alt=""> **Ray of Frost** | Cantrip | ranged atk | `1d8` cold | 60 feet | Target's speed −10 ft until your next turn. | `2d8`/`3d8`/`4d8` at 5/11/17 | [[classes/sorcerer|Sorcerer]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="chill-touch" alt=""> **Chill Touch** | Cantrip | ranged atk | `1d8` necrotic | 120 feet | Target can't regain hit points until your next turn; undead also get disadvantage vs. you. | `2d8`/`3d8`/`4d8` at 5/11/17 | [[classes/sorcerer|Sorcerer]], [[classes/warlock|Warlock]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="eldritch-blast" alt=""> **Eldritch Blast** | Cantrip | ranged atk | `1d10` force | 120 feet | Beams aim independently at any targets. | 2/3/4 beams at 5/11/17 | [[classes/warlock|Warlock]] |
| <img class="sic" data-i="produce-flame" alt=""> **Produce Flame** | Cantrip | ranged atk | `1d8` fire | Self | Held flame doubles as a 10-ft light for 10 min; hurl it up to 30 ft to attack. | `2d8`/`3d8`/`4d8` at 5/11/17 | [[classes/druid|Druid]] |
| <img class="sic" data-i="acid-splash" alt=""> **Acid Splash** | Cantrip | DEX save | `1d6` acid | 60 feet | The hurled bubble can catch two creatures within 5 ft of each other. | `2d6`/`3d6`/`4d6` at 5/11/17 | [[classes/sorcerer|Sorcerer]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="magic-missile" alt=""> **Magic Missile** | 1 | auto-hit | 3 × `1d4+1` force | 120 feet | Three darts, split freely among targets, all strike simultaneously — no roll, no save. | +1 dart per slot | [[classes/sorcerer|Sorcerer]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="guiding-bolt" alt=""> **Guiding Bolt** | 1 | ranged atk | `4d6` radiant | 120 feet | Next attack roll against the target before your next turn has advantage. | +`1d6` per slot | [[classes/cleric|Cleric]] |
| <img class="sic" data-i="acid-arrow" alt=""> **Acid Arrow** | 2 | ranged atk | `4d4` acid + `2d4` delayed | 90 feet | Delayed damage lands at the end of the target's next turn; on a miss, half the initial damage and no delayed. | +`1d4` to both per slot | [[classes/wizard|Wizard]] |
| <img class="sic" data-i="scorching-ray" alt=""> **Scorching Ray** | 2 | 3 ranged atks | `2d6` fire per ray | 120 feet | Each ray is a separate attack at any targets. | +1 ray per slot | [[classes/sorcerer|Sorcerer]], [[classes/wizard|Wizard]] |
| **Ray of Enfeeblement** | 2 | ranged atk | — | 60 feet | Target deals half damage with Strength-based weapon attacks; Con save at each turn end to shake it. Concentration, 1 min. | — | [[classes/warlock|Warlock]], [[classes/wizard|Wizard]] |
| <img class="sic" data-i="disintegrate" alt=""> **Disintegrate** | 6 | DEX save | `10d6+40` force | 60 feet | At 0 hp the target turns to dust (no Revivify); also vaporizes Large-or-smaller nonmagical objects and force constructs. | +`3d6` per slot | [[classes/sorcerer|Sorcerer]], [[classes/wizard|Wizard]] |

## The pricing spectrum

Missiles show the same costed-variation logic as the [[families/attack-cantrips|damage-cantrip engine]] (which supplies half this table), extended along the **to-hit axis**:

- **Auto-hit** pays in die size — Magic Missile's guaranteed `1d4+1` darts are the floor.
- **Attack roll** buys the big dice — Fire Bolt's `1d10`, Guiding Bolt's `4d6` — and riders are paid for with die-size cuts (Ray of Frost's slow costs a step down to `1d8`).
- **Save-based** missiles trade accuracy mechanics for splash or severity — Acid Splash catches two targets; Disintegrate's save gates the game's nastiest single-target number (`10d6+40` and dust).

**Multi-projectile** is its own upcast currency: Scorching Ray and Eldritch Blast scale in *count*, Guiding Bolt and Acid Arrow in *dice* — same engine, different knob.

**Not measurable here:** the PHB/expansion missiles outside the SRD — Chromatic Orb, Witch Bolt, Ray of Sickness — per the [[methodology|data limits]].

Back to [[overview|Overview]] · [[spells|All Spells, Tagged]]

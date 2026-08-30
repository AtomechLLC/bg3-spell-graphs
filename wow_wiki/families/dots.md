# <span class="femoji">🩸</span> The Affliction Engine

<span class="tier tier-engine">Shared engine</span><span class="pv"><b>18</b> abilities</span><span class="pv">similarity <b>0.21–0.86</b></span><span class="pv"><b>7</b> classes</span><span class="pv pvc">Druid, Hunter, Priest, Rogue, Shaman, Warlock, Warrior</span>

| Ability | Class | Level | School | Ranks | Tooltip |
|---|---|---|---|---|---|
| <img class="sic" data-i="rake" alt=""> **Rake** | Druid | 54 | Physical | 4 | Rake the target for X damage and an additional X damage over X. Awards X combo X:points;. |
| <img class="sic" data-i="moonfire" alt=""> **Moonfire** | Druid | 58 | Arcane | 10 | Burns the enemy for X Arcane damage and then an additional X Arcane damage over X. |
| <img class="sic" data-i="insect-swarm" alt=""> **Insect Swarm** | Druid | 60 | Nature | 5 | The enemy target is swarmed by insects, decreasing their chance to hit by X% and causing X Nature damage over  |
| <img class="sic" data-i="rip" alt=""> **Rip** | Druid | 60 | Physical | 6 | Finishing move that causes damage over time. Damage increases per combo point and by your Attack Power: 1 poin |
| <img class="sic" data-i="scorpid-sting" alt=""> **Scorpid Sting** | Hunter | 52 | Nature | 4 | Stings the target, reducing Strength and Agility by X for X. Only one Sting per Hunter can be active on any on |
| <img class="sic" data-i="viper-sting" alt=""> **Viper Sting** | Hunter | 56 | Nature | 3 | Stings the target, draining X mana over X. Only one Sting per Hunter can be active on any one target. |
| <img class="sic" data-i="black-arrow" alt=""> **Black Arrow** | Hunter | 60 | Shadow | 2 | Fires a Black Arrow into the target, slowing the target's movement speed by X%, causing X Shadow damage and dr |
| <img class="sic" data-i="serpent-sting" alt=""> **Serpent Sting** | Hunter | 60 | Nature | 9 | Stings the target, causing X Nature damage over X. Only one Sting per Hunter can be active on any one target. |
| <img class="sic" data-i="shadow-word-pain" alt=""> **Shadow Word: Pain** | Priest | 58 | Shadow | 8 | A word of darkness that causes X Shadow damage over X. |
| <img class="sic" data-i="starshards" alt=""> **Starshards** | Priest | 58 | Arcane | 7 | Rains starshards down on the enemy target's head, causing X Arcane damage over X. |
| <img class="sic" data-i="devouring-plague" alt=""> **Devouring Plague** | Priest | 60 | Shadow | 6 | Afflicts the target with a disease that causes X Shadow damage over X. Damage caused by the Devouring Plague h |
| <img class="sic" data-i="mind-flay" alt=""> **Mind Flay** | Priest | 60 | Shadow | 6 | Assault the target's mind with Shadow energy, causing X Shadow damage over X$?A1226557[.][ and slowing their m |
| <img class="sic" data-i="garrote" alt=""> **Garrote** | Rogue | 54 | Physical | 6 | Garrote the enemy, causing X damage over X, increased by your Attack Power. Must be stealthed and behind the t |
| <img class="sic" data-i="rupture" alt=""> **Rupture** | Rogue | 60 | Physical | 6 | Finishing move that causes damage over time, increased by your Attack Power. Lasts longer per combo point: 1 p |
| <img class="sic" data-i="flame-shock" alt=""> **Flame Shock** | Shaman | 60 | Fire | 6 | Instantly sears the target with fire, causing X Fire damage immediately and X Fire damage over X. |
| <img class="sic" data-i="corruption" alt=""> **Corruption** | Warlock | 60 | Shadow | 7 | Corrupts the target, causing X Shadow damage over X. |
| <img class="sic" data-i="immolate" alt=""> **Immolate** | Warlock | 60 | Fire | 8 | Burns the enemy for X Fire damage and then an additional X Fire damage over X. |
| <img class="sic" data-i="rend" alt=""> **Rend** | Warrior | 60 | Physical | 7 | Wounds the target causing them to bleed for X damage over X. |

**Shared skeleton.** 'Causes X damage over Y sec' on a single target. Moonfire/Immolate measure 0.82 — the same design under different star signs — and the engine scales without changing: cast dots (SW:Pain / Corruption / Devouring Plague / Starshards — the priest racials are literal SW:Pain reskins), sting-delivered dots and drains (Serpent / Scorpid / Viper, 0.81–0.89 pairwise), physical bleeds on weapon damage (Rend / Garrote / Rupture / Rake / Rip), and channeled dots (Mind Flay). The same aura painted over an area is [[families/aoe-damage|the Area Barrage]].

**What varies.** School, tick rate, delivery (cast, sting, bleed, channel), and whether an upfront hit rides along.

**Design read.** One damage-over-time chassis serving all nine classes.

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/druid|Druid]] · [[classes/hunter|Hunter]] · [[classes/priest|Priest]] · [[classes/rogue|Rogue]] · [[classes/shaman|Shaman]] · [[classes/warlock|Warlock]] · [[classes/warrior|Warrior]] · [[families/hots|The Mending Clock]] · [[families/interrupts|The Interrupt Union]] · [[findings|The Identical-Spell List]] · [[spells|All Abilities, Tagged]]*

# <span class="femoji">🌩️</span> The Static Shell

<span class="plate"><span class="tier tier-clone">Verbatim clone</span><span class="pv"><b>4</b> abilities</span><span class="pv">similarity <b>0.22–0.79</b></span><span class="pv"><b>4</b> classes</span><span class="pv pvc">Druid, Priest, Shaman, Warrior</span></span>

| Ability | Class | Level | School | Ranks | Tooltip |
|---|---|---|---|---|---|
| <img class="sic" data-i="thorns" alt=""> **Thorns** | Druid | 54 | Nature | 6 | Thorns sprout from the friendly target causing X Nature damage to attackers when hit.  Lasts X. |
| <img class="sic" data-i="shadowguard" alt=""> **Shadowguard** | Priest | 60 | Shadow | 6 | The caster is surrounded by shadows.  When a spell, melee or ranged attack hits the caster, the attacker will  |
| <img class="sic" data-i="lightning-shield" alt=""> **Lightning Shield** | Shaman | 56 | Nature | 7 | The caster is surrounded by X balls of lightning.  When a spell, melee or ranged attack hits the caster, the a |
| <img class="sic" data-i="retaliation" alt=""> **Retaliation** | Warrior | 20 | Physical | 1 | Instantly counterattack any enemy that strikes you in melee for X.  Melee attacks made from behind cannot be c |

**Shared skeleton.** Lightning Shield and Shadowguard are structurally identical proc-shells (`Proc Trigger Spell` firing a damage payload at attackers) — the Troll Priest racial even ships with Lightning Shield's icon. Thorns is the same retaliation design on the plain `Damage Shield` aura.

**What varies.** The school (nature/shadow), charge counting, and which class wears it.

**Design read.** A cross-class SKU caught red-handed by both the effect table and the art pipeline.

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/druid|Druid]] · [[classes/priest|Priest]] · [[classes/shaman|Shaman]] · [[classes/warrior|Warrior]] · [[findings|The Identical-Spell List]] · [[spells|All Abilities, Tagged]]*

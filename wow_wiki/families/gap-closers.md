# <span class="femoji">🏃</span> The Gap Closers

<span class="tier tier-clone">Verbatim clone</span><span class="pv"><b>2</b> abilities</span><span class="pv">similarity <b>0.64</b></span><span class="pv"><b>1</b> classes</span><span class="pv pvc">Warrior</span>

| Ability | Class | Level | School | Ranks | Tooltip |
|---|---|---|---|---|---|
| <img class="sic" data-i="charge" alt=""> **Charge** | Warrior | 46 | Physical | 3 | Charge an enemy, generate $/10;s2 rage, and stun it for X. Cannot be used in combat. |
| <img class="sic" data-i="intercept" alt=""> **Intercept** | Warrior | 52 | Physical | 3 | Charge an enemy, causing X damage and stunning it for X. |

**Shared skeleton.** Both are the literal `Charge` effect (id 96) plus a rider on arrival — the same movement engine sold to Battle Stance and Berserker Stance separately.

**What varies.** The stance gate, the resource (generates rage vs. costs it), and the arrival rider.

**Design read.** A within-class SKU pair exposed by the effect data: one charge, two stances, two spellbook lines.

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/warrior|Warrior]] · [[findings|The Identical-Spell List]] · [[spells|All Abilities, Tagged]]*

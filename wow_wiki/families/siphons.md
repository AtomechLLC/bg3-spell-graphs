# <span class="femoji">🧛</span> The Siphon Set

<span class="tier tier-engine">Shared engine</span><span class="pv"><b>10</b> abilities</span><span class="pv">similarity <b>0.13–0.93</b></span><span class="pv"><b>4</b> classes</span><span class="pv pvc">Druid, Priest, Warlock, Warrior</span>

| Ability | Class | Level | School | Ranks | Tooltip |
|---|---|---|---|---|---|
| <img class="sic" data-i="enrage" alt=""> **Enrage** | Druid | 12 | Physical | 1 | $?a436895[Instantly generates X Rage and another ][Generates ]X rage over X$?p456328[][, but reduces base armo |
| <img class="sic" data-i="vampiric-embrace" alt=""> **Vampiric Embrace** | Priest | 1 | Shadow | 1 | Afflicts your target with Shadow energy that causes all party members to be healed for X% of any Shadow spell  |
| <img class="sic" data-i="mana-burn" alt=""> **Mana Burn** | Priest | 56 | Shadow | 5 | Drains X mana from a target. For each mana drained in this way, the target takes 0.5 Shadow damage. |
| <img class="sic" data-i="feedback" alt=""> **Feedback** | Priest | 60 | Shadow | 5 | The priest becomes surrounded with anti-magic energy. Any successful spell cast against the priest will burn X |
| <img class="sic" data-i="drain-life" alt=""> **Drain Life** | Warlock | 54 | Shadow | 6 | Transfers X health every second from the target to the caster. Lasts X. |
| <img class="sic" data-i="drain-mana" alt=""> **Drain Mana** | Warlock | 54 | Shadow | 4 | Transfers X Mana every X sec from the target to the caster. Lasts X. |
| <img class="sic" data-i="life-tap" alt=""> **Life Tap** | Warlock | 56 | Shadow | 6 | Converts X health into X mana$?s435395[ for you and your Demon pet][] |
| <img class="sic" data-i="siphon-life" alt=""> **Siphon Life** | Warlock | 58 | Shadow | 4 | Transfers X health from the target to the caster every X sec. Lasts X. |
| <img class="sic" data-i="dark-pact" alt=""> **Dark Pact** | Warlock | 60 | Shadow | 3 | Drains X of your pet's Mana, returning 100% to you. |
| <img class="sic" data-i="bloodrage" alt=""> **Bloodrage** | Warrior | 10 | Physical | 1 | Generates $/10;s1 rage at the cost of health, and then generates an additional $/10;29131o1 rage over X. The w |

**Shared skeleton.** The resource-warfare engine as a family: Drain Life and Siphon Life run `Periodic Leech`, Drain Mana runs `Periodic Mana Leech`, Mana Burn is the burst `Power Burn`, and Life Tap points the same pump at yourself (health → mana).

**What varies.** The drained resource (health/mana), the direction (enemy → you, or you → you), and channel vs. burst.

**Design read.** One pump, five plumbings — the Warlock and Priest split a design D&D barely has.

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/druid|Druid]] · [[classes/priest|Priest]] · [[classes/warlock|Warlock]] · [[classes/warrior|Warrior]] · [[findings|The Identical-Spell List]] · [[spells|All Abilities, Tagged]]*

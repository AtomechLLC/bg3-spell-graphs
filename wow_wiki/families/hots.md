# <span class="femoji">⏳</span> The Mending Clock

<span class="tier tier-clone">Verbatim clone</span><span class="pv"><b>7</b> abilities</span><span class="pv">similarity <b>0.17–0.79</b></span><span class="pv"><b>4</b> classes</span><span class="pv pvc">Druid, Hunter, Priest, Warlock</span>

| Ability | Class | Level | School | Ranks | Tooltip |
|---|---|---|---|---|---|
| <img class="sic" data-i="frenzied-regeneration" alt=""> **Frenzied Regeneration** | Druid | 56 | Physical | 3 | Converts up to 10 rage per second into health for X. Each point of rage is converted into X health. |
| <img class="sic" data-i="regrowth" alt=""> **Regrowth** | Druid | 60 | Nature | 9 | Heals a friendly target for X and another X over X. |
| <img class="sic" data-i="rejuvenation" alt=""> **Rejuvenation** | Druid | 60 | Nature | 11 | Heals the target for X over X. |
| <img class="sic" data-i="tranquility" alt=""> **Tranquility** | Druid | 60 | Nature | 4 | Regenerates all nearby group members for $?X[X][X] every X seconds for X. Druid must channel to maintain the s |
| <img class="sic" data-i="mend-pet" alt=""> **Mend Pet** | Hunter | 60 | Nature | 7 | Heals your pet X health every second while you focus. Lasts X. |
| <img class="sic" data-i="renew" alt=""> **Renew** | Priest | 60 | Holy | 10 | Heals the target of X damage over X. |
| <img class="sic" data-i="health-funnel" alt=""> **Health Funnel** | Warlock | 60 | Shadow | 7 | Gives X health to the caster's pet every second for X as long as the caster channels. |

**Shared skeleton.** Healing on a timer: all of it runs the `Periodic Heal` engine. Renew and Rejuvenation are the cross-class twins — the Priest's and Druid's versions of the identical tick engine; Regrowth bolts a direct heal onto the front, Tranquility channels it into the whole party, and the pet-keepers get their own pair — Mend Pet (Hunter, mana-paid) and Health Funnel (Warlock, blood-paid): the same channeled HoT pointed at a companion, priced in two currencies.

**What varies.** The class stamp, the tick size and duration, the delivery (single, front-loaded, channeled group, channeled-at-pet), and the resource paying for it.

**Design read.** The heal-over-time engine is [[families/dots|the affliction engine]] with the sign flipped — same clock, opposite payload, and the same cross-class twinning (Renew/Rejuvenation mirror SW:Pain/Corruption).

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/druid|Druid]] · [[classes/hunter|Hunter]] · [[classes/priest|Priest]] · [[classes/warlock|Warlock]] · [[findings|The Identical-Spell List]] · [[spells|All Abilities, Tagged]]*

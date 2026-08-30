# <span class="femoji">⏳</span> The Mending Clock

<span class="tier tier-clone">Verbatim clone</span> · 4 abilities · mechanical similarity 0.32–0.79

| Ability | Class | Level | School | Ranks | Tooltip |
|---|---|---|---|---|---|
| <img class="sic" data-i="regrowth" alt=""> **Regrowth** | Druid | 60 | Nature | 9 | Heals a friendly target for X and another X over X. |
| <img class="sic" data-i="rejuvenation" alt=""> **Rejuvenation** | Druid | 60 | Nature | 11 | Heals the target for X over X. |
| <img class="sic" data-i="tranquility" alt=""> **Tranquility** | Druid | 60 | Nature | 4 | Regenerates all nearby group members for $?X[X][X] every X seconds for X.  Druid must channel to maintain the  |
| <img class="sic" data-i="renew" alt=""> **Renew** | Priest | 60 | Holy | 10 | Heals the target of X damage over X. |

**Shared skeleton.** Healing on a timer: all four run the `Periodic Heal` aura (id 8). Renew and Rejuvenation are the cross-class twins — the Priest's and Druid's versions of the identical tick engine; Regrowth bolts a direct heal onto the front, Tranquility channels it into the whole party.

**What varies.** The class stamp, the tick size and duration, and the delivery (single, front-loaded, or channeled group).

**Design read.** The heal-over-time engine is [[families/dots|the affliction engine]] with the sign flipped — same clock, opposite payload, and the same cross-class twinning (Renew/Rejuvenation mirror SW:Pain/Corruption).

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/druid|Druid]] · [[classes/priest|Priest]] · [[findings|The Identical-Spell List]] · [[spells|All Abilities, Tagged]]*

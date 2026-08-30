# <span class="femoji">❤️‍🩹</span> The Cure Family

<span class="tier tier-clone">Verbatim clone</span> · 8 spells · mechanical similarity 0.68–0.97

| Spell | Lv | School | Type | Cost | Damage | Save / Attack | Classes |
|---|---|---|---|---|---|---|---|
| <img class="sic" data-i="Target_CureWounds" alt=""> **Cure Wounds** | 1 | Evocation | Target | Action + L1 slot | heal `1d8+mod` |  | [[classes/bard|Bard]], [[classes/cleric|Cleric]], [[classes/druid|Druid]], [[classes/paladin|Paladin]], [[classes/ranger|Ranger]] |
| <img class="sic" data-i="Target_HealingWord" alt=""> **Healing Word** | 1 | Evocation | Target | Bonus + L1 slot | heal `1d4+mod` |  | [[classes/bard|Bard]], [[classes/cleric|Cleric]], [[classes/druid|Druid]] |
| <img class="sic" data-i="Shout_PrayerOfHealing" alt=""> **Prayer of Healing** | 2 | Evocation | Shout | Action + L2 slot | heal `2d8+mod` |  | [[classes/cleric|Cleric]] |
| <img class="sic" data-i="Shout_BeaconOfHope" alt=""> **Beacon of Hope** | 3 | Abjuration | Shout | Action + L3 slot |  |  | [[classes/cleric|Cleric]] |
| <img class="sic" data-i="Shout_HealingWord_Mass" alt=""> **Mass Healing Word** | 3 | Evocation | Shout | Bonus + L3 slot | heal `1d4+mod` |  | [[classes/bard|Bard]], [[classes/cleric|Cleric]] |
| <img class="sic" data-i="Shout_AuraOfVitality" alt=""> **Warden of Vitality** | 3 | Evocation | Shout | Action + L3 slot |  |  | [[classes/bard|Bard]], [[classes/paladin|Paladin]] |
| <img class="sic" data-i="Target_CureWounds_Mass" alt=""> **Mass Cure Wounds** | 5 | Evocation | Target | Action + L5 slot | heal `3d8+mod` |  | [[classes/bard|Bard]], [[classes/cleric|Cleric]], [[classes/druid|Druid]] |
| <img class="sic" data-i="Target_Heal" alt=""> **Heal** | 6 | Evocation | Target | Action + L6 slot | heal `70` |  | [[classes/cleric|Cleric]], [[classes/druid|Druid]] |

**Shared skeleton.** RegainHitPoints(XdY + modifier); the same healing engine as tabletop, ported intact. Cure Wounds vs. Healing Word measures 0.93 on mechanics; the whole family stays high. Heal is the top rung (a flat 70), Warden of Vitality is the engine on a repeat timer — BG3's one heal-over-time, the WoW hots shelf reduced to a single SKU — and Beacon of Hope is the amplifier attachment: every heal received while it burns rolls maximum.

**What varies.** Delivery only: d8 touch action, d4 ranged bonus action, the multi-target versions of each, the flat-number top rung, the per-turn drip, and the maximizer.

**Design read.** The SRD's cleanest parameterized line survives the adaptation unchanged — five spells, one formula.

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/bard|Bard]] · [[classes/cleric|Cleric]] · [[classes/druid|Druid]] · [[classes/paladin|Paladin]] · [[classes/ranger|Ranger]] · [[findings|The Identical-Spell List]] · [[spells|All Spells, Tagged]]*

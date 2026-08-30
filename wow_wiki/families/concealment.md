# <span class="femoji">🎭</span> The Vanishing Act

<span class="tier tier-clone">Verbatim clone</span><span class="pv"><b>5</b> abilities</span><span class="pv">similarity <b>0.21–0.82</b></span><span class="pv"><b>3</b> classes</span><span class="pv pvc">Druid, Hunter, Rogue</span>

| Ability | Class | Level | School | Ranks | Tooltip |
|---|---|---|---|---|---|
| <img class="sic" data-i="prowl" alt=""> **Prowl** | Druid | 60 | Physical | 3 | Allows the Druid to prowl around, but reduces your movement speed by X%. Lasts until cancelled. |
| <img class="sic" data-i="feign-death" alt=""> **Feign Death** | Hunter | 30 | Physical | 1 | Feign death which may trick enemies into ignoring you. Lasts up to X. |
| <img class="sic" data-i="prowl" alt=""> **Prowl** | Hunter | 50 | Physical | 3 | Puts your pet in stealth mode, but slows its movement to X% of normal. The first attack from stealth receives  |
| <img class="sic" data-i="vanish" alt=""> **Vanish** | Rogue | 42 | Physical | 2 | Allows the rogue to vanish from sight, entering an improved stealth mode for X. Also breaks movement impairing |
| <img class="sic" data-i="stealth" alt=""> **Stealth** | Rogue | 60 | Physical | 4 | Allows the rogue to sneak around, but reduces your speed by X%. Lasts until cancelled. |

**Shared skeleton.** Stealth and Prowl are the same `Mod Stealth` package (0.8+ pair, rogue→cat); Vanish is Stealth with an escape trigger (the effect chain resolves to `Mod Stealth` + speed); Feign Death fakes the exit instead of taking it.

**What varies.** The exit mechanism (crouch, escape, play dead) and the class stamp.

**Design read.** Not being attackable is one design with three doors — two of them photocopied between Rogue and Druid.

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/druid|Druid]] · [[classes/hunter|Hunter]] · [[classes/rogue|Rogue]] · [[findings|The Identical-Spell List]] · [[overview|Overview]] · [[spells|All Abilities, Tagged]]*

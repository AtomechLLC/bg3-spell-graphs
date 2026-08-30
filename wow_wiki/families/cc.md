# <span class="femoji">⛓️</span> The Crowd Control Cabinet

<span class="plate"><span class="tier tier-template">Shared template</span><span class="pv"><b>25</b> abilities</span><span class="pv">similarity <b>0.14–0.98</b></span><span class="pv"><b>8</b> classes</span><span class="pv pvc">Druid, Hunter, Mage, Paladin, Priest, Rogue, Warlock, Warrior</span></span>

| Ability | Class | Level | School | Ranks | Tooltip |
|---|---|---|---|---|---|
| <img class="sic" data-i="bash" alt=""> **Bash** | Druid | 46 | Physical | 3 | Stuns the target for X. |
| <img class="sic" data-i="pounce" alt=""> **Pounce** | Druid | 56 | Physical | 3 | Pounce, stunning the target for X and causing X damage over X.  Must be prowling and behind the target.  Award |
| <img class="sic" data-i="hibernate" alt=""> **Hibernate** | Druid | 58 | Nature | 3 | Forces the enemy target to sleep for up to X.  Any damage will awaken the target.  Only one target can be forc |
| <img class="sic" data-i="scare-beast" alt=""> **Scare Beast** | Hunter | 46 | Nature | 3 | Scares a beast, causing it to run in fear for up to X.  Damage caused may interrupt the effect.  Only one beas |
| <img class="sic" data-i="wyvern-sting" alt=""> **Wyvern Sting** | Hunter | 60 | Nature | 3 | A stinging shot that puts the target to sleep for X.  Any damage will cancel the effect.  When the target wake |
| <img class="sic" data-i="polymorph" alt=""> **Polymorph** | Mage | 60 | Arcane | 5 | Transforms the enemy into a sheep, forcing it to wander around for up to X.  While wandering, the sheep cannot |
| <img class="sic" data-i="polymorph-cow" alt=""> **Polymorph: Cow** | Mage | 60 | Arcane | 1 | Transforms the enemy into a cow, forcing it to wander around for up to X.  While wandering, the cow cannot att |
| <img class="sic" data-i="repentance" alt=""> **Repentance** | Paladin | 20 | Holy | 1 | Puts the enemy target in a state of meditation, incapacitating them for up to X.  Any damage caused will awake |
| <img class="sic" data-i="turn-undead" alt=""> **Turn Undead** | Paladin | 52 | Nature | 3 | The targeted undead enemy will be compelled to flee for up to X.  Damage caused may interrupt the effect.  Onl |
| <img class="sic" data-i="hammer-of-justice" alt=""> **Hammer of Justice** | Paladin | 54 | Holy | 4 | Stuns the target for X. |
| <img class="sic" data-i="psychic-scream" alt=""> **Psychic Scream** | Priest | 56 | Shadow | 4 | The caster lets out a psychic scream, causing X enemies within X yards to flee for X.  Damage caused may inter |
| <img class="sic" data-i="mind-control" alt=""> **Mind Control** | Priest | 58 | Shadow | 3 | Controls a humanoid mind up to level X, but increases the time between attacks by X%.  Lasts up to X. |
| <img class="sic" data-i="shackle-undead" alt=""> **Shackle Undead** | Priest | 60 | Holy | 3 | Shackles the target undead enemy for up to X.  The shackled unit is unable to move, attack or cast spells.  An |
| <img class="sic" data-i="cheap-shot" alt=""> **Cheap Shot** | Rogue | 26 | Physical | 1 | Stuns the target for X.  Must be stealthed.  Awards X combo X:points;. |
| <img class="sic" data-i="blind" alt=""> **Blind** | Rogue | 34 | Nature | 1 | Blinds the target, causing it to wander disoriented for up to X.  Any damage caused will remove the effect. |
| <img class="sic" data-i="sap" alt=""> **Sap** | Rogue | 48 | Physical | 3 | Incapacitates the target for up to X.  Must be stealthed.  Only works on Humanoids that are not in combat.     |
| <img class="sic" data-i="kidney-shot" alt=""> **Kidney Shot** | Rogue | 50 | Physical | 2 | Finishing move that stuns the target.  Lasts longer per combo point:
   1 point  : 2 seconds
   2 points: 3  |
| <img class="sic" data-i="gouge" alt=""> **Gouge** | Rogue | 60 | Physical | 5 | Causes X damage, incapacitating the opponent for X, and turns off your attack.  Target must be facing you.  An |
| <img class="sic" data-i="banish" alt=""> **Banish** | Warlock | 48 | Shadow | 2 | Banishes the enemy target, preventing all action but making it invulnerable for up to X.  Only one target can  |
| <img class="sic" data-i="howl-of-terror" alt=""> **Howl of Terror** | Warlock | 54 | Shadow | 2 | Howl, causing X enemies within X yds to flee in terror for X.  Damage caused may interrupt the effect. |
| <img class="sic" data-i="fear" alt=""> **Fear** | Warlock | 56 | Shadow | 3 | Strikes fear in the enemy, causing it to run in fear for up to X.  Damage caused may interrupt the effect.  On |
| <img class="sic" data-i="death-coil" alt=""> **Death Coil** | Warlock | 58 | Shadow | 3 | Causes the enemy target to run in horror for X and causes X Shadow damage.  The caster gains 100% of the damag |
| <img class="sic" data-i="subjugate-demon" alt=""> **Subjugate Demon** | Warlock | 58 | Shadow | 3 | Subjugates the target demon, up to level X, forcing it to do your bidding.  While subjugated, the time between |
| <img class="sic" data-i="disarm" alt=""> **Disarm** | Warrior | 18 | Physical | 1 | Disarm the enemy's weapon for X. |
| <img class="sic" data-i="intimidating-shout" alt=""> **Intimidating Shout** | Warrior | 22 | Physical | 1 | The warrior shouts, causing the targeted enemy to cower in fear.  Up to X total nearby enemies will flee in fe |

**Shared skeleton.** One purpose — deny the target its turns — implemented through a handful of aura codes and dressed in every class's colors. The fears (Fear / Psychic Scream / Intimidating Shout / Scare Beast / Howl of Terror / Turn Undead) all apply `Mod Fear`; the sleeps (Hibernate / Wyvern Sting / Sap / Gouge / Blind) and stuns (Bash / Hammer of Justice / Cheap Shot / Kidney Shot / Pounce) run the same `Stun`-shaped incapacitates, with Bash/Hammer of Justice measuring ≥ 0.78 as a cross-class pair; the charms (Mind Control / Subjugate Demon) share `Mod Charm`; and the exiles (Banish / Shackle Undead / Repentance / Polymorph) are the same removal-without-damage parameterized by creature type.

**What varies.** The aura flavor, the legal target types, the delivery (cast, sting, ambush), and the damage-breaks clause.

**Design read.** Crowd control is one design department in every class's uniform — target-type gating (beasts-only, undead-only, demons-only, humanoids-only) does the work D&D does with spell level.

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/druid|Druid]] · [[classes/hunter|Hunter]] · [[classes/mage|Mage]] · [[classes/paladin|Paladin]] · [[classes/priest|Priest]] · [[classes/rogue|Rogue]] · [[classes/warlock|Warlock]] · [[classes/warrior|Warrior]] · [[families/snares|The Slow Lane]] · [[findings|The Identical-Spell List]] · [[spells|All Abilities, Tagged]]*

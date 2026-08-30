# The Effects Ledger

Every ability's **effect boxes in wowhead's vocabulary**, categorized purely by **effect
composition** — what the machinery does, with no reading of names or tooltip prose. Sourcing:
57 abilities carry effect boxes pulled verbatim from wowhead.com/classic before its CDN blocked
bulk access; the remaining 366 are decoded from the client's own `SpellEffect` rows (the
identical data wowhead renders) into the same vocabulary, including effect names learned from
the wowhead overlap itself. Validation on the 57-page overlap: 78% of wowhead's labels are
reproduced exactly after normalization; the rest differ only in wowhead's added qualifiers.

## Profiles by composition

| Effect profile | Abilities | Share |
|---|---|---|
| **Companion care** | 4 | 1% |
| **Summoning** | 43 | 10% |
| **Concealment** | 8 | 2% |
| **Shapeshift** | 10 | 2% |
| **Teleportation** | 8 | 2% |
| **Item creation** | 27 | 6% |
| **Resurrection** | 4 | 1% |
| **Threat manipulation** | 14 | 3% |
| **Interrupt / lockout** | 5 | 1% |
| **Dispel / cleanse** | 16 | 4% |
| **Hard control** | 29 | 7% |
| **Root & snare** | 10 | 2% |
| **Damage + affliction** | 9 | 2% |
| **Damage over time** | 21 | 5% |
| **Weapon strike** | 17 | 4% |
| **Direct spell damage** | 30 | 7% |
| **Healing** | 18 | 4% |
| **Absorb & shields** | 8 | 2% |
| **Resource manipulation** | 8 | 2% |
| **Stat & combat mods** | 53 | 13% |
| **Perception** | 16 | 4% |
| **Movement** | 14 | 3% |
| **Immunity** | 5 | 1% |
| **Other / utility** | 46 | 11% |

## Every ability's effect boxes

| Ability | Classes | Effect boxes (wowhead) | Profile |
|---|---|---|---|
| <img class="sic" data-i="fire-ward" alt=""> **Fire Ward** | Mage | Apply Aura: School Absorb + Apply Aura: Reflect School Spells | Absorb & shields |
| <img class="sic" data-i="frost-ward" alt=""> **Frost Ward** | Mage | Apply Aura: School Absorb + Apply Aura: Reflect School Spells | Absorb & shields |
| <img class="sic" data-i="ice-barrier" alt=""> **Ice Barrier** | Mage | Apply Aura: School Absorb | Absorb & shields |
| <img class="sic" data-i="mana-shield" alt=""> **Mana Shield** | Mage | Apply Aura: Mana Shield | Absorb & shields |
| <img class="sic" data-i="power-word-shield" alt=""> **Power Word: Shield** | Priest | Apply Aura: School Absorb | Absorb & shields |
| <img class="sic" data-i="retribution-aura" alt=""> **Retribution Aura** | Paladin | Apply Area Aura: Damage Shield | Absorb & shields |
| <img class="sic" data-i="shadow-ward" alt=""> **Shadow Ward** | Warlock | Apply Aura: School Absorb | Absorb & shields |
| <img class="sic" data-i="thorns" alt=""> **Thorns** | Druid | Apply Aura: Damage Shield | Absorb & shields |
| <img class="sic" data-i="dismiss-pet" alt=""> **Dismiss Pet** | Hunter | Drain Power (27) + Dismiss Pet | Companion care |
| <img class="sic" data-i="eyes-of-the-beast" alt=""> **Eyes of the Beast** | Hunter | Apply Aura: Mod Possess Pet + Apply Aura: Dummy | Companion care |
| <img class="sic" data-i="feed-pet" alt=""> **Feed Pet** | Hunter | Feed Pet | Companion care |
| <img class="sic" data-i="revive-pet" alt=""> **Revive Pet** | Hunter | Summon Dead Pet | Companion care |
| <img class="sic" data-i="detect-greater-invisibility" alt=""> **Detect Greater Invisibility** | Warlock | Apply Aura: Mod Invisibility Detection | Concealment |
| <img class="sic" data-i="detect-invisibility" alt=""> **Detect Invisibility** | Warlock | Apply Aura: Mod Invisibility Detection | Concealment |
| <img class="sic" data-i="detect-lesser-invisibility" alt=""> **Detect Lesser Invisibility** | Warlock | Apply Aura: Mod Invisibility Detection | Concealment |
| <img class="sic" data-i="detect-traps" alt=""> **Detect Traps** | Rogue | Apply Aura: Mod Stealth Detect + Apply Aura: Mod Invisibility Detection | Concealment |
| <img class="sic" data-i="feign-death" alt=""> **Feign Death** | Hunter | Apply Aura: Feign Death | Concealment |
| <img class="sic" data-i="prowl" alt=""> **Prowl** | Druid | Apply Aura: Stealth + Apply Aura: Decrease Run Speed % | Concealment |
| <img class="sic" data-i="stealth" alt=""> **Stealth** | Rogue | Apply Aura: Shapeshift + Apply Aura: Mod Stealth + Apply Aura: Mod Decrease Speed | Concealment |
| <img class="sic" data-i="track-hidden" alt=""> **Track Hidden** | Hunter | Apply Aura: Track Hidden + Apply Aura: Stealth Detection | Concealment |
| <img class="sic" data-i="fireball" alt=""> **Fireball** | Mage | School Damage (Fire) + Apply Aura: Periodic Damage | Damage + affliction |
| <img class="sic" data-i="flame-shock" alt=""> **Flame Shock** | Shaman | School Damage (Fire) + Apply Aura: Periodic Damage + Apply Aura: Dummy | Damage + affliction |
| <img class="sic" data-i="flamestrike" alt=""> **Flamestrike** | Mage | School Damage (Fire) + Apply Aura: Periodic Damage | Damage + affliction |
| <img class="sic" data-i="hellfire" alt=""> **Hellfire** | Warlock | Apply Aura: Periodically trigger spell + → School Damage (Fire) + Apply Aura: Periodic Damage + Apply Aura: Immunity - Mechanic | Damage + affliction |
| <img class="sic" data-i="holy-fire" alt=""> **Holy Fire** | Priest | School Damage (Holy) + Apply Aura: Periodic Damage | Damage + affliction |
| <img class="sic" data-i="immolate" alt=""> **Immolate** | Warlock | Apply Aura: Periodic Damage + School Damage (Fire) + Script Effect | Damage + affliction |
| <img class="sic" data-i="moonfire" alt=""> **Moonfire** | Druid | Apply Aura: Periodic Damage + School Damage (Arcane) | Damage + affliction |
| <img class="sic" data-i="pyroblast" alt=""> **Pyroblast** | Mage | School Damage (Fire) + Apply Aura: Periodic Damage | Damage + affliction |
| <img class="sic" data-i="rake" alt=""> **Rake** | Druid | School Damage (Physical) + Apply Aura: Periodic Damage + Add Combo Points | Damage + affliction |
| <img class="sic" data-i="black-arrow" alt=""> **Black Arrow** | Hunter | Apply Aura: Decrease Run Speed % + Apply Aura: Periodic Damage + Apply Aura: Periodically Drain Power (Mana) | Damage over time |
| <img class="sic" data-i="blizzard" alt=""> **Blizzard** | Mage | Apply Aura: Periodic Damage | Damage over time |
| <img class="sic" data-i="consecration" alt=""> **Consecration** | Paladin | Apply Aura: Periodic Damage | Damage over time |
| <img class="sic" data-i="corruption" alt=""> **Corruption** | Warlock | Apply Aura: Periodic Damage | Damage over time |
| <img class="sic" data-i="curse-of-agony" alt=""> **Curse of Agony** | Warlock | Apply Aura: Periodic Damage | Damage over time |
| <img class="sic" data-i="curse-of-doom" alt=""> **Curse of Doom** | Warlock | Apply Aura: Periodic Damage | Damage over time |
| <img class="sic" data-i="devouring-plague" alt=""> **Devouring Plague** | Priest | Apply Aura: Periodic Leech | Damage over time |
| <img class="sic" data-i="drain-life" alt=""> **Drain Life** | Warlock | Apply Aura: Periodic Leech | Damage over time |
| <img class="sic" data-i="entangling-roots" alt=""> **Entangling Roots** | Druid | Apply Aura: Root + Apply Aura: Periodic Damage | Damage over time |
| <img class="sic" data-i="garrote" alt=""> **Garrote** | Rogue | Apply Aura: Periodic Damage + Add Combo Points | Damage over time |
| <img class="sic" data-i="hurricane" alt=""> **Hurricane** | Druid | Persistent Area Aura: Periodic Damage + Persistent Area Aura: Mod Melee Attack Speed - % | Damage over time |
| <img class="sic" data-i="insect-swarm" alt=""> **Insect Swarm** | Druid | Apply Aura: Periodic Damage + Apply Aura: Mod Melee & Ranged Hit Chance % | Damage over time |
| <img class="sic" data-i="rain-of-fire" alt=""> **Rain of Fire** | Warlock | Apply Aura: Periodic Damage + Apply Aura: Dummy | Damage over time |
| <img class="sic" data-i="rend" alt=""> **Rend** | Warrior | Apply Aura: Periodic Damage | Damage over time |
| <img class="sic" data-i="rip" alt=""> **Rip** | Druid | Apply Aura: Periodic Damage | Damage over time |
| <img class="sic" data-i="rupture" alt=""> **Rupture** | Rogue | Apply Aura: Periodic Damage + Dummy | Damage over time |
| <img class="sic" data-i="serpent-sting" alt=""> **Serpent Sting** | Hunter | Apply Aura: Periodic Damage | Damage over time |
| <img class="sic" data-i="shadow-word-pain" alt=""> **Shadow Word: Pain** | Priest | Apply Aura: Periodic Damage | Damage over time |
| <img class="sic" data-i="siphon-life" alt=""> **Siphon Life** | Warlock | Apply Aura: Periodic Leech | Damage over time |
| <img class="sic" data-i="starshards" alt=""> **Starshards** | Priest | Apply Aura: Periodic Damage | Damage over time |
| <img class="sic" data-i="volley" alt=""> **Volley** | Hunter | Apply Aura: Periodic Damage | Damage over time |
| <img class="sic" data-i="arcane-explosion" alt=""> **Arcane Explosion** | Mage | School Damage (Arcane) | Direct spell damage |
| <img class="sic" data-i="arcane-missiles" alt=""> **Arcane Missiles** | Mage | Apply Aura: Periodically trigger spell + → School Damage (Arcane) + Apply Aura: Dummy | Direct spell damage |
| <img class="sic" data-i="arcane-shot" alt=""> **Arcane Shot** | Hunter | School Damage (Arcane) | Direct spell damage |
| <img class="sic" data-i="bloodthirst" alt=""> **Bloodthirst** | Warrior | School Damage (Physical) | Direct spell damage |
| <img class="sic" data-i="chain-lightning" alt=""> **Chain Lightning** | Shaman | School Damage (Nature) | Direct spell damage |
| <img class="sic" data-i="conflagrate" alt=""> **Conflagrate** | Warlock | School Damage (Fire) | Direct spell damage |
| <img class="sic" data-i="counterattack" alt=""> **Counterattack** | Hunter | School Damage (Physical) + Apply Aura: Root | Direct spell damage |
| <img class="sic" data-i="divine-intervention" alt=""> **Divine Intervention** | Paladin | Abort All Pending Attacks + Trigger Spell
Divine Intervention + Instakill | Direct spell damage |
| <img class="sic" data-i="eviscerate" alt=""> **Eviscerate** | Rogue | School Damage (Physical) + Dummy | Direct spell damage |
| <img class="sic" data-i="exorcism" alt=""> **Exorcism** | Paladin | School Damage (Holy) | Direct spell damage |
| <img class="sic" data-i="ferocious-bite" alt=""> **Ferocious Bite** | Druid | School Damage (Physical) | Direct spell damage |
| <img class="sic" data-i="fire-blast" alt=""> **Fire Blast** | Mage | School Damage (Fire) | Direct spell damage |
| <img class="sic" data-i="frost-nova" alt=""> **Frost Nova** | Mage | School Damage (Frost) + Apply Aura: Root | Direct spell damage |
| <img class="sic" data-i="hammer-of-wrath" alt=""> **Hammer of Wrath** | Paladin | School Damage (Holy) | Direct spell damage |
| <img class="sic" data-i="holy-nova" alt=""> **Holy Nova** | Priest | School Damage (Holy) | Direct spell damage |
| <img class="sic" data-i="holy-wrath" alt=""> **Holy Wrath** | Paladin | School Damage (Holy) | Direct spell damage |
| <img class="sic" data-i="lightning-bolt" alt=""> **Lightning Bolt** | Shaman | School Damage (Nature) | Direct spell damage |
| <img class="sic" data-i="mind-blast" alt=""> **Mind Blast** | Priest | School Damage (Shadow) | Direct spell damage |
| <img class="sic" data-i="mongoose-bite" alt=""> **Mongoose Bite** | Hunter | School Damage (Physical) | Direct spell damage |
| <img class="sic" data-i="revenge" alt=""> **Revenge** | Warrior | School Damage (Physical) | Direct spell damage |
| <img class="sic" data-i="scorch" alt=""> **Scorch** | Mage | School Damage (Fire) | Direct spell damage |
| <img class="sic" data-i="searing-pain" alt=""> **Searing Pain** | Warlock | School Damage (Fire) | Direct spell damage |
| <img class="sic" data-i="shadow-bolt" alt=""> **Shadow Bolt** | Warlock | School Damage (Shadow) | Direct spell damage |
| <img class="sic" data-i="smite" alt=""> **Smite** | Priest | School Damage (Holy) | Direct spell damage |
| <img class="sic" data-i="soul-fire" alt=""> **Soul Fire** | Warlock | School Damage (Fire) | Direct spell damage |
| <img class="sic" data-i="starfire" alt=""> **Starfire** | Druid | School Damage (Arcane) | Direct spell damage |
| <img class="sic" data-i="swipe" alt=""> **Swipe** | Druid | School Damage (Physical) | Direct spell damage |
| <img class="sic" data-i="thunder-clap" alt=""> **Thunder Clap** | Warrior | School Damage (Physical) + Apply Aura: Mod Haste | Direct spell damage |
| <img class="sic" data-i="wing-clip" alt=""> **Wing Clip** | Hunter | Apply Aura: Decrease Run Speed % + School Damage (Physical) | Direct spell damage |
| <img class="sic" data-i="wrath" alt=""> **Wrath** | Druid | School Damage (Nature) | Direct spell damage |
| <img class="sic" data-i="abolish-disease" alt=""> **Abolish Disease** | Priest | Apply Aura: Periodically trigger spell + → Dispel + Dispel | Dispel / cleanse |
| <img class="sic" data-i="abolish-poison" alt=""> **Abolish Poison** | Druid | Apply Aura: Periodically trigger spell + Dispel (Poison) | Dispel / cleanse |
| <img class="sic" data-i="cleanse" alt=""> **Cleanse** | Paladin | Dispel + Dispel + Dispel | Dispel / cleanse |
| <img class="sic" data-i="cure-disease" alt=""> **Cure Disease** | Priest | Dispel | Dispel / cleanse |
| <img class="sic" data-i="cure-disease" alt=""> **Cure Disease** | Shaman | Dispel | Dispel / cleanse |
| <img class="sic" data-i="cure-poison" alt=""> **Cure Poison** | Druid | Dispel | Dispel / cleanse |
| <img class="sic" data-i="cure-poison" alt=""> **Cure Poison** | Shaman | Dispel | Dispel / cleanse |
| <img class="sic" data-i="dispel-magic" alt=""> **Dispel Magic** | Priest | Dispel | Dispel / cleanse |
| <img class="sic" data-i="polymorph" alt=""> **Polymorph** | Mage | Apply Aura: Mod Confuse + Apply Aura: Transform + Dispel Mechanic | Dispel / cleanse |
| <img class="sic" data-i="polymorph-cow" alt=""> **Polymorph: Cow** | Mage | Apply Aura: Mod Confuse + Apply Aura: Transform + Dispel Mechanic | Dispel / cleanse |
| <img class="sic" data-i="purge" alt=""> **Purge** | Shaman | Dispel | Dispel / cleanse |
| <img class="sic" data-i="purify" alt=""> **Purify** | Paladin | Dispel + Dispel | Dispel / cleanse |
| <img class="sic" data-i="remove-curse" alt=""> **Remove Curse** | Druid | Dispel | Dispel / cleanse |
| <img class="sic" data-i="remove-lesser-curse" alt=""> **Remove Lesser Curse** | Mage | Dispel | Dispel / cleanse |
| <img class="sic" data-i="shield-slam" alt=""> **Shield Slam** | Warrior | Dispel + School Damage (Physical) | Dispel / cleanse |
| <img class="sic" data-i="tranquilizing-shot" alt=""> **Tranquilizing Shot** | Hunter | Dispel | Dispel / cleanse |
| <img class="sic" data-i="banish" alt=""> **Banish** | Warlock | Apply Aura: Stun + Apply Aura: School Immunity | Hard control |
| <img class="sic" data-i="bash" alt=""> **Bash** | Druid | Apply Aura: Stun | Hard control |
| <img class="sic" data-i="blessing-of-protection" alt=""> **Blessing of Protection** | Paladin | Apply Aura: School Immunity + Apply Aura: Mod Pacify | Hard control |
| <img class="sic" data-i="blind" alt=""> **Blind** | Rogue | Apply Aura: Mod Decrease Speed + Apply Aura: Mod Confuse | Hard control |
| <img class="sic" data-i="charge" alt=""> **Charge** | Warrior | Charge + Give Power (Rage) + Trigger Spell
Charge Stun | Hard control |
| <img class="sic" data-i="cheap-shot" alt=""> **Cheap Shot** | Rogue | Apply Aura: Stun + Add Combo Points | Hard control |
| <img class="sic" data-i="death-coil" alt=""> **Death Coil** | Warlock | Health Leech + Apply Aura: Mod Fear | Hard control |
| <img class="sic" data-i="divine-protection" alt=""> **Divine Protection** | Paladin | Apply Aura: Mod Pacify + Apply Aura: School Immunity + Apply Aura: School Immunity | Hard control |
| <img class="sic" data-i="fear" alt=""> **Fear** | Warlock | Apply Aura: Mod Fear + Apply Aura: Mod Increase Speed | Hard control |
| <img class="sic" data-i="gouge" alt=""> **Gouge** | Rogue | School Damage (Physical) + Add Combo Points + Apply Aura: Stun | Hard control |
| <img class="sic" data-i="hammer-of-justice" alt=""> **Hammer of Justice** | Paladin | Apply Aura: Stun | Hard control |
| <img class="sic" data-i="hibernate" alt=""> **Hibernate** | Druid | Apply Aura: Stun | Hard control |
| <img class="sic" data-i="howl-of-terror" alt=""> **Howl of Terror** | Warlock | Apply Aura: Mod Fear + Apply Aura: Mod Increase Speed | Hard control |
| <img class="sic" data-i="ice-block" alt=""> **Ice Block** | Mage | Apply Aura: Stun + Apply Aura: Immunity (Physical) + Apply Aura: Immunity (All) | Hard control |
| <img class="sic" data-i="intercept" alt=""> **Intercept** | Warrior | Charge + Trigger Spell
Intercept Stun | Hard control |
| <img class="sic" data-i="intimidating-shout" alt=""> **Intimidating Shout** | Warrior | Trigger Spell + → Apply Aura: Stun + Apply Aura: Mod Fear + Apply Aura: Mod Increase Speed | Hard control |
| <img class="sic" data-i="kidney-shot" alt=""> **Kidney Shot** | Rogue | Apply Aura: Stun + Dummy + Apply Aura: Mod Damage % Taken | Hard control |
| <img class="sic" data-i="mangle" alt=""> **Mangle** | Druid | School Damage (Physical) + Apply Aura: Stun | Hard control |
| <img class="sic" data-i="mind-control" alt=""> **Mind Control** | Priest | Apply Aura: Mod Possess + Apply Aura: Dummy + Apply Aura: Mod Haste | Hard control |
| <img class="sic" data-i="pounce" alt=""> **Pounce** | Druid | Apply Aura: Stun + Trigger Spell
Pounce Bleed + Add Combo Points | Hard control |
| <img class="sic" data-i="psychic-scream" alt=""> **Psychic Scream** | Priest | Apply Aura: Mod Fear + Apply Aura: Mod Increase Speed | Hard control |
| <img class="sic" data-i="repentance" alt=""> **Repentance** | Paladin | Apply Aura: Stun | Hard control |
| <img class="sic" data-i="sap" alt=""> **Sap** | Rogue | Apply Aura: Stun | Hard control |
| <img class="sic" data-i="scare-beast" alt=""> **Scare Beast** | Hunter | Apply Aura: Fear + Apply Aura: Increase Run Speed % | Hard control |
| <img class="sic" data-i="seal-of-justice" alt=""> **Seal of Justice** | Paladin | Apply Aura: Proc Trigger Spell + → Apply Aura: Stun + Apply Aura: Dummy | Hard control |
| <img class="sic" data-i="shackle-undead" alt=""> **Shackle Undead** | Priest | Apply Aura: Stun | Hard control |
| <img class="sic" data-i="subjugate-demon" alt=""> **Subjugate Demon** | Warlock | Apply Aura: Mod Charm + Apply Aura: Mod Haste + Apply Aura: Mod Casting Speed | Hard control |
| <img class="sic" data-i="turn-undead" alt=""> **Turn Undead** | Paladin | Apply Aura: Mod Fear + Apply Aura: Mod Increase Speed | Hard control |
| <img class="sic" data-i="wyvern-sting" alt=""> **Wyvern Sting** | Hunter | Apply Aura: Stun | Hard control |
| <img class="sic" data-i="chain-heal" alt=""> **Chain Heal** | Shaman | Heal | Healing |
| <img class="sic" data-i="desperate-prayer" alt=""> **Desperate Prayer** | Priest | Heal | Healing |
| <img class="sic" data-i="flash-heal" alt=""> **Flash Heal** | Priest | Heal | Healing |
| <img class="sic" data-i="greater-heal" alt=""> **Greater Heal** | Priest | Heal | Healing |
| <img class="sic" data-i="heal" alt=""> **Heal** | Priest | Heal | Healing |
| <img class="sic" data-i="healing-touch" alt=""> **Healing Touch** | Druid | Heal | Healing |
| <img class="sic" data-i="healing-wave" alt=""> **Healing Wave** | Shaman | Heal | Healing |
| <img class="sic" data-i="health-funnel" alt=""> **Health Funnel** | Warlock | Apply Aura: Periodic Heal + Apply Aura: Mod Health Regen % | Healing |
| <img class="sic" data-i="lay-on-hands" alt=""> **Lay on Hands** | Paladin | Heal Max Health + Give Power | Healing |
| <img class="sic" data-i="lesser-heal" alt=""> **Lesser Heal** | Priest | Heal | Healing |
| <img class="sic" data-i="lesser-healing-wave" alt=""> **Lesser Healing Wave** | Shaman | Heal | Healing |
| <img class="sic" data-i="mend-pet" alt=""> **Mend Pet** | Hunter | Apply Aura: Periodic Heal | Healing |
| <img class="sic" data-i="prayer-of-healing" alt=""> **Prayer of Healing** | Priest | Heal | Healing |
| <img class="sic" data-i="regrowth" alt=""> **Regrowth** | Druid | Heal + Apply Aura: Periodic Heal | Healing |
| <img class="sic" data-i="rejuvenation" alt=""> **Rejuvenation** | Druid | Apply Aura: Periodic Heal | Healing |
| <img class="sic" data-i="renew" alt=""> **Renew** | Priest | Apply Aura: Periodic Heal | Healing |
| <img class="sic" data-i="seal-of-light" alt=""> **Seal of Light** | Paladin | Apply Aura: Proc Trigger Spell + → Heal + Apply Aura: Dummy | Healing |
| <img class="sic" data-i="tranquility" alt=""> **Tranquility** | Druid | Apply Area Aura: Periodic Heal | Healing |
| <img class="sic" data-i="berserker-rage" alt=""> **Berserker Rage** | Warrior | Apply Aura: Immunity - Mechanic + Apply Aura: Immunity - Mechanic | Immunity |
| <img class="sic" data-i="blessing-of-freedom" alt=""> **Blessing of Freedom** | Paladin | Apply Aura: Immunity - Mechanic + Apply Aura: Immunity - Mechanic | Immunity |
| <img class="sic" data-i="blink" alt=""> **Blink** | Mage | Blink + Apply Aura: Immunity - Mechanic (Stunned) + Apply Aura: Immunity - Mechanic (Rooted) | Immunity |
| <img class="sic" data-i="fear-ward" alt=""> **Fear Ward** | Priest | Apply Aura: Immunity - Mechanic | Immunity |
| <img class="sic" data-i="flare" alt=""> **Flare** | Hunter | Persistent Area Aura: Immunity - Debuffs Only (5) + Persistent Area Aura: Immunity - Debuffs Only (6) | Immunity |
| <img class="sic" data-i="counterspell" alt=""> **Counterspell** | Mage | Interrupt Cast | Interrupt / lockout |
| <img class="sic" data-i="earth-shock" alt=""> **Earth Shock** | Shaman | School Damage (Nature) + Interrupt Cast | Interrupt / lockout |
| <img class="sic" data-i="kick" alt=""> **Kick** | Rogue | School Damage (Physical) + Interrupt Cast | Interrupt / lockout |
| <img class="sic" data-i="pummel" alt=""> **Pummel** | Warrior | School Damage (Physical) + Interrupt Cast | Interrupt / lockout |
| <img class="sic" data-i="shield-bash" alt=""> **Shield Bash** | Warrior | Interrupt Cast + School Damage (Physical) | Interrupt / lockout |
| <img class="sic" data-i="conjure-food" alt=""> **Conjure Food** | Mage | Create Item | Item creation |
| <img class="sic" data-i="conjure-mana-agate" alt=""> **Conjure Mana Agate** | Mage | Create Item | Item creation |
| <img class="sic" data-i="conjure-mana-citrine" alt=""> **Conjure Mana Citrine** | Mage | Create Item | Item creation |
| <img class="sic" data-i="conjure-mana-jade" alt=""> **Conjure Mana Jade** | Mage | Create Item | Item creation |
| <img class="sic" data-i="conjure-mana-ruby" alt=""> **Conjure Mana Ruby** | Mage | Create Item | Item creation |
| <img class="sic" data-i="conjure-water" alt=""> **Conjure Water** | Mage | Create Item | Item creation |
| <img class="sic" data-i="create-firestone" alt=""> **Create Firestone** | Warlock | Create Item | Item creation |
| <img class="sic" data-i="create-firestone-greater" alt=""> **Create Firestone (Greater)** | Warlock | Create Item | Item creation |
| <img class="sic" data-i="create-firestone-lesser" alt=""> **Create Firestone (Lesser)** | Warlock | Create Item | Item creation |
| <img class="sic" data-i="create-firestone-major" alt=""> **Create Firestone (Major)** | Warlock | Create Item | Item creation |
| <img class="sic" data-i="create-soulstone" alt=""> **Create Soulstone** | Warlock | Create Item | Item creation |
| <img class="sic" data-i="create-soulstone-greater" alt=""> **Create Soulstone (Greater)** | Warlock | Create Item | Item creation |
| <img class="sic" data-i="create-soulstone-lesser" alt=""> **Create Soulstone (Lesser)** | Warlock | Create Item | Item creation |
| <img class="sic" data-i="create-soulstone-major" alt=""> **Create Soulstone (Major)** | Warlock | Create Item | Item creation |
| <img class="sic" data-i="create-soulstone-minor" alt=""> **Create Soulstone (Minor)** | Warlock | Create Item | Item creation |
| <img class="sic" data-i="create-spellstone" alt=""> **Create Spellstone** | Warlock | Create Item | Item creation |
| <img class="sic" data-i="create-spellstone-greater" alt=""> **Create Spellstone (Greater)** | Warlock | Create Item | Item creation |
| <img class="sic" data-i="create-spellstone-major" alt=""> **Create Spellstone (Major)** | Warlock | Create Item | Item creation |
| <img class="sic" data-i="drain-soul" alt=""> **Drain Soul** | Warlock | Apply Aura: Create Item on Death
Soul Shard + Apply Aura: Periodic Damage + Apply Aura: Proc Trigger Spell | Item creation |
| <img class="sic" data-i="flametongue-weapon" alt=""> **Flametongue Weapon** | Shaman | Enchant Item (temporary) | Item creation |
| <img class="sic" data-i="frostbrand-weapon" alt=""> **Frostbrand Weapon** | Shaman | Enchant Item (temporary) | Item creation |
| <img class="sic" data-i="mind-numbing-poison" alt=""> **Mind-numbing Poison** | Rogue | Create Item | Item creation |
| <img class="sic" data-i="mind-numbing-poison-ii" alt=""> **Mind-numbing Poison II** | Rogue | Create Item | Item creation |
| <img class="sic" data-i="mind-numbing-poison-iii" alt=""> **Mind-numbing Poison III** | Rogue | Create Item | Item creation |
| <img class="sic" data-i="rockbiter-weapon" alt=""> **Rockbiter Weapon** | Shaman | Enchant Item (temporary) | Item creation |
| <img class="sic" data-i="shadowburn" alt=""> **Shadowburn** | Warlock | Apply Aura: Create Item on Death
Soul Shard + School Damage (Shadow) | Item creation |
| <img class="sic" data-i="windfury-weapon" alt=""> **Windfury Weapon** | Shaman | Enchant Item (temporary) | Item creation |
| <img class="sic" data-i="aquatic-form-passive" alt=""> **Aquatic Form (Passive)** | Druid | Apply Aura: Increase Swim Speed % + Apply Aura: Underwater Breathing | Movement |
| <img class="sic" data-i="aspect-of-the-cheetah" alt=""> **Aspect of the Cheetah** | Hunter | Apply Aura: Increase Run Speed % + Apply Aura: Proc Trigger Spell | Movement |
| <img class="sic" data-i="aspect-of-the-pack" alt=""> **Aspect of the Pack** | Hunter | Apply Area Aura: Increase Run Speed % + Apply Area Aura: Proc Trigger Spell | Movement |
| <img class="sic" data-i="dash" alt=""> **Dash** | Druid | Apply Aura: Mod Increase Speed | Movement |
| <img class="sic" data-i="levitate" alt=""> **Levitate** | Priest | Apply Aura: Feather Fall + Apply Aura: Hover + Apply Aura: Water Walk | Movement |
| <img class="sic" data-i="slow-fall" alt=""> **Slow Fall** | Mage | Apply Aura: Feather Fall | Movement |
| <img class="sic" data-i="sprint" alt=""> **Sprint** | Rogue | Apply Aura: Mod Increase Speed | Movement |
| <img class="sic" data-i="summon-charger" alt=""> **Summon Charger** | Paladin | Apply Aura: Mounted + Apply Aura: Mod Increase Mounted Speed + Script Effect | Movement |
| <img class="sic" data-i="summon-dreadsteed" alt=""> **Summon Dreadsteed** | Warlock | Apply Aura: Mounted + Apply Aura: Mod Increase Mounted Speed + Script Effect | Movement |
| <img class="sic" data-i="summon-felsteed" alt=""> **Summon Felsteed** | Warlock | Apply Aura: Mounted + Apply Aura: Mod Increase Mounted Speed + Script Effect | Movement |
| <img class="sic" data-i="summon-warhorse" alt=""> **Summon Warhorse** | Paladin | Apply Aura: Mounted + Apply Aura: Mod Increase Mounted Speed + Script Effect | Movement |
| <img class="sic" data-i="unending-breath" alt=""> **Unending Breath** | Warlock | Apply Aura: Underwater Breathing | Movement |
| <img class="sic" data-i="water-breathing" alt=""> **Water Breathing** | Shaman | Apply Aura: Underwater Breathing | Movement |
| <img class="sic" data-i="water-walking" alt=""> **Water Walking** | Shaman | Apply Aura: Water Walk | Movement |
| <img class="sic" data-i="aspect-of-the-beast" alt=""> **Aspect of the Beast** | Hunter | Apply Aura: Untrackable | Other / utility |
| <img class="sic" data-i="barkskin" alt=""> **Barkskin** | Druid | Apply Aura: Decrease Pushback Time by % (Arcane, Fire, Frost, Holy, Nature, Physical, Shadow) + Apply Aura: Modifies Cast Time (10) | Other / utility |
| <img class="sic" data-i="beast-lore" alt=""> **Beast Lore** | Hunter | Apply Aura: Empathy | Other / utility |
| <img class="sic" data-i="beast-training" alt=""> **Beast Training** | Hunter | Trade Skill Window | Other / utility |
| <img class="sic" data-i="blessing-of-kings" alt=""> **Blessing of Kings** | Paladin | Apply Aura: Mod Total Stat % | Other / utility |
| <img class="sic" data-i="blessing-of-light" alt=""> **Blessing of Light** | Paladin | Apply Aura: Dummy + Apply Aura: Dummy | Other / utility |
| <img class="sic" data-i="blessing-of-sacrifice" alt=""> **Blessing of Sacrifice** | Paladin | Apply Aura: Split Damage % | Other / utility |
| <img class="sic" data-i="blessing-of-wisdom" alt=""> **Blessing of Wisdom** | Paladin | Apply Aura: Periodically give power | Other / utility |
| <img class="sic" data-i="cobra-reflexes" alt=""> **Cobra Reflexes** | Hunter | Learn Spell | Other / utility |
| <img class="sic" data-i="combustion" alt=""> **Combustion** | Mage | Apply Aura: Dummy + Trigger Spell
Combustion | Other / utility |
| <img class="sic" data-i="concentration-aura" alt=""> **Concentration Aura** | Paladin | Apply Area Aura: Decrease Pushback Time by % (Arcane, Fire, Frost, Holy, Nature, Physical, Shadow) + Apply Area Aura: Give % Chance to Resist Mechanic (Interrupted) + Apply Area Aura: Give % Chance to Resist Mechanic (Silenced) | Other / utility |
| <img class="sic" data-i="create-healthstone" alt=""> **Create Healthstone** | Warlock | Script Effect | Other / utility |
| <img class="sic" data-i="create-healthstone-greater" alt=""> **Create Healthstone (Greater)** | Warlock | Script Effect | Other / utility |
| <img class="sic" data-i="create-healthstone-lesser" alt=""> **Create Healthstone (Lesser)** | Warlock | Script Effect | Other / utility |
| <img class="sic" data-i="create-healthstone-major" alt=""> **Create Healthstone (Major)** | Warlock | Script Effect | Other / utility |
| <img class="sic" data-i="create-healthstone-minor" alt=""> **Create Healthstone (Minor)** | Warlock | Script Effect | Other / utility |
| <img class="sic" data-i="disarm" alt=""> **Disarm** | Warrior | Apply Aura: Mod Disarm | Other / utility |
| <img class="sic" data-i="disarm-trap" alt=""> **Disarm Trap** | Rogue | Open Lock | Other / utility |
| <img class="sic" data-i="distract" alt=""> **Distract** | Rogue | Distract | Other / utility |
| <img class="sic" data-i="execute" alt=""> **Execute** | Warrior | Dummy + Trigger Spell + → Apply Aura: Dummy | Other / utility |
| <img class="sic" data-i="feline-grace" alt=""> **Feline Grace** | Druid | Apply Aura: Safe Fall | Other / utility |
| <img class="sic" data-i="flash-of-light" alt=""> **Flash of Light** | Paladin | Script Effect | Other / utility |
| <img class="sic" data-i="frenzied-regeneration" alt=""> **Frenzied Regeneration** | Druid | Apply Aura: Periodically trigger spell | Other / utility |
| <img class="sic" data-i="greater-blessing-of-kings" alt=""> **Greater Blessing of Kings** | Paladin | Apply Aura: Mod Total Stat % | Other / utility |
| <img class="sic" data-i="greater-blessing-of-light" alt=""> **Greater Blessing of Light** | Paladin | Apply Aura: Dummy + Apply Aura: Dummy | Other / utility |
| <img class="sic" data-i="greater-blessing-of-wisdom" alt=""> **Greater Blessing of Wisdom** | Paladin | Apply Aura: Periodically give power | Other / utility |
| <img class="sic" data-i="holy-light" alt=""> **Holy Light** | Paladin | Script Effect | Other / utility |
| <img class="sic" data-i="judgement" alt=""> **Judgement** | Paladin | Script Effect | Other / utility |
| <img class="sic" data-i="life-tap" alt=""> **Life Tap** | Warlock | Dummy | Other / utility |
| <img class="sic" data-i="lightning-breath" alt=""> **Lightning Breath** | Hunter | Learn Spell | Other / utility |
| <img class="sic" data-i="lightning-shield" alt=""> **Lightning Shield** | Shaman | Apply Aura: Proc Trigger Spell + → Dummy | Other / utility |
| <img class="sic" data-i="pick-lock" alt=""> **Pick Lock** | Rogue | Open Lock | Other / utility |
| <img class="sic" data-i="pick-pocket" alt=""> **Pick Pocket** | Rogue | Pickpocket | Other / utility |
| <img class="sic" data-i="poisons" alt=""> **Poisons** | Rogue | Trade Skill Window | Other / utility |
| <img class="sic" data-i="prowl" alt=""> **Prowl** | Hunter | Learn Spell | Other / utility |
| <img class="sic" data-i="rapid-fire" alt=""> **Rapid Fire** | Hunter | Apply Aura: Mod Ranged Attack Speed - % + Apply Aura: Mod Melee Attack Speed - % | Other / utility |
| <img class="sic" data-i="reincarnation" alt=""> **Reincarnation** | Shaman | Apply Aura: Dummy | Other / utility |
| <img class="sic" data-i="retaliation" alt=""> **Retaliation** | Warrior | Apply Aura: Dummy | Other / utility |
| <img class="sic" data-i="safe-fall" alt=""> **Safe Fall** | Rogue | Apply Aura: Safe Fall | Other / utility |
| <img class="sic" data-i="scorpid-poison" alt=""> **Scorpid Poison** | Hunter | Learn Spell | Other / utility |
| <img class="sic" data-i="seal-of-righteousness" alt=""> **Seal of Righteousness** | Paladin | Apply Aura: Dummy + Apply Aura: Dummy | Other / utility |
| <img class="sic" data-i="shadowguard" alt=""> **Shadowguard** | Priest | Apply Aura: Proc Trigger Spell + → Dummy | Other / utility |
| <img class="sic" data-i="slice-and-dice" alt=""> **Slice and Dice** | Rogue | Dummy + Apply Aura: Mod Haste | Other / utility |
| <img class="sic" data-i="touch-of-weakness" alt=""> **Touch of Weakness** | Priest | Apply Aura: Proc Trigger Spell + → Dummy | Other / utility |
| <img class="sic" data-i="vampiric-embrace" alt=""> **Vampiric Embrace** | Priest | Apply Aura: Dummy | Other / utility |
| <img class="sic" data-i="vanish" alt=""> **Vanish** | Rogue | Trigger Spell
Vanish + Trigger Spell
Vanish Purge + Abort All Pending Attacks | Other / utility |
| <img class="sic" data-i="detect-magic" alt=""> **Detect Magic** | Mage | Apply Aura: Detect Magic Aura | Perception |
| <img class="sic" data-i="eagle-eye" alt=""> **Eagle Eye** | Hunter | Far Sight + Apply Aura: Dummy | Perception |
| <img class="sic" data-i="far-sight" alt=""> **Far Sight** | Shaman | Far Sight + Apply Aura: Dummy | Perception |
| <img class="sic" data-i="mind-soothe" alt=""> **Mind Soothe** | Priest | Apply Aura: Mod Detect Range | Perception |
| <img class="sic" data-i="mind-vision" alt=""> **Mind Vision** | Priest | Apply Aura: Bind Sight + Apply Aura: Dummy + Apply Aura: Mod Stalked | Perception |
| <img class="sic" data-i="sense-demons" alt=""> **Sense Demons** | Warlock | Apply Aura: Track Creatures | Perception |
| <img class="sic" data-i="sense-undead" alt=""> **Sense Undead** | Paladin | Apply Aura: Track Creatures (Undead) + Update Player Phase | Perception |
| <img class="sic" data-i="soothe-animal" alt=""> **Soothe Animal** | Druid | Apply Aura: Mod Detect Range | Perception |
| <img class="sic" data-i="track-beasts" alt=""> **Track Beasts** | Hunter | Apply Aura: Track Creatures (Beast) + Apply Aura: Track Resources (24) | Perception |
| <img class="sic" data-i="track-demons" alt=""> **Track Demons** | Hunter | Apply Aura: Track Creatures | Perception |
| <img class="sic" data-i="track-dragonkin" alt=""> **Track Dragonkin** | Hunter | Apply Aura: Track Creatures | Perception |
| <img class="sic" data-i="track-elementals" alt=""> **Track Elementals** | Hunter | Apply Aura: Track Creatures | Perception |
| <img class="sic" data-i="track-giants" alt=""> **Track Giants** | Hunter | Apply Aura: Track Creatures | Perception |
| <img class="sic" data-i="track-humanoids" alt=""> **Track Humanoids** | Druid | Apply Aura: Track Creatures | Perception |
| <img class="sic" data-i="track-humanoids" alt=""> **Track Humanoids** | Hunter | Apply Aura: Track Creatures | Perception |
| <img class="sic" data-i="track-undead" alt=""> **Track Undead** | Hunter | Apply Aura: Track Creatures | Perception |
| <img class="sic" data-i="bloodrage" alt=""> **Bloodrage** | Warrior | Give Power + Trigger Spell + → Apply Aura: Periodically give power + → Apply Aura: Interrupt Power Decay | Resource manipulation |
| <img class="sic" data-i="dark-pact" alt=""> **Dark Pact** | Warlock | Power Drain | Resource manipulation |
| <img class="sic" data-i="drain-mana" alt=""> **Drain Mana** | Warlock | Apply Aura: Periodic Mana Leech | Resource manipulation |
| <img class="sic" data-i="enrage" alt=""> **Enrage** | Druid | Apply Aura: Periodically give power (Rage) + Give Power (Rage) + Apply Aura: Interrupt Power Decay + Apply Aura: Dummy | Resource manipulation |
| <img class="sic" data-i="feedback" alt=""> **Feedback** | Priest | Apply Aura: Proc Trigger Spell + → Power Burn | Resource manipulation |
| <img class="sic" data-i="mana-burn" alt=""> **Mana Burn** | Priest | Power Burn | Resource manipulation |
| <img class="sic" data-i="seal-of-wisdom" alt=""> **Seal of Wisdom** | Paladin | Apply Aura: Proc Trigger Spell + → Give Power + Apply Aura: Dummy | Resource manipulation |
| <img class="sic" data-i="viper-sting" alt=""> **Viper Sting** | Hunter | Apply Aura: Periodic Mana Leech | Resource manipulation |
| <img class="sic" data-i="ancestral-spirit" alt=""> **Ancestral Spirit** | Shaman | Resurrect | Resurrection |
| <img class="sic" data-i="rebirth" alt=""> **Rebirth** | Druid | Resurrect | Resurrection |
| <img class="sic" data-i="redemption" alt=""> **Redemption** | Paladin | Resurrect | Resurrection |
| <img class="sic" data-i="resurrection" alt=""> **Resurrection** | Priest | Resurrect | Resurrection |
| <img class="sic" data-i="blast-wave" alt=""> **Blast Wave** | Mage | School Damage (Fire) + Apply Aura: Mod Decrease Speed | Root & snare |
| <img class="sic" data-i="chilled" alt=""> **Chilled** | Mage | Apply Aura: Mod Decrease Speed | Root & snare |
| <img class="sic" data-i="concussive-shot" alt=""> **Concussive Shot** | Hunter | Apply Aura: Mod Decrease Speed | Root & snare |
| <img class="sic" data-i="cone-of-cold" alt=""> **Cone of Cold** | Mage | Apply Aura: Mod Decrease Speed + School Damage (Frost) | Root & snare |
| <img class="sic" data-i="frost-shock" alt=""> **Frost Shock** | Shaman | Apply Aura: Mod Decrease Speed + School Damage (Frost) | Root & snare |
| <img class="sic" data-i="frostbolt" alt=""> **Frostbolt** | Mage | Apply Aura: Mod Decrease Speed + School Damage (Frost) | Root & snare |
| <img class="sic" data-i="hamstring" alt=""> **Hamstring** | Warrior | School Damage (Physical) + Apply Aura: Mod Decrease Speed | Root & snare |
| <img class="sic" data-i="ice-armor" alt=""> **Ice Armor** | Mage | Apply Aura: Mod Resistance + Apply Aura: Proc Trigger Spell + → Apply Aura: Mod Decrease Speed + → Apply Aura: Mod Haste + Apply Aura: Mod Resistance | Root & snare |
| <img class="sic" data-i="mind-flay" alt=""> **Mind Flay** | Priest | Apply Aura: Periodic Damage + Apply Aura: Mod Decrease Speed | Root & snare |
| <img class="sic" data-i="nature-s-grasp" alt=""> **Nature's Grasp** | Druid | Apply Aura: Proc Trigger Spell + → Apply Aura: Mod Root + → Apply Aura: Periodic Damage | Root & snare |
| <img class="sic" data-i="aquatic-form" alt=""> **Aquatic Form** | Druid | Apply Aura: Shapeshift (Aquatic Form) + Apply Aura: Immunity - Mechanic (Polymorphed) | Shapeshift |
| <img class="sic" data-i="battle-stance" alt=""> **Battle Stance** | Warrior | Apply Aura: Shapeshift | Shapeshift |
| <img class="sic" data-i="bear-form" alt=""> **Bear Form** | Druid | Apply Aura: Shapeshift (Bear Form) + Apply Aura: Immunity - Mechanic (Polymorphed) | Shapeshift |
| <img class="sic" data-i="berserker-stance" alt=""> **Berserker Stance** | Warrior | Apply Aura: Shapeshift | Shapeshift |
| <img class="sic" data-i="cat-form" alt=""> **Cat Form** | Druid | Apply Aura: Shapeshift (Cat Form) + Apply Aura: Immunity - Mechanic (Polymorphed) + Apply Aura: Periodically trigger spell | Shapeshift |
| <img class="sic" data-i="defensive-stance" alt=""> **Defensive Stance** | Warrior | Apply Aura: Shapeshift | Shapeshift |
| <img class="sic" data-i="dire-bear-form" alt=""> **Dire Bear Form** | Druid | Apply Aura: Shapeshift (Dire Bear Form) + Apply Aura: Immunity - Mechanic (Polymorphed) | Shapeshift |
| <img class="sic" data-i="ghost-wolf" alt=""> **Ghost Wolf** | Shaman | Apply Aura: Shapeshift + Apply Aura: Mod Increase Speed | Shapeshift |
| <img class="sic" data-i="moonkin-form" alt=""> **Moonkin Form** | Druid | Apply Aura: Shapeshift (Moonkin Form) + Apply Aura: Immunity - Mechanic (Polymorphed) + Trigger Spell
Moonkin Aura + Apply Aura: Mod Threat (72) | Shapeshift |
| <img class="sic" data-i="travel-form" alt=""> **Travel Form** | Druid | Apply Aura: Shapeshift (Travel Form) + Apply Aura: Immunity - Mechanic (Polymorphed) | Shapeshift |
| <img class="sic" data-i="amplify-magic" alt=""> **Amplify Magic** | Mage | Apply Aura: Mod Damage Taken (All) + Apply Aura: Mod Healing Taken - Flat (All) | Stat & combat mods |
| <img class="sic" data-i="arcane-brilliance" alt=""> **Arcane Brilliance** | Mage | Apply Aura: Mod Stat (Intellect) | Stat & combat mods |
| <img class="sic" data-i="arcane-intellect" alt=""> **Arcane Intellect** | Mage | Apply Aura: Mod Stat (Intellect) | Stat & combat mods |
| <img class="sic" data-i="aspect-of-the-hawk" alt=""> **Aspect of the Hawk** | Hunter | Apply Aura: Mod Ranged Attack Power + Apply Aura: Proc Trigger Spell | Stat & combat mods |
| <img class="sic" data-i="aspect-of-the-monkey" alt=""> **Aspect of the Monkey** | Hunter | Apply Aura: Mod Dodge % | Stat & combat mods |
| <img class="sic" data-i="aspect-of-the-wild" alt=""> **Aspect of the Wild** | Hunter | Apply Area Aura: Mod Resistance - Flat - Does not Stack | Stat & combat mods |
| <img class="sic" data-i="battle-shout" alt=""> **Battle Shout** | Warrior | Apply Aura: Mod Attack Power | Stat & combat mods |
| <img class="sic" data-i="blessing-of-might" alt=""> **Blessing of Might** | Paladin | Apply Aura: Mod Attack Power | Stat & combat mods |
| <img class="sic" data-i="curse-of-idiocy" alt=""> **Curse of Idiocy** | Warlock | Apply Aura: Mod Stat (Intellect) + Apply Aura: Mod Stat (Spirit) + Apply Aura: Periodically trigger spell | Stat & combat mods |
| <img class="sic" data-i="curse-of-recklessness" alt=""> **Curse of Recklessness** | Warlock | Apply Aura: Mod Melee Attack Power + Apply Aura: Mod Resistance (Physical) + Apply Aura: Cannot Flee | Stat & combat mods |
| <img class="sic" data-i="curse-of-shadow" alt=""> **Curse of Shadow** | Warlock | Apply Aura: Mod Resistance + Apply Aura: Mod Damage % Taken | Stat & combat mods |
| <img class="sic" data-i="curse-of-tongues" alt=""> **Curse of Tongues** | Warlock | Apply Aura: Mod Casting Speed + Apply Aura: Mod Language | Stat & combat mods |
| <img class="sic" data-i="curse-of-weakness" alt=""> **Curse of Weakness** | Warlock | Apply Aura: Mod Damage Done | Stat & combat mods |
| <img class="sic" data-i="curse-of-the-elements" alt=""> **Curse of the Elements** | Warlock | Apply Aura: Mod Resistance + Apply Aura: Mod Damage % Taken | Stat & combat mods |
| <img class="sic" data-i="dampen-magic" alt=""> **Dampen Magic** | Mage | Apply Aura: Mod Damage Taken + Apply Aura: Mod Healing Taken - Flat | Stat & combat mods |
| <img class="sic" data-i="demon-armor" alt=""> **Demon Armor** | Warlock | Apply Aura: Mod Resistance (Physical) + Apply Aura: Mod Resistance (Shadow) + Apply Aura: Regen Health - Works in Combat | Stat & combat mods |
| <img class="sic" data-i="demon-skin" alt=""> **Demon Skin** | Warlock | Apply Aura: Mod Resistance (Physical) + Apply Aura: Regen Health - Works in Combat | Stat & combat mods |
| <img class="sic" data-i="demoralizing-roar" alt=""> **Demoralizing Roar** | Druid | Apply Aura: Mod Attack Power | Stat & combat mods |
| <img class="sic" data-i="demoralizing-shout" alt=""> **Demoralizing Shout** | Warrior | Apply Aura: Mod Attack Power | Stat & combat mods |
| <img class="sic" data-i="devotion-aura" alt=""> **Devotion Aura** | Paladin | Apply Area Aura: Mod Resistance | Stat & combat mods |
| <img class="sic" data-i="divine-shield" alt=""> **Divine Shield** | Paladin | Apply Aura: School Immunity + Apply Aura: Mod Haste + Apply Aura: School Immunity + Apply Aura: Mod Damage % Done | Stat & combat mods |
| <img class="sic" data-i="divine-spirit" alt=""> **Divine Spirit** | Priest | Apply Aura: Mod Stat (Spirit) | Stat & combat mods |
| <img class="sic" data-i="elune-s-grace" alt=""> **Elune's Grace** | Priest | Apply Aura: Mod Ranged Damage Taken - Flat (1) + Apply Aura: Mod Dodge % | Stat & combat mods |
| <img class="sic" data-i="evasion" alt=""> **Evasion** | Rogue | Apply Aura: Mod Dodge % | Stat & combat mods |
| <img class="sic" data-i="expose-armor" alt=""> **Expose Armor** | Rogue | Apply Aura: Mod Resistance + Dummy | Stat & combat mods |
| <img class="sic" data-i="faerie-fire" alt=""> **Faerie Fire** | Druid | Apply Aura: Mod Resistance (Physical) + Apply Aura: Immunity - Debuffs Only (6) + Apply Aura: Immunity - Debuffs Only (5) | Stat & combat mods |
| <img class="sic" data-i="faerie-fire-feral" alt=""> **Faerie Fire (Feral)** | Druid | Apply Aura: Mod Resistance (Physical) + Apply Aura: Immunity - Debuffs Only (6) + Apply Aura: Immunity - Debuffs Only (5) | Stat & combat mods |
| <img class="sic" data-i="fire-resistance-aura" alt=""> **Fire Resistance Aura** | Paladin | Apply Area Aura: Mod Resistance - Flat - Does not Stack | Stat & combat mods |
| <img class="sic" data-i="frost-armor" alt=""> **Frost Armor** | Mage | Apply Aura: Mod Resistance (Physical) + Apply Aura: Proc Trigger Spell | Stat & combat mods |
| <img class="sic" data-i="frost-resistance-aura" alt=""> **Frost Resistance Aura** | Paladin | Apply Area Aura: Mod Resistance - Flat - Does not Stack | Stat & combat mods |
| <img class="sic" data-i="gift-of-the-wild" alt=""> **Gift of the Wild** | Druid | Apply Aura: Mod Resistance (Physical) + Apply Aura: Mod Stat (All) + Apply Aura: Mod Resistance - Flat - Does not Stack (126) | Stat & combat mods |
| <img class="sic" data-i="greater-blessing-of-might" alt=""> **Greater Blessing of Might** | Paladin | Apply Aura: Mod Attack Power | Stat & combat mods |
| <img class="sic" data-i="greater-blessing-of-sanctuary" alt=""> **Greater Blessing of Sanctuary** | Paladin | Apply Aura: Mod Damage Taken + Apply Aura: Proc Trigger Damage | Stat & combat mods |
| <img class="sic" data-i="hex-of-weakness" alt=""> **Hex of Weakness** | Priest | Apply Aura: Mod Damage Done + Apply Aura: Mod Healing Received % | Stat & combat mods |
| <img class="sic" data-i="hunter-s-mark" alt=""> **Hunter's Mark** | Hunter | Apply Aura: Stalked + Apply Aura: Mod Attacker Ranged Attack Power | Stat & combat mods |
| <img class="sic" data-i="inner-fire" alt=""> **Inner Fire** | Priest | Apply Aura: Mod Resistance | Stat & combat mods |
| <img class="sic" data-i="mage-armor" alt=""> **Mage Armor** | Mage | Apply Aura: Mod Resistance + Apply Aura: Mod Manaregen Interrupt | Stat & combat mods |
| <img class="sic" data-i="mark-of-the-wild" alt=""> **Mark of the Wild** | Druid | Apply Aura: Mod Resistance (Physical) + Apply Aura: Mod Stat (All) + Apply Aura: Mod Resistance - Flat - Does not Stack (126) | Stat & combat mods |
| <img class="sic" data-i="power-infusion" alt=""> **Power Infusion** | Priest | Apply Aura: Mod Healing Power - % (All) + Apply Aura: Mod Damage Done % (All) | Stat & combat mods |
| <img class="sic" data-i="power-word-fortitude" alt=""> **Power Word: Fortitude** | Priest | Apply Aura: Mod Stat (Stamina) | Stat & combat mods |
| <img class="sic" data-i="prayer-of-fortitude" alt=""> **Prayer of Fortitude** | Priest | Apply Aura: Mod Stat (Stamina) | Stat & combat mods |
| <img class="sic" data-i="prayer-of-shadow-protection" alt=""> **Prayer of Shadow Protection** | Priest | Apply Aura: Mod Resistance - Flat - Does not Stack | Stat & combat mods |
| <img class="sic" data-i="prayer-of-spirit" alt=""> **Prayer of Spirit** | Priest | Apply Aura: Mod Stat (Spirit) | Stat & combat mods |
| <img class="sic" data-i="recklessness" alt=""> **Recklessness** | Warrior | Apply Aura: Mod Crit % + Apply Aura: Mod Damage % Taken + Apply Aura: Immunity - Mechanic | Stat & combat mods |
| <img class="sic" data-i="sanctity-aura" alt=""> **Sanctity Aura** | Paladin | Apply Area Aura: Mod Damage % Done | Stat & combat mods |
| <img class="sic" data-i="scorpid-sting" alt=""> **Scorpid Sting** | Hunter | Apply Aura: Mod Stat (Strength) + Apply Aura: Mod Stat (Agility) | Stat & combat mods |
| <img class="sic" data-i="seal-of-the-crusader" alt=""> **Seal of the Crusader** | Paladin | Apply Aura: Mod Attack Power + Apply Aura: Mod Attack Speed + Apply Aura: Dummy | Stat & combat mods |
| <img class="sic" data-i="shadow-protection" alt=""> **Shadow Protection** | Priest | Apply Aura: Mod Resistance - Flat - Does not Stack | Stat & combat mods |
| <img class="sic" data-i="shadow-resistance-aura" alt=""> **Shadow Resistance Aura** | Paladin | Apply Area Aura: Mod Resistance - Flat - Does not Stack | Stat & combat mods |
| <img class="sic" data-i="shield-block" alt=""> **Shield Block** | Warrior | Apply Aura: Mod Block % | Stat & combat mods |
| <img class="sic" data-i="shield-wall" alt=""> **Shield Wall** | Warrior | Apply Aura: Mod Damage % Taken | Stat & combat mods |
| <img class="sic" data-i="sunder-armor" alt=""> **Sunder Armor** | Warrior | Apply Aura: Mod Resistance | Stat & combat mods |
| <img class="sic" data-i="tiger-s-fury" alt=""> **Tiger's Fury** | Druid | Apply Aura: Mod Damage Done | Stat & combat mods |
| <img class="sic" data-i="call-pet" alt=""> **Call Pet** | Hunter | Summon Pet (0) + Script Effect | Summoning |
| <img class="sic" data-i="disease-cleansing-totem" alt=""> **Disease Cleansing Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="earthbind-totem" alt=""> **Earthbind Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="explosive-trap" alt=""> **Explosive Trap** | Hunter | Summon Trap | Summoning |
| <img class="sic" data-i="eye-of-kilrogg" alt=""> **Eye of Kilrogg** | Warlock | Summon + Apply Aura: Dummy | Summoning |
| <img class="sic" data-i="fire-nova-totem" alt=""> **Fire Nova Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="fire-resistance-totem" alt=""> **Fire Resistance Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="flametongue-totem" alt=""> **Flametongue Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="freezing-trap" alt=""> **Freezing Trap** | Hunter | Summon Trap | Summoning |
| <img class="sic" data-i="frost-resistance-totem" alt=""> **Frost Resistance Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="frost-trap" alt=""> **Frost Trap** | Hunter | Summon Trap | Summoning |
| <img class="sic" data-i="grace-of-air-totem" alt=""> **Grace of Air Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="grounding-totem" alt=""> **Grounding Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="healing-stream-totem" alt=""> **Healing Stream Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="immolation-trap" alt=""> **Immolation Trap** | Hunter | Summon Trap | Summoning |
| <img class="sic" data-i="inferno" alt=""> **Inferno** | Warlock | Summon | Summoning |
| <img class="sic" data-i="lightwell" alt=""> **Lightwell** | Priest | Trans Door | Summoning |
| <img class="sic" data-i="magma-totem" alt=""> **Magma Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="mana-spring-totem" alt=""> **Mana Spring Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="mana-tide-totem" alt=""> **Mana Tide Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="nature-resistance-totem" alt=""> **Nature Resistance Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="poison-cleansing-totem" alt=""> **Poison Cleansing Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="portal-darnassus" alt=""> **Portal: Darnassus** | Mage | Trans Door | Summoning |
| <img class="sic" data-i="portal-ironforge" alt=""> **Portal: Ironforge** | Mage | Trans Door | Summoning |
| <img class="sic" data-i="portal-orgrimmar" alt=""> **Portal: Orgrimmar** | Mage | Trans Door | Summoning |
| <img class="sic" data-i="portal-stormwind" alt=""> **Portal: Stormwind** | Mage | Trans Door | Summoning |
| <img class="sic" data-i="portal-thunder-bluff" alt=""> **Portal: Thunder Bluff** | Mage | Trans Door | Summoning |
| <img class="sic" data-i="portal-undercity" alt=""> **Portal: Undercity** | Mage | Trans Door | Summoning |
| <img class="sic" data-i="ritual-of-doom" alt=""> **Ritual of Doom** | Warlock | Trans Door | Summoning |
| <img class="sic" data-i="ritual-of-summoning" alt=""> **Ritual of Summoning** | Warlock | Trans Door | Summoning |
| <img class="sic" data-i="searing-totem" alt=""> **Searing Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="sentry-totem" alt=""> **Sentry Totem** | Shaman | Summon + Apply Aura: Dummy | Summoning |
| <img class="sic" data-i="stoneclaw-totem" alt=""> **Stoneclaw Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="stoneskin-totem" alt=""> **Stoneskin Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="strength-of-earth-totem" alt=""> **Strength of Earth Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="summon-felhunter" alt=""> **Summon Felhunter** | Warlock | Summon Pet | Summoning |
| <img class="sic" data-i="summon-imp" alt=""> **Summon Imp** | Warlock | Summon Pet | Summoning |
| <img class="sic" data-i="summon-incubus" alt=""> **Summon Incubus** | Warlock | Summon Pet | Summoning |
| <img class="sic" data-i="summon-succubus" alt=""> **Summon Succubus** | Warlock | Summon Pet | Summoning |
| <img class="sic" data-i="summon-voidwalker" alt=""> **Summon Voidwalker** | Warlock | Summon Pet | Summoning |
| <img class="sic" data-i="tremor-totem" alt=""> **Tremor Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="windfury-totem" alt=""> **Windfury Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="windwall-totem" alt=""> **Windwall Totem** | Shaman | Summon | Summoning |
| <img class="sic" data-i="astral-recall" alt=""> **Astral Recall** | Shaman | Teleport Units | Teleportation |
| <img class="sic" data-i="teleport-darnassus" alt=""> **Teleport: Darnassus** | Mage | Teleport Units + Script Effect | Teleportation |
| <img class="sic" data-i="teleport-ironforge" alt=""> **Teleport: Ironforge** | Mage | Teleport Units + Script Effect | Teleportation |
| <img class="sic" data-i="teleport-moonglade" alt=""> **Teleport: Moonglade** | Druid | Teleport Units | Teleportation |
| <img class="sic" data-i="teleport-orgrimmar" alt=""> **Teleport: Orgrimmar** | Mage | Teleport Units + Script Effect | Teleportation |
| <img class="sic" data-i="teleport-stormwind" alt=""> **Teleport: Stormwind** | Mage | Teleport Units + Script Effect | Teleportation |
| <img class="sic" data-i="teleport-thunder-bluff" alt=""> **Teleport: Thunder Bluff** | Mage | Teleport Units + Script Effect | Teleportation |
| <img class="sic" data-i="teleport-undercity" alt=""> **Teleport: Undercity** | Mage | Teleport Units + Script Effect | Teleportation |
| <img class="sic" data-i="blessing-of-salvation" alt=""> **Blessing of Salvation** | Paladin | Apply Aura: Mod Threat | Threat manipulation |
| <img class="sic" data-i="challenging-roar" alt=""> **Challenging Roar** | Druid | Apply Aura: Taunt | Threat manipulation |
| <img class="sic" data-i="challenging-shout" alt=""> **Challenging Shout** | Warrior | Apply Aura: Taunt | Threat manipulation |
| <img class="sic" data-i="cower" alt=""> **Cower** | Druid | Threat | Threat manipulation |
| <img class="sic" data-i="disengage" alt=""> **Disengage** | Hunter | Threat | Threat manipulation |
| <img class="sic" data-i="distracting-shot" alt=""> **Distracting Shot** | Hunter | Threat | Threat manipulation |
| <img class="sic" data-i="fade" alt=""> **Fade** | Priest | Apply Aura: Mod Total Threat | Threat manipulation |
| <img class="sic" data-i="feint" alt=""> **Feint** | Rogue | Threat | Threat manipulation |
| <img class="sic" data-i="greater-blessing-of-salvation" alt=""> **Greater Blessing of Salvation** | Paladin | Apply Aura: Mod Threat | Threat manipulation |
| <img class="sic" data-i="growl" alt=""> **Growl** | Druid | Taunt + Apply Aura: Taunt | Threat manipulation |
| <img class="sic" data-i="mocking-blow" alt=""> **Mocking Blow** | Warrior | School Damage (Physical) + Apply Aura: Taunt | Threat manipulation |
| <img class="sic" data-i="righteous-fury" alt=""> **Righteous Fury** | Paladin | Apply Aura: Mod Threat + Apply Aura: Add Pct Modifier | Threat manipulation |
| <img class="sic" data-i="tame-beast" alt=""> **Tame Beast** | Hunter | Threat + Apply Aura: Periodically trigger spell + Apply Aura: Mod Resistance % (Physical) | Threat manipulation |
| <img class="sic" data-i="taunt" alt=""> **Taunt** | Warrior | Taunt + Apply Aura: Taunt | Threat manipulation |
| <img class="sic" data-i="ambush" alt=""> **Ambush** | Rogue | Normalized Weapon Dmg + Weapon % Damage + Add Combo Points | Weapon strike |
| <img class="sic" data-i="auto-shot" alt=""> **Auto Shot** | Hunter | Weapon Damage | Weapon strike |
| <img class="sic" data-i="backstab" alt=""> **Backstab** | Rogue | Normalized Weapon Dmg + Weapon % Damage + Add Combo Points | Weapon strike |
| <img class="sic" data-i="claw" alt=""> **Claw** | Druid | Deal Weapon Damage + Add Combo Points | Weapon strike |
| <img class="sic" data-i="cleave" alt=""> **Cleave** | Warrior | Weapon Damage (noschool) | Weapon strike |
| <img class="sic" data-i="hemorrhage" alt=""> **Hemorrhage** | Rogue | Weapon Damage (noschool) + Add Combo Points + Apply Aura: Mod Damage Taken | Weapon strike |
| <img class="sic" data-i="heroic-strike" alt=""> **Heroic Strike** | Warrior | Weapon Damage (noschool) | Weapon strike |
| <img class="sic" data-i="maul" alt=""> **Maul** | Druid | Weapon Damage | Weapon strike |
| <img class="sic" data-i="mortal-strike" alt=""> **Mortal Strike** | Warrior | Apply Aura: Mod Healing Received % + Normalized Weapon Dmg | Weapon strike |
| <img class="sic" data-i="multi-shot" alt=""> **Multi-Shot** | Hunter | Normalized Weapon Dmg | Weapon strike |
| <img class="sic" data-i="overpower" alt=""> **Overpower** | Warrior | Normalized Weapon Dmg | Weapon strike |
| <img class="sic" data-i="raptor-strike" alt=""> **Raptor Strike** | Hunter | Weapon Damage | Weapon strike |
| <img class="sic" data-i="ravage" alt=""> **Ravage** | Druid | Deal Weapon Damage + Weapon Damage - % + Add Combo Points | Weapon strike |
| <img class="sic" data-i="shred" alt=""> **Shred** | Druid | Deal Weapon Damage + Weapon Damage - % + Add Combo Points | Weapon strike |
| <img class="sic" data-i="sinister-strike" alt=""> **Sinister Strike** | Rogue | Normalized Weapon Dmg + Add Combo Points | Weapon strike |
| <img class="sic" data-i="slam" alt=""> **Slam** | Warrior | Weapon Damage (noschool) | Weapon strike |
| <img class="sic" data-i="whirlwind" alt=""> **Whirlwind** | Warrior | Normalized Weapon Dmg | Weapon strike |

Back to [[overview|Overview]] · [[methodology|Methodology]]

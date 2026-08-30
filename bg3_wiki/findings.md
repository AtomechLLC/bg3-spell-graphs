# The Identical-Spell List

Which Baldur's Gate 3 spells are mostly the same spell. Of the **211 distinct spells** reachable through class progressions, **107 fall into 16 families** — and that's *before* counting Larian's own admission: the [[containers|28 container spells]] whose 136 variant children are reskins by design.

- <span class="tier tier-clone">Verbatim clone</span> — same mechanics, nouns swapped (or literally the same entry duplicated).
- <span class="tier tier-template">Shared template</span> — same structure, parameters differ.
- <span class="tier tier-engine">Shared engine</span> — same underlying subsystem in different clothes.

## All families

| Family | Tier | Spells | Peak mechanics | What actually differs |
|---|---|---|---|---|
| [[families/duplicate-skus|🛍️ The Duplicate SKUs]] | <span class="tier tier-clone">Verbatim clone</span> | Darkness, Eyes of the Dark: Darkness, Shield | 1.00 | nothing but the class that sells it |
| [[families/cure|❤️‍🩹 The Cure Family]] | <span class="tier tier-clone">Verbatim clone</span> | Cure Wounds, Healing Word, Mass Cure Wounds, Mass Healing Word, Prayer of Healing | 0.97 | die size, touch vs. ranged, action vs. bonus action, target count |
| [[families/ac-wardrobe|🛡️ The Armour-Class Wardrobe]] | <span class="tier tier-clone">Verbatim clone</span> | Barkskin, Mage Armour, Shield of Faith | 0.86 | how the AC number is phrased: 13+Dex, +2, or 16 |
| [[families/invisibility|🫥 The Invisibility Ladder]] | <span class="tier tier-clone">Verbatim clone</span> | Greater Invisibility, Invisibility | 0.92 | breaks-on-attack clause; duration |
| [[families/bane-bless|⚖️ Bane & Bless]] | <span class="tier tier-clone">Verbatim clone</span> | Bane, Bless | 0.77 | sign of the d4; Bane allows a save |
| [[families/cc|⛓️ The Crowd Control Cabinet]] | <span class="tier tier-template">Shared template</span> | Animal Friendship, Banishment, Blindness, Charm Person, Colour Spray, Command, Confusion, Dominate Beast, Dominate Person, Eyebite, Fear, Hold Monster, Hold Person, Hypnotic Pattern, Otto's Irresistible Dance, Sleep, Slow, Tasha's Hideous Laughter | 0.96 | the flavor of lost agency: hold, charm, sleep, fear, dance, or exile |
| [[families/melee-enhance|⚔️ The Whetstone]] | <span class="tier tier-template">Shared template</span> | Banishing Smite, Blinding Smite, Branding Smite, Crusader's Mantle, Divine Favour, Elemental Weapon, Flame Blade, Magic Weapon, Searing Smite, Shadow Blade, Staggering Smite, Thunderous Smite, Wrathful Smite | 0.94 | how the weapon hit is made bigger: smite, imbue, aura, or conjured blade |
| [[families/surfaces|🕸️ The Surface Engine]] | <span class="tier tier-template">Shared template</span> | Cloudkill, Entangle, Evard's Black Tentacles, Fog Cloud, Grease, Plant Growth, Sleet Storm, Spike Growth, Stinking Cloud, Web | 0.94 | which surface gets painted on the ground |
| [[families/blast|💥 The Elemental Blast Template]] | <span class="tier tier-template">Shared template</span> | Circle of Death, Cone of Cold, Fireball, Flame Strike, Ice Storm, Lightning Bolt, Sunbeam, Thunderwave | 0.96 | area shape, damage type, dice, save |
| [[families/travel|🌀 The Travel Agency]] | <span class="tier tier-template">Shared template</span> | Dimension Door, Enhance Leap, Feather Fall, Freedom of Movement, Gaseous Form, Grant Flight, Longstrider, Misty Step | 0.93 | the mode of getting there |
| [[families/conjure|🧞 The Summoning Contract]] | <span class="tier tier-template">Shared template</span> | Animate Dead, Conjure Elemental, Conjure Minor Elemental, Find Familiar, Flaming Sphere, Planar Ally, Spiritual Weapon | 0.97 | who — or what — answers the call |
| [[families/walls|🧱 The Wall Foundry]] | <span class="tier tier-template">Shared template</span> | Blade Barrier, Wall of Fire, Wall of Ice, Wall of Stone, Wall of Thorns | 0.97 | material, damage type, dice |
| [[families/attack-cantrips|🪄 The Damage Cantrip Engine]] | <span class="tier tier-engine">Shared engine</span> | Acid Splash, Bone Chill, Eldritch Blast, Fire Bolt, Poison Spray, Ray of Frost, Sacred Flame, Shocking Grasp, Thorn Whip | 0.95 | damage type, die size, attack vs. save, rider |
| [[families/fieldcraft|🎒 The Fieldcraft Kit]] | <span class="tier tier-engine">Shared engine</span> | Darkvision, Detect Thoughts, Disguise Self, Feign Death, Friends, Knock, Speak with Animals, Speak with Dead | 0.89 | which non-combat problem it solves: dialogue, minds, locks, faces, or sight |
| [[families/cleanse|🧼 The Cleanse Counter]] | <span class="tier tier-engine">Shared engine</span> | Greater Restoration, Lesser Restoration, Protection from Poison, Remove Curse | 0.89 | which status list gets wiped |
| [[families/d4-riders|🎲 Guidance & Resistance]] | <span class="tier tier-engine">Shared engine</span> | Guidance, Resistance | 0.89 | checks vs. saves |

## Top measured pairs

Score = 0.6 × masked mechanical-signature similarity + 0.4 × masked description similarity ([[methodology|how]]). The mechanics column is the strong signal — BG3 descriptions are short flavor text.

| Score | Mechanics | Description | Spell A | Spell B |
|---|---|---|---|---|
| `1.000` | `1.000` | `1.000` | Shield (L1) | Shield (L1) |
| `1.000` | `1.000` | `1.000` | Shield (L1) | Shield (L1) |
| `1.000` | `1.000` | `1.000` | Shield (L1) | Shield (L1) |
| `0.948` | `0.914` | `1.000` | Darkness (L2) | Eyes of the Dark: Darkness (L2) |
| `0.908` | `0.963` | `0.826` | Dominate Beast (L4) | Dominate Person (L5) |
| `0.892` | `0.932` | `0.833` | Cure Wounds (L1) | Healing Word (L1) |
| `0.887` | `0.952` | `0.789` | Hold Monster (L5) | Hold Person (L2) |
| `0.886` | `0.925` | `0.828` | Invisibility (L2) | Greater Invisibility (L4) |
| `0.829` | `0.810` | `0.857` | Barkskin (L2) | Shield of Faith (L1) |
| `0.824` | `0.930` | `0.667` | Prayer of Healing (L2) | Healing Word (L1) |
| `0.814` | `0.857` | `0.750` | Barkskin (L2) | Mage Armour (L1) |
| `0.771` | `0.773` | `0.769` | Bane (L1) | Bless (L1) |
| `0.767` | `0.944` | `0.500` | Prayer of Healing (L2) | Cure Wounds (L1) |
| `0.758` | `0.800` | `0.696` | Mage Armour (L1) | Shield of Faith (L1) |
| `0.743` | `0.857` | `0.571` | Enhance Leap (L1) | Longstrider (L1) |
| `0.741` | `0.959` | `0.414` | Lightning Bolt (L3) | Thunderwave (L1) |
| `0.741` | `0.810` | `0.636` | Blur (L2) | Dispel Evil And Good (L5) |
| `0.732` | `0.897` | `0.483` | Grease (L1) | Web (L2) |
| `0.726` | `0.810` | `0.600` | Sleep (L1) | Colour Spray (L1) |
| `0.723` | `0.974` | `0.345` | Wall of Fire (L4) | Wall of Ice (L6) |

The `1.000` rows are not measurement artifacts — Shield genuinely exists three times, once per class ([[families/duplicate-skus|the Duplicate SKUs]]).

---
*Linked from: [[classes/bard|Bard]] · [[classes/cleric|Cleric]] · [[classes/druid|Druid]] · [[classes/fighter|Fighter]] · [[classes/monk|Monk]] · [[classes/paladin|Paladin]] · [[classes/ranger|Ranger]] · [[classes/rogue|Rogue]] · [[classes/sorcerer|Sorcerer]] · [[classes/warlock|Warlock]] · [[classes/wizard|Wizard]] · [[containers|Container Spells]] · [[families/ac-wardrobe|The Armour-Class Wardrobe]] · [[families/attack-cantrips|The Damage Cantrip Engine]] · [[families/bane-bless|Bane & Bless]] · [[families/blast|The Elemental Blast Template]] · [[families/cc|The Crowd Control Cabinet]] · [[families/cleanse|The Cleanse Counter]] · [[families/conjure|The Summoning Contract]] · [[families/cure|The Cure Family]] · [[families/d4-riders|Guidance & Resistance]] · [[families/duplicate-skus|The Duplicate SKUs]] · [[families/fieldcraft|The Fieldcraft Kit]] · [[families/invisibility|The Invisibility Ladder]] · [[families/melee-enhance|The Whetstone]] · [[families/surfaces|The Surface Engine]] · [[families/travel|The Travel Agency]] · [[families/walls|The Wall Foundry]] · [[overview|Overview]] · [[spells|All Spells, Tagged]]*

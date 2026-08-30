# The Identical-Spell List

The deliverable: which D&D 5e spells are mostly the same spell. **79 of 319 SRD spells (25%) fall into 24 families** of near-identical design, sorted into three tiers:

- <span class="tier tier-clone">Verbatim clone</span> — the rules text is the same spell with nouns swapped (damage type, target type, check vs. save).
- <span class="tier tier-template">Shared template</span> — same sentence-level structure and resolution; parameters and one or two clauses differ.
- <span class="tier tier-engine">Shared engine</span> — the text diverges, but the underlying subsystem (pricing table, resolution rule, sentence skeleton) is identical.

Two recurring shapes worth naming: **horizontal reskins** (same level band, different element or target type — [[families/blast|Fireball / Lightning Bolt]], [[families/guidance-resistance|Guidance / Resistance]]) and **vertical ladders** (the same spell re-sold at a higher level with one parameter raised — [[families/dominate|Dominate]], [[families/suggestion|Suggestion → Mass Suggestion]], [[families/invisibility|Invisibility → Greater]]).

## All families

| Family | Tier | Spells | Peak similarity | What actually differs |
|---|---|---|---|---|
| [[families/cure|❤️‍🩹 The Cure Family]] | <span class="tier tier-clone">Verbatim clone</span> | Cure Wounds, Healing Word, Mass Cure Wounds, Mass Healing Word, Prayer of Healing | 0.90 | die size, action vs. bonus action, touch vs. ranged, one vs. six targets |
| [[families/dominate|🧠 The Dominate Chain]] | <span class="tier tier-clone">Verbatim clone</span> | Dominate Beast, Dominate Monster, Dominate Person | 1.00 | target creature type and spell level; upcast table |
| [[families/conjure-table|🐾 Conjure by Menu]] | <span class="tier tier-clone">Verbatim clone</span> | Conjure Animals, Conjure Minor Elementals, Conjure Woodland Beings | 0.97 | which creature-type menu you order from |
| [[families/guidance-resistance|🎲 Guidance & Resistance]] | <span class="tier tier-clone">Verbatim clone</span> | Guidance, Resistance | 0.91 | d4 on ability checks vs. d4 on saving throws |
| [[families/hold|⛓️ The Hold Pair]] | <span class="tier tier-clone">Verbatim clone</span> | Hold Monster, Hold Person | 0.69 | humanoid vs. any creature; level 2 vs. 5 |
| [[families/bane-bless|⚖️ Bane & Bless]] | <span class="tier tier-clone">Verbatim clone</span> | Bane, Bless | 0.86 | add vs. subtract the d4; Bane allows a save |
| [[families/blast|💥 The Elemental Blast Template]] | <span class="tier tier-template">Shared template</span> | Burning Hands, Circle of Death, Cone of Cold, Fireball, Flame Strike, Hellish Rebuke, Ice Storm, Lightning Bolt | 0.74 | area shape, damage type, dice, save ability |
| [[families/conjure-single|🧞 Conjure a Champion]] | <span class="tier tier-template">Shared template</span> | Conjure Celestial, Conjure Elemental, Conjure Fey | 0.81 | creature type, CR cap, what happens when concentration breaks |
| [[families/locate|🧭 The Locate Series]] | <span class="tier tier-template">Shared template</span> | Locate Animals or Plants, Locate Creature, Locate Object | 0.63 | what is sensed; the blocking material |
| [[families/detect|👁️ The Detect Series]] | <span class="tier tier-template">Shared template</span> | Detect Evil and Good, Detect Magic, Detect Poison and Disease | 0.62 | what is sensed |
| [[families/polymorph|🐸 The Polymorph Ladder]] | <span class="tier tier-template">Shared template</span> | Animal Shapes, Polymorph, True Polymorph | 0.71 | scope, permanence, target count |
| [[families/suggestion|💬 The Suggestion Pair]] | <span class="tier tier-template">Shared template</span> | Mass Suggestion, Suggestion | 0.81 | one target vs. twelve; concentration dropped; duration |
| [[families/image|🖼️ The Image Ladder]] | <span class="tier tier-template">Shared template</span> | Major Image, Silent Image | 0.72 | sound/smell/temperature added; cube size; level |
| [[families/hp-pool|🧮 The Hit-Point Pool Engine]] | <span class="tier tier-template">Shared template</span> | Color Spray, Sleep | 0.76 | unconscious vs. blinded; dice; duration |
| [[families/undead|💀 The Undead Workshop]] | <span class="tier tier-template">Shared template</span> | Animate Dead, Create Undead | 0.71 | skeleton/zombie vs. ghoul; count; level |
| [[families/invisibility|🫥 The Invisibility Ladder]] | <span class="tier tier-template">Shared template</span> | Greater Invisibility, Invisibility | 0.58 | breaks on attack/cast vs. doesn't; duration |
| [[families/disguise-seeming|🎭 The Disguise Ladder]] | <span class="tier tier-template">Shared template</span> | Disguise Self, Seeming | 0.69 | one target vs. everyone in range; duration |
| [[families/attack-cantrips|🪄 The Damage Cantrip Engine]] | <span class="tier tier-engine">Shared engine</span> | Acid Splash, Chill Touch, Eldritch Blast, Fire Bolt, Poison Spray, Ray of Frost, Sacred Flame, Shocking Grasp | 0.67 | damage type, die size, attack vs. save, minor rider |
| [[families/phantom-armory|⚔️ The Phantom Armory]] | <span class="tier tier-engine">Shared engine</span> | Arcane Hand, Arcane Sword, Faithful Hound, Flaming Sphere, Spiritual Weapon, Unseen Servant | 0.38 | what is conjured and how it attacks |
| [[families/touch-buffs|🤝 The Touch-Buff Skeleton]] | <span class="tier tier-engine">Shared engine</span> | Darkvision, Fly, Longstrider, Spider Climb, Water Breathing, Water Walk | 0.66 | the movement capability granted |
| [[families/speak-with|🗣️ The Speak-With Series]] | <span class="tier tier-engine">Shared engine</span> | Speak with Animals, Speak with Dead, Speak with Plants | 0.18 | conversation partner; what it can tell you |
| [[families/protection|🛡️ The Protection Series]] | <span class="tier tier-engine">Shared engine</span> | Protection From Energy, Protection from Evil and Good, Protection from Poison | 0.25 | threat category; exact benefit |
| [[families/dispel|🧯 The Dispel Engine]] | <span class="tier tier-engine">Shared engine</span> | Counterspell, Dispel Magic | 0.60 | action on an effect vs. reaction on a cast |
| [[families/darkness-daylight|🌗 Darkness & Daylight]] | <span class="tier tier-engine">Shared engine</span> | Darkness, Daylight | 0.66 | light vs. dark; each suppresses the other |

## Top measured pairs

Highest masked-text similarity scores across all 50,721 spell pairs (see [[methodology|Methodology]] for the masking):

| Similarity | Spell A | Spell B | Family |
|---|---|---|---|
| `1.000` | Dominate Beast (L4) | Dominate Monster (L8) | [[families/dominate|🧠 The Dominate Chain]] |
| `0.966` | Conjure Minor Elementals (L4) | Conjure Woodland Beings (L4) | [[families/conjure-table|🐾 Conjure by Menu]] |
| `0.933` | Conjure Animals (L3) | Conjure Woodland Beings (L4) | [[families/conjure-table|🐾 Conjure by Menu]] |
| `0.931` | Dominate Beast (L4) | Dominate Person (L5) | [[families/dominate|🧠 The Dominate Chain]] |
| `0.931` | Dominate Monster (L8) | Dominate Person (L5) | [[families/dominate|🧠 The Dominate Chain]] |
| `0.931` | Conjure Animals (L3) | Conjure Minor Elementals (L4) | [[families/conjure-table|🐾 Conjure by Menu]] |
| `0.907` | Guidance (L0) | Resistance (L0) | [[families/guidance-resistance|🎲 Guidance & Resistance]] |
| `0.895` | Healing Word (L1) | Prayer of Healing (L2) | [[families/cure|❤️‍🩹 The Cure Family]] |
| `0.895` | Mass Healing Word (L3) | Prayer of Healing (L2) | [[families/cure|❤️‍🩹 The Cure Family]] |
| `0.878` | Cure Wounds (L1) | Healing Word (L1) | [[families/cure|❤️‍🩹 The Cure Family]] |
| `0.857` | Bane (L1) | Bless (L1) | [[families/bane-bless|⚖️ Bane & Bless]] |
| `0.847` | Healing Word (L1) | Mass Healing Word (L3) | [[families/cure|❤️‍🩹 The Cure Family]] |
| `0.815` | Mass Suggestion (L6) | Suggestion (L2) | [[families/suggestion|💬 The Suggestion Pair]] |
| `0.814` | Conjure Elemental (L5) | Conjure Fey (L6) | [[families/conjure-single|🧞 Conjure a Champion]] |
| `0.772` | Cure Wounds (L1) | Prayer of Healing (L2) | [[families/cure|❤️‍🩹 The Cure Family]] |
| `0.764` | Color Spray (L1) | Sleep (L1) | [[families/hp-pool|🧮 The Hit-Point Pool Engine]] |
| `0.748` | Cure Wounds (L1) | Mass Healing Word (L3) | [[families/cure|❤️‍🩹 The Cure Family]] |
| `0.743` | Circle of Death (L6) | Flame Strike (L5) | [[families/blast|💥 The Elemental Blast Template]] |
| `0.738` | Healing Word (L1) | Mass Cure Wounds (L5) | [[families/cure|❤️‍🩹 The Cure Family]] |
| `0.734` | Conjure Celestial (L7) | Conjure Fey (L6) | [[families/conjure-single|🧞 Conjure a Champion]] |
| `0.733` | Flame Strike (L5) | Ice Storm (L4) | [[families/blast|💥 The Elemental Blast Template]] |
| `0.730` | Circle of Death (L6) | Cone of Cold (L5) | [[families/blast|💥 The Elemental Blast Template]] |
| `0.722` | Burning Hands (L1) | Lightning Bolt (L3) | [[families/blast|💥 The Elemental Blast Template]] |
| `0.722` | Circle of Death (L6) | Ice Storm (L4) | [[families/blast|💥 The Elemental Blast Template]] |
| `0.721` | Fireball (L3) | Lightning Bolt (L3) | [[families/blast|💥 The Elemental Blast Template]] |

Similarity is evidence, not the verdict — [[families/hold|Hold Person / Hold Monster]] score only 0.69 because of one extra targeting clause, yet are mechanically a pure clone pair. Tier assignments above weigh the mechanics.

---
*Linked from: [[classes/bard|Bard]] · [[classes/cleric|Cleric]] · [[classes/druid|Druid]] · [[classes/paladin|Paladin]] · [[classes/ranger|Ranger]] · [[classes/sorcerer|Sorcerer]] · [[classes/warlock|Warlock]] · [[classes/wizard|Wizard]] · [[families/attack-cantrips|The Damage Cantrip Engine]] · [[families/bane-bless|Bane & Bless]] · [[families/blast|The Elemental Blast Template]] · [[families/conjure-single|Conjure a Champion]] · [[families/conjure-table|Conjure by Menu]] · [[families/cure|The Cure Family]] · [[families/darkness-daylight|Darkness & Daylight]] · [[families/detect|The Detect Series]] · [[families/disguise-seeming|The Disguise Ladder]] · [[families/dispel|The Dispel Engine]] · [[families/dominate|The Dominate Chain]] · [[families/guidance-resistance|Guidance & Resistance]] · [[families/hold|The Hold Pair]] · [[families/hp-pool|The Hit-Point Pool Engine]] · [[families/image|The Image Ladder]] · [[families/invisibility|The Invisibility Ladder]] · [[families/locate|The Locate Series]] · [[families/phantom-armory|The Phantom Armory]] · [[families/polymorph|The Polymorph Ladder]] · [[families/protection|The Protection Series]] · [[families/speak-with|The Speak-With Series]] · [[families/suggestion|The Suggestion Pair]] · [[families/touch-buffs|The Touch-Buff Skeleton]] · [[families/undead|The Undead Workshop]] · [[methodology|Methodology]] · [[overview|Overview]] · [[spells|All Spells, Tagged]]*

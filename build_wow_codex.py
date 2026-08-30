"""Build the WoW Classic spell-homogeneity codex -> wow_codex.html + wow_wiki/."""
import base64
import csv as csvlib
import html as htmllib
import io
import json
import os
import re
from collections import defaultdict
from difflib import SequenceMatcher
from itertools import combinations

from PIL import Image

from wow_analyze import mask, prep, pair_score

RECS = json.load(open("wow_spells.json", encoding="utf-8"))
prep(RECS)
BYID = {r["id"]: r for r in RECS}
ICON_MAP = json.load(open("wow_icon_map.json", encoding="utf-8")) if os.path.exists("wow_icon_map.json") else {}

CLASSES = ["Druid", "Hunter", "Mage", "Paladin", "Priest", "Rogue", "Shaman", "Warlock", "Warrior"]

def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

def by_name(name):
    return [r for r in RECS if r["name"] == name]

def sim(a, b):
    """Blended mechanical similarity: 0.6 x SpellEffect signature + 0.4 x masked tooltip."""
    return pair_score(BYID[a], BYID[b])[0]

# ---------------------------------------------------------------- families
CLONE, TEMPLATE, ENGINE = "clone", "template", "engine"
TIER_LABEL = {CLONE: "Verbatim clone", TEMPLATE: "Shared template", ENGINE: "Shared engine"}

F = []
def fam(slug_, title, tier, icon, member_names, differs, shared, varies, read):
    members = []
    for nm in member_names:
        rs = by_name(nm)
        if not rs:
            print(f"  ! family {slug_}: no ability named {nm!r}")
        members += [r["id"] for r in rs]
    if len(members) > 1:
        F.append(dict(slug=slug_, title=title, tier=tier, icon=icon, members=members,
                      differs=differs, shared=shared, varies=varies, read=read))

fam("tracking", "The Surveillance Suite", CLONE, "🐾",
    ["Track Beasts", "Track Humanoids", "Track Undead", "Track Hidden", "Track Elementals",
     "Track Demons", "Track Giants", "Track Dragonkin", "Sense Undead", "Sense Demons",
     "Far Sight", "Eagle Eye", "Mind Vision", "Sentry Totem", "Detect Magic",
     "Detect Traps", "Flare",
     "Detect Lesser Invisibility", "Detect Invisibility", "Detect Greater Invisibility"],
    "what is revealed, and through which lens",
    "Information as a product line. The tracking dial: 'Shows the location of all nearby X on the minimap' — one sentence, one noun slot, ten copies (masked similarity ≥ 0.9 across all of them). The remote eyes: Far Sight / Eagle Eye / Mind Vision / Sentry Totem all run `Bind Sight`-style viewing — the same periscope sold to four classes. The reveals: Detect Magic, Detect Traps, Flare, and the three-tier Detect Invisibility ladder (one `Mod Invisibility Detection` aura at three magnitudes).",
    "The revealed category (creatures, terrain, minds, magic, traps, the invisible), the lens (minimap, remote camera, aura), and the class stamp.",
    "Every way classic lets you know what you couldn't see, filed as one function — the purest reskin racks in the game live here."),
fam("teleports", "The Hearth Network", CLONE, "🌀",
    ["Teleport: Stormwind", "Teleport: Ironforge", "Teleport: Darnassus", "Teleport: Orgrimmar",
     "Teleport: Undercity", "Teleport: Thunder Bluff", "Portal: Stormwind", "Portal: Ironforge",
     "Portal: Darnassus", "Portal: Orgrimmar", "Portal: Undercity", "Portal: Thunder Bluff"],
    "the destination city; self vs. group",
    "'Teleports the caster to X' / 'Creates a portal, teleporting group members that use it to X.' Twelve spellbook entries from two sentence templates and six city names.",
    "The city, and the self/group tier — the same single-vs-group axis as the [[families/status-boosts|status-boost rack]].",
    "A 6×2 product matrix shipped as twelve spells. The faction split even hides half the matrix from each player."),
fam("conjured", "The Conjured Commissary", CLONE, "💎",
    ["Conjure Mana Agate", "Conjure Mana Jade", "Conjure Mana Citrine", "Conjure Mana Ruby",
     "Create Healthstone (Minor)", "Create Healthstone (Lesser)", "Create Healthstone",
     "Create Healthstone (Greater)", "Create Healthstone (Major)",
     "Create Firestone (Lesser)", "Create Firestone", "Create Firestone (Greater)",
     "Create Firestone (Major)", "Create Spellstone", "Create Spellstone (Greater)",
     "Create Spellstone (Major)", "Conjure Food", "Conjure Water"],
    "the item conjured; the tier in parentheses",
    "'Creates/Conjures an X that can be used to Y.' The Mage's mana gems and the Warlock's Healthstones measure ≥ 0.85 against each other — the same vending-machine engine across two classes, with the tier ladder written into the item name instead of a rank number.",
    "The item, its potency tier, and which class's flavor it wears (gems vs. stones).",
    "Classic's most honest reskin: the parenthetical '(Greater)' is a rank label promoted into the spell name — a shelf of spellbook lines from one template. (The Soulstones share this vending chassis but their *purpose* is revival, so they file under [[families/rez|the Resurrection Union]].)"),
fam("hots", "The Mending Clock", CLONE, "⏳",
    ["Renew", "Rejuvenation", "Regrowth", "Tranquility", "Frenzied Regeneration",
     "Mend Pet", "Health Funnel"],
    "class stamp, tick budget, delivery — and who pays for the ticks",
    "Healing on a timer: all of it runs the `Periodic Heal` engine. Renew and Rejuvenation are the cross-class twins — the Priest's and Druid's versions of the identical tick engine; Regrowth bolts a direct heal onto the front, Tranquility channels it into the whole party, and the pet-keepers get their own pair — Mend Pet (Hunter, mana-paid) and Health Funnel (Warlock, blood-paid): the same channeled HoT pointed at a companion, priced in two currencies.",
    "The class stamp, the tick size and duration, the delivery (single, front-loaded, channeled group, channeled-at-pet), and the resource paying for it.",
    "The heal-over-time engine is [[families/dots|the affliction engine]] with the sign flipped — same clock, opposite payload, and the same cross-class twinning (Renew/Rejuvenation mirror SW:Pain/Corruption)."),
fam("heals", "One Heal, Nine Names", CLONE, "❤️‍🩹",
    ["Lesser Heal", "Heal", "Greater Heal", "Flash Heal", "Healing Touch",
     "Healing Wave", "Lesser Healing Wave", "Holy Light", "Flash of Light",
     "Chain Heal", "Prayer of Healing", "Lay on Hands", "Desperate Prayer"],
    "class flavor, cast speed, and efficiency knobs",
    "'Heal your target for X.' Four healing classes, nine spells, one design: Flash Heal / Flash of Light / Lesser Healing Wave are the fast-expensive skin, Greater Heal / Holy Light / Healing Wave the slow-efficient skin, all measuring 0.85+ against their cross-class twins.",
    "The class stamp, cast time, and coefficient — plus the Priest's vertical Lesser→Heal→Greater ladder sold as three separate spells *before* ranks multiply them.",
    "The definitive cross-class clone: every healer bought the same spell in a different box. Homogeneity in classic WoW runs across classes more than within them."),
fam("status-boosts", "The Status Boost Rack", TEMPLATE, "🙌",
    ["Arcane Intellect", "Arcane Brilliance", "Power Word: Fortitude", "Prayer of Fortitude",
     "Divine Spirit", "Prayer of Spirit", "Shadow Protection", "Prayer of Shadow Protection",
     "Mark of the Wild", "Gift of the Wild",
     "Blessing of Might", "Blessing of Wisdom", "Blessing of Kings", "Blessing of Salvation",
     "Blessing of Light", "Blessing of Freedom", "Blessing of Sacrifice",
     "Devotion Aura", "Retribution Aura", "Concentration Aura", "Sanctity Aura",
     "Shadow Resistance Aura", "Frost Resistance Aura", "Fire Resistance Aura",
     "Greater Blessing of Kings", "Greater Blessing of Might", "Greater Blessing of Wisdom",
     "Greater Blessing of Salvation", "Greater Blessing of Sanctuary", "Greater Blessing of Light",
     "Battle Shout", "Power Infusion", "Combustion", "Recklessness", "Rapid Fire"],
    "the stat granted, and the delivery: touch, blessing slot, or radius",
    "One design — 'grant a friendly target a persistent stat modifier' — delivered through three chassis. The buff-and-prayer pairs (Arcane Intellect→Brilliance, Fortitude→Prayer of Fortitude, Mark→Gift) double every buff into a party version with a reagent cost. The Blessing rack sells the same chassis seven times (Might/Wisdom/Kings measure 0.83–0.91), each with a 'Greater' twin. The Aura carousel broadcasts it in a 30-yard radius, one at a time — the resistance trio is word-identical but for the school (0.9+).",
    "The stat (intellect, stamina, spirit, attack power, resistances…), the delivery mechanism (cast buff / blessing slot / radiating aura), single vs. group, and the reagent.",
    "The whole ally-buff economy of classic is one status-boost design: 24 spellbook entries, three delivery skins, four classes. The modal one-at-a-time dial reappears zoologically as the Hunter's [[families/aspects|Aspects]]."),
fam("aspects", "The Aspect Dial", TEMPLATE, "🦅",
    ["Aspect of the Monkey", "Aspect of the Hawk", "Aspect of the Cheetah",
     "Aspect of the Beast", "Aspect of the Pack", "Aspect of the Wild"],
    "the animal and its bonus",
    "'The hunter takes on the aspect of X, gaining Y. Only one Aspect can be active at a time.' Monkey/Hawk measure 0.82.",
    "The animal skin and the stat it carries; Pack/Wild are the group-cast versions — the group-cast axis of the [[families/status-boosts|status-boost rack]] inside the dial.",
    "Same modal engine as the [[families/status-boosts|Paladin auras]], reskinned zoologically."),
fam("forms", "The Form Rack", TEMPLATE, "🐻",
    ["Bear Form", "Dire Bear Form", "Cat Form", "Aquatic Form", "Travel Form", "Moonkin Form",
     "Battle Stance", "Defensive Stance", "Berserker Stance"],
    "the body — or posture — worn",
    "Every druid form is the identical two-aura package: `Shapeshift (X)` plus `Immunity - Mechanic (Polymorphed)`, all clustering above 0.78. The Warrior's stances run the *same `Shapeshift` aura* with the fur removed — the effect data files Battle, Defensive, and Berserker Stance as forms.",
    "The form or stance, its stat payload, and which kit it unlocks.",
    "One mode-switch chassis across two classes; the abilities each mode unlocks are filed in the function families they belong to (the cat's openers with the [[families/melee-enhance|strikes]], the bear's roar with the [[families/threat|Aggro Ledger]])."),
fam("siphons", "The Siphon Set", ENGINE, "🧛",
    ["Drain Life", "Drain Mana", "Siphon Life", "Mana Burn", "Life Tap",
     "Vampiric Embrace", "Dark Pact", "Feedback", "Bloodrage", "Enrage"],
    # Health Funnel moved to the Mending Clock: its function is pet healing
    "what is drained, and in which direction",
    "The resource-warfare engine as a family: Drain Life and Siphon Life run `Periodic Leech`, Drain Mana runs `Periodic Mana Leech`, Mana Burn is the burst `Power Burn`, and Life Tap points the same pump at yourself (health → mana).",
    "The drained resource (health/mana), the direction (enemy → you, or you → you), and channel vs. burst.",
    "One pump, five plumbings — the Warlock and Priest split a design D&D barely has."),
fam("cc", "The Crowd Control Cabinet", TEMPLATE, "⛓️",
    ["Fear", "Psychic Scream", "Intimidating Shout", "Scare Beast", "Howl of Terror",
     "Turn Undead", "Polymorph", "Polymorph: Cow", "Hibernate", "Wyvern Sting", "Sap",
     "Bash", "Hammer of Justice", "Cheap Shot", "Kidney Shot", "Pounce",
     "Mind Control", "Subjugate Demon", "Banish", "Shackle Undead", "Repentance",
     "Blind", "Gouge", "Death Coil", "Disarm"],
    "the flavor of lost agency: flee, sleep, stun, sheep, charm, or exile",
    "One purpose — deny the target its turns — implemented through a handful of aura codes and dressed in every class's colors. The fears (Fear / Psychic Scream / Intimidating Shout / Scare Beast / Howl of Terror / Turn Undead) all apply `Mod Fear`; the sleeps (Hibernate / Wyvern Sting / Sap / Gouge / Blind) and stuns (Bash / Hammer of Justice / Cheap Shot / Kidney Shot / Pounce) run the same `Stun`-shaped incapacitates, with Bash/Hammer of Justice measuring ≥ 0.78 as a cross-class pair; the charms (Mind Control / Subjugate Demon) share `Mod Charm`; and the exiles (Banish / Shackle Undead / Repentance / Polymorph) are the same removal-without-damage parameterized by creature type.",
    "The aura flavor, the legal target types, the delivery (cast, sting, ambush), and the damage-breaks clause.",
    "Crowd control is one design department in every class's uniform — target-type gating (beasts-only, undead-only, demons-only, humanoids-only) does the work D&D does with spell level."),
fam("static-shell", "The Static Shell", CLONE, "🌩️",
    ["Lightning Shield", "Shadowguard", "Thorns", "Retaliation"],
    "the school of the retaliation",
    "Lightning Shield and Shadowguard are structurally identical proc-shells (`Proc Trigger Spell` firing a damage payload at attackers) — the Troll Priest racial even ships with Lightning Shield's icon. Thorns is the same retaliation design on the plain `Damage Shield` aura.",
    "The school (nature/shadow), charge counting, and which class wears it.",
    "A cross-class SKU caught red-handed by both the effect table and the art pipeline."),
fam("traps", "The Trap Line", TEMPLATE, "🪤",
    ["Explosive Trap", "Freezing Trap", "Frost Trap", "Immolation Trap"],
    "the payload buried in the ground",
    "All four run the identical `Summon Trap` effect (id 320 in the game data) — one buried trigger object, four payloads: burst fire, freeze, frost slow, immolation DoT. An effect-revealed family: the tooltips read differently, the machinery is one line.",
    "The payload and its school; arming time and cooldown are shared.",
    "The Hunter's [[families/totems|totem foundry]] inverted — instead of a standing object that helps allies, a buried object that ambushes enemies, stamped four times."),
fam("gap-closers", "The Gap Closers", CLONE, "🏃",
    ["Charge", "Intercept"],
    "which stance sells it, and stun vs. daze",
    "Both are the literal `Charge` effect (id 96) plus a rider on arrival — the same movement engine sold to Battle Stance and Berserker Stance separately.",
    "The stance gate, the resource (generates rage vs. costs it), and the arrival rider.",
    "A within-class SKU pair exposed by the effect data: one charge, two stances, two spellbook lines."),
fam("fieldcraft", "The Fieldcraft Kit", ENGINE, "🎒",
    ["Mind Soothe", "Soothe Animal", "Unending Breath", "Water Breathing",
     "Pick Lock", "Pick Pocket", "Disarm Trap", "Poisons"],
    "which non-combat problem it solves: notice, breath, locks, purses, traps, or vials",
    "The abilities whose job is the world, not the fight. The soothes (Mind Soothe / Soothe Animal — one `Mod Detect Range` aura, two creature types, two classes: WoW's Charm Person / Animal Friendship split) shrink how far things notice you; the breaths (Unending Breath / Water Breathing — one `Underwater Breathing` aura in two class books) keep you under; and the Rogue's toolkit (Pick Lock / Pick Pocket / Disarm Trap / the Poisons crafting window) opens, empties, defuses, and brews.",
    "The problem solved, the target (mind, lungs, lock, pocket, trap, vial), and the class stamp.",
    "Downtime is a design space too — and even here the reskins run cross-class: both soothe spells and both breath spells are single auras sold twice."),
fam("shards", "The Shard Economy", ENGINE, "🔮",
    ["Drain Soul", "Shadowburn"],
    "channel vs. burst delivery",
    "Both carry `Create Soul Shard on Death` (aura 86) — the Warlock's reagent economy implemented as a rider on two very different damage spells.",
    "The delivery (slow channel vs. instant burst) and the damage profile.",
    "An economy engine hiding inside damage spells; invisible to tooltip reading, obvious in the aura table."),
fam("totems", "The Totem Foundry", TEMPLATE, "🗿",
    ["Stoneskin Totem", "Windwall Totem", "Strength of Earth Totem", "Grace of Air Totem",
     "Mana Spring Totem", "Mana Tide Totem", "Healing Stream Totem", "Searing Totem",
     "Magma Totem", "Fire Nova Totem", "Poison Cleansing Totem", "Disease Cleansing Totem",
     "Tremor Totem", "Grounding Totem", "Windfury Totem", "Flametongue Totem",
     "Frost Resistance Totem", "Fire Resistance Totem", "Nature Resistance Totem",
     "Stoneclaw Totem", "Earthbind Totem"],
    "the payload planted in the ground",
    "'Summons an X Totem with 5 health at the feet of the caster for Y sec, that does Z.' Twenty-one spells share the summoning chassis; the pairs inside (resistance totems, cleansing totems, stat totems) measure 0.8–0.95.",
    "The totem's payload and element bucket (one totem per element active).",
    "The largest single-class template family in classic — a foundry casting one mold with twenty-one fillings."),
fam("curses", "The Debuff Bureau", TEMPLATE, "💀",
    ["Curse of Agony", "Curse of Weakness", "Curse of Recklessness", "Curse of Tongues",
     "Curse of the Elements", "Curse of Shadow", "Curse of Doom", "Curse of Idiocy",
     "Hex of Weakness", "Touch of Weakness", "Faerie Fire", "Faerie Fire (Feral)",
     "Hunter's Mark", "Expose Armor", "Sunder Armor", "Demoralizing Shout",
     "Demoralizing Roar"],
    "the stat taken away, and which class's stamp is on the form",
    "Weakening without disabling, filed by function: the Warlock's modal curse rack ('Curses the target with X' — Elements/Shadow are the same spell with the school swapped, 0.85), the Priest racials that photocopy it (Hex of Weakness / Touch of Weakness are Curse of Weakness in a cassock), the marks that make targets easier to kill (Faerie Fire ×2 / Hunter's Mark), the armor shredders (Expose Armor / Sunder Armor — rogue and warrior versions of one `Mod Resistance` debuff), and the war-cries that shrink attack power (Demoralizing Shout→Roar, another warrior→bear photocopy).",
    "The drained quantity (stats, armor, attack power, castability), the stacking rule, and the class stamp.",
    "The [[families/status-boosts|status-boost rack]] with the sign flipped — and just as cross-class."),
fam("protection", "The Protection Rack", TEMPLATE, "🧿",
    ["Frost Armor", "Ice Armor", "Mage Armor", "Demon Skin", "Demon Armor",
     "Inner Fire", "Fire Ward", "Frost Ward", "Shadow Ward", "Power Word: Shield",
     "Ice Barrier", "Mana Shield", "Barkskin", "Shield Block", "Evasion",
     "Ice Block", "Shield Wall", "Divine Shield", "Divine Protection",
     "Blessing of Protection", "Fear Ward", "Divine Intervention", "Elune's Grace",
     "Berserker Rage"],
    "how the damage is refused: armor, absorb, ward, dodge, or a wall of no",
    "One protection effect in four grammars. The armors — 'Increases armor by X' plus a class rider — where Frost→Ice Armor is a renamed rank jump (0.9) and Demon Skin→Demon Armor the same trick in the Warlock book, with Inner Fire and Barkskin as further skins. The absorbs — the school wards (0.9+ across Fire/Frost/Shadow Ward, the WoW twin of BG3's triple Shield SKUs), Power Word: Shield, Ice Barrier, and Mana Shield, all `School Absorb`. The avoidances — Shield Block and Evasion, the same dodge/block-percent dial in two books. And the panic buttons — Ice Block / Shield Wall / Divine Shield / Divine Protection / Blessing of Protection / Fear Ward: temporary immunity or heavy mitigation on a long cooldown, one design in five class colors.",
    "The refusal mechanism (armor value, absorb pool, avoidance percent, immunity window), the duration-versus-cooldown ratio, and which class's book carries it.",
    "Merged on the effect, not the name: everything whose only job is 'take less damage' is one defensive design wearing four vocabularies across seven classes."),
fam("bolts", "The Bolt Engine", ENGINE, "🏹",
    ["Fireball", "Pyroblast", "Frostbolt", "Shadow Bolt", "Wrath", "Starfire",
     "Lightning Bolt", "Smite", "Holy Fire", "Mind Blast", "Fire Blast", "Scorch", "Soul Fire",
     "Arcane Missiles", "Arcane Shot",
     "Searing Pain", "Conflagrate", "Exorcism", "Hammer of Wrath"],
    "school, speed, and rider",
    "Cast-time nuke: 'Hurls/Launches/Causes X school damage.' Fireball/Pyroblast measure 0.80; the cross-class copies (Wrath, Lightning Bolt, Smite) share the skeleton with class-flavored verbs.",
    "The school, cast time, coefficient, and a small rider (Fireball's dot, Frostbolt's slow, Holy Fire's burn).",
    "Every caster's default button is the same engine — the classic archetype-defining spell is the least differentiated design in the game."),
fam("dots", "The Affliction Engine", ENGINE, "🩸",
    ["Shadow Word: Pain", "Corruption", "Immolate", "Moonfire", "Rend",
     "Garrote", "Rupture", "Serpent Sting", "Scorpid Sting", "Viper Sting",
     "Devouring Plague", "Starshards", "Insect Swarm", "Rake", "Rip", "Black Arrow",
     "Mind Flay", "Flame Shock"],
    "school, duration, and delivery",
    "'Causes X damage over Y sec' on a single target. Moonfire/Immolate measure 0.82 — the same design under different star signs — and the engine scales without changing: cast dots (SW:Pain / Corruption / Devouring Plague / Starshards — the priest racials are literal SW:Pain reskins), sting-delivered dots and drains (Serpent / Scorpid / Viper, 0.81–0.89 pairwise), physical bleeds on weapon damage (Rend / Garrote / Rupture / Rake / Rip), and channeled dots (Mind Flay). The same aura painted over an area is [[families/aoe-damage|the Area Barrage]].",
    "School, tick rate, delivery (cast, sting, bleed, channel), and whether an upfront hit rides along.",
    "One damage-over-time chassis serving all nine classes."),
fam("summons", "The Menagerie", TEMPLATE, "😈",
    ["Summon Imp", "Summon Voidwalker", "Summon Succubus", "Summon Felhunter",
     "Summon Incubus", "Summon Warhorse", "Summon Charger", "Summon Felsteed", "Summon Dreadsteed",
     "Eye of Kilrogg", "Ritual of Summoning", "Inferno", "Ritual of Doom",
     "Call Pet", "Tame Beast", "Revive Pet", "Dismiss Pet", "Eyes of the Beast", "Lightwell",
     "Beast Training", "Beast Lore", "Feed Pet", "Cobra Reflexes", "Lightning Breath",
     "Scorpid Poison"],
    "who — or what — answers the call, and which class holds the leash",
    "'Summons an X under the command of the caster' — every class's companion runs the same contract. The Warlock's four demons are one contract with four signatories (0.85+); the Hunter's stable is the same system with a taming step (Tame Beast / Call Pet / Dismiss Pet / Revive Pet mirror the demon workflow verb for verb); the mounts are the same ladder twice, holy and fel; and the engine stretches to scouting eyes (Eye of Kilrogg, Eyes of the Beast), player-summoning taxi rituals, and one-shot infernals.",
    "The summoned entity (demon, beast, steed, eye, party member, infernal), its permanence, the acquisition step, and the ritual cost. (The pets' own abilities — Spell Lock, Devour Magic — are taught to the pet, outside the trainer-book population studied here.)",
    "Cross-class summoning is one engine wearing class-flavored leashes — BG3's container spells, twenty years early."),
fam("rez", "The Resurrection Union", CLONE, "⚰️",
    ["Resurrection", "Redemption", "Ancestral Spirit", "Rebirth", "Reincarnation",
     "Create Soulstone (Minor)", "Create Soulstone (Lesser)", "Create Soulstone",
     "Create Soulstone (Greater)", "Create Soulstone (Major)"],
    "the class label, the cooldown, and whether the rez is cast or carried",
    "'Returns the spirit to the body, restoring a dead target to life with X health and mana.' Four classes, four names, one sentence (0.85+ pairwise; Rebirth adds 'usable in combat') — plus the Warlock's five Soulstone tiers: the same resurrection pre-paid into an item, cast before death instead of after.",
    "The name, Rebirth's combat clause, and the delivery — direct cast vs. the Soulstone's stored charge (with its tier ladder written into the item name).",
    "The clearest evidence that class kits were filled from a shared parts bin: death care is a franchise, and the Warlock's branch sells it as a prepaid card."),
fam("aoe-damage", "The Area Barrage", TEMPLATE, "💥",
    ["Blizzard", "Rain of Fire", "Hurricane", "Volley", "Flamestrike", "Consecration",
     "Hellfire", "Arcane Explosion", "Holy Nova", "Chain Lightning", "Holy Wrath",
     "Multi-Shot", "Whirlwind", "Cleave", "Thunder Clap", "Blast Wave", "Cone of Cold"],
    "the shape and school of the field",
    "Damage that hits more than one target, in every delivery the game knows: the channeled rains (Blizzard / Rain of Fire / Hurricane / Volley — a four-class verbatim clone of one channel-the-sky design), the ground fields (Flamestrike / Consecration / Hellfire), the point-blank bursts (Arcane Explosion / Holy Nova / Thunder Clap / Blast Wave / Cone of Cold), the weapon sweeps (Whirlwind / Cleave / Multi-Shot), and the bounces (Chain Lightning — [[families/heals|Chain Heal]]'s hostile twin — and Holy Wrath).",
    "School, shape (rain, field, nova, sweep, bounce), channel vs. instant, and the rider (slow, daze).",
    "AoE damage as one product in five shapes — the rains alone are as tight a cross-class clone as the heals."),
fam("melee-enhance", "The Whetstone & The Strike", TEMPLATE, "⚔️",
    ["Rockbiter Weapon", "Flametongue Weapon", "Frostbrand Weapon", "Windfury Weapon",
     "Mind-numbing Poison", "Mind-numbing Poison II", "Mind-numbing Poison III",
     "Auto Shot", "Mortal Strike", "Heroic Strike", "Slam",
     "Overpower", "Revenge", "Bloodthirst", "Execute", "Counterattack",
     "Sinister Strike", "Hemorrhage", "Eviscerate", "Slice and Dice",
     "Raptor Strike", "Mongoose Bite",
     "Ambush", "Ravage", "Backstab", "Shred", "Claw", "Maul", "Swipe", "Mangle",
     "Ferocious Bite", "Tiger's Fury"],
    "how the weapon hit is made bigger: imbue, on-next-swing, opener, or finisher",
    "Everything that turns a weapon swing into more than a swing. The imbues (Rockbiter / Flametongue / Frostbrand / Windfury, plus the Rogue's poison coatings — Mind-numbing I–III, rank numbers promoted into spell names) are one `Enchant Item (temporary)` rack; the strikes (Mortal Strike / Heroic Strike / Slam / Cleave / Raptor Strike / Sinister Strike…) all run `Weapon Damage` / `Normalized Weapon Dmg` effects; the stealth-openers photocopy across classes (Ambush→Ravage, Backstab→Shred measure 0.8–0.95); and the finishers (Eviscerate / Ferocious Bite) spend the same combo currency.",
    "The delivery slot (imbue, next-swing, opener, finisher), the class, the resource, and the rider.",
    "The melee half of the game is one enhancement engine wearing thirty coats — including the Feral Druid's, whose cat kit is a licensed photocopy of the Rogue's (Backstab→Shred, Ambush→Ravage) and whose bear kit borrows the Warrior's (Heroic Strike→Maul)."),
fam("threat", "The Aggro Ledger", CLONE, "😡",
    ["Taunt", "Growl", "Challenging Shout", "Challenging Roar", "Mocking Blow",
     "Cower", "Feint", "Fade", "Disengage", "Distracting Shot", "Righteous Fury",
     "Distract"],
    "the sign of the threat edit, and who performs it",
    "Every entry edits the threat table and nothing else: the taunts (Taunt / Growl / Mocking Blow / Challenging Shout / Challenging Roar — `Taunt` and `Attack Me` effects, with Taunt→Growl a verbatim cross-class pair) force attention; the dumps (Cower / Feint / Fade / Disengage / Distracting Shot — `Mod Threat` with a negative sign) shed it; Righteous Fury multiplies it passively.",
    "The sign (+/−), the delivery, and the class stamp.",
    "The purpose born in the MMO gets its own family: one ledger, eleven pens, and the druid's entries are photocopies of the warrior's and rogue's."),
fam("travel", "The Travel Agency", CLONE, "🌀",
    ["Blink", "Teleport: Moonglade", "Astral Recall", "Sprint", "Dash", "Ghost Wolf",
     "Water Walking", "Levitate", "Slow Fall", "Feline Grace", "Safe Fall",
     "Aquatic Form (Passive)"],
    "the mode of getting there (or of not dying on arrival)",
    "Movement as a product line: short-range teleports (Blink), hearth-style returns (Astral Recall, Teleport: Moonglade), sprint buffs (Sprint→Dash, another verbatim rogue→cat photocopy on `Mod Increase Speed`), travel modes (Ghost Wolf), water and air utilities (Water Walking / Levitate / Slow Fall), and fall protection (Safe Fall→Feline Grace, one aura in two books).",
    "The medium (ground, water, air), the delivery, and the class stamp.",
    "The [[families/teleports|Hearth Network]] handles the cities; this family covers every other way classic lets you move — or land."),
fam("concealment", "The Vanishing Act", CLONE, "🎭",
    ["Stealth", "Prowl", "Vanish", "Feign Death"],
    "how you stop being a target",
    "Stealth and Prowl are the same `Mod Stealth` package (0.8+ pair, rogue→cat); Vanish is Stealth with an escape trigger (the effect chain resolves to `Mod Stealth` + speed); Feign Death fakes the exit instead of taking it.",
    "The exit mechanism (crouch, escape, play dead) and the class stamp.",
    "Not being attackable is one design with three doors — two of them photocopied between Rogue and Druid."),
fam("snares", "The Slow Lane", TEMPLATE, "🥶",
    ["Entangling Roots", "Frost Nova", "Nature's Grasp", "Hamstring", "Wing Clip",
     "Concussive Shot", "Chilled", "Frost Shock"],
    "root vs. snare, and the delivery",
    "Soft control on one pair of auras: the roots (Entangling Roots / Frost Nova / Nature's Grasp — `Mod Root`) pin in place; the snares (Hamstring / Wing Clip / Concussive Shot / Chilled / Cone of Cold / Blast Wave — `Mod Decrease Speed`) slow the chase.",
    "Root vs. snare, single vs. area, and whether damage rides along.",
    "The [[families/cc|Crowd Control Cabinet]]'s outpatient wing: agency reduced, not removed."),
fam("interrupts", "The Interrupt Union", CLONE, "✋",
    ["Kick", "Pummel", "Shield Bash", "Counterspell", "Earth Shock"],
    "the limb, element, or arcana used",
    "'Interrupts the spell being cast, preventing that school of magic for Y sec.' Kick/Pummel/Shield Bash are word-for-word siblings; Earth Shock is the same lockout wearing an elemental coat (0.72 against the melee versions — the famous shock trio dissolves by function: Flame Shock to [[families/dots|the Affliction Engine]], Frost Shock to [[families/snares|the Slow Lane]]); Counterspell is the lockout without the damage rider. (The Felhunter's Spell Lock runs the identical design as a pet ability, outside this trainer-book population.)",
    "The animation, the resource paying for it, and whether a damage rider comes along.",
    "Like [[families/rez|resurrection]], a cross-class utility franchise — every class got the same button with a different glove."),
fam("cleanses", "The Cleanse Counter", CLONE, "🧼",
    ["Cure Poison", "Cure Disease", "Abolish Poison", "Abolish Disease",
     "Remove Lesser Curse", "Remove Curse", "Purify", "Cleanse", "Dispel Magic", "Purge",
     "Shield Slam", "Tranquilizing Shot"],
    "the debuff type removed — Cure Poison ships in two class books verbatim",
    "'Cures/Removes X from the friendly target.' Cure Poison appears in both the Druid and Shaman books as the *same spell* — name, text, and all (the WoW equivalent of BG3's duplicate Shield SKUs). Abolish adds a re-tick; Purify/Cleanse bundle two types.",
    "The debuff category and the bundling tier.",
    "A one-verb engine with a type parameter, sold across five classes."),
fam("mirror", "Amplify & Dampen", CLONE, "🪞",
    ["Amplify Magic", "Dampen Magic"],
    "the sign",
    "'Amplifies/Dampens magic used against the targeted party member, increasing/decreasing healing and damage taken by X.' A perfect mirror pair (0.87).",
    "The sign of the modifier.",
    "WoW's Bane & Bless — the mirror clone survives every ruleset."),
fam("seals", "The Seal Press", TEMPLATE, "✝️",
    ["Seal of Righteousness", "Seal of Light", "Seal of Wisdom", "Seal of Justice",
     "Seal of the Crusader", "Judgement"],
    "the on-hit payload",
    "'Fills the Paladin with holy power, causing attacks to X. Lasts 30 sec. Unleashing this Seal's energy will judge an enemy…' Light/Wisdom measure 0.94.",
    "The proc payload and its judged counterpart.",
    "A two-stage engine (seal + judgement) with six cartridges — the deepest template in the Paladin's warehouse."),

FAMILY_OF = {}
for f in F:
    for m in f["members"]:
        FAMILY_OF[m] = f

# ---------------------------------------------- cross-class mechanical twins
# An ability in class A counts toward A->B if class B's book holds a different
# ability with blended effect similarity >= TWIN_T. Diagonal = within-class twins.
TWIN_T = 0.75
TWIN = {A: {B: set() for B in CLASSES} for A in CLASSES}
if os.path.exists("wow_cluster_sims.json"):
    for k, v in json.load(open("wow_cluster_sims.json")).items():
        if v < TWIN_T:
            continue
        a, b = (int(x) for x in k.split("|"))
        ra, rb = BYID.get(a), BYID.get(b)
        if not ra or not rb:
            continue
        for ca in ra["classes"]:
            for cb in rb["classes"]:
                TWIN[ca][cb].add(a)
                TWIN[cb][ca].add(b)

# ---------------------------------------------------------------- icons
ICON_URIS = {}
def icon_key(r):
    s = slug(r["name"])
    p = ICON_MAP.get(s)
    if not p or not os.path.exists(p):
        return None
    if s not in ICON_URIS:
        buf = io.BytesIO()
        Image.open(p).convert("RGBA").resize((56, 56), Image.LANCZOS).save(buf, "WEBP", quality=82)
        ICON_URIS[s] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    return s

def sp_name(r):
    k = icon_key(r)
    tag = f'<img class="sic" data-i="{k}" alt=""> ' if k else ""
    return f"{tag}**{r['name']}**"

# ---------------------------------------------------------------- pages
PAGES = {}
def page(slug_, title, group, md, icon=None):
    PAGES[slug_] = dict(title=title, group=group, md=md, icon=icon)

TIER_COLOR = {"clone": "var(--clone)", "template": "var(--template)", "engine": "var(--engine)"}

for f in F:
    mem = sorted((BYID[m] for m in f["members"]), key=lambda r: (r["classes"], r["level"], r["name"]))
    sims = sorted((sim(a, b) for a, b in combinations(f["members"], 2)), reverse=True)
    simtxt = f"{sims[0]:.2f}" if len(sims) == 1 else f"{sims[-1]:.2f}–{sims[0]:.2f}"
    rows = ["| Ability | Class | Level | School | Ranks | Tooltip |", "|---|---|---|---|---|---|"]
    for r in mem:
        d = re.sub(r"\$\{[^}]*\}", "X", r["desc"])
        d = re.sub(r"\$\w+", "X", d)
        d = d.replace("|", "/")[:110]
        rows.append(f"| {sp_name(r)} | {'/'.join(r['classes'])} | {r['level']} | {r['school']} | "
                    f"{r['rank_count']} | {d} |")
    fam_cls = sorted({c for r in mem for c in r["classes"]})
    md = f"""# <span class="femoji">{f['icon']}</span> {f['title']}

<span class="plate"><span class="tier tier-{f['tier']}">{TIER_LABEL[f['tier']]}</span>\
<span class="pv"><b>{len(mem)}</b> abilities</span>\
<span class="pv">similarity <b>{simtxt}</b></span>\
<span class="pv"><b>{len(fam_cls)}</b> classes</span>\
<span class="pv pvc">{', '.join(fam_cls) or '—'}</span></span>

{chr(10).join(rows)}

**Shared skeleton.** {f['shared']}

**What varies.** {f['varies']}

**Design read.** {f['read']}

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]
"""
    page(f"families/{f['slug']}", f["title"], "Families · " + TIER_LABEL[f["tier"]] + "s", md, icon=f["icon"])

# class pages
def class_recs(c):
    return sorted((r for r in RECS if c in r["classes"]), key=lambda r: (r["level"], r["name"]))

for c in CLASSES:
    lst = class_recs(c)
    in_fam = [r for r in lst if r["id"] in FAMILY_OF]
    ranks = sum(r["rank_count"] for r in lst)
    ov = sorted(((100 * len(TWIN[c][b]) / len(lst), b)
                 for b in CLASSES if b != c), reverse=True)[:3]
    ovtxt = ", ".join(f"**{p:.0f}%** with {f'[[classes/{b.lower()}|{b}]]'}" for p, b in ov)
    ovtxt += f" — and **{100 * len(TWIN[c][c]) / len(lst):.0f}%** twinned inside its own book"
    rows = ["| Lv | Ability | School | Ranks | Family |", "|---|---|---|---|---|"]
    for r in lst:
        fm = FAMILY_OF.get(r["id"])
        fl = f"[[families/{fm['slug']}|{fm['icon']} {fm['title']}]]" if fm else "—"
        rows.append(f"| {r['level']} | {sp_name(r)} | {r['school']} | {r['rank_count']} | {fl} |")
    md = f"""# {c} Spellbook (Classic)

**{len(lst)} abilities** ({ranks} spellbook entries counting ranks — {100*(ranks-len(lst))/max(1,ranks):.0f}% of the book is rank copies) · **{len(in_fam)}** in an identified family ({100*len(in_fam)/max(1,len(lst)):.0f}%)

Mechanical twins (effect similarity ≥ {TWIN_T}): {ovtxt}.

{chr(10).join(rows)}

Back to [[overview|Overview]] · [[findings|The Identical-Spell List]]
"""
    page(f"classes/{c.lower()}", c, "Classes", md)

# findings
fam_rows = ["| Family | Tier | Size | Peak sim | What actually differs |", "|---|---|---|---|---|"]
for f in sorted(F, key=lambda f: ([CLONE, TEMPLATE, ENGINE].index(f["tier"]), -len(f["members"]))):
    peak = max(sim(a, b) for a, b in combinations(f["members"], 2))
    cls = sorted({c for m in f["members"] for c in BYID[m]["classes"]})
    fam_rows.append(f"| [[families/{f['slug']}|{f['icon']} {f['title']}]] | "
                    f"<span class=\"tier tier-{f['tier']}\">{TIER_LABEL[f['tier']]}</span> | "
                    f"{len(f['members'])} abilities · {len(cls)} classes | {peak:.2f} | {f['differs']} |")

prow = ["| Similarity | Ability A | Ability B |", "|---|---|---|"]
with open("wow_similar_pairs.csv", encoding="utf-8") as fh:
    rd = csvlib.reader(fh)
    next(rd)
    for i, row in enumerate(rd):
        if i >= 20:
            break
        prow.append(f"| `{row[0]}` | {row[1]} ({row[2]}) | {row[3]} ({row[4]}) |")

n_fam = len(FAMILY_OF)
N = len(RECS)
page("findings", "The Identical-Spell List", "Start", f"""# The Identical-Spell List

Which WoW Classic abilities are mostly the same ability. Of **{N} distinct trainer-taught class abilities**, **{n_fam} ({100*n_fam/N:.0f}%) fall into {len(F)} families** — by far the highest of the three games studied, because classic WoW reskins along an axis the others barely use: **across classes**.

- <span class="tier tier-clone">Verbatim clone</span> — same sentence, one noun swapped (often into a different class's book).
- <span class="tier tier-template">Shared template</span> — one chassis, many payloads (totems, blessings, curses).
- <span class="tier tier-engine">Shared engine</span> — same underlying design in class-flavored prose.

{chr(10).join(fam_rows)}

## Top measured pairs

{chr(10).join(prow)}

Scores are the blended mechanical similarity — 0.6 × `SpellEffect` signature (effect types, aura codes, targets) + 0.4 × masked tooltip ([[methodology|method]]) — so two abilities that act through the same machinery measure as twins even when their tooltips read differently.
""")

# effects ledger — wowhead effect boxes per ability, categorized by composition
EFFECT_PROFILES = [
    ("Companion care",        r"Tame Creature|Dismiss Pet|Feed Pet|Learn Pet Spell|Mod Possess Pet|Health Funnel|Summon Dead Pet"),
    ("Summoning",             r"Summon|Trans Door"),
    ("Concealment",           r"\bStealth\b|Invisibility|Feign Death|Camouflage"),
    ("Shapeshift",            r"Shapeshift"),
    ("Teleportation",         r"Teleport"),
    ("Item creation",         r"Create Item|Enchant Item"),
    ("Resurrection",          r"Resurrect"),
    ("Threat manipulation",   r"Attack Me|Taunt|Mod (Total )?Threat|^Threat"),
    ("Interrupt / lockout",   r"Interrupt Cast|Mod Silence"),
    ("Dispel / cleanse",      r"Dispel"),
    ("Hard control",          r"\bStun\b|Fear\b|Confuse|\bCharm|Mod Possess(?! Pet)|Transform|Pacify|\bSleep\b"),
    ("Root & snare",          r"Mod Root|Mod Decrease Speed"),
    ("Damage + affliction",   None),   # direct + periodic, resolved in code
    ("Damage over time",      r"Periodic (Damage|Leech)"),
    ("Weapon strike",         r"Weapon (Damage|Dmg)|Normalized|Extra Attacks|Combo Points"),
    ("Direct spell damage",   r"School Damage|Health Leech|Instakill|Environmental Damage"),
    ("Heal + regeneration",   None),   # direct + periodic heal, resolved in code
    ("Heal over time",        r"Periodic Heal|Obs Mod Health|Periodic Health Funnel|Health Regen"),
    ("Direct healing",        r"\bHeal\b|Heal Max Health"),
    ("Absorb & shields",      r"School Absorb|Mana Shield|Damage Shield"),
    ("Resource manipulation", r"Energize|Give Power|Power (Drain|Burn|Funnel)|Mana Leech|Obs Mod Power|Power Regen"),
    ("Stat & combat mods",    r"Mod Stat|Attack Power|Mod Damage|Mod Resistance|Mod (Spell )?(Crit|Hit)|Mod Attack Speed|Mod Casting Speed|Mod (Parry|Dodge|Block)|Mod Healing|Mod Skill|Flat Modifier|Pct Modifier|Mod Scale"),
    ("Perception",            r"Track |Far Sight|Bind Sight|Detect|Stealth Detect"),
    ("Movement",              r"Increase.*Speed|Mounted|Water Walk|Feather Fall|Water Breathing|Underwater Breathing|Hover|Leap"),
    ("Immunity",              r"Immunity"),
]

def effect_profile(labels):
    joined = " | ".join(labels)
    direct = re.search(r"School Damage|Weapon (Damage|Dmg)|Normalized|Health Leech", joined)
    periodic = re.search(r"Periodic (Damage|Leech)", joined)
    direct_heal = re.search(r"(?<!Periodic )\bHeal\b|Heal Max Health", joined)
    periodic_heal = re.search(r"Periodic Heal|Obs Mod Health", joined)
    for name, pat in EFFECT_PROFILES:
        if name == "Damage + affliction":
            if direct and periodic:
                return name
            continue
        if name == "Heal + regeneration":
            if direct_heal and periodic_heal:
                return name
            continue
        if pat and re.search(pat, joined):
            return name
    return "Other / utility"

WH = {}
if os.path.exists("wow_effects_labels.json"):
    WH = json.load(open("wow_effects_labels.json", encoding="utf-8"))

if WH:
    prof_of = {}
    with open("wow_effects.csv", "w", newline="", encoding="utf-8") as fh:
        w = csvlib.writer(fh)
        w.writerow(["ability", "classes", "wowhead_effects", "effect_profile"])
        for r in sorted(RECS, key=lambda r: r["name"]):
            labels = (WH.get(str(r["id"])) or {}).get("effects") or []
            prof = effect_profile(labels) if labels else "Other / utility"
            prof_of[r["id"]] = (prof, labels)
            w.writerow([r["name"], "/".join(r["classes"]), " + ".join(labels), prof])

    prof_counts = defaultdict(int)
    for prof, _ in prof_of.values():
        prof_counts[prof] += 1
    order = [p for p, _ in EFFECT_PROFILES] + ["Other / utility"]
    sumrows = ["| Effect profile | Abilities | Share |", "|---|---|---|"]
    for p in order:
        if prof_counts.get(p):
            sumrows.append(f"| **{p}** | {prof_counts[p]} | {100*prof_counts[p]/len(RECS):.0f}% |")

    lrows = ["| Ability | Classes | Effect boxes (wowhead) | Profile |", "|---|---|---|---|"]
    for r in sorted(RECS, key=lambda r: (prof_of[r['id']][0], r["name"])):
        prof, labels = prof_of[r["id"]]
        fx = " + ".join(labels).replace("|", "/") or "*(no effect boxes)*"
        lrows.append(f"| {sp_name(r)} | {'/'.join(r['classes'])} | {fx} | {prof} |")

    page("effects", "The Effects Ledger", "Start", f"""# The Effects Ledger

Every ability's **effect boxes in wowhead's vocabulary**, categorized purely by **effect
composition** — what the machinery does, with no reading of names or tooltip prose. Sourcing:
57 abilities carry effect boxes pulled verbatim from wowhead.com/classic before its CDN blocked
bulk access; the remaining 366 are decoded from the client's own `SpellEffect` rows (the
identical data wowhead renders) into the same vocabulary, including effect names learned from
the wowhead overlap itself. Validation on the 57-page overlap: 78% of wowhead's labels are
reproduced exactly after normalization; the rest differ only in wowhead's added qualifiers.

## Profiles by composition

{chr(10).join(sumrows)}

## Every ability's effect boxes

{chr(10).join(lrows)}

Back to [[overview|Overview]] · [[methodology|Methodology]]
""", icon="⚙️")

# methodology
n_rank_entries = sum(r["rank_count"] for r in RECS)
page("methodology", "Methodology", "Start", f"""# Methodology

**Source.** The game's own client database tables for **WoW Classic Era** (build 1.15.9.69547), fetched as CSV from [wago.tools](https://wago.tools): `SpellName`, `Spell` (tooltips), `SkillLineAbility` + `SkillLine` (class attribution via class masks), `SpellLevels`, `SpellMisc` (school masks). Population: abilities in the nine classes' skill lines with a trainer level requirement — filtering out talents, hidden procs, and Season of Discovery additions (spell ids ≥ 100000, Engraving/Runes lines). **{N} distinct abilities** remain, spanning **{n_rank_entries} spellbook entries** once ranks are counted.

**The rank clone farm.** {n_rank_entries - N} of those entries ({100*(n_rank_entries-N)/n_rank_entries:.0f}%) are rank duplicates — the same spell re-taught with bigger numbers. Classic's ranks are BG3's upcast clones and D&D's spell-level laddering taken to their logical extreme: two-thirds of the classic spellbook is the same spell again.

**Similarity.** Blended mechanical score: 0.6 × the *effect signature* (each ability's `SpellEffect` rows — effect types, aura codes, mechanics, base-point sign, implicit targets — the game's actual machinery) + 0.4 × the masked tooltip (macros `$s1`/`$d`/`${{formulas}}`, schools, elements, creature types, cities, and stat names replaced with tokens). Two abilities that stun, drain, or buff through the same aura code measure as siblings even when their tooltips are written differently. Highest rank per ability is analyzed; ranks collapse first.

**Icons.** Fetched from [warcraft.wiki.gg](https://warcraft.wiki.gg) (the community wiki), by reading each ability page's infobox `icon=` parameter through the MediaWiki API — batched and throttled. Icons © Blizzard Entertainment, shown for research reference.

**Known limits.** Talents are excluded (trainer spellbook only); pet abilities excluded; Classic Era data includes minor anniversary-era tuning. Cross-era comparison uses the same masks as the SRD and BG3 studies but the population definitions differ slightly per game — the headline percentages are directional, not decimal-precise.

**Reproduce.** `wow_dataset.py` → `wow_analyze.py` (blended `SpellEffect`-signature similarity) → `wow_icons.py` → `wow_wowhead_pull.py` + `wow_effects_decode.py` (the Effects Ledger) → `build_wow_codex.py` → `build_wow_map.py`. Family curation is function-primary, verified against effect rows and documented player usage. Companion codices: the D&D 5e SRD and Baldur's Gate 3.
""")

# overview — cross-class mechanical-twin matrix (diagonal = within-class twins)
mat = ["| ↓ has effect-twins in → | " + " | ".join(f"[[classes/{c.lower()}|{c[:4]}]]" for c in CLASSES) + " |",
       "|---|" + "---|" * len(CLASSES)]
for a in CLASSES:
    na = len(class_recs(a))
    cells = []
    for b in CLASSES:
        cells.append("—" if a == b else f"{100 * len(TWIN[a][b]) / na:.0f}%")
    mat.append(f"| [[classes/{a.lower()}|{a}]] ({na}) | " + " | ".join(cells) + " |")

internal = sorted(((100 * len(TWIN[c][c]) / len(class_recs(c)), c) for c in CLASSES),
                  reverse=True)
internal_txt = " · ".join(f"[[classes/{c.lower()}|{c}]] **{p:.0f}%**" for p, c in internal)

top_cross = sorted(((100 * len(TWIN[a][b]) / len(class_recs(a)), a, b)
                    for a in CLASSES for b in CLASSES if a != b), reverse=True)[:3]
top_cross_txt = "; ".join(
    f"**{p:.0f}%** of the {a} book has a twin in {b}'s" for p, a, b in top_cross)

page("overview", "Overview", "Start", f"""# How Homogeneous Are WoW Classic Spells?

The third dataset in the homogeneity study — and the most homogeneous of the three. Everything below is read from WoW Classic Era's own client database ({N} trainer-taught class abilities), with icons from the community wiki. See [[findings|The Identical-Spell List]] for the full family catalogue and [[methodology|Methodology]] for the pipeline.

## Axis 0 — the rank clone farm

Before any reskin analysis: **{100*(n_rank_entries-N)/n_rank_entries:.0f}% of the classic spellbook is rank duplicates** ({n_rank_entries} entries for {N} abilities). BG3 hides its upcast clones in the data files; classic sells them at the trainer.

## Axis 1 — the same ability in several class books

Unlike D&D (where classes share one spell list) or BG3 (where lists overlap), classic WoW ships **the same design as separate class-branded spells**: nine heals that are [[families/heals|one heal]], five [[families/interrupts|interrupts]], the [[families/rez|resurrection franchise]], one [[families/protection|protection effect]] wearing armor, ward, and shield vocabularies across four classes, Cure Poison printed verbatim in two books, and the Feral Druid — a licensed photocopy of the Rogue and Warrior kits, now filed by function (its openers with [[families/melee-enhance|the strikes]], its roars in [[families/threat|the Aggro Ledger]], its prowl in [[families/concealment|the Vanishing Act]]). Because the *names* are the reskin, name sharing is near zero and useless as a measure — so the matrix below measures **mechanics**: the share of the row class's kit that has an effect-twin in the column class's book (a *different* ability with blended `SpellEffect`-signature similarity ≥ {TWIN_T}). Standouts: {top_cross_txt}.

{chr(10).join(mat)}

**Internal redundancy** — the same measure pointed at each class's *own* book (how much of the kit has a different in-book twin): {internal_txt}. The teleport matrix, the totem foundry, and the conjured-stone commissary are why the top three look the way they do.

## Axis 2 — one chassis, many payloads

Classic's signature template shape is the **payload rack**: [[families/totems|21 totems]], [[families/status-boosts|24 status boosts]] (blessings, prayers, and auras), [[families/curses|8 curses]], [[families/tracking|10 tracking dials]], [[families/teleports|a 6×2 teleport matrix]], [[families/conjured|23 conjured consumables]], [[families/seals|6 seals]], [[families/poisons|5 poisons]], [[families/aspects|6 aspects]]. **{n_fam} of {N} abilities ({100*n_fam/N:.0f}%) sit in {len(F)} families.**

## Browse

- **Classes:** {" · ".join(f"[[classes/{c.lower()}|{c}]]" for c in CLASSES)}
- **The list:** [[findings|The Identical-Spell List]] · **Every ability, tagged:** [[spells|All Abilities, Tagged]]
- **How:** [[methodology|Methodology]]
""")

# tagged table + csv
from purpose_defs import load_purposes, PEMOJI as PUR_EMOJI, PLABEL as PUR_LABEL
WOW_PUR = load_purposes("WoW Classic")

def pur_txt(name):
    p = WOW_PUR.get(name.lower())
    return f'{PUR_EMOJI[p]} {PUR_LABEL[p]}' if p else ""

trow = ["| Lv | Ability | Classes | School | Ranks | Family | Tier | Purpose |", "|---|---|---|---|---|---|---|---|"]
with open("wow_spells_tagged.csv", "w", newline="", encoding="utf-8") as fh:
    w = csvlib.writer(fh)
    w.writerow(["ability", "classes", "level", "school", "ranks", "family", "tier", "purpose"])
    for r in sorted(RECS, key=lambda r: (r["level"], r["name"])):
        fm = FAMILY_OF.get(r["id"])
        w.writerow([r["name"], "/".join(r["classes"]), r["level"], r["school"], r["rank_count"],
                    fm["title"] if fm else "", TIER_LABEL[fm["tier"]] if fm else "",
                    PUR_LABEL.get(WOW_PUR.get(r["name"].lower(), ""), "")])
        fl = f"[[families/{fm['slug']}|{fm['icon']} {fm['title']}]]" if fm else "—"
        tt = f'<span class="tier tier-{fm["tier"]}">{TIER_LABEL[fm["tier"]]}</span>' if fm else ""
        trow.append(f"| {r['level']} | {sp_name(r)} | {'/'.join(r['classes'])} | {r['school']} | "
                    f"{r['rank_count']} | {fl} | {tt} | {pur_txt(r['name'])} |")

page("spells", "All Abilities, Tagged", "Start", f"""# All Abilities, Tagged by Family

All **{N} distinct trainer abilities** across the nine classes, with family tags and rank counts.

{chr(10).join(trow)}

Back to [[overview|Overview]] · [[findings|The Identical-Spell List]]
""")

# ---------------------------------------------------------------- backlinks + md out
WIKILINK = re.compile(r"\[\[([a-zA-Z0-9\-/]+)(?:\|([^\]]+))?\]\]")
links_to = defaultdict(set)
for s, p in PAGES.items():
    for m in WIKILINK.finditer(p["md"]):
        if m.group(1) in PAGES and m.group(1) != s:
            links_to[m.group(1)].add(s)
for s, p in PAGES.items():
    bl = sorted(links_to.get(s, []))
    if bl:
        p["md"] += "\n---\n*Linked from: " + " · ".join(f"[[{b}|{PAGES[b]['title']}]]" for b in bl) + "*\n"

os.makedirs("wow_wiki/families", exist_ok=True)
os.makedirs("wow_wiki/classes", exist_ok=True)
for s, p in PAGES.items():
    with open(os.path.join("wow_wiki", s + ".md"), "w", encoding="utf-8") as fh:
        fh.write(p["md"])

# ---------------------------------------------------------------- md -> html
INLINE = [
    (re.compile(r"`([^`]+)`"), r"<code>\1</code>"),
    (re.compile(r"\*\*([^*]+)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"\*([^*]+)\*"), r"<em>\1</em>"),
    (re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)"), r'<a href="\2" target="_blank" rel="noopener">\1</a>'),
]

def inline(text):
    spans = []
    def stash(m):
        spans.append(m.group(0))
        return f"\x00{len(spans)-1}\x00"
    text = re.sub(r"<span[^>]*>.*?</span>|<img[^>]*>", stash, text)
    text = htmllib.escape(text, quote=False)
    for pat, rep in INLINE:
        text = pat.sub(rep, text)
    def wl(m):
        tgt, label = m.group(1), m.group(2)
        return f'<a class="wl" href="#/{tgt}">{label or PAGES.get(tgt, {}).get("title", tgt)}</a>'
    text = WIKILINK.sub(wl, text)
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)

def md_to_html(md):
    out, i = [], 0
    lines = md.split("\n")
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("|"):
            tbl = []
            while i < len(lines) and lines[i].startswith("|"):
                tbl.append(WIKILINK.sub(lambda m: m.group(0).replace("|", "\x01"), lines[i]))
                i += 1
            def cells(row):
                return [c.strip().replace("\x01", "|") for c in row.strip("|").split("|")]
            out.append('<div class="tw"><table><thead><tr>' +
                       "".join(f"<th>{inline(c)}</th>" for c in cells(tbl[0])) + "</tr></thead><tbody>")
            for row in tbl[2:]:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells(row)) + "</tr>")
            out.append("</tbody></table></div>")
            continue
        if ln.startswith("- "):
            out.append("<ul>")
            while i < len(lines) and lines[i].startswith("- "):
                out.append(f"<li>{inline(lines[i][2:])}</li>")
                i += 1
            out.append("</ul>")
            continue
        if ln.startswith("## "):
            out.append(f"<h2>{inline(ln[3:])}</h2>")
        elif ln.startswith("# "):
            out.append(f"<h1>{inline(ln[2:])}</h1>")
        elif ln.strip() == "---":
            out.append("<hr>")
        elif ln.strip():
            para = [ln]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"^(#|\||- |---)", lines[i + 1]):
                para.append(lines[i + 1])
                i += 1
            out.append(f"<p>{inline(' '.join(para))}</p>")
        i += 1
    return "\n".join(out)

PAGES_HTML = {s: md_to_html(p["md"]) for s, p in PAGES.items()}

NAV = [
    ("Start", ["overview", "findings", "spells"] +
     (["effects"] if "effects" in PAGES else []) + ["methodology"]),
    ("Families · Clones", [f"families/{f['slug']}" for f in F if f["tier"] == CLONE]),
    ("Families · Templates", [f"families/{f['slug']}" for f in F if f["tier"] == TEMPLATE]),
    ("Families · Engines", [f"families/{f['slug']}" for f in F if f["tier"] == ENGINE]),
    ("Class Spellbooks", [f"classes/{c.lower()}" for c in CLASSES]),
]
nav_html = []
for label, slugs in NAV:
    nav_html.append(f'<div class="navgroup"><div class="navlabel">{label}</div>')
    for s in slugs:
        ic = PAGES[s].get("icon")
        lab = (f'<span class="femoji">{ic}</span> ' if ic else "") + PAGES[s]["title"]
        nav_html.append(f'<a data-slug="{s}" href="#/{s}">{lab}</a>')
    nav_html.append("</div>")
nav_html = "\n".join(nav_html)

HTML = """<title>The Azeroth Codex</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&family=Lora:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --bg:#F0E7D3; --panel:#E5D9BE; --ink:#33281A; --muted:#6E5F45;
  --line:#D2C4A2; --accent:#8A6A1F; --accent-ink:#6E5314; --accent-bg:#8A6A1F14;
  --clone:#7E3FB8; --clone-bg:#7E3FB816; --template:#1F5FB8; --template-bg:#1F5FB816;
  --engine:#2E7D32; --engine-bg:#2E7D3216; --code-bg:#E0D3B2;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#17130E; --panel:#211B12; --ink:#E7D9B8; --muted:#A2937A;
    --line:#3A3122; --accent:#E6C35C; --accent-ink:#F0D283; --accent-bg:#E6C35C1A;
    --clone:#B67AF0; --clone-bg:#B67AF01A; --template:#5A9BF0; --template-bg:#5A9BF01A;
    --engine:#5FBF63; --engine-bg:#5FBF631A; --code-bg:#2B2417;
  }
}
:root[data-theme="dark"]{
  --bg:#17130E; --panel:#211B12; --ink:#E7D9B8; --muted:#A2937A;
  --line:#3A3122; --accent:#E6C35C; --accent-ink:#F0D283; --accent-bg:#E6C35C1A;
  --clone:#B67AF0; --clone-bg:#B67AF01A; --template:#5A9BF0; --template-bg:#5A9BF01A;
  --engine:#5FBF63; --engine-bg:#5FBF631A; --code-bg:#2B2417;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:400 16.5px/1.62 Lora,Georgia,serif}
a{color:var(--accent);text-decoration:none}
a:hover{color:var(--accent-ink)}
.layout{display:flex;min-height:100vh}
nav{width:256px;flex:0 0 256px;background:var(--panel);border-right:1px solid var(--line);
  padding:20px 0 40px;position:sticky;top:0;height:100vh;overflow-y:auto}
.brand{font-family:Marcellus,Georgia,serif;font-size:19px;letter-spacing:.05em;
  padding:6px 20px 14px;border-bottom:1px solid var(--line);margin-bottom:10px;color:var(--accent-ink)}
.brand small{display:block;font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:10.5px;
  color:var(--muted);letter-spacing:.04em;margin-top:3px}
.navlabel{font:500 10.5px/1 "IBM Plex Mono",ui-monospace,monospace;color:var(--muted);
  text-transform:uppercase;letter-spacing:.12em;padding:14px 20px 6px}
nav a{display:block;padding:4px 20px;font-size:14.5px;color:var(--ink)}
nav a:hover{background:var(--accent-bg)}
nav a.on{color:var(--accent-ink);background:var(--accent-bg);box-shadow:inset 3px 0 0 var(--accent)}
main{flex:1;min-width:0;padding:36px 44px 90px}
article{max-width:78ch;margin:0 auto}
.crumb{font:400 12px/1 "IBM Plex Mono",ui-monospace,monospace;color:var(--muted);
  letter-spacing:.03em;margin-bottom:22px}
h1{font-family:Marcellus,Georgia,serif;font-size:30px;line-height:1.2;text-wrap:balance;
  margin:0 0 16px;color:var(--accent-ink)}
h2{font-family:Lora,Georgia,serif;font-weight:600;font-size:21px;margin:34px 0 10px}
p{margin:0 0 14px}
ul{margin:0 0 14px;padding-left:22px}
li{margin-bottom:6px}
hr{border:0;border-top:1px solid var(--line);margin:28px 0 14px}
code{font:500 13px "IBM Plex Mono",ui-monospace,monospace;background:var(--code-bg);
  padding:1px 5px;border-radius:3px;font-variant-numeric:tabular-nums}
.wl{border-bottom:1px dotted var(--accent)}
.wl:hover{background:var(--accent-bg)}
.tw{overflow-x:auto;margin:16px 0 20px;border:1px solid var(--line);border-radius:4px}
table{border-collapse:collapse;width:100%;font-size:13.5px;line-height:1.45;font-family:Lora,Georgia,serif}
th{font:500 11px "IBM Plex Mono",ui-monospace,monospace;text-transform:uppercase;
  letter-spacing:.07em;color:var(--muted);text-align:left;padding:8px 10px;
  border-bottom:1px solid var(--line);background:var(--panel);white-space:nowrap}
td{padding:6px 10px;border-bottom:1px solid var(--line);vertical-align:top;font-variant-numeric:tabular-nums}
tr:last-child td{border-bottom:0}
.tier{font:500 10.5px "IBM Plex Mono",ui-monospace,monospace;text-transform:uppercase;
  letter-spacing:.08em;padding:2px 7px;border-radius:3px;white-space:nowrap}
.tier-clone{color:var(--clone);background:var(--clone-bg)}
.tier-template{color:var(--template);background:var(--template-bg)}
.tier-engine{color:var(--engine);background:var(--engine-bg)}
.sic{width:22px;height:22px;vertical-align:-6px;margin-right:5px;border-radius:4px;
  border:1px solid var(--line)}
.femoji{font-family:"Segoe UI Emoji","Apple Color Emoji","Noto Color Emoji",sans-serif;font-style:normal}
h1 .femoji{font-size:25px;margin-right:2px}
nav .femoji{display:inline-block;width:20px;font-size:13px}
#menu{display:none;position:fixed;top:10px;left:10px;z-index:3;background:var(--panel);
  border:1px solid var(--line);border-radius:4px;padding:6px 12px;color:var(--ink);
  font:500 13px "IBM Plex Mono",ui-monospace,monospace;cursor:pointer}
@media (max-width:820px){
  #menu{display:block}
  nav{position:fixed;left:0;top:0;z-index:2;transform:translateX(-100%);transition:transform .2s}
  nav.open{transform:none;box-shadow:0 0 0 100vmax #0006}
  main{padding:58px 18px 70px}
}
@media (prefers-reduced-motion: reduce){nav{transition:none}}
footer{max-width:78ch;margin:50px auto 0;padding-top:14px;border-top:1px solid var(--line);
  font-size:12.5px;color:var(--muted);line-height:1.75}
::selection{background:color-mix(in srgb,var(--accent) 26%,transparent)}
h2,h3{text-wrap:balance}
a:focus-visible,button:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:3px}
nav{scrollbar-width:thin;scrollbar-color:var(--line) transparent;overscroll-behavior:contain}
.crumb{text-transform:uppercase;letter-spacing:.11em;font-size:10.5px}
.tw{border-radius:8px}
tbody tr:nth-child(even) td{background:color-mix(in srgb,var(--ink) 3%,transparent)}
tbody tr:hover td{background:color-mix(in srgb,var(--accent) 10%,transparent)}
.tier{border:1px solid color-mix(in srgb,currentColor 30%,transparent)}
.sic{background:var(--panel);border:1px solid color-mix(in srgb,var(--line) 70%,transparent)}
.crumb a{color:inherit}
.crumb a:hover{color:var(--accent-ink)}
.plate{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;margin:2px 0 18px;
  padding:10px 14px;border:1px solid var(--line);border-radius:8px;background:var(--panel);
  font:400 12px "IBM Plex Mono",ui-monospace,monospace;color:var(--muted)}
.plate .pv b{color:var(--ink);font-weight:500}
.plate .pvc{flex-basis:100%;font-size:11px}
.pn{display:flex;justify-content:space-between;gap:14px;margin:30px 0 0;padding-top:14px;
  border-top:1px solid var(--line);font-size:14px}
.pn a{max-width:48%}
.backlinks{margin:26px 0 0;padding-top:12px;border-top:1px dashed var(--line);
  font-size:12.5px;color:var(--muted);line-height:1.8}
.backlinks .bl-l{font:500 10px "IBM Plex Mono",ui-monospace,monospace;text-transform:uppercase;
  letter-spacing:.1em;margin-right:6px}
.tfilter{display:block;width:100%;max-width:340px;margin:12px 0 -6px;padding:6px 10px;
  font:400 12.5px "IBM Plex Mono",ui-monospace,monospace;color:var(--ink);
  background:var(--panel);border:1px solid var(--line);border-radius:6px}
.tfilter:focus{outline:2px solid var(--accent);outline-offset:1px}
th.sortable{cursor:pointer;user-select:none}
th.sortable:hover{color:var(--accent-ink)}
th.s-a::after{content:" 91"}
th.s-d::after{content:" 93"}
#peek{position:absolute;display:none;z-index:5;background:var(--panel);border:1px solid var(--line);
  border-radius:8px;padding:9px 12px;max-width:340px;box-shadow:0 8px 24px #0004;
  font-size:12.5px;line-height:1.5;pointer-events:none}
#peek b{display:block;color:var(--accent-ink);margin-bottom:2px}
#peek span{color:var(--muted)}
</style>
<button id="menu" aria-label="Menu">☰ pages</button>
<div class="layout">
<nav id="nav">
<div class="brand">The Azeroth Codex<small>wow classic era · __N__ abilities · 9 classes</small></div>
__NAV__
</nav>
<main>
<div class="crumb" id="crumb"></div>
<article id="art"></article>
<footer>Ability data from WoW Classic Era client tables (via wago.tools); icons via warcraft.wiki.gg —
© Blizzard Entertainment; private research reference. Third volume of the spell-homogeneity study,
with the Reskin Codex (D&amp;D 5e SRD) and the Larian Codex (Baldur's Gate 3).</footer>
</main>
</div>
<script>
const PAGES = __PAGES__;
const ICONS = __ICONS__;
const art = document.getElementById('art'), crumb = document.getElementById('crumb');
const nav = document.getElementById('nav');
function render(){
  let slug = location.hash.replace(/^#\\//,'') || 'overview';
  if(!PAGES[slug]) slug = 'overview';
  art.innerHTML = PAGES[slug].html;
  art.querySelectorAll('img.sic').forEach(el => {
    const d = ICONS[el.dataset.i];
    if(d) el.src = d; else el.remove();
  });
  const parts = slug.split('/');
  crumb.innerHTML = crumbHTML(slug, parts);
  document.querySelectorAll('nav a[data-slug]').forEach(a=>a.classList.toggle('on', a.dataset.slug===slug));
  nav.classList.remove('open');
  const onA = document.querySelector('nav a.on');
  if (onA && onA.scrollIntoView) onA.scrollIntoView({block:'nearest'});
  enhance(slug);
  window.scrollTo(0,0);
}

/* usability pass */
const FAMS = Object.keys(PAGES).filter(s => s.indexOf('families/') === 0);
function crumbHTML(slug, parts){
  let h = '<a href="#/overview">azeroth codex</a>';
  if (parts.length > 1) h += PAGES[parts[0]] ? ' / <a href="#/' + parts[0] + '">' + parts[0] + '</a>' : ' / ' + parts[0];
  return h + ' / ' + PAGES[slug].title.toLowerCase();
}
function firstText(h){
  const d = document.createElement('div'); d.innerHTML = h;
  let t = '';
  for (const el of d.querySelectorAll('p')){ t = el.textContent.trim(); if (t.length > 40) break; }
  if (!t) t = d.textContent;
  t = t.split(String.fromCharCode(10)).join(' ').split(String.fromCharCode(9)).join(' ');
  while (t.indexOf('  ') !== -1) t = t.split('  ').join(' ');
  t = t.trim();
  return t.length > 180 ? t.slice(0, 177) + '…' : t;
}
const peek = document.createElement('div'); peek.id = 'peek'; document.body.appendChild(peek);
let peekT;
art.addEventListener('mouseover', e => {
  const a = e.target.closest('a[href^="#/"]'); if (!a) return;
  const t = a.getAttribute('href').slice(2), p = PAGES[t];
  if (!p) return;
  clearTimeout(peekT);
  peekT = setTimeout(() => {
    peek.innerHTML = '<b></b><span></span>';
    peek.firstChild.textContent = p.title;
    peek.lastChild.textContent = firstText(p.html);
    const r = a.getBoundingClientRect(), pw = Math.min(340, innerWidth - 24);
    peek.style.display = 'block';
    peek.style.left = Math.max(8, Math.min(r.left, innerWidth - pw - 12)) + 'px';
    peek.style.top = (r.bottom + 6 + scrollY) + 'px';
  }, 220);
});
art.addEventListener('mouseout', e => {
  if (e.target.closest('a[href^="#/"]')){ clearTimeout(peekT); peek.style.display = 'none'; }
});
window.addEventListener('hashchange', () => { peek.style.display = 'none'; });
function enhance(slug){
  if (slug.indexOf('families/') === 0){
    const i = FAMS.indexOf(slug);
    const pn = document.createElement('div'); pn.className = 'pn';
    const pv = i > 0 ? FAMS[i-1] : null, nx = i < FAMS.length - 1 ? FAMS[i+1] : null;
    pn.innerHTML =
      (pv ? '<a href="#/' + pv + '">← ' + PAGES[pv].title + '</a>' : '<span></span>') +
      (nx ? '<a href="#/' + nx + '">' + PAGES[nx].title + ' →</a>' : '<span></span>');
    art.appendChild(pn);
  }
  art.querySelectorAll('.tw table').forEach(tbl => {
    const all = [...tbl.querySelectorAll('tr')].filter(r => r.querySelector('td'));
    if (!all.length) return;
    if (all.length > 14){
      const box = document.createElement('input');
      box.className = 'tfilter'; box.type = 'search';
      box.placeholder = 'filter ' + all.length + ' rows…';
      box.addEventListener('input', () => {
        const q = box.value.toLowerCase();
        all.forEach(r => { r.style.display = r.textContent.toLowerCase().indexOf(q) !== -1 ? '' : 'none'; });
      });
      tbl.parentElement.parentElement.insertBefore(box, tbl.parentElement);
    }
    const ths = tbl.querySelectorAll('tr:first-child th');
    ths.forEach((th, ci) => {
      th.classList.add('sortable');
      th.title = 'sort';
      th.addEventListener('click', () => {
        const dir = th.dataset.d === 'a' ? -1 : 1;
        ths.forEach(x => { delete x.dataset.d; x.classList.remove('s-a', 's-d'); });
        th.dataset.d = dir === 1 ? 'a' : 'd';
        th.classList.add(dir === 1 ? 's-a' : 's-d');
        const body = all[0].parentElement;
        const key = r => r.cells[ci] ? r.cells[ci].textContent.trim() : '';
        const isNum = all.every(r => { const v = key(r); return v === '' || !isNaN(parseFloat(v)); });
        all.slice().sort((a, b) => {
          const va = key(a), vb = key(b);
          if (isNum) return dir * ((parseFloat(va) || -1e9) - (parseFloat(vb) || -1e9));
          return dir * va.localeCompare(vb);
        }).forEach(r => body.appendChild(r));
      });
    });
  });
}

window.addEventListener('hashchange', render);
document.getElementById('menu').addEventListener('click',()=>nav.classList.toggle('open'));
render();
</script>
"""
HTML = (HTML.replace("__NAV__", nav_html).replace("__N__", str(len(RECS)))
        .replace("__PAGES__", json.dumps({s: {"title": p["title"], "html": PAGES_HTML[s]}
                                          for s, p in PAGES.items()}))
        .replace("__ICONS__", json.dumps(ICON_URIS)))
with open("wow_codex.html", "w", encoding="utf-8") as fh:
    fh.write(HTML)
print(f"{len(PAGES)} pages; {len(RECS)} abilities; {n_fam} in {len(F)} families; "
      f"{len(ICON_URIS)} icons embedded")
print(f"wow_codex.html: {os.path.getsize('wow_codex.html') / 1024:.0f} KB")

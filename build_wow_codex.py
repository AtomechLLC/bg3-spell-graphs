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

fam("tracking", "The Tracking Dial", CLONE, "🐾",
    ["Track Beasts", "Track Humanoids", "Track Undead", "Track Hidden", "Track Elementals",
     "Track Demons", "Track Giants", "Track Dragonkin", "Sense Undead", "Sense Demons"],
    "the creature type on the minimap",
    "'Shows the location of all nearby X on the minimap.' One sentence, one noun slot. The Hunter gets eight copies; the Paladin and Warlock each get one with 'Sense' stamped on the label (masked similarity ≥ 0.9 across all ten).",
    "The tracked creature type. Nothing else.",
    "The purest reskin family in classic WoW — a radio with eight stations sold as eight spells, plus two single-station radios sold to other classes."),
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
fam("heals", "One Heal, Nine Names", CLONE, "❤️‍🩹",
    ["Lesser Heal", "Heal", "Greater Heal", "Flash Heal", "Healing Touch",
     "Healing Wave", "Lesser Healing Wave", "Holy Light", "Flash of Light"],
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
     "Shadow Resistance Aura", "Frost Resistance Aura", "Fire Resistance Aura"],
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
fam("stings", "The Sting Clip", CLONE, "🦂",
    ["Serpent Sting", "Scorpid Sting", "Viper Sting"],
    "the payload injected",
    "'Stings the target, causing X over/for Y sec.' Serpent/Viper measure 0.89, Scorpid 0.81 against both.",
    "The payload: nature DoT, stat drain, or mana drain.",
    "A three-round clip of the same dart — and the Scorpid/Curse of Weakness pair (0.70) shows the template leaking across classes into [[families/curses|Warlock curses]]."),
fam("shocks", "The Shock Battery", CLONE, "⚡",
    ["Earth Shock", "Flame Shock", "Frost Shock"],
    "element and rider",
    "'Instantly shocks the target with X, causing Y damage plus Z.' The famous instant-nuke trio; Earth Shock even measures 0.72 against Warrior and Rogue interrupts — it IS the Shaman's [[families/interrupts|interrupt]] wearing an elemental coat.",
    "The element and the rider (interrupt / DoT / slow).",
    "Three buttons, one circuit — and proof that the same design can be a 'school' variation in one class and an 'interrupt' clone in another."),
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
fam("curses", "The Curse Catalogue", TEMPLATE, "💀",
    ["Curse of Agony", "Curse of Weakness", "Curse of Recklessness", "Curse of Tongues",
     "Curse of the Elements", "Curse of Shadow", "Curse of Doom"],
    "the affliction applied",
    "'Curses the target with X for Y.' Elements/Shadow are the same spell with the school swapped (0.85); only one Curse per Warlock per target — the debuff version of the modal engine.",
    "The affliction (DoT, stat down, school vulnerability, slow…).",
    "The [[families/status-boosts|one-active-slot]] engine pointed at enemies."),
fam("protection", "The Protection Rack", TEMPLATE, "🧿",
    ["Frost Armor", "Ice Armor", "Mage Armor", "Demon Skin", "Demon Armor",
     "Inner Fire", "Fire Ward", "Frost Ward", "Shadow Ward", "Power Word: Shield"],
    "how the damage is refused: armor, absorb, or school ward",
    "One protection effect in three grammars. The armors — 'Increases armor by X' plus a class rider — where Frost→Ice Armor is a renamed rank jump (0.9) and Demon Skin→Demon Armor the same trick in the Warlock book, with the Priest's Inner Fire as a third skin. The wards — 'Absorbs X Fire/Frost/Shadow damage. Lasts 30 sec.' — the identical spell stocked in the Mage and Warlock shops (0.9+ across all three), the WoW twin of BG3's triple Shield SKUs. And Power Word: Shield, the ward with the school parameter removed.",
    "The refusal mechanism (armor value, school-typed absorb, universal absorb), the rider, and which class's book carries it.",
    "Merged on the effect, not the name: armors, wards, and shields are one defensive design wearing three vocabularies across four classes."),
fam("bolts", "The Bolt Engine", ENGINE, "🏹",
    ["Fireball", "Pyroblast", "Frostbolt", "Shadow Bolt", "Wrath", "Starfire",
     "Lightning Bolt", "Smite", "Holy Fire", "Mind Blast"],
    "school, speed, and rider",
    "Cast-time nuke: 'Hurls/Launches/Causes X school damage.' Fireball/Pyroblast measure 0.80; the cross-class copies (Wrath, Lightning Bolt, Smite) share the skeleton with class-flavored verbs.",
    "The school, cast time, coefficient, and a small rider (Fireball's dot, Frostbolt's slow, Holy Fire's burn).",
    "Every caster's default button is the same engine — the classic archetype-defining spell is the least differentiated design in the game."),
fam("dots", "The Affliction Engine", ENGINE, "🩸",
    ["Shadow Word: Pain", "Corruption", "Immolate", "Moonfire", "Rend",
     "Garrote", "Rupture", "Serpent Sting"],
    "school, duration, and delivery",
    "'Causes X damage over Y sec.' Moonfire/Immolate measure 0.82 — a druid spell and a warlock spell that are the same design with different star signs. The physical bleeds (Rend/Garrote/Rupture) run the same engine on weapon damage.",
    "School, tick rate, and whether an upfront hit rides along.",
    "One damage-over-time chassis serving six classes."),
fam("summons", "The Menagerie", TEMPLATE, "😈",
    ["Summon Imp", "Summon Voidwalker", "Summon Succubus", "Summon Felhunter",
     "Summon Warhorse", "Summon Charger", "Summon Felsteed", "Summon Dreadsteed",
     "Eye of Kilrogg", "Ritual of Summoning", "Inferno", "Ritual of Doom",
     "Call Pet", "Tame Beast", "Revive Pet", "Dismiss Pet", "Eyes of the Beast"],
    "who — or what — answers the call, and which class holds the leash",
    "'Summons an X under the command of the caster' — every class's companion runs the same contract. The Warlock's four demons are one contract with four signatories (0.85+); the Hunter's stable is the same system with a taming step (Tame Beast / Call Pet / Dismiss Pet / Revive Pet mirror the demon workflow verb for verb); the mounts are the same ladder twice, holy and fel; and the engine stretches to scouting eyes (Eye of Kilrogg, Eyes of the Beast), player-summoning taxi rituals, and one-shot infernals.",
    "The summoned entity (demon, beast, steed, eye, party member, infernal), its permanence, the acquisition step, and the ritual cost. (The pets' own abilities — Spell Lock, Devour Magic — are taught to the pet, outside the trainer-book population studied here.)",
    "Cross-class summoning is one engine wearing class-flavored leashes — BG3's container spells, twenty years early."),
fam("rez", "The Resurrection Union", CLONE, "⚰️",
    ["Resurrection", "Redemption", "Ancestral Spirit", "Rebirth",
     "Create Soulstone (Minor)", "Create Soulstone (Lesser)", "Create Soulstone",
     "Create Soulstone (Greater)", "Create Soulstone (Major)"],
    "the class label, the cooldown, and whether the rez is cast or carried",
    "'Returns the spirit to the body, restoring a dead target to life with X health and mana.' Four classes, four names, one sentence (0.85+ pairwise; Rebirth adds 'usable in combat') — plus the Warlock's five Soulstone tiers: the same resurrection pre-paid into an item, cast before death instead of after.",
    "The name, Rebirth's combat clause, and the delivery — direct cast vs. the Soulstone's stored charge (with its tier ladder written into the item name).",
    "The clearest evidence that class kits were filled from a shared parts bin: death care is a franchise, and the Warlock's branch sells it as a prepaid card."),
fam("cat-is-rogue", "The Druid Costume Shop", CLONE, "🐱",
    ["Stealth", "Prowl", "Ambush", "Ravage", "Backstab", "Shred", "Cower", "Feint",
     "Taunt", "Growl", "Challenging Shout", "Challenging Roar"],
    "which body performs it",
    "Six rogue/warrior abilities, photocopied into the Druid's cat and bear forms: Stealth→Prowl, Ambush→Ravage, Backstab→Shred, Feint→Cower, Taunt→Growl, Challenging Shout→Challenging Roar. Every pair measures 0.8–0.95.",
    "The animal performing it and small coefficient nudges.",
    "The whole Feral druid is a licensed reskin of two other classes — homogeneity as a class design *strategy*, and it worked."),
fam("interrupts", "The Interrupt Union", CLONE, "✋",
    ["Kick", "Pummel", "Shield Bash", "Earth Shock", "Counterspell"],
    "the limb, element, or arcana used",
    "'Interrupts the spell being cast, preventing that school of magic for Y sec.' Kick/Pummel/Shield Bash are word-for-word siblings; Earth Shock measures 0.72 against them from another class's book; Counterspell is the same lockout without the damage rider. (The Felhunter's Spell Lock runs the identical design as a pet ability, outside this trainer-book population.)",
    "The animation, the resource paying for it, and whether a damage rider comes along.",
    "Like [[families/rez|resurrection]], a cross-class utility franchise — every class got the same button with a different glove."),
fam("fears", "The Fear Franchise", TEMPLATE, "😱",
    ["Fear", "Psychic Scream", "Intimidating Shout", "Scare Beast", "Howl of Terror"],
    "targets, count, and radius",
    "'Strikes fear in the target(s), causing them to flee for Y sec.' Fear/Scare Beast measure 0.82 — the Hunter's copy just narrows the target type, exactly like D&D's Hold Person→Hold Monster in reverse.",
    "Single vs. area, target type, and the class stamp.",
    "One panic button, five brandings."),
fam("cleanses", "The Cleanse Counter", CLONE, "🧼",
    ["Cure Poison", "Cure Disease", "Abolish Poison", "Abolish Disease",
     "Remove Lesser Curse", "Remove Curse", "Purify", "Cleanse", "Dispel Magic"],
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
     "Seal of the Crusader"],
    "the on-hit payload",
    "'Fills the Paladin with holy power, causing attacks to X. Lasts 30 sec. Unleashing this Seal's energy will judge an enemy…' Light/Wisdom measure 0.94.",
    "The proc payload and its judged counterpart.",
    "A two-stage engine (seal + judgement) with six cartridges — the deepest template in the Paladin's warehouse."),
fam("polymorph", "The Polymorph Barn", CLONE, "🐑",
    ["Polymorph", "Polymorph: Cow"],
    "the barnyard animal",
    "'Transforms the enemy into a X, forcing it to wander around for up to Y sec.' The variants are literal reskins of the base spell (0.9+), obtained as rare drops — the reskin as a *collectible*.",
    "The animal.",
    "BG3 ships variant menus in a container; classic WoW sold them as loot. Same design, different economy."),
fam("poisons", "The Numbered Vials", CLONE, "🧪",
    ["Mind-numbing Poison", "Mind-numbing Poison II", "Mind-numbing Poison III"],
    "the roman numeral",
    "'Coats a weapon with poison that lasts X…' — the same vial three times, with the rank number promoted into the spell name (0.9+ pairwise). The rest of the poison rack (Instant, Deadly, Crippling, Wound) is item-crafted rather than trainer-taught, so it sits outside this population.",
    "The number on the label.",
    "The rank clone farm caught red-handed: when a rank escapes the rank system, it becomes a 'new' spell by suffix."),

FAMILY_OF = {}
for f in F:
    for m in f["members"]:
        FAMILY_OF[m] = f

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
    md = f"""# <span class="femoji">{f['icon']}</span> {f['title']}

<span class="tier tier-{f['tier']}">{TIER_LABEL[f['tier']]}</span> · {len(mem)} abilities · mechanical similarity {simtxt}

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

names_of = {c: {r["name"] for r in class_recs(c)} for c in CLASSES}
for c in CLASSES:
    lst = class_recs(c)
    in_fam = [r for r in lst if r["id"] in FAMILY_OF]
    ranks = sum(r["rank_count"] for r in lst)
    ov = sorted(((100 * len(names_of[c] & names_of[b]) / len(names_of[c]), b)
                 for b in CLASSES if b != c), reverse=True)[:3]
    ovtxt = ", ".join(f"**{p:.0f}%** with {f'[[classes/{b.lower()}|{b}]]'}" for p, b in ov)
    rows = ["| Lv | Ability | School | Ranks | Family |", "|---|---|---|---|---|"]
    for r in lst:
        fm = FAMILY_OF.get(r["id"])
        fl = f"[[families/{fm['slug']}|{fm['icon']} {fm['title']}]]" if fm else "—"
        rows.append(f"| {r['level']} | {sp_name(r)} | {r['school']} | {r['rank_count']} | {fl} |")
    md = f"""# {c} Spellbook (Classic)

**{len(lst)} abilities** ({ranks} spellbook entries counting ranks — {100*(ranks-len(lst))/max(1,ranks):.0f}% of the book is rank copies) · **{len(in_fam)}** in an identified family ({100*len(in_fam)/max(1,len(lst)):.0f}%)

Shared ability names: {ovtxt}.

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

Scores are masked-tooltip similarity ([[methodology|method]]); classic tooltips are macro-parameterized in the game data itself, so the masking mostly just removes what Blizzard already treats as a variable.
""")

# methodology
n_rank_entries = sum(r["rank_count"] for r in RECS)
page("methodology", "Methodology", "Start", f"""# Methodology

**Source.** The game's own client database tables for **WoW Classic Era** (build 1.15.9.69547), fetched as CSV from [wago.tools](https://wago.tools): `SpellName`, `Spell` (tooltips), `SkillLineAbility` + `SkillLine` (class attribution via class masks), `SpellLevels`, `SpellMisc` (school masks). Population: abilities in the nine classes' skill lines with a trainer level requirement — filtering out talents, hidden procs, and Season of Discovery additions (spell ids ≥ 100000, Engraving/Runes lines). **{N} distinct abilities** remain, spanning **{n_rank_entries} spellbook entries** once ranks are counted.

**The rank clone farm.** {n_rank_entries - N} of those entries ({100*(n_rank_entries-N)/n_rank_entries:.0f}%) are rank duplicates — the same spell re-taught with bigger numbers. Classic's ranks are BG3's upcast clones and D&D's spell-level laddering taken to their logical extreme: two-thirds of the classic spellbook is the same spell again.

**Similarity.** Blended mechanical score: 0.6 × the *effect signature* (each ability's `SpellEffect` rows — effect types, aura codes, mechanics, base-point sign, implicit targets — the game's actual machinery) + 0.4 × the masked tooltip (macros `$s1`/`$d`/`${{formulas}}`, schools, elements, creature types, cities, and stat names replaced with tokens). Two abilities that stun, drain, or buff through the same aura code measure as siblings even when their tooltips are written differently. Highest rank per ability is analyzed; ranks collapse first.

**Icons.** Fetched from [warcraft.wiki.gg](https://warcraft.wiki.gg) (the community wiki), by reading each ability page's infobox `icon=` parameter through the MediaWiki API — batched and throttled. Icons © Blizzard Entertainment, shown for research reference.

**Known limits.** Talents are excluded (trainer spellbook only); pet abilities excluded; Classic Era data includes minor anniversary-era tuning. Cross-era comparison uses the same masks as the SRD and BG3 studies but the population definitions differ slightly per game — the headline percentages are directional, not decimal-precise.

**Reproduce.** `wow_dataset.py` → `wow_analyze.py` → `wow_icons.py` → `build_wow_codex.py`. Companion codices: the D&D 5e SRD and Baldur's Gate 3.
""")

# overview
mat = ["| ↓ · shares names with → | " + " | ".join(f"[[classes/{c.lower()}|{c[:4]}]]" for c in CLASSES) + " |",
       "|---|" + "---|" * len(CLASSES)]
for a in CLASSES:
    cells = []
    for b in CLASSES:
        cells.append("—" if a == b else f"{100 * len(names_of[a] & names_of[b]) / len(names_of[a]):.0f}%")
    mat.append(f"| [[classes/{a.lower()}|{a}]] ({len(names_of[a])}) | " + " | ".join(cells) + " |")

page("overview", "Overview", "Start", f"""# How Homogeneous Are WoW Classic Spells?

The third dataset in the homogeneity study — and the most homogeneous of the three. Everything below is read from WoW Classic Era's own client database ({N} trainer-taught class abilities), with icons from the community wiki. See [[findings|The Identical-Spell List]] for the full family catalogue and [[methodology|Methodology]] for the pipeline.

## Axis 0 — the rank clone farm

Before any reskin analysis: **{100*(n_rank_entries-N)/n_rank_entries:.0f}% of the classic spellbook is rank duplicates** ({n_rank_entries} entries for {N} abilities). BG3 hides its upcast clones in the data files; classic sells them at the trainer.

## Axis 1 — the same ability in several class books

Unlike D&D (where classes share one spell list) or BG3 (where lists overlap), classic WoW ships **the same design as separate class-branded spells**: nine heals that are [[families/heals|one heal]], four [[families/rez|resurrections]], four [[families/interrupts|interrupts]], one [[families/protection|protection effect]] wearing armor, ward, and shield vocabularies across four classes, Cure Poison printed verbatim in two books, and the Feral Druid — [[families/cat-is-rogue|a licensed photocopy of the Rogue and Warrior kits]]. Exact name sharing is rare (the matrix below), because the *names* are the reskin:

{chr(10).join(mat)}

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
    ("Start", ["overview", "findings", "spells", "methodology"]),
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
  font-size:12.5px;color:var(--muted)}
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
  crumb.textContent = 'azeroth codex' + (parts.length>1 ? ' / '+parts[0] : '') + ' / ' + PAGES[slug].title.toLowerCase();
  document.querySelectorAll('nav a[data-slug]').forEach(a=>a.classList.toggle('on', a.dataset.slug===slug));
  nav.classList.remove('open');
  window.scrollTo(0,0);
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

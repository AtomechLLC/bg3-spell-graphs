"""Build the spell-homogeneity wiki: markdown pages (wiki/) + single-file HTML.

Karpathy-wiki pattern: many small pages, densely interlinked with [[wikilinks]],
an index, and backlinks at the bottom of every page.
"""
import json
import os
import re
import html as htmllib
from collections import defaultdict
from difflib import SequenceMatcher

import analyze_spells as A

spells = json.load(open("spells_2014.json", encoding="utf-8"))
BY = {s["index"]: s for s in spells}
for s in spells:
    s["_classes"] = sorted(c["name"] for c in s.get("classes", []))
    s["_norm"] = A.normalize(A.spell_text(s)).split()

CLASSES = ["Bard", "Cleric", "Druid", "Paladin", "Ranger", "Sorcerer", "Warlock", "Wizard"]
CLASS_LISTS = {c: sorted([s for s in spells if c in s["_classes"]],
                         key=lambda s: (int(s["level"]), s["name"])) for c in CLASSES}


def sim(a, b):
    return SequenceMatcher(None, BY[a]["_norm"], BY[b]["_norm"], autojunk=False).ratio()


# BG3 icons (bg3_icons/<slug>.png, fetched from bg3.wiki where the spell exists in BG3)
import base64
BG3_URIS = {}
if os.path.isdir("bg3_icons"):
    for fn in os.listdir("bg3_icons"):
        if fn.endswith(".png"):
            with open(os.path.join("bg3_icons", fn), "rb") as fh_:
                BG3_URIS[fn[:-4]] = "data:image/png;base64," + base64.b64encode(fh_.read()).decode()


def sp_name(s):
    """Spell name cell, with its BG3 icon when the spell exists in BG3."""
    tag = f'<img class="sic" data-i="{s["index"]}" alt=""> ' if s["index"] in BG3_URIS else ""
    return f"{tag}**{s['name']}**"


# ---------------------------------------------------------------- family spec
CLONE, TEMPLATE, ENGINE = "clone", "template", "engine"
TIER_LABEL = {CLONE: "Verbatim clone", TEMPLATE: "Shared template", ENGINE: "Shared engine"}

FAMILIES = [
 dict(slug="guidance-resistance", title="Guidance & Resistance", tier=CLONE,
  members=["guidance", "resistance"],
  differs="d4 on ability checks vs. d4 on saving throws",
  shared="Touch a willing creature; concentration, up to 1 minute; once before the spell ends, the target rolls a d4 and adds it to one roll of the named kind. Every other word — casting time, range, components, duration, the roll-before-or-after clause — is identical.",
  varies="One noun. Guidance feeds ability checks, Resistance feeds saving throws.",
  read="The purest clone pair in the SRD: one spell, published twice, differentiated by a single game-term substitution. Both even sit on the same two class lists (Cleric, Druid)."),
 dict(slug="dominate", title="The Dominate Chain", tier=CLONE,
  members=["dominate-beast", "dominate-person", "dominate-monster"],
  differs="target creature type and spell level; upcast table",
  shared="Wisdom save or charmed; telepathic command while conscious; take total control as an action; the target repeats the save each time it takes damage. Dominate Beast and Dominate Monster have a masked-text similarity of 1.000 — word-for-word the same spell.",
  varies="The noun in the targeting line (beast / humanoid / creature), the spell level the same text is sold at (4 / 5 / 8), and how upcasting extends duration.",
  read="Horizontal homogeneity priced vertically: widening the legal target set from 'beast' to 'any creature' costs four spell levels while the mechanical text stays frozen."),
 dict(slug="conjure-table", title="Conjure by Menu", tier=CLONE,
  members=["conjure-animals", "conjure-minor-elementals", "conjure-woodland-beings"],
  differs="which creature-type menu you order from",
  shared="Summon from the identical CR menu — one CR 2, or two CR 1, or four CR 1/2, or eight CR 1/4; they obey verbal commands, act on their own initiative, and doubling counts on upcast. Masked similarity runs 0.93–0.97 across the trio.",
  varies="Only the creature type filling the menu (beasts / elementals / fey) and the base level (3 / 4 / 4).",
  read="A literal template: the summoning engine is one block of rules text with a creature-type parameter. Druid gets all three menus."),
 dict(slug="cure", title="The Cure Family", tier=CLONE,
  members=["cure-wounds", "healing-word", "mass-cure-wounds", "mass-healing-word", "prayer-of-healing"],
  differs="die size, action vs. bonus action, touch vs. ranged, one vs. six targets",
  shared="Creature(s) regain XdY + spellcasting modifier hit points; +1 die per higher slot; no effect on undead or constructs. Cure Wounds vs. Healing Word masks to 0.878, Healing Word vs. Prayer of Healing to 0.895.",
  varies="Delivery parameters only: d8 touch action (Cure Wounds), d4 ranged bonus action (Healing Word), and the six-target versions of each one to four levels up. Related fixed-amount tier: Heal (70 hp) and Mass Heal (700 hp shared), plus the damage mirror Inflict Wounds.",
  read="One healing engine sold five times, priced along two axes — action economy and target count. This is the cleanest example of a parameterized spell line in the SRD."),
 dict(slug="hold", title="The Hold Pair", tier=CLONE,
  members=["hold-person", "hold-monster"],
  differs="humanoid vs. any creature; level 2 vs. 5",
  shared="Wisdom save or paralyzed; repeat the save at the end of each of its turns; upcast targets one additional creature. The paralysis engine is untouched between the two.",
  varies="The target noun and three spell levels of price. (Masked similarity 0.694 — the Person text carries an extra targeting clause, but mechanically nothing else changes.)",
  read="Same pricing logic as the [[families/dominate|Dominate chain]]: 'works on anything' is treated as a rarity upgrade, not a mechanical one."),
 dict(slug="bane-bless", title="Bane & Bless", tier=CLONE,
  members=["bane", "bless"],
  differs="add vs. subtract the d4; Bane allows a save",
  shared="Up to three creatures within 30 feet; concentration, 1 minute; a d4 rides on every attack roll and saving throw; +1 target per higher slot. Masked similarity 0.857.",
  varies="The sign of the d4 (buff vs. debuff) and one balancing clause — the hostile version grants a Charisma save.",
  read="A mirror clone: the same spell reflected across the friend/enemy axis, with the save as the only asymmetric cost."),
 dict(slug="blast", title="The Elemental Blast Template", tier=TEMPLATE,
  members=["burning-hands", "fireball", "lightning-bolt", "ice-storm", "cone-of-cold", "flame-strike", "circle-of-death", "hellish-rebuke"],
  differs="area shape, damage type, dice, save ability",
  shared="Pick an area; creatures inside make a save; XdY typed damage, half on a success; +1 die per higher slot. Fireball vs. Lightning Bolt is the flagship: same level, same 8d6, same Dex-save-for-half, same +1d6 upcast, even the same 'ignites flammable objects not being worn or carried' sentence — only the shape (20-ft sphere vs. 100-ft line) and the damage type differ.",
  varies="Shape (cone / sphere / line / cylinder), element, die size and count, and occasionally the save ability (Con for cold, Dex for the rest).",
  read="The workhorse template of evocation. The design intent is legible: damage type and shape are the flavor knobs, dice-per-slot-level is the balance knob, and the sentence structure never changes."),
 dict(slug="suggestion", title="The Suggestion Pair", tier=TEMPLATE,
  members=["suggestion", "mass-suggestion"],
  differs="one target vs. twelve; concentration dropped; duration",
  shared="Suggest a course of activity in a sentence or two; Wisdom save or the creature pursues it; the suggestion must sound reasonable; damage breaks the effect. Masked similarity 0.815.",
  varies="Target count (1 vs. 12), duration (8 hours vs. 24), concentration (required vs. not), and four spell levels.",
  read="The standard 'Mass' ladder move — see also [[families/cure|Mass Cure Wounds / Mass Healing Word]] and [[families/disguise-seeming|Seeming]]."),
 dict(slug="conjure-single", title="Conjure a Champion", tier=TEMPLATE,
  members=["conjure-elemental", "conjure-fey", "conjure-celestial"],
  differs="creature type, CR cap, what happens when concentration breaks",
  shared="Summon a single creature of the named type up to a CR cap; it's friendly, obeys commands, acts on its own initiative; upcast raises the CR cap. Elemental vs. Fey masks to 0.814.",
  varies="Creature type, CR cap (5 / 6 / 4), level (5 / 6 / 7), and the failure mode — a loosed elemental turns hostile, a fey merely leaves.",
  read="Sibling of [[families/conjure-table|Conjure by Menu]]: the same summoning contract at single-creature scale, with the danger clause as the flavor differentiator."),
 dict(slug="image", title="The Image Ladder", tier=TEMPLATE,
  members=["silent-image", "major-image"],
  differs="sound/smell/temperature added; cube size; level",
  shared="Create an illusory object/creature/phenomenon in a cube that you can move with an action; physical interaction reveals it; an Investigation check against your DC sees through it. Masked similarity 0.711.",
  varies="Major Image adds the sensory channels (sound, smell, temperature), grows the cube from 15 to 20 feet, and costs two more levels.",
  read="A vertical ladder where each rung unlocks a sensory channel — the illusion engine itself (interaction, Investigation check, action-to-move) is copied down verbatim."),
 dict(slug="hp-pool", title="The Hit-Point Pool Engine", tier=TEMPLATE,
  members=["sleep", "color-spray"],
  differs="unconscious vs. blinded; dice; duration",
  shared="Roll a dice pool; that many hit points of creatures are affected, in ascending order of current hit points, subtracting each affected creature from the pool; +2 dice per higher slot. Masked similarity 0.764.",
  varies="The pool (5d8 vs. 6d10), the condition inflicted (unconscious vs. blinded), and duration (1 minute vs. 1 round).",
  read="The SRD's most unusual shared engine — no save, no attack roll, a bidding system against current hit points — implemented exactly twice, both at level 1."),
 dict(slug="undead", title="The Undead Workshop", tier=TEMPLATE,
  members=["animate-dead", "create-undead"],
  differs="skeleton/zombie vs. ghoul; count; level",
  shared="Cast on corpses to raise undead you command verbally within 60 feet; control lapses after 24 hours unless you recast the spell to reassert it; upcast raises the head-count. Masked similarity 0.712.",
  varies="The product tier (skeletons and zombies at 3rd, ghouls at 6th) and the batch sizes.",
  read="A subscription mechanic — the 24-hour re-upkeep clause — copied wholesale between two levels of the same product line."),
 dict(slug="locate", title="The Locate Series", tier=TEMPLATE,
  members=["locate-object", "locate-creature", "locate-animals-or-plants"],
  differs="what is sensed; the blocking material",
  shared="Name or describe a thing familiar to you; sense the direction to the nearest one within 1,000 feet; the text of Locate Creature tracks Locate Object clause for clause.",
  varies="Object vs. creature vs. kind-of-beast/plant, and the counter-measure (lead blocks objects, running water blocks creatures). Locate Animals or Plants swaps the engine to a single ritual ping.",
  read="Notable for the flavored counter-measures: the one clearly hand-written clause in an otherwise copied text."),
 dict(slug="detect", title="The Detect Series", tier=TEMPLATE,
  members=["detect-magic", "detect-poison-and-disease", "detect-evil-and-good"],
  differs="what is sensed",
  shared="'For the duration, you sense X within 30 feet' — then the identical shielding paragraph: blocked by 1 foot of stone, 1 inch of common metal, a thin sheet of lead, or 3 feet of wood or dirt, in the same order every time.",
  varies="The sensed category, and small trimmings (Detect Magic doubles as the see-auras action).",
  read="The shielding paragraph is the tell: a boilerplate block pasted into all three spells verbatim, down to the material order."),
 dict(slug="invisibility", title="The Invisibility Ladder", tier=TEMPLATE,
  members=["invisibility", "greater-invisibility"],
  differs="breaks on attack/cast vs. doesn't; duration",
  shared="A creature you touch becomes invisible; anything worn or carried is invisible with it. Concentration on both.",
  varies="Greater deletes one sentence (the ends-if-you-attack clause), shrinks duration from 1 hour to 1 minute, and costs two more levels.",
  read="Rare case where the upgrade is defined by removing text: the ladder rung is priced at exactly one sentence."),
 dict(slug="disguise-seeming", title="The Disguise Ladder", tier=TEMPLATE,
  members=["disguise-self", "seeming"],
  differs="one target vs. everyone in range; duration",
  shared="An illusory makeover — change appearance, clothing, and gear within your rough size; physical inspection reveals it; Investigation check against your spell DC discerns it. Masked similarity 0.686.",
  varies="Self-only 1 hour at 1st level becomes any number of creatures in range for 8 hours at 5th.",
  read="The 'Mass' ladder again, with the same interaction/Investigation boilerplate as the [[families/image|Image ladder]]."),
 dict(slug="polymorph", title="The Polymorph Ladder", tier=TEMPLATE,
  members=["polymorph", "true-polymorph", "animal-shapes"],
  differs="scope, permanence, target count",
  shared="Transform a creature into a new form; the target takes the form's hit points; dropping to 0 in the new form reverts it to its own hit points; gear melds or drops. Animal Shapes vs. Polymorph masks to 0.710.",
  varies="Polymorph is beast-forms only; True Polymorph adds creature-to-creature and object conversions and can become permanent; Animal Shapes is the whole-party broadcast version.",
  read="One transformation rulebook shared by three spells; the ladder sells scope (what forms) and persistence (how long) rather than bigger dice."),
 dict(slug="phantom-armory", title="The Phantom Armory", tier=ENGINE,
  members=["spiritual-weapon", "arcane-sword", "arcane-hand", "flaming-sphere",
           "faithful-hound", "unseen-servant"],
  differs="what is conjured and how it attacks",
  shared="Conjure a persistent magical object or force that acts on its own slot in your action economy: created at a point in range, it attacks or acts when it appears and can be moved and reused as a bonus action or action each turn. Spiritual Weapon and Arcane Sword are the tight pair — both 'create a weapon, strike on cast, bonus/action to move it and strike again.'",
  varies="The conjured thing (floating weapon, sword of force, giant hand, rolling fire sphere, watchdog, invisible butler), its damage or utility, and its duration.",
  read="The third shelf of the conjuration aisle: [[families/conjure-table|units by menu]], [[families/conjure-single|single champions]], and here the objects and weapons — the summoning contract applied to things instead of creatures.",
 ),
 dict(slug="attack-cantrips", title="The Damage Cantrip Engine", tier=ENGINE,
  members=["fire-bolt", "ray-of-frost", "chill-touch", "shocking-grasp", "eldritch-blast", "acid-splash", "poison-spray", "sacred-flame"],
  differs="damage type, die size, attack vs. save, minor rider",
  shared="One die of typed damage at range, scaling to 2/3/4 dice at character levels 5, 11, and 17 — the identical scaling clause appears in every one.",
  varies="The die is priced by the rider: Fire Bolt gets a clean 1d10; Ray of Frost trades down to 1d8 for a 10-ft slow; Chill Touch takes 1d8 for a no-healing rider; Shocking Grasp takes 1d8 for no-reactions plus advantage vs. metal armor; Poison Spray gets 1d12 for 10-ft range; Eldritch Blast splits into multiple 1d10 beams.",
  read="The clearest pricing table in the game: hold the scaling engine constant, then trade die size against range, delivery (attack vs. save), and rider. A textbook for costed skill variation."),
 dict(slug="dispel", title="The Dispel Engine", tier=ENGINE,
  members=["dispel-magic", "counterspell"],
  differs="action on an effect vs. reaction on a cast",
  shared="Spells of 3rd level or lower end automatically; for anything higher, make a spellcasting ability check against DC 10 + the spell's level; upcast raises the automatic threshold. Masked similarity 0.600.",
  varies="Timing and target only: Dispel Magic is an action against a standing effect, Counterspell a reaction against one being cast.",
  read="One resolution subsystem serving two tactical niches — the same numbers moved to a different point in the timing chart."),
 dict(slug="darkness-daylight", title="Darkness & Daylight", tier=ENGINE,
  members=["darkness", "daylight"],
  differs="light vs. dark; each suppresses the other",
  shared="A 60-foot sphere of (anti-)light spreads from a point you choose; cast it on an object and the effect moves with it; cover the object to shut it off; each spell dispels the other's lower-level effects. Masked similarity 0.664.",
  varies="The photon budget, and one level of price.",
  read="A mirror pair like [[families/bane-bless|Bane & Bless]], with the dispel-each-other clause making the symmetry explicit in the rules text itself."),
 dict(slug="speak-with", title="The Speak-With Series", tier=ENGINE,
  members=["speak-with-animals", "speak-with-plants", "speak-with-dead"],
  differs="conversation partner; what it can tell you",
  shared="For the duration, comprehend and verbally communicate with a category of normally-mute interlocutor, whose knowledge is limited by its nature.",
  varies="The partner (beasts / plants / corpses) and bolted-on specifics — Speak with Dead is metered at five questions; Speak with Plants adds terrain manipulation.",
  read="A design-slot series: the texts diverge, but the slot ('unlock dialogue with X') is the same product on three shelves."),
 dict(slug="protection", title="The Protection Series", tier=ENGINE,
  members=["protection-from-poison", "protection-from-energy", "protection-from-evil-and-good"],
  differs="threat category; exact benefit",
  shared="Touch one creature; for the duration it gets a defensive package against a named threat category.",
  varies="The category (poison / one energy type / four creature types) and the package (cure + advantage, resistance, or disadvantage-to-hit plus charm/fright/possession immunity).",
  read="Same shelf label, different contents — the weakest homogeneity tier, where the name template promises more sharing than the text delivers."),
 dict(slug="touch-buffs", title="The Touch-Buff Skeleton", tier=ENGINE,
  members=["longstrider", "darkvision", "fly", "spider-climb", "water-breathing", "water-walk"],
  differs="the movement capability granted",
  shared="'Touch a willing creature; until the spell ends, it gains [capability]' — with 'one additional creature per higher slot' as the standard upcast on several of them.",
  varies="The capability (10-ft speed, darkvision, flight, wall-crawling, water-breathing, water-walking), the duration, and whether it needs concentration (only Fly).",
  read="The utility shelf: one sentence skeleton, six movement verbs. Fly vs. Longstrider masks to 0.660 despite two levels' distance."),
]

ICONS = {
    "guidance-resistance": "🎲", "dominate": "🧠", "conjure-table": "🐾",
    "cure": "❤️‍🩹", "hold": "⛓️", "bane-bless": "⚖️", "blast": "💥",
    "suggestion": "💬", "conjure-single": "🧞", "image": "🖼️",
    "hp-pool": "🧮", "undead": "💀", "locate": "🧭", "detect": "👁️",
    "invisibility": "🫥", "disguise-seeming": "🎭", "polymorph": "🐸",
    "attack-cantrips": "🪄", "phantom-armory": "⚔️", "dispel": "🧯", "darkness-daylight": "🌗",
    "speak-with": "🗣️", "protection": "🛡️", "touch-buffs": "🤝",
}
for f in FAMILIES:
    f["icon"] = ICONS[f["slug"]]

FAMILY_OF = {}
for f in FAMILIES:
    for m in f["members"]:
        assert m in BY, f"unknown slug {m}"
        FAMILY_OF[m] = f

# ------------------------------------------------------------------- helpers
def fam_link(f):
    return f"[[families/{f['slug']}|{f['icon']} {f['title']}]]"


def cls_link(c):
    return f"[[classes/{c.lower()}|{c}]]"


def spell_stat(s):
    """Compact stat cells for family member tables."""
    ct = s.get("casting_time", "").replace("1 action", "action").replace(
        "1 bonus action", "bonus").replace("1 reaction", "reaction")
    dur = s.get("duration", "")
    if s.get("concentration"):
        dur = f"Conc. {dur}"
    sv = ""
    if s.get("dc"):
        suc = {"half": " ½", "none": "", "other": " *"}.get(s["dc"].get("dc_success", ""), "")
        sv = s["dc"]["dc_type"]["name"] + suc
    elif s.get("attack_type"):
        sv = s["attack_type"] + " atk"
    dmg = ""
    d = s.get("damage") or {}
    dt = (d.get("damage_type") or {}).get("name", "")
    if "damage_at_slot_level" in d:
        lv = min(d["damage_at_slot_level"], key=int)
        dmg = f"`{d['damage_at_slot_level'][lv]}` {dt.lower()}"
    elif "damage_at_character_level" in d:
        lv = min(d["damage_at_character_level"], key=int)
        dmg = f"`{d['damage_at_character_level'][lv]}` {dt.lower()}"
    elif "heal_at_slot_level" in (s or {}):
        lv = min(s["heal_at_slot_level"], key=int)
        dmg = f"heal `{s['heal_at_slot_level'][lv]}`"
    aoe = s.get("area_of_effect")
    if aoe:
        sv = (sv + f" · {aoe['size']}-ft {aoe['type']}").strip(" ·")
    return ct, s.get("range", ""), dur, sv, dmg


def lvl(s):
    n = int(s["level"])
    return "Cantrip" if n == 0 else f"{n}"


# --------------------------------------------------------------- page bodies
PAGES = {}   # slug -> dict(title, group, md)


def page(slug, title, group, md, icon=None):
    PAGES[slug] = dict(title=title, group=group, md=md, icon=icon)


# family pages
for f in FAMILIES:
    mem = [BY[m] for m in f["members"]]
    mem.sort(key=lambda s: (int(s["level"]), s["name"]))
    sims = sorted((sim(a, b) for i, a in enumerate(f["members"])
                   for b in f["members"][i + 1:]), reverse=True)
    simtxt = f"{sims[0]:.2f}" if len(sims) == 1 else f"{sims[-1]:.2f}–{sims[0]:.2f}"
    rows = ["| Spell | Lv | School | Cast | Range | Duration | Save / Attack | Damage | Classes |",
            "|---|---|---|---|---|---|---|---|---|"]
    for s in mem:
        ct, rng, dur, sv, dmg = spell_stat(s)
        cls = ", ".join(cls_link(c) for c in s["_classes"])
        rows.append(f"| {sp_name(s)} | {lvl(s)} | {s['school']['name']} | {ct} | {rng} | {dur} | {sv} | {dmg} | {cls} |")
    md = f"""# <span class="femoji">{f['icon']}</span> {f['title']}

<span class="tier tier-{f['tier']}">{TIER_LABEL[f['tier']]}</span> · {len(mem)} spells · masked-text similarity {simtxt}

{chr(10).join(rows)}

**Shared skeleton.** {f['shared']}

**What varies.** {f['varies']}

**Design read.** {f['read']}

See the full ranked list on [[findings|The Identical-Spell List]], or how scores were computed in [[methodology|Methodology]].
"""
    page(f"families/{f['slug']}", f["title"], "Families · " + TIER_LABEL[f["tier"]] + "s", md,
         icon=f["icon"])

# class pages
overlap = {a: sorted(((100 * len({x['name'] for x in CLASS_LISTS[a]} & {x['name'] for x in CLASS_LISTS[b]}) / len(CLASS_LISTS[a]), b)
                      for b in CLASSES if b != a), reverse=True) for a in CLASSES}
for c in CLASSES:
    lst = CLASS_LISTS[c]
    in_fam = [s for s in lst if s["index"] in FAMILY_OF]
    top = overlap[c][:3]
    toptxt = ", ".join(f"**{p:.0f}%** shared with {cls_link(b)}" for p, b in top)
    rows = ["| Lv | Spell | School | Family | Also on |", "|---|---|---|---|---|"]
    for s in lst:
        f = FAMILY_OF.get(s["index"])
        fl = fam_link(f) if f else "—"
        others = [x for x in s["_classes"] if x != c]
        also = ", ".join(cls_link(o) for o in others) if others else "*(exclusive)*"
        rows.append(f"| {lvl(s)} | {sp_name(s)} | {s['school']['name']} | {fl} | {also} |")
    excl = sum(1 for s in lst if len(s["_classes"]) == 1)
    md = f"""# {c} Spell List

**{len(lst)} spells** in the SRD · **{excl}** exclusive to {c} ({100*excl/len(lst):.0f}%) · **{len(in_fam)}** belong to an identified [[findings|template family]] ({100*len(in_fam)/len(lst):.0f}%)

List overlap: {toptxt}.

{chr(10).join(rows)}

Back to [[overview|Overview]] · compare on [[findings|The Identical-Spell List]].
"""
    page(f"classes/{c.lower()}", c, "Classes", md)

# findings page
fam_rows = ["| Family | Tier | Spells | Peak similarity | What actually differs |",
            "|---|---|---|---|---|"]
for f in sorted(FAMILIES, key=lambda f: ([CLONE, TEMPLATE, ENGINE].index(f["tier"]), -len(f["members"]))):
    mem = [BY[m] for m in f["members"]]
    peak = max(sim(a, b) for i, a in enumerate(f["members"]) for b in f["members"][i + 1:])
    names = ", ".join(sorted(s["name"] for s in mem))
    fam_rows.append(f"| {fam_link(f)} | <span class=\"tier tier-{f['tier']}\">{TIER_LABEL[f['tier']]}</span> | {names} | {peak:.2f} | {f['differs']} |")

pair_rows = ["| Similarity | Spell A | Spell B | Family |", "|---|---|---|---|"]
with open("similar_pairs.csv", encoding="utf-8") as fh:
    next(fh)
    for i, line in enumerate(fh):
        if i >= 25:
            break
        parts = line.strip().split(",")
        r, a, la, b, lb = parts[0], parts[1], parts[2], parts[3], parts[4]
        fa = FAMILY_OF.get(a.lower().replace(" ", "-").replace("/", "-"))
        pair_rows.append(f"| `{r}` | {a} (L{la}) | {b} (L{lb}) | {fam_link(fa) if fa else '—'} |")

n_fam_spells = len(FAMILY_OF)
page("findings", "The Identical-Spell List", "Start", f"""# The Identical-Spell List

The deliverable: which D&D 5e spells are mostly the same spell. **{n_fam_spells} of 319 SRD spells ({100*n_fam_spells/319:.0f}%) fall into {len(FAMILIES)} families** of near-identical design, sorted into three tiers:

- <span class="tier tier-clone">Verbatim clone</span> — the rules text is the same spell with nouns swapped (damage type, target type, check vs. save).
- <span class="tier tier-template">Shared template</span> — same sentence-level structure and resolution; parameters and one or two clauses differ.
- <span class="tier tier-engine">Shared engine</span> — the text diverges, but the underlying subsystem (pricing table, resolution rule, sentence skeleton) is identical.

Two recurring shapes worth naming: **horizontal reskins** (same level band, different element or target type — [[families/blast|Fireball / Lightning Bolt]], [[families/guidance-resistance|Guidance / Resistance]]) and **vertical ladders** (the same spell re-sold at a higher level with one parameter raised — [[families/dominate|Dominate]], [[families/suggestion|Suggestion → Mass Suggestion]], [[families/invisibility|Invisibility → Greater]]).

## All families

{chr(10).join(fam_rows)}

## Top measured pairs

Highest masked-text similarity scores across all 50,721 spell pairs (see [[methodology|Methodology]] for the masking):

{chr(10).join(pair_rows)}

Similarity is evidence, not the verdict — [[families/hold|Hold Person / Hold Monster]] score only 0.69 because of one extra targeting clause, yet are mechanically a pure clone pair. Tier assignments above weigh the mechanics.
""")

# all-spells table, tagged by family
import csv as _csv
with open("spells_tagged_by_family.csv", "w", newline="", encoding="utf-8") as fh:
    w = _csv.writer(fh)
    w.writerow(["spell", "level", "school", "family", "family_icon", "tier", "classes", "in_bg3"])
    for s in sorted(spells, key=lambda s: (int(s["level"]), s["name"])):
        f = FAMILY_OF.get(s["index"])
        w.writerow([s["name"], int(s["level"]), s["school"]["name"],
                    f["title"] if f else "", f["icon"] if f else "",
                    TIER_LABEL[f["tier"]] if f else "",
                    "/".join(s["_classes"]),
                    "yes" if s["index"] in BG3_URIS else ""])

tag_rows = ["| Lv | Spell | School | Family | Tier | Classes |", "|---|---|---|---|---|---|"]
for s in sorted(spells, key=lambda s: (int(s["level"]), s["name"])):
    f = FAMILY_OF.get(s["index"])
    ftxt = fam_link(f) if f else "—"
    ttxt = f'<span class="tier tier-{f["tier"]}">{TIER_LABEL[f["tier"]]}</span>' if f else ""
    cls = ", ".join(cls_link(c) for c in s["_classes"])
    tag_rows.append(f"| {lvl(s)} | {sp_name(s)} | {s['school']['name']} | {ftxt} | {ttxt} | {cls} |")

page("spells", "All Spells, Tagged", "Start", f"""# All Spells, Tagged by Family

Every one of the **319 SRD spells**, flat, with its family tag — **{len(FAMILY_OF)} spells carry a tag** ({100*len(FAMILY_OF)/319:.0f}%), the rest are mechanically singular designs (marked —). Tiers are defined on [[findings|The Identical-Spell List]]; family pages hold the member stat tables and design reads.

{chr(10).join(tag_rows)}

Back to [[overview|Overview]] · [[findings|The Identical-Spell List]] · [[methodology|Methodology]]
""")

# missile spells
MISSILES = [
    # slug, to-hit, damage, effect/rider, upcast
    ("fire-bolt", "ranged atk", "`1d10` fire", "Ignites unattended flammable objects.", "`2d10`/`3d10`/`4d10` at char lv 5/11/17"),
    ("ray-of-frost", "ranged atk", "`1d8` cold", "Target's speed −10 ft until your next turn.", "`2d8`/`3d8`/`4d8` at 5/11/17"),
    ("chill-touch", "ranged atk", "`1d8` necrotic", "Target can't regain hit points until your next turn; undead also get disadvantage vs. you.", "`2d8`/`3d8`/`4d8` at 5/11/17"),
    ("eldritch-blast", "ranged atk", "`1d10` force", "Beams aim independently at any targets.", "2/3/4 beams at 5/11/17"),
    ("produce-flame", "ranged atk", "`1d8` fire", "Held flame doubles as a 10-ft light for 10 min; hurl it up to 30 ft to attack.", "`2d8`/`3d8`/`4d8` at 5/11/17"),
    ("acid-splash", "DEX save", "`1d6` acid", "The hurled bubble can catch two creatures within 5 ft of each other.", "`2d6`/`3d6`/`4d6` at 5/11/17"),
    ("magic-missile", "auto-hit", "3 × `1d4+1` force", "Three darts, split freely among targets, all strike simultaneously — no roll, no save.", "+1 dart per slot"),
    ("guiding-bolt", "ranged atk", "`4d6` radiant", "Next attack roll against the target before your next turn has advantage.", "+`1d6` per slot"),
    ("acid-arrow", "ranged atk", "`4d4` acid + `2d4` delayed", "Delayed damage lands at the end of the target's next turn; on a miss, half the initial damage and no delayed.", "+`1d4` to both per slot"),
    ("scorching-ray", "3 ranged atks", "`2d6` fire per ray", "Each ray is a separate attack at any targets.", "+1 ray per slot"),
    ("ray-of-enfeeblement", "ranged atk", "—", "Target deals half damage with Strength-based weapon attacks; Con save at each turn end to shake it. Concentration, 1 min.", "—"),
    ("disintegrate", "DEX save", "`10d6+40` force", "At 0 hp the target turns to dust (no Revivify); also vaporizes Large-or-smaller nonmagical objects and force constructs.", "+`3d6` per slot"),
]
mrows = ["| Spell | Lv | To-hit | Damage | Range | Effect / rider | Scaling | Classes |",
         "|---|---|---|---|---|---|---|---|"]
for slug, hit, dmg, fx, up in MISSILES:
    s = BY[slug]
    f = FAMILY_OF.get(slug)
    cls = ", ".join(cls_link(c) for c in s["_classes"])
    mrows.append(f"| {sp_name(s)} | {lvl(s)} | {hit} | {dmg} | {s.get('range')} | {fx} | {up} | {cls} |")

page("missiles", "Missile Spells", "Start", f"""# <span class="femoji">🏹</span> Missile Spells

Every SRD spell that fires a **single-target projectile** — a bolt, ray, dart, orb, or hurled missile — with what it does on impact. Beam-and-blast spells whose projectile explodes into an area ([[families/blast|Fireball's]] "bright streak" is flavor text for an AoE) are excluded, as are melee touch spells (Shocking Grasp, Inflict Wounds, Vampiric Touch) and effects that descend from above (Sacred Flame, Call Lightning).

{chr(10).join(mrows)}

## The pricing spectrum

Missiles show the same costed-variation logic as the [[families/attack-cantrips|damage-cantrip engine]] (which supplies half this table), extended along the **to-hit axis**:

- **Auto-hit** pays in die size — Magic Missile's guaranteed `1d4+1` darts are the floor.
- **Attack roll** buys the big dice — Fire Bolt's `1d10`, Guiding Bolt's `4d6` — and riders are paid for with die-size cuts (Ray of Frost's slow costs a step down to `1d8`).
- **Save-based** missiles trade accuracy mechanics for splash or severity — Acid Splash catches two targets; Disintegrate's save gates the game's nastiest single-target number (`10d6+40` and dust).

**Multi-projectile** is its own upcast currency: Scorching Ray and Eldritch Blast scale in *count*, Guiding Bolt and Acid Arrow in *dice* — same engine, different knob.

**Not measurable here:** the PHB/expansion missiles outside the SRD — Chromatic Orb, Witch Bolt, Ray of Sickness — per the [[methodology|data limits]].

Back to [[overview|Overview]] · [[spells|All Spells, Tagged]]
""", icon="🏹")

# methodology
page("methodology", "Methodology", "Start", f"""# Methodology

**Source.** The [SRD 5.1 spell database](https://github.com/5e-bits/5e-database) (the dataset behind dnd5eapi.co) — all **319 spells** of the 2014 System Reference Document with full rules text and per-class lists. Includes content from the SRD 5.1 by Wizards of the Coast, CC-BY-4.0. D&D Beyond was not scraped: its terms block automated access, and its spell content beyond the SRD is paywalled licensed material.

**Pipeline.**

1. **Mask the flavor.** Lowercase each spell description, then replace surface variables with tokens: damage types → `DMG`, element words (flame, frost, shock…) → `ELEM`, creature words (beast, humanoid, fey…) → `CRT`, ability names → `ABL`, dice expressions → `DICE`, all numbers → `N`.
2. **Compare structure.** Token-level `difflib.SequenceMatcher` ratio (autojunk off) over every pair of masked descriptions — 50,721 pairs.
3. **Cluster.** Union-find over pairs above 0.72 seeds the clone groups; the 0.60–0.72 band plus mechanical judgment fills out the template and engine tiers.

After masking, two spells that differ only in damage type, dice, or target creature become near-identical strings — which is precisely the definition of a reskin.

**What the score misses.** It reads *wording*, not *rules*. A copied spell with one extra sentence loses several points ([[families/hold|Hold Person/Monster]], 0.69); two spells with the same mechanic written by different hands score low ([[families/speak-with|the Speak-With series]]). Tier calls on [[findings|the list]] therefore combine the metric with a mechanical read.

**Known limits.** The SRD is a subset of the 2014 Player's Handbook (319 of 361 spells — no Chromatic Orb, no subclass-expansion lists), and excludes later books entirely; notably Tasha's *Summon X* series, the most aggressively templated spell family in 5e, cannot be measured here. The 2024 revision is also out of scope.

**Icons.** Spell rows carry the spell's *Baldur's Gate 3* icon where the spell exists in BG3 ({len(BG3_URIS)} of 319 — itself a rough measure of which SRD spells survived into the video-game adaptation, which caps at 6th-level slots). Icons were extracted from a locally owned BG3 install (`Game.pak` controller-UI DDS assets, downscaled to 64 px); © Larian Studios & Wizards of the Coast, embedded for private research reference.

**Reproduce.** `analyze_spells.py` builds `similar_pairs.csv`, `clusters.json`, and `spell_lists_per_class.csv`; `class_stats.py` prints the overlap matrix; `build_wiki.py` renders this wiki.
""")

# overview
mat_rows = ["| ↓ list · shared with → | " + " | ".join(cls_link(c) for c in CLASSES) + " |",
            "|---|" + "---|" * len(CLASSES)]
for a in CLASSES:
    cells = []
    names_a = {x["name"] for x in CLASS_LISTS[a]}
    for b in CLASSES:
        if a == b:
            cells.append("—")
        else:
            pct = 100 * len(names_a & {x["name"] for x in CLASS_LISTS[b]}) / len(names_a)
            cells.append(f"{pct:.0f}%")
    mat_rows.append(f"| {cls_link(a)} ({len(names_a)}) | " + " | ".join(cells) + " |")

share = defaultdict(list)
for s in spells:
    share[len(s["_classes"])].append(s["name"])
most_shared = sorted(share[7] + share[6], key=str)

page("overview", "Overview", "Start", f"""# How Homogeneous Are D&D 5e Spells?

A research wiki mapping **skill homogeneity** in the D&D 5e (2014 SRD) spell system: where the game re-sells the same design with a new coat of paint, and where classes genuinely differ. Built from all 319 SRD spells — see [[methodology|Methodology]] for the pipeline, and [[findings|The Identical-Spell List]] for the headline deliverable.

Homogeneity shows up on two independent axes:

## Axis 1 — the same spell, on many class lists

Spell lists overlap heavily. The 319 unique spells fill **778 class-list slots** — the average spell appears on **2.4 lists**, and **74%** of spells appear on two or more. {" and ".join(most_shared[:2])} sit on **7 of 8** lists; {", ".join(most_shared[2:])} on 6.

| | |
|---|---|
| {cls_link('Sorcerer')} | **94%** of its list is inside {cls_link('Wizard')}'s |
| {cls_link('Warlock')} | **92%** inside {cls_link('Wizard')}'s |
| {cls_link('Ranger')} | **89%** inside {cls_link('Druid')}'s |
| {cls_link('Paladin')} | **84%** inside {cls_link('Cleric')}'s |

Read column-wise, the matrix shows the four "parent" lists (Wizard, Cleric, Druid, Bard) and four classes largely assembled from them:

{chr(10).join(mat_rows)}

## Axis 2 — different spells, same design

Even *within* a list, many spells are one design published several times. **{n_fam_spells} spells ({100*n_fam_spells/319:.0f}%) fall into {len(FAMILIES)} template families** — from word-for-word clones ([[families/guidance-resistance|Guidance & Resistance]], [[families/dominate|the Dominate chain]]) through parameterized templates ([[families/blast|Fireball / Lightning Bolt]], [[families/cure|the Cure family]]) to shared engines ([[families/attack-cantrips|the damage-cantrip pricing table]], [[families/dispel|Dispel / Counterspell]]).

The full tiered list, with what differs in each family, is on [[findings|The Identical-Spell List]].

## Browse

- **Classes:** {" · ".join(cls_link(c) for c in CLASSES)}
- **The list:** [[findings|The Identical-Spell List]]
- **Every spell, tagged:** [[spells|All Spells, Tagged]]
- **How it was measured:** [[methodology|Methodology]]
""")

# ------------------------------------------------------- backlinks + writing
WIKILINK = re.compile(r"\[\[([a-zA-Z0-9\-/]+)(?:\|([^\]]+))?\]\]")
links_to = defaultdict(set)
for slug, p in PAGES.items():
    for m in WIKILINK.finditer(p["md"]):
        tgt = m.group(1)
        if tgt in PAGES and tgt != slug:
            links_to[tgt].add(slug)

for slug, p in PAGES.items():
    bl = sorted(links_to.get(slug, []))
    if bl:
        p["md"] += "\n---\n*Linked from: " + " · ".join(f"[[{b}|{PAGES[b]['title']}]]" for b in bl) + "*\n"

os.makedirs("wiki/families", exist_ok=True)
os.makedirs("wiki/classes", exist_ok=True)
for slug, p in PAGES.items():
    with open(os.path.join("wiki", slug + ".md"), "w", encoding="utf-8") as fh:
        fh.write(p["md"])

# ------------------------------------------------------------- md -> html
INLINE_PATTERNS = [
    (re.compile(r"`([^`]+)`"), r"<code>\1</code>"),
    (re.compile(r"\*\*([^*]+)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"\*([^*]+)\*"), r"<em>\1</em>"),
    (re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)"), r'<a href="\2" target="_blank" rel="noopener">\1</a>'),
]


def inline(text):
    # protect raw-HTML spans (tier badges) from escaping
    spans = []
    def stash(m):
        spans.append(m.group(0))
        return f"\x00{len(spans)-1}\x00"
    text = re.sub(r"<span[^>]*>.*?</span>|<img[^>]*>", stash, text)
    text = htmllib.escape(text, quote=False)
    for pat, rep in INLINE_PATTERNS:
        text = pat.sub(rep, text)
    def wl(m):
        tgt, label = m.group(1), m.group(2)
        title = PAGES.get(tgt, {}).get("title", tgt)
        return f'<a class="wl" href="#/{tgt}">{label or title}</a>'
    text = WIKILINK.sub(wl, text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)
    return text


def md_to_html(md):
    out, i = [], 0
    lines = md.split("\n")
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("|"):
            tbl = []
            while i < len(lines) and lines[i].startswith("|"):
                # shield the | inside [[slug|label]] from the cell splitter
                tbl.append(WIKILINK.sub(lambda m: m.group(0).replace("|", "\x01"), lines[i]))
                i += 1
            def cells_of(row):
                return [c.strip().replace("\x01", "|") for c in row.strip("|").split("|")]
            out.append('<div class="tw"><table><thead><tr>' +
                       "".join(f"<th>{inline(c)}</th>" for c in cells_of(tbl[0])) + "</tr></thead><tbody>")
            for row in tbl[2:]:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells_of(row)) + "</tr>")
            out.append("</tbody></table></div>")
            continue
        if ln.startswith("- "):
            out.append("<ul>")
            while i < len(lines) and lines[i].startswith("- "):
                out.append(f"<li>{inline(lines[i][2:])}</li>"); i += 1
            out.append("</ul>")
            continue
        if ln.startswith("### "):
            out.append(f"<h3>{inline(ln[4:])}</h3>")
        elif ln.startswith("## "):
            out.append(f"<h2>{inline(ln[3:])}</h2>")
        elif ln.startswith("# "):
            out.append(f"<h1>{inline(ln[2:])}</h1>")
        elif ln.strip() == "---":
            out.append("<hr>")
        elif ln.strip():
            para = [ln]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"^(#|\||- |---)", lines[i + 1]):
                para.append(lines[i + 1]); i += 1
            out.append(f"<p>{inline(' '.join(para))}</p>")
        i += 1
    return "\n".join(out)


PAGES_HTML = {slug: md_to_html(p["md"]) for slug, p in PAGES.items()}

# --------------------------------------------------------------- html shell
NAV = [
    ("Start", ["overview", "findings", "spells", "methodology"]),
    ("Families · Clones", [f"families/{f['slug']}" for f in FAMILIES if f["tier"] == CLONE]),
    ("Families · Templates", [f"families/{f['slug']}" for f in FAMILIES if f["tier"] == TEMPLATE]),
    ("Families · Engines", [f"families/{f['slug']}" for f in FAMILIES if f["tier"] == ENGINE]),
    ("Class Spell Lists", [f"classes/{c.lower()}" for c in CLASSES]),
]

nav_html = []
for label, slugs in NAV:
    nav_html.append(f'<div class="navgroup"><div class="navlabel">{label}</div>')
    for s in slugs:
        ic = PAGES[s].get("icon")
        label = (f'<span class="femoji">{ic}</span> ' if ic else "") + PAGES[s]["title"]
        nav_html.append(f'<a data-slug="{s}" href="#/{s}">{label}</a>')
    nav_html.append("</div>")
nav_html = "\n".join(nav_html)

pages_json = json.dumps({slug: {"title": p["title"], "html": PAGES_HTML[slug]}
                         for slug, p in PAGES.items()})

HTML = """<title>The Reskin Codex</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Spectral:wght@500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --bg:#F4F5F2; --panel:#ECEEE9; --ink:#22262B; --muted:#5C645F;
  --line:#D6DAD2; --accent:#5A4FB0; --accent-ink:#473E92; --accent-bg:#5A4FB014;
  --clone:#A03A50; --clone-bg:#A03A5016; --template:#96671F; --template-bg:#96671F16;
  --engine:#2E7D74; --engine-bg:#2E7D7416; --code-bg:#E4E7E0;
}
:root:not([data-theme="light"]){}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#191B1E; --panel:#1F2226; --ink:#D6D8D2; --muted:#98A09A;
    --line:#33373C; --accent:#A79BF0; --accent-ink:#BCB2F5; --accent-bg:#A79BF01A;
    --clone:#E08A9B; --clone-bg:#E08A9B1A; --template:#D8A75C; --template-bg:#D8A75C1A;
    --engine:#7CC4BB; --engine-bg:#7CC4BB1A; --code-bg:#2A2E33;
  }
}
:root[data-theme="dark"]{
  --bg:#191B1E; --panel:#1F2226; --ink:#D6D8D2; --muted:#98A09A;
  --line:#33373C; --accent:#A79BF0; --accent-ink:#BCB2F5; --accent-bg:#A79BF01A;
  --clone:#E08A9B; --clone-bg:#E08A9B1A; --template:#D8A75C; --template-bg:#D8A75C1A;
  --engine:#7CC4BB; --engine-bg:#7CC4BB1A; --code-bg:#2A2E33;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:400 16px/1.65 "Source Serif 4",Georgia,serif;}
a{color:var(--accent);text-decoration:none}
a:hover{color:var(--accent-ink)}
.layout{display:flex;min-height:100vh}
nav{width:248px;flex:0 0 248px;background:var(--panel);border-right:1px solid var(--line);
  padding:20px 0 40px;position:sticky;top:0;height:100vh;overflow-y:auto}
.brand{font-family:Spectral,Georgia,serif;font-weight:700;font-size:19px;
  padding:4px 20px 14px;border-bottom:1px solid var(--line);margin-bottom:10px}
.brand small{display:block;font-family:"IBM Plex Mono",ui-monospace,monospace;
  font-size:10.5px;font-weight:400;color:var(--muted);letter-spacing:.04em;margin-top:2px}
.navlabel{font:500 10.5px/1 "IBM Plex Mono",ui-monospace,monospace;color:var(--muted);
  text-transform:uppercase;letter-spacing:.12em;padding:14px 20px 6px}
nav a{display:block;padding:4px 20px;font-size:14px;color:var(--ink)}
nav a:hover{background:var(--accent-bg)}
nav a.on{color:var(--accent-ink);background:var(--accent-bg);
  box-shadow:inset 3px 0 0 var(--accent)}
main{flex:1;min-width:0;padding:36px 44px 90px}
article{max-width:74ch;margin:0 auto}
.crumb{font:400 12px/1 "IBM Plex Mono",ui-monospace,monospace;color:var(--muted);
  letter-spacing:.03em;margin-bottom:22px}
h1{font-family:Spectral,Georgia,serif;font-weight:600;font-size:32px;line-height:1.15;
  text-wrap:balance;margin:0 0 14px}
h2{font-family:Spectral,Georgia,serif;font-weight:600;font-size:22px;margin:34px 0 10px}
h3{font-family:Spectral,Georgia,serif;font-weight:600;font-size:17px;margin:26px 0 8px}
p{margin:0 0 14px}
ul{margin:0 0 14px;padding-left:22px}
li{margin-bottom:6px}
hr{border:0;border-top:1px solid var(--line);margin:28px 0 14px}
code{font:500 13px "IBM Plex Mono",ui-monospace,monospace;background:var(--code-bg);
  padding:1px 5px;border-radius:3px;font-variant-numeric:tabular-nums}
.wl{border-bottom:1px dotted var(--accent)}
.wl:hover{background:var(--accent-bg)}
.tw{overflow-x:auto;margin:16px 0 20px;border:1px solid var(--line);border-radius:4px}
table{border-collapse:collapse;width:100%;font-size:13.5px;line-height:1.45}
th{font:500 11px "IBM Plex Mono",ui-monospace,monospace;text-transform:uppercase;
  letter-spacing:.07em;color:var(--muted);text-align:left;padding:8px 10px;
  border-bottom:1px solid var(--line);background:var(--panel);white-space:nowrap}
td{padding:6px 10px;border-bottom:1px solid var(--line);vertical-align:top;
  font-variant-numeric:tabular-nums}
tr:last-child td{border-bottom:0}
.sic{width:22px;height:22px;vertical-align:-6px;margin-right:5px;border-radius:4px}
.femoji{font-family:"Segoe UI Emoji","Apple Color Emoji","Noto Color Emoji",sans-serif;font-style:normal}
h1 .femoji{font-size:26px;margin-right:2px}
nav .femoji{display:inline-block;width:20px;font-size:13px}
.tier{font:500 10.5px "IBM Plex Mono",ui-monospace,monospace;text-transform:uppercase;
  letter-spacing:.08em;padding:2px 7px;border-radius:3px;white-space:nowrap}
.tier-clone{color:var(--clone);background:var(--clone-bg)}
.tier-template{color:var(--template);background:var(--template-bg)}
.tier-engine{color:var(--engine);background:var(--engine-bg)}
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
footer{max-width:74ch;margin:50px auto 0;padding-top:14px;border-top:1px solid var(--line);
  font-size:12.5px;color:var(--muted)}
</style>
<button id="menu" aria-label="Menu">☰ pages</button>
<div class="layout">
<nav id="nav">
<div class="brand">The Reskin Codex<small>d&amp;d 5e · srd 5.1 · 319 spells</small></div>
__NAV__
</nav>
<main>
<div class="crumb" id="crumb"></div>
<article id="art"></article>
<footer>Includes content from the SRD 5.1 by Wizards of the Coast, licensed CC-BY-4.0.
Similarity = masked-token sequence ratio; see the Methodology page.
Spell icons from <em>Baldur's Gate 3</em> (extracted from an owned install) — © Larian Studios
&amp; Wizards of the Coast; shown where the spell exists in BG3, for private research reference.</footer>
</main>
</div>
<script>
const PAGES = __PAGES__;
const BG3 = __BG3__;
const art = document.getElementById('art'), crumb = document.getElementById('crumb');
const nav = document.getElementById('nav');
function render(){
  let slug = location.hash.replace(/^#\\//,'') || 'overview';
  if(!PAGES[slug]) slug = 'overview';
  art.innerHTML = PAGES[slug].html;
  art.querySelectorAll('img.sic').forEach(el=>{
    const d = BG3[el.dataset.i];
    if(d) el.src = d; else el.remove();
  });
  const parts = slug.split('/');
  crumb.textContent = 'reskin codex' + (parts.length>1 ? ' / '+parts[0] : '') + ' / ' + PAGES[slug].title.toLowerCase();
  document.querySelectorAll('nav a[data-slug]').forEach(a=>{
    a.classList.toggle('on', a.dataset.slug===slug);
  });
  nav.classList.remove('open');
  window.scrollTo(0,0);
}
window.addEventListener('hashchange', render);
document.getElementById('menu').addEventListener('click',()=>nav.classList.toggle('open'));
render();
</script>
"""

HTML = HTML.replace("__NAV__", nav_html).replace("__PAGES__", pages_json)
HTML = HTML.replace("__BG3__", json.dumps(BG3_URIS))
with open("wiki.html", "w", encoding="utf-8") as fh:
    fh.write(HTML)

print(f"{len(PAGES)} pages, {len(FAMILY_OF)} spells in {len(FAMILIES)} families")
print(f"wiki.html: {os.path.getsize('wiki.html')/1024:.0f} KB")

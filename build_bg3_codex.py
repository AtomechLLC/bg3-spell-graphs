"""Build the BG3 spell-homogeneity codex: markdown pages (bg3_wiki/) + bg3_codex.html."""
import base64
import csv as csvlib
import html as htmllib
import json
import os
import re
from collections import defaultdict
from itertools import combinations

from bg3_analyze import prep, pair_score

recs = json.load(open("bg3_spells.json", encoding="utf-8"))
BY = {r["id"]: r for r in recs}
POP = [r for r in recs if r["is_spell"] and not r["upcast_variant"] and not r["container"]]
prep(POP)
prep([r for r in recs if r["container"]])  # children get masks too (unused but harmless)
POP_IDS = {r["id"] for r in POP}

BYNAME = defaultdict(list)
for r in POP:
    BYNAME[r["name"]].append(r)


def rid(name, level=None):
    """Resolve a population spell id by display name (level disambiguates)."""
    cands = [r for r in BYNAME.get(name, []) if level is None or r["level"] == level]
    assert cands, f"no spell named {name!r} (L{level})"
    return cands[0]["id"]


def sim(a, b):
    """Mechanical-signature similarity — the strong signal for BG3 data."""
    return pair_score(BY[a], BY[b])[1]


# deduped view for class stats: same (name, level) -> one spell, class union
DEDUP = {}
for r in POP:
    key = (r["name"], r["level"])
    if key in DEDUP:
        DEDUP[key]["classes"] = sorted(set(DEDUP[key]["classes"]) | set(r["classes"]))
    else:
        DEDUP[key] = dict(r)
DPOP = list(DEDUP.values())

CLASSES = ["Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger",
           "Rogue", "Sorcerer", "Warlock", "Wizard"]
ACTIONS = [r for r in recs if not r["is_spell"] and not r["upcast_variant"]
           and not r["container"]]

# ---------------------------------------------------------------- families
CLONE, TEMPLATE, ENGINE = "clone", "template", "engine"
TIER_LABEL = {CLONE: "Verbatim clone", TEMPLATE: "Shared template", ENGINE: "Shared engine"}

F = []
def fam(slug, title, tier, icon, members, differs, shared, varies, read):
    F.append(dict(slug=slug, title=title, tier=tier, icon=icon, members=members,
                  differs=differs, shared=shared, varies=varies, read=read))

fam("duplicate-skus", "The Duplicate SKUs", CLONE, "🛍️",
    [rid("Shield"), "Shout_Shield_Warlock", "Shout_Shield_Wizard",
     rid("Darkness"), rid("Eyes of the Dark: Darkness")],
    "nothing but the class that sells it",
    "Shield exists three times in the game data — `Shout_Shield_Sorcerer`, `Shout_Shield_Warlock`, `Shout_Shield_Wizard` — with measured similarity **1.000**: byte-identical mechanics, one entry per class that learns it. Darkness ships twice: once as the spell, once as the Shadow Magic sorcerer's 'Eyes of the Dark' feature grant (0.91 on mechanics).",
    "The id string and which list references it. Nothing else.",
    "The purest homogeneity in the game: not a reskin but a re-SKU. Larian duplicates entries so each grantor can own its copy — the same spell as three products. (Spirit Guardians pulls the same trick inside a [[containers|container]], with radiant/necrotic twins.)"),
fam("cure", "The Cure Family", CLONE, "❤️‍🩹",
    [rid("Cure Wounds"), rid("Healing Word"), rid("Prayer of Healing"),
     rid("Mass Cure Wounds"), rid("Mass Healing Word")],
    "die size, touch vs. ranged, action vs. bonus action, target count",
    "RegainHitPoints(XdY + modifier); the same healing engine as tabletop, ported intact. Cure Wounds vs. Healing Word measures 0.93 on mechanics; the whole family stays high.",
    "Delivery only: d8 touch action, d4 ranged bonus action, and the multi-target versions of each.",
    "The SRD's cleanest parameterized line survives the adaptation unchanged — five spells, one formula."),
fam("dominate", "The Dominate Pair", CLONE, "🧠",
    [rid("Dominate Beast"), rid("Dominate Person")],
    "target creature type; spell level",
    "Wisdom save or charmed and commanded; identical control mechanics (0.96). BG3 cuts the chain at 6th-level slots, so Dominate Monster didn't make the port.",
    "The legal target set (beast vs. humanoid) and one level of price.",
    "Tabletop's three-rung ladder arrives as two rungs — the pricing logic (wider target = higher slot) is preserved."),
fam("hold", "The Hold Pair", CLONE, "⛓️",
    [rid("Hold Person"), rid("Hold Monster")],
    "humanoid vs. any creature; level 2 vs. 5",
    "Wisdom save or Paralysed, repeat save each turn; 0.95 on mechanics. Both upcast by adding targets — implemented, like all BG3 upcasts, as [[methodology|cloned child entries]].",
    "The target noun and three spell levels.",
    "Same as tabletop; BG3 even keeps the paralysis-crit synergy that makes the pair famous."),
fam("invisibility", "The Invisibility Ladder", CLONE, "🫥",
    [rid("Invisibility"), rid("Greater Invisibility")],
    "breaks-on-attack clause; duration",
    "Apply the Invisible condition to a touched creature; 0.93 on mechanics.",
    "Greater removes the breaks-on-attack rule and costs two more levels.",
    "An upgrade defined by deleting a sentence, exactly as in the SRD."),
fam("ac-wardrobe", "The Armour-Class Wardrobe", CLONE, "🛡️",
    [rid("Mage Armour"), rid("Shield of Faith"), rid("Barkskin")],
    "how the AC number is phrased: 13+Dex, +2, or 16",
    "Touch/target a creature, apply a long-duration armour condition. Measured 0.80–0.86 on mechanics — Larian's status-effect engine makes three different tabletop wordings into one shape.",
    "The formula (base 13 + Dex / flat +2 / floor of 16), the class wearing it, and concentration (Shield of Faith only).",
    "A BG3-made clone family: in the 2014 rules these three read quite differently; the video game's condition system flattens them into siblings."),
fam("bane-bless", "Bane & Bless", CLONE, "⚖️",
    [rid("Bane"), rid("Bless")],
    "sign of the d4; Bane allows a save",
    "Up to 3 targets, a d4 riding attack rolls and saving throws, concentration; 0.77 on mechanics.",
    "Add vs. subtract, and the Charisma save on the hostile version.",
    "The mirror clone, ported intact."),
fam("charm", "The Charm Pair", CLONE, "💘",
    [rid("Animal Friendship"), rid("Charm Person")],
    "beast vs. humanoid",
    "Wisdom save or the Charmed condition; mechanical signature similarity 0.96 — in BG3 these two are the same spell against different phyla.",
    "The target type and the save-DC flavor.",
    "Tabletop wrote them as different texts; BG3's condition engine reveals them as one design."),

fam("walls", "The Wall Foundry", TEMPLATE, "🧱",
    [rid("Wall of Fire"), rid("Wall of Ice", 6), rid("Wall of Stone"),
     rid("Wall of Thorns"), rid("Blade Barrier")],
    "material, damage type, dice",
    "Draw a wall shape on the ground; it deals typed damage to creatures inside or crossing; signature similarity runs 0.86–0.97 across all five — the tightest template family in the game.",
    "The material (fire/ice/stone/thorns/spinning blades), damage dice, and what the wall does when touched vs. entered.",
    "Larian implements every wall through one zone system, so the five spells differ mainly by particle effect and damage row."),
fam("blast", "The Elemental Blast Template", TEMPLATE, "💥",
    [rid("Fireball"), rid("Lightning Bolt"), rid("Thunderwave"), rid("Flame Strike"),
     rid("Ice Storm"), rid("Cone of Cold"), rid("Sunbeam"), rid("Circle of Death")],
    "area shape, damage type, dice, save",
    "Area, save, XdY typed damage, half on success. Fireball vs. Lightning Bolt: 0.90 signature similarity. Lightning Bolt vs. Thunderwave: 0.96 — in BG3 they're nearly the same entry with different shapes.",
    "Shape (sphere/line/cone/cylinder), element, dice, and the save ability.",
    "The tabletop template, tightened: BG3's targeting system reduces 'shape' to a data field, pulling the family even closer together than in print."),
fam("surfaces", "The Surface Engine", TEMPLATE, "🕸️",
    [rid("Grease"), rid("Web"), rid("Entangle"), rid("Fog Cloud"),
     rid("Stinking Cloud"), rid("Evard's Black Tentacles"), rid("Plant Growth"),
     rid("Cloudkill"), rid("Spike Growth"), rid("Sleet Storm")],
    "which surface gets painted on the ground",
    "Pick an area; the game paints a surface or cloud that applies a condition to anyone inside. Signature similarities run 0.88–0.96 across the family (Grease/Web 0.90, Entangle/Stinking Cloud 0.94).",
    "The surface type (grease, webs, vines, fog, poison, tentacles…), its condition, and whether it's flammable, freezable, or dispellable by wind.",
    "BG3's signature homogenizer. Larian rebuilt tabletop's varied area-control spells on one ground-surface system — the game's most distinctive engine, and its strongest flattening force."),
fam("smites", "The Smite Armoury", TEMPLATE, "🔨",
    ["Target_Smite_Searing", "Target_Smite_Thunderous", "Target_Smite_Wrathful",
     "Target_Smite_Branding_Container", "Target_Smite_Blinding",
     "Target_StaggeringSmite", "Projectile_Smite_Banishing_Container"],
    "rider condition and damage type; two are melee/ranged containers",
    "Bonus-action weapon strike + XdY typed damage + a rider condition on hit; measured 0.92–0.94 signature similarity between smites.",
    "The rider (burning, prone, frightened, branded, blinded, staggered, banished), the element, and the level the rider is priced at. Branding and Banishing are themselves [[containers|containers]] with melee/ranged children.",
    "Seven products from one on-hit engine — a pricing table for conditions, with the smite name as the flavor knob."),
fam("teleports", "The Blink Ladder", TEMPLATE, "🌀",
    [rid("Misty Step"), rid("Dimension Door")],
    "range and passenger capacity",
    "Teleport to a visible point; 0.93 signature similarity.",
    "18m bonus-action self-only vs. long-range action with a passenger.",
    "A two-rung vertical ladder selling range and cargo."),
fam("hp-pool", "The Hit-Point Pool Engine", TEMPLATE, "🧮",
    [rid("Sleep"), rid("Colour Spray")],
    "unconscious vs. blinded",
    "Roll a pool of hit points; affect creatures in ascending current-HP order until it runs out; 0.81 on mechanics.",
    "The condition applied and the pool dice.",
    "Tabletop's oddest shared engine survives the port intact, still exactly twice, still both at level 1."),
fam("conjure", "The Summoning Contract", TEMPLATE, "🧞",
    [rid("Conjure Elemental"), rid("Conjure Minor Elemental"), rid("Find Familiar"),
     rid("Animate Dead"), rid("Planar Ally"), rid("Spiritual Weapon"), rid("Flaming Sphere")],
    "who — or what — answers the call",
    "Summon a persistent ally that fights and acts under your command: a creature chosen from a menu (Conjure Elemental/Minor Elemental, 0.94 signature similarity), a familiar, a raised corpse, a planar servant — or an *object* on the same contract: Spiritual Weapon and Flaming Sphere are summons whose 'creature' is a floating weapon or rolling fireball with its own place in your action economy.",
    "The summoned thing (elemental, familiar, undead, celestial, weapon, sphere), its control verbs, and duration. Five of the seven are [[containers|containers]], their menus implemented as child spells.",
    "One summoning engine spanning units, creatures, and conjured objects — the whole conjuration aisle runs on a single contract, and Larian's container system makes each menu literal."),

fam("attack-cantrips", "The Damage Cantrip Engine", ENGINE, "🪄",
    [rid("Fire Bolt"), rid("Ray of Frost"), rid("Bone Chill"), rid("Shocking Grasp"),
     rid("Eldritch Blast"), rid("Acid Splash"), rid("Poison Spray"),
     rid("Sacred Flame"), rid("Thorn Whip")],
    "damage type, die size, attack vs. save, rider",
    "One die of typed damage, scaling at character levels 5 and 10; Acid Splash vs. Poison Spray measures 0.95 on mechanics. Bone Chill is Chill Touch renamed.",
    "The die (d6–d12), delivery (attack roll vs. save), range, and the rider — slow, no-healing, pull, push, ignite.",
    "The same costed-variation table as tabletop, plus BG3's own twist: many of these also interact with the [[families/surfaces|surface engine]] (Fire Bolt ignites grease, Ray of Frost freezes water)."),
fam("cleanse", "The Cleanse Counter", ENGINE, "🧼",
    [rid("Lesser Restoration"), rid("Greater Restoration"), rid("Remove Curse"),
     rid("Protection from Poison")],
    "which status list gets wiped",
    "Touch a creature, remove conditions from a named list; signatures measure 0.83–0.89 — one RemoveStatus() engine with different shopping lists.",
    "The list (disease/poison vs. curses vs. everything) and the level.",
    "A vertical ladder of the same verb: pay more, cleanse more."),
fam("touch-buffs", "The Touch-Buff Skeleton", ENGINE, "🤝",
    [rid("Longstrider"), rid("Enhance Leap"), rid("Grant Flight"), rid("Darkvision"),
     rid("Feather Fall"), rid("Freedom of Movement")],
    "the movement verb granted",
    "Touch a willing creature; apply a long-duration movement condition. Enhance Leap vs. Longstrider: 0.86 signature.",
    "The verb (speed, jump, fly, see, fall, move freely), duration, and ritual eligibility.",
    "The utility shelf again — note Grant Flight is Fly renamed, and Enhance Leap is Jump renamed; Larian's names drift, the skeleton doesn't."),
fam("d4-riders", "Guidance & Resistance", ENGINE, "🎲",
    [rid("Guidance"), rid("Resistance")],
    "checks vs. saves",
    "Concentration cantrip, touch, a d4 riding one category of d20 roll; 0.89 signature similarity.",
    "One noun, as in tabletop.",
    "The purest SRD clone pair survives as the purest BG3 clone pair — some things are load-bearing."),

FAMILY_OF = {}
for f in F:
    for m in f["members"]:
        assert m in BY, f"unknown member {m}"
        FAMILY_OF[m] = f

# container axis annotations
CONTAINER_AXIS = {
    "Animate Dead": "undead form", "Banishing Smite": "melee / ranged",
    "Bestow Curse": "curse choice (9)", "Branding Smite": "melee / ranged",
    "Chromatic Orb": "damage type (6)", "Command": "verb (5)",
    "Conjure Barrage": "weapon held", "Conjure Elemental": "element (4)",
    "Conjure Minor Elemental": "creature (3)", "Contagion": "disease (6)",
    "Create or Destroy Water": "create / destroy", "Daylight": "sphere / enchant item",
    "Destructive Wave": "necrotic / radiant", "Disguise Self": "race × build × gender (32)",
    "Elemental Weapon": "damage type (5)", "Enhance Ability": "ability (6)",
    "Enlarge/Reduce": "enlarge / reduce", "Ensnaring Strike": "melee / ranged",
    "Eyebite": "condition (3)", "Find Familiar": "creature (6)",
    "Fire Shield": "chill / warm", "Glyph of Warding": "glyph effect (7)",
    "Hex": "ability (6)", "Otiluke's Freezing Sphere": "throw now / pocket it",
    "Planar Ally": "creature (3)", "Protection from Energy": "damage type (5)",
    "Spirit Guardians": "radiant / necrotic", "Spiritual Weapon": "weapon form (6)",
}
CONTAINERS = sorted((r for r in POP if r["children"]), key=lambda r: (r["level"], r["name"]))
N_CHILDREN = sum(len(r["children"]) for r in CONTAINERS)

# ---------------------------------------------------------------- icons
import io
from PIL import Image
BG3_URIS = {}
for fn in os.listdir("bg3_codex_icons"):
    if fn.endswith(".png"):
        buf = io.BytesIO()
        Image.open(os.path.join("bg3_codex_icons", fn)).save(buf, "WEBP", quality=82)
        BG3_URIS[fn[:-4]] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def sp_name(r):
    tag = f'<img class="sic" data-i="{r["id"]}" alt=""> ' if r["id"] in BG3_URIS else ""
    return f"{tag}**{r['name']}**"


# ---------------------------------------------------------------- helpers
def fmt_cost(uc):
    parts = []
    for p in uc.split(";"):
        if p.startswith("ActionPoint"):
            parts.append("Action")
        elif p.startswith("BonusActionPoint"):
            parts.append("Bonus")
        elif p.startswith("ReactionActionPoint"):
            parts.append("Reaction")
        elif p.startswith("SpellSlotsGroup"):
            parts.append("L" + p.split(":")[-1] + " slot")
        elif p.startswith("SpellSlot"):
            parts.append("L" + p.split(":")[-1] + " slot")
    return " + ".join(parts)


def fmt_damage(r):
    td = r["tooltip_damage"]
    out = []
    for dice, typ in re.findall(r"DealDamage\(([^,)]+),\s*(\w+)", td):
        out.append(f"`{dice.strip()}` {typ.lower()}")
    for heal in re.findall(r"RegainHitPoints\(([^)]+)\)", td):
        out.append("heal `" + heal.replace("SpellCastingAbilityModifier", "mod") + "`")
    return ", ".join(out)


def fmt_save(r):
    s = r["attack_save"]
    if not s:
        return ""
    if "Attack" in s:
        return {"RangedSpellAttack": "ranged atk", "MeleeSpellAttack": "melee atk",
                "RangedWeaponAttack": "ranged wpn", "MeleeWeaponAttack": "melee wpn"}.get(s, s)
    return s[:3].upper() + " save"


def lvl(r):
    return "Cantrip" if r["level"] == 0 else str(r["level"])


def fam_link(f):
    return f"[[families/{f['slug']}|{f['icon']} {f['title']}]]"


def cls_link(c):
    return f"[[classes/{c.lower()}|{c}]]"


# ---------------------------------------------------------------- pages
PAGES = {}
def page(slug, title, group, md, icon=None):
    PAGES[slug] = dict(title=title, group=group, md=md, icon=icon)


for f in F:
    mem = sorted((BY[m] for m in f["members"]), key=lambda r: (r["level"], r["name"], r["id"]))
    sims = sorted((sim(a, b) for a, b in combinations(f["members"], 2)), reverse=True)
    simtxt = f"{sims[0]:.2f}" if len(sims) == 1 else f"{sims[-1]:.2f}–{sims[0]:.2f}"
    rows = ["| Spell | Lv | School | Type | Cost | Damage | Save / Attack | Classes |",
            "|---|---|---|---|---|---|---|---|"]
    for r in mem:
        kids = f" *(+{len(r['children'])} variants)*" if r["children"] else ""
        rows.append(f"| {sp_name(r)}{kids} | {lvl(r)} | {r['school']} | {r['stype']} | "
                    f"{fmt_cost(r['use_costs'])} | {fmt_damage(r)} | {fmt_save(r)} | "
                    f"{', '.join(cls_link(c) for c in r['classes'])} |")
    md = f"""# <span class="femoji">{f['icon']}</span> {f['title']}

<span class="tier tier-{f['tier']}">{TIER_LABEL[f['tier']]}</span> · {len(mem)} spells · mechanical similarity {simtxt}

{chr(10).join(rows)}

**Shared skeleton.** {f['shared']}

**What varies.** {f['varies']}

**Design read.** {f['read']}

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]
"""
    page(f"families/{f['slug']}", f["title"], "Families · " + TIER_LABEL[f["tier"]] + "s",
         md, icon=f["icon"])

# containers page
crow = ["| Container | Lv | Variant axis | Variants |", "|---|---|---|---|"]
for r in CONTAINERS:
    kids = [BY[k] for k in r["children"] if k in BY]
    kn = ", ".join(k["name"].replace(r["name"] + ": ", "") for k in kids[:8])
    if len(kids) > 8:
        kn += f", … ({len(kids)} total)"
    axis = CONTAINER_AXIS.get(r["name"], "")
    crow.append(f"| {sp_name(r)} | {lvl(r)} | {axis} | {kn} |")

page("containers", "Container Spells", "Start", f"""# <span class="femoji">📦</span> Container Spells

Larian's answer to the reskin: make it a **feature**. A container spell is one spell whose cast button opens a menu of variant child spells — **{len(CONTAINERS)} containers wrap {N_CHILDREN} variant spells**, every child a separate `SpellData` entry inheriting from its parent.

Where tabletop publishes Chromatic Orb as one paragraph with a damage-type clause, BG3 ships **six sibling entries** differing in one damage row. Where the SRD's [[families/smites|smites]] are seven spells, two of them here are containers *again* (melee/ranged) — reskins inside reskins.

{chr(10).join(crow)}

The variant axes tell the design story: **damage type** (Chromatic Orb, Elemental Weapon, Glyph, Protection), **ability** (Hex, Enhance Ability — six children each, one per ability score), **weapon form** (Spiritual Weapon's six cosmetic weapons), and pure presentation (Disguise Self's 32 race/build/gender bodies — one mechanical effect, thirty-two costumes).

Back to [[overview|Overview]] · [[findings|The Identical-Spell List]]
""", icon="📦")

# class pages
def class_spells(c):
    return sorted((r for r in DPOP if c in r["classes"]), key=lambda r: (r["level"], r["name"]))

names_of = {c: {r["name"] for r in class_spells(c)} for c in CLASSES}
for c in CLASSES:
    lst = class_spells(c)
    acts = sorted((r for r in ACTIONS if c in r["classes"]), key=lambda r: (r["level"], r["name"]))
    in_fam = [r for r in lst if r["id"] in FAMILY_OF or any(
        x["id"] in FAMILY_OF for x in POP if x["name"] == r["name"] and x["level"] == r["level"])]
    ov = sorted(((100 * len(names_of[c] & names_of[b]) / len(names_of[c]), b)
                 for b in CLASSES if b != c and names_of[c]), reverse=True)[:3]
    ovtxt = ", ".join(f"**{p:.0f}%** with {cls_link(b)}" for p, b in ov)
    rows = ["| Lv | Spell | School | Family | Also on |", "|---|---|---|---|---|"]
    for r in lst:
        fm = FAMILY_OF.get(r["id"])
        if not fm:
            for x in POP:
                if x["name"] == r["name"] and x["level"] == r["level"] and x["id"] in FAMILY_OF:
                    fm = FAMILY_OF[x["id"]]
                    break
        fl = fam_link(fm) if fm else ("📦 [[containers|container]]" if r["children"] else "—")
        others = [x for x in r["classes"] if x != c]
        also = ", ".join(cls_link(o) for o in others) if others else "*(exclusive)*"
        rows.append(f"| {lvl(r)} | {sp_name(r)} | {r['school']} | {fl} | {also} |")
    amd = ""
    if acts:
        arows = ["| Action | Source class | Cost |", "|---|---|---|"]
        seen = set()
        for r in acts:
            if r["name"] in seen:
                continue
            seen.add(r["name"])
            arows.append(f"| {sp_name(r)} | {c} | {fmt_cost(r['use_costs'])} |")
        amd = f"\n## Class actions\n\nAbilities implemented in the same `SpellData` system but flagged as non-spells ({len(seen)}):\n\n" + "\n".join(arows) + "\n"
    md = f"""# {c} Spell List (BG3)

**{len(lst)} spells** reachable through {c} progressions · **{len(in_fam)}** in an identified family ({100*len(in_fam)/max(1,len(lst)):.0f}%)

List overlap: {ovtxt}.

{chr(10).join(rows)}
{amd}
Back to [[overview|Overview]] · [[findings|The Identical-Spell List]]
"""
    page(f"classes/{c.lower()}", c, "Classes", md)

# findings
fam_rows = ["| Family | Tier | Spells | Peak mechanics | What actually differs |", "|---|---|---|---|---|"]
for f in sorted(F, key=lambda f: ([CLONE, TEMPLATE, ENGINE].index(f["tier"]), -len(f["members"]))):
    peak = max(sim(a, b) for a, b in combinations(f["members"], 2))
    names = ", ".join(sorted({BY[m]["name"] for m in f["members"]}))
    fam_rows.append(f"| {fam_link(f)} | <span class=\"tier tier-{f['tier']}\">{TIER_LABEL[f['tier']]}</span> | {names} | {peak:.2f} | {f['differs']} |")

prow = ["| Score | Mechanics | Description | Spell A | Spell B |", "|---|---|---|---|---|"]
with open("bg3_similar_pairs.csv", encoding="utf-8") as fh:
    rd = csvlib.reader(fh)
    next(rd)
    for i, row in enumerate(rd):
        if i >= 20:
            break
        prow.append(f"| `{row[0]}` | `{row[1]}` | `{row[2]}` | {row[3]} (L{row[4]}) | {row[5]} (L{row[6]}) |")

n_fam = len({BY[m]["name"] for f in F for m in f["members"]})
page("findings", "The Identical-Spell List", "Start", f"""# The Identical-Spell List

Which Baldur's Gate 3 spells are mostly the same spell. Of the **{len(DEDUP)} distinct spells** reachable through class progressions, **{n_fam} fall into {len(F)} families** — and that's *before* counting Larian's own admission: the [[containers|{len(CONTAINERS)} container spells]] whose {N_CHILDREN} variant children are reskins by design.

- <span class="tier tier-clone">Verbatim clone</span> — same mechanics, nouns swapped (or literally the same entry duplicated).
- <span class="tier tier-template">Shared template</span> — same structure, parameters differ.
- <span class="tier tier-engine">Shared engine</span> — same underlying subsystem in different clothes.

## All families

{chr(10).join(fam_rows)}

## Top measured pairs

Score = 0.6 × masked mechanical-signature similarity + 0.4 × masked description similarity ([[methodology|how]]). The mechanics column is the strong signal — BG3 descriptions are short flavor text.

{chr(10).join(prow)}

The `1.000` rows are not measurement artifacts — Shield genuinely exists three times, once per class ([[families/duplicate-skus|the Duplicate SKUs]]).
""")

# methodology
page("methodology", "Methodology", "Start", f"""# Methodology

**Source.** A locally owned Baldur's Gate 3 install (Patch 8). Everything is read from the game's own data: `SpellData` stat entries from `Shared`/`Gustav`/`GustavX` paks (parsed with `using`-inheritance resolved), display names and descriptions from `english.loca` (232,878 strings), class attribution from `SpellLists.lsx` + `Progressions.lsx` (spell lists referenced by class and subclass progressions), and icons from the controller-UI DDS assets. All content © Larian Studios & Wizards of the Coast, used for private research reference.

**Population.** {len(recs)} spell-like records are reachable from class progressions. After collapsing upcast variants and container children and filtering to entries flagged `IsSpell`, **{len(POP)} root spell entries** remain ({len(DEDUP)} distinct spells after merging duplicate SKUs). Non-spell class actions (Channel Divinity, manoeuvres, ki abilities — implemented in the same system) are listed on class pages but excluded from family analysis.

**Similarity.** Each spell gets a *mechanical signature* — its stat fields (`SpellRoll`, `SpellSuccess`, `SpellProperties`, radii, costs, flags…) — and its description text. Both are masked (damage types, elements, ability names, dice, numbers, GUIDs → tokens), then compared per pair with token-level sequence matching. Score = 0.6 × signature + 0.4 × description. High-signature/low-description pairs (Wall of Fire vs. Wall of Ice: 0.97 vs. 0.33) are exactly the reskins this hunts.

**The upcast clone farm.** BG3 implements upcasting by *cloning entries*: casting Fireball from a 4th-level slot uses `Projectile_Fireball_4`, a child entry inheriting the base and overriding one line. The stats database holds **4,614 SpellData entries, of which 1,012 (22%) are these numbered upcast clones** — the game's own data model treats a higher slot as a reskin of the spell.

**Known limits.** Item-granted spells, monster-only abilities, and hireling oddities are out of scope (population = class-progression-reachable). Subclass grants attribute to their parent class. BG3 renames tabletop spells freely (Bone Chill = Chill Touch, Grant Flight = Fly, Enhance Leap = Jump); families use BG3 names.

**Reproduce.** `bg3pak.py` reads the LSPK archives; `extract_bg3_data.py` + `bg3_dataset.py` build `bg3_spells.json`; `bg3_analyze.py` scores pairs; `build_bg3_codex.py` renders this codex. The tabletop companion codex covers the same analysis for the D&D 5e SRD.
""")

# overview
mat = ["| ↓ list · shared with → | " + " | ".join(cls_link(c) for c in CLASSES) + " |",
       "|---|" + "---|" * len(CLASSES)]
for a in CLASSES:
    cells = []
    for b in CLASSES:
        if a == b:
            cells.append("—")
        elif not names_of[a]:
            cells.append("")
        else:
            cells.append(f"{100 * len(names_of[a] & names_of[b]) / len(names_of[a]):.0f}%")
    mat.append(f"| {cls_link(a)} ({len(names_of[a])}) | " + " | ".join(cells) + " |")

share = defaultdict(list)
for r in DPOP:
    share[len(r["classes"])].append(r["name"])
top_shared = sorted(share[max(share)])
slots = sum(len(r["classes"]) for r in DPOP)

page("overview", "Overview", "Start", f"""# How Homogeneous Are Baldur's Gate 3 Spells?

The companion codex to the tabletop study: the same homogeneity analysis, run on **Baldur's Gate 3's actual game data** — every spell reachable through class progressions, read straight from the install's pak files. The result: the video game is *more* homogeneous than the book, and honest about it.

## Axis 1 — the same spell, on many class lists

{len(DEDUP)} distinct spells fill {slots} class-list slots ({slots/len(DEDUP):.1f} lists per spell). The most-shared spells sit on {max(share)} of 11 lists: {", ".join(top_shared[:4])}{"…" if len(top_shared) > 4 else ""}. Bard's Magical Secrets and the half-caster subclasses (Eldritch Knight, Arcane Trickster) import other classes' lists wholesale:

{chr(10).join(mat)}

## Axis 2 — different spells, same design

**{n_fam} of {len(DEDUP)} spells sit in {len(F)} template families** — see [[findings|The Identical-Spell List]]. Beyond the tabletop-inherited families, BG3 adds four homogenizers of its own:

- **[[containers|Container spells]]** — {len(CONTAINERS)} spells whose cast button opens a menu of {N_CHILDREN} variant children. The reskin as a shipped feature.
- **[[families/duplicate-skus|Duplicate SKUs]]** — Shield exists three times in the data, once per class that learns it. Similarity: 1.000.
- **[[families/surfaces|The surface engine]]** — Larian rebuilt tabletop's area spells on one ground-surface system; ten spells measure 0.88–0.96 on mechanics.
- **The upcast clone farm** — 22% of the entire spell database is numbered upcast copies ([[methodology|Methodology]]).

## Browse

- **Classes:** {" · ".join(cls_link(c) for c in CLASSES)}
- **The list:** [[findings|The Identical-Spell List]] · **Containers:** [[containers|Container Spells]]
- **Every spell, tagged:** [[spells|All Spells, Tagged]] · **How:** [[methodology|Methodology]]
""")

# all-spells table + csv
from purpose_defs import load_purposes, PEMOJI as PUR_EMOJI, PLABEL as PUR_LABEL
BG3_PUR = load_purposes("Baldur's Gate 3")

def pur_txt(name):
    p = BG3_PUR.get(name.lower())
    return f'{PUR_EMOJI[p]} {PUR_LABEL[p]}' if p else ""

trow = ["| Lv | Spell | School | Family | Tier | Purpose | Classes |", "|---|---|---|---|---|---|---|"]
with open("bg3_spells_tagged.csv", "w", newline="", encoding="utf-8") as fh:
    w = csvlib.writer(fh)
    w.writerow(["spell", "level", "school", "type", "family", "tier", "purpose", "container_variants", "classes"])
    for r in sorted(DPOP, key=lambda r: (r["level"], r["name"])):
        fm = FAMILY_OF.get(r["id"]) or next(
            (FAMILY_OF[x["id"]] for x in POP
             if x["name"] == r["name"] and x["level"] == r["level"] and x["id"] in FAMILY_OF), None)
        w.writerow([r["name"], r["level"], r["school"], r["stype"],
                    fm["title"] if fm else "", TIER_LABEL[fm["tier"]] if fm else "",
                    PUR_LABEL.get(BG3_PUR.get(r["name"].lower(), ""), ""),
                    len(r["children"]) or "", "/".join(r["classes"])])
        fl = fam_link(fm) if fm else ("📦 [[containers|container]]" if r["children"] else "—")
        tt = f'<span class="tier tier-{fm["tier"]}">{TIER_LABEL[fm["tier"]]}</span>' if fm else ""
        trow.append(f"| {lvl(r)} | {sp_name(r)} | {r['school']} | {fl} | {tt} | {pur_txt(r['name'])} | "
                    f"{', '.join(cls_link(c) for c in r['classes'])} |")

page("spells", "All Spells, Tagged", "Start", f"""# All Spells, Tagged by Family

All **{len(DEDUP)} distinct class-list spells** in Baldur's Gate 3, with family tags. Containers are marked 📦 — their variant children are catalogued on [[containers|Container Spells]].

{chr(10).join(trow)}

Back to [[overview|Overview]] · [[findings|The Identical-Spell List]]
""")

# ---------------------------------------------------------------- backlinks, md out
WIKILINK = re.compile(r"\[\[([a-zA-Z0-9\-/]+)(?:\|([^\]]+))?\]\]")
links_to = defaultdict(set)
for slug, p in PAGES.items():
    for m in WIKILINK.finditer(p["md"]):
        if m.group(1) in PAGES and m.group(1) != slug:
            links_to[m.group(1)].add(slug)
for slug, p in PAGES.items():
    bl = sorted(links_to.get(slug, []))
    if bl:
        p["md"] += "\n---\n*Linked from: " + " · ".join(f"[[{b}|{PAGES[b]['title']}]]" for b in bl) + "*\n"

os.makedirs("bg3_wiki/families", exist_ok=True)
os.makedirs("bg3_wiki/classes", exist_ok=True)
for slug, p in PAGES.items():
    with open(os.path.join("bg3_wiki", slug + ".md"), "w", encoding="utf-8") as fh:
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
        title = PAGES.get(tgt, {}).get("title", tgt)
        return f'<a class="wl" href="#/{tgt}">{label or title}</a>'
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


PAGES_HTML = {slug: md_to_html(p["md"]) for slug, p in PAGES.items()}

NAV = [
    ("Start", ["overview", "findings", "containers", "spells", "methodology"]),
    ("Families · Clones", [f"families/{f['slug']}" for f in F if f["tier"] == CLONE]),
    ("Families · Templates", [f"families/{f['slug']}" for f in F if f["tier"] == TEMPLATE]),
    ("Families · Engines", [f"families/{f['slug']}" for f in F if f["tier"] == ENGINE]),
    ("Class Spell Lists", [f"classes/{c.lower()}" for c in CLASSES]),
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

HTML = """<title>The Larian Codex</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Alegreya:ital,wght@0,400;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --bg:#16141B; --panel:#1D1A23; --ink:#DCD3BF; --muted:#9A907B;
  --line:#322D3B; --accent:#D4AF5E; --accent-ink:#E3C377; --accent-bg:#D4AF5E1A;
  --clone:#E58A9B; --clone-bg:#E58A9B1A; --template:#DBA84F; --template-bg:#DBA84F1A;
  --engine:#72C4AE; --engine-bg:#72C4AE1A; --code-bg:#262230;
}
@media (prefers-color-scheme: light){
  :root:not([data-theme="dark"]){
    --bg:#F1EBDD; --panel:#E7DFCC; --ink:#2A2117; --muted:#6B5E49;
    --line:#D6CBB2; --accent:#8A6A1F; --accent-ink:#6E5314; --accent-bg:#8A6A1F14;
    --clone:#A23B4E; --clone-bg:#A23B4E14; --template:#8A6215; --template-bg:#8A621514;
    --engine:#2E7D6E; --engine-bg:#2E7D6E14; --code-bg:#E2D9C2;
  }
}
:root[data-theme="light"]{
  --bg:#F1EBDD; --panel:#E7DFCC; --ink:#2A2117; --muted:#6B5E49;
  --line:#D6CBB2; --accent:#8A6A1F; --accent-ink:#6E5314; --accent-bg:#8A6A1F14;
  --clone:#A23B4E; --clone-bg:#A23B4E14; --template:#8A6215; --template-bg:#8A621514;
  --engine:#2E7D6E; --engine-bg:#2E7D6E14; --code-bg:#E2D9C2;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:400 16.5px/1.62 Alegreya,Georgia,serif}
a{color:var(--accent);text-decoration:none}
a:hover{color:var(--accent-ink)}
.layout{display:flex;min-height:100vh}
nav{width:256px;flex:0 0 256px;background:var(--panel);border-right:1px solid var(--line);
  padding:20px 0 40px;position:sticky;top:0;height:100vh;overflow-y:auto}
.brand{font-family:Cinzel,Georgia,serif;font-weight:700;font-size:17px;letter-spacing:.04em;
  padding:6px 20px 14px;border-bottom:1px solid var(--line);margin-bottom:10px;color:var(--accent-ink)}
.brand small{display:block;font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:10.5px;
  font-weight:400;color:var(--muted);letter-spacing:.04em;margin-top:3px;text-transform:none}
.navlabel{font:500 10.5px/1 "IBM Plex Mono",ui-monospace,monospace;color:var(--muted);
  text-transform:uppercase;letter-spacing:.12em;padding:14px 20px 6px}
nav a{display:block;padding:4px 20px;font-size:14.5px;color:var(--ink)}
nav a:hover{background:var(--accent-bg)}
nav a.on{color:var(--accent-ink);background:var(--accent-bg);box-shadow:inset 3px 0 0 var(--accent)}
main{flex:1;min-width:0;padding:36px 44px 90px}
article{max-width:76ch;margin:0 auto}
.crumb{font:400 12px/1 "IBM Plex Mono",ui-monospace,monospace;color:var(--muted);
  letter-spacing:.03em;margin-bottom:22px}
h1{font-family:Cinzel,Georgia,serif;font-weight:600;font-size:28px;line-height:1.2;
  text-wrap:balance;margin:0 0 16px;color:var(--accent-ink)}
h2{font-family:Alegreya,Georgia,serif;font-weight:700;font-size:21px;margin:34px 0 10px}
p{margin:0 0 14px}
ul{margin:0 0 14px;padding-left:22px}
li{margin-bottom:6px}
hr{border:0;border-top:1px solid var(--line);margin:28px 0 14px}
code{font:500 13px "IBM Plex Mono",ui-monospace,monospace;background:var(--code-bg);
  padding:1px 5px;border-radius:3px;font-variant-numeric:tabular-nums}
.wl{border-bottom:1px dotted var(--accent)}
.wl:hover{background:var(--accent-bg)}
.tw{overflow-x:auto;margin:16px 0 20px;border:1px solid var(--line);border-radius:4px}
table{border-collapse:collapse;width:100%;font-size:13.5px;line-height:1.45;
  font-family:Alegreya,Georgia,serif}
th{font:500 11px "IBM Plex Mono",ui-monospace,monospace;text-transform:uppercase;
  letter-spacing:.07em;color:var(--muted);text-align:left;padding:8px 10px;
  border-bottom:1px solid var(--line);background:var(--panel);white-space:nowrap}
td{padding:6px 10px;border-bottom:1px solid var(--line);vertical-align:top;
  font-variant-numeric:tabular-nums}
tr:last-child td{border-bottom:0}
.tier{font:500 10.5px "IBM Plex Mono",ui-monospace,monospace;text-transform:uppercase;
  letter-spacing:.08em;padding:2px 7px;border-radius:3px;white-space:nowrap}
.tier-clone{color:var(--clone);background:var(--clone-bg)}
.tier-template{color:var(--template);background:var(--template-bg)}
.tier-engine{color:var(--engine);background:var(--engine-bg)}
.sic{width:22px;height:22px;vertical-align:-6px;margin-right:5px;border-radius:4px}
.femoji{font-family:"Segoe UI Emoji","Apple Color Emoji","Noto Color Emoji",sans-serif;font-style:normal}
h1 .femoji{font-size:24px;margin-right:2px}
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
footer{max-width:76ch;margin:50px auto 0;padding-top:14px;border-top:1px solid var(--line);
  font-size:12.5px;color:var(--muted)}
</style>
<button id="menu" aria-label="Menu">☰ pages</button>
<div class="layout">
<nav id="nav">
<div class="brand">The Larian Codex<small>baldur's gate 3 · patch 8 · __NSPELLS__ spells</small></div>
__NAV__
</nav>
<main>
<div class="crumb" id="crumb"></div>
<article id="art"></article>
<footer>All spell data and icons from a locally owned Baldur's Gate 3 install —
© Larian Studios &amp; Wizards of the Coast; private research reference.
Companion to the tabletop Reskin Codex.</footer>
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
  crumb.textContent = 'larian codex' + (parts.length>1 ? ' / '+parts[0] : '') + ' / ' + PAGES[slug].title.toLowerCase();
  document.querySelectorAll('nav a[data-slug]').forEach(a=>a.classList.toggle('on', a.dataset.slug===slug));
  nav.classList.remove('open');
  window.scrollTo(0,0);
}
window.addEventListener('hashchange', render);
document.getElementById('menu').addEventListener('click',()=>nav.classList.toggle('open'));
render();
</script>
"""
HTML = (HTML.replace("__NAV__", nav_html)
        .replace("__NSPELLS__", str(len(DEDUP)))
        .replace("__PAGES__", json.dumps({s: {"title": p["title"], "html": PAGES_HTML[s]}
                                          for s, p in PAGES.items()}))
        .replace("__BG3__", json.dumps(BG3_URIS)))
with open("bg3_codex.html", "w", encoding="utf-8") as fh:
    fh.write(HTML)

print(f"{len(PAGES)} pages; {len(DEDUP)} distinct spells; {n_fam} in {len(F)} families; "
      f"{len(CONTAINERS)} containers / {N_CHILDREN} children")
print(f"bg3_codex.html: {os.path.getsize('bg3_codex.html')/1024:.0f} KB")

"""Classify every ability in all three datasets by PURPOSE (functional role).

Order of attack: manual overrides > family mapping > keyword rules > fallback.
Outputs purpose_tagged.csv (one row per game+ability) and a summary matrix.
"""
import csv
import json
import re
from collections import defaultdict

# ---------------------------------------------------------------- taxonomy
from purpose_defs import PURPOSES
PKEYS = [p[0] for p in PURPOSES]

# ------------------------------------------------- family -> purpose (all games)
FAM_PURPOSE = {
    # SRD
    "cure": "heal", "dominate": "disable", "conjure-table": "create",
    "conjure-single": "create", "hold": "disable", "bane-bless": "offboost",
    "blast": "damage", "suggestion": "disable", "image": "stealth",
    "hp-pool": "disable", "undead": "create", "locate": "info", "detect": "info",
    "invisibility": "stealth", "disguise-seeming": "stealth", "polymorph": "disable",
    "attack-cantrips": "damage", "phantom-armory": "create", "dispel": "negation",
    "darkness-daylight": "zone", "speak-with": "info", "protection": "defboost",
    "touch-buffs": "mobility", "guidance-resistance": "offboost",
    # BG3
    "duplicate-skus": "defboost", "charm": "disable", "walls": "zone",
    "surfaces": "zone", "smites": "damage", "teleports": "mobility",
    "conjure": "create", "cleanse": "negation", "d4-riders": "offboost",
    "ac-wardrobe": "defboost", "hp-pool-bg3": "disable",
    # WoW
    "tracking": "info", "conjured": "provision", "heals": "heal",
    "group-ladder": "offboost", "blessings": "offboost", "auras": "defboost",
    "aspects": "roleshift", "stings": "degrade", "shocks": "damage",
    "totems": "create", "curses": "degrade", "protection-wow": "defboost",
    "bolts": "damage", "dots": "damage", "summons": "create", "rez": "heal",
    "cat-is-rogue": "damage", "interrupts": "negation", "fears": "disable",
    "cleanses": "negation", "mirror": "defboost", "seals": "offboost",
    "polymorph-wow": "disable", "poisons": "degrade",
}

# ------------------------------------------------- keyword rules (ordered)
RULES = [
    ("heal",     r"regain(s)? (\d+|[^.]*hit point)|heal(s|ing)? (a|the|your|all|nearby)|restor\w+ (health|\d+ hit|life)|returns? the spirit|revive|resurrect|rebirth|brought back to life|cure wounds"),
    ("remove",   r"banish|turn(s|ed)? undead|sent to another plane|cease(s)? to exist|exile"),
    ("negation", r"counter(s|spell)|dispel|remov\w+ (\d+ )?(beneficial )?(curse|poison|disease|magic|effect)|cure(s)? (poison|disease)|abolish|purif|purge|cleanse|interrupt|neutraliz"),
    ("threat",   r"taunt|threat (is |gets )?reduc|less likely to attack|attack (you|the caster) instead|mocking|feign death|aggro"),
    ("zone",     r"wall of|creates? (a )?(surface|cloud|area|zone|field)|fills? (the|an) area|persists? on the ground|barrier|web\b|grease|entangl"),
    ("create",   r"summon(s|ing)?|conjure(s)? (an? |forth )?(creature|elemental|fey|celestial|spirit|servant|familiar|steed|mass of)|animate(s)? (the )?dead|raise(s)? (a )?(skeleton|zombie|corpse)|creates? an? (spectral|floating|guardian)|familiar"),
    ("provision",r"create(s)? (food|water|an? healthstone|an? soulstone|an? firestone|an? spellstone)|conjure(s)? (food|water|mana|refreshment|a mana)|manufactur"),
    ("disable",  r"stun(s|ned)?|paraly|incapacitat|unconscious|sleep(s)?\b|charm(s|ed)?\b|fear(s)?\b|flee(s)?\b|polymorph|hex\b|frozen in place|cannot (move|act|attack)|root(s|ed)?\b|immobiliz|silenc(e|ed|ing)|blind(s|ed)?\b|dazed?|sap\b|gouge|knock(s|ed)? (out|down|back)|slow(s|ed|ing)?\b|reduc\w+ (its |the )?(movement|speed)|prone|restrain|held\b|hibernat"),
    ("degrade",  r"reduc\w+ (strength|agility|stamina|intellect|spirit|armor|attack power|damage (done|dealt))|weaken|vulnerab|takes? (more|increased|additional) damage|lowers?\b|drain(s|ing)? (strength|stat)|disadvantage on (attack|ability|saving)"),
    ("mobility", r"teleport|blink|misty step|portal|speed (is )?increas|movement speed|fly(ing)? speed|dash|sprint|charge(s)? (to|at)|leap|jump(s|ing)?\b|levitat|feather fall|water walk|far ?step"),
    ("stealth",  r"invisib|stealth|prowl|camouflag|disguise|illusion|illusory|duplicate|mirror image|blur\b|mislead|vanish|shadowmeld|hide(s)?\b|undetect"),
    ("info",     r"detect(s)?\b|track(s|ing)?\b|sense(s)?\b|reveal(s)?|scry|locate|identify|true seeing|see invisible|darkvision|far ?sight|eagle eye|beast lore|mind vision|read (the )?(thoughts|mind)|comprehend|divination|augury|commune"),
    ("offboost",r"attack (rolls?|power) (is |are )?increas|adds? .* to (attack|damage)|bonus to (attack|damage|hit)|increas\w+ (attack power|damage|strength|agility|critical|spell power|haste)|advantage on attack|next attack|empowers?"),
    ("defboost", r"armor (is )?increas|increas\w+ (armor|defense|stamina|resistance|block)|absorb(s|ing)? damage|damage (is )?reduc|resistance to|shield(s|ed)?\b|protect(s|ion|ed)?\b|ward(s)?\b|deflect|barkskin|stoneskin|damage taken.*reduc"),
    ("roleshift",r"(bear|cat|travel|aquatic|moonkin|dire bear) form|shapeshift|stance\b|aspect of|presence\b|transform(s)? (yourself|into)|metamorph|wild shape|only one .* active"),
    ("damage",   r"damage\b|DealDamage|deals? \d|d\d+ (fire|cold|frost|shadow|nature|holy|arcane|force|necrotic|radiant|thunder|lightning|acid|poison|psychic|slashing|piercing|bludgeoning)"),
]

def classify(name, desc, fam_slug, overrides):
    key = name.lower()
    if key in overrides:
        return overrides[key], "override"
    if fam_slug and fam_slug in FAM_PURPOSE:
        return FAM_PURPOSE[fam_slug], "family"
    text = (name + " " + desc).lower()
    for purpose, pat in RULES:
        if re.search(pat, text):
            return purpose, "rule"
    return "utility", "fallback"

OVERRIDES = {
    # cross-game judgment calls
    "magic missile": "damage", "eldritch blast": "damage", "spiritual weapon": "create",
    "counterspell": "negation", "dispel magic": "negation", "silence": "disable",
    "banishment": "remove", "turn undead": "remove", "exorcism": "damage",
    "hearthstone": "mobility", "astral recall": "mobility", "word of recall": "mobility",
    "light": "utility", "dancing lights": "utility", "prestidigitation": "utility",
    "goodberry": "provision", "leomund's tiny hut": "defboost",
    "life tap": "provision", "dark pact": "provision", "evocation": "provision",
    "soulstone": "provision", "first aid": "heal",
    "lay on hands": "heal", "power word: shield": "defboost",
    "fade": "threat", "cower": "threat", "feint": "threat", "growl": "threat",
    "taunt": "threat", "challenging shout": "threat", "challenging roar": "threat",
    "mocking blow": "threat", "blessing of salvation": "threat",
    "greater blessing of salvation": "threat",
    "battle stance": "roleshift", "defensive stance": "roleshift",
    "berserker stance": "roleshift", "bear form": "roleshift", "cat form": "roleshift",
    "dire bear form": "roleshift", "travel form": "roleshift", "aquatic form": "roleshift",
    "eye of kilrogg": "info", "farsight": "info", "mind vision": "info",
    "ritual of summoning": "mobility",
    "polymorph": "disable", "sleep": "disable", "fear": "disable",
    "resurrection": "heal", "redemption": "heal", "ancestral spirit": "heal",
    "rebirth": "heal", "revivify": "heal", "raise dead": "heal", "reincarnate": "heal",
    # QA round
    "web": "zone", "blink": "mobility", "slow fall": "mobility",
    "shillelagh": "offboost", "rockbiter weapon": "offboost",
    "flametongue weapon": "offboost", "frostbrand weapon": "offboost",
    "windfury weapon": "offboost", "evasion": "defboost", "spare the dying": "heal",
    "frenzied regeneration": "heal", "judgement": "damage", "siphon life": "damage",
    "purge": "negation", "glibness": "stealth", "alarm": "info",
    "health funnel": "heal", "compelled duel": "threat", "shadow blade": "create",
    "crusader's mantle": "offboost", "sunder armor": "degrade",
    "demoralizing shout": "degrade", "tiny hut": "defboost",
    "ghost wolf": "mobility", "travel form": "mobility", "aquatic form": "mobility",
    "mind control": "disable", "auto shot": "damage", "disarm": "disable",
    "aid": "defboost", "haste": "offboost", "blessing of light": "defboost",
    "greater blessing of light": "defboost",
}

# ---------------------------------------------------------------- load games
rows = []

# SRD
import analyze_spells as A
srd = json.load(open("spells_2014.json", encoding="utf-8"))
fam_of_srd = {}
with open("spells_tagged_by_family.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        fam_of_srd[r["spell"].lower()] = r["family"]
# family title -> slug-ish key used in FAM_PURPOSE (SRD titles differ; map by title)
SRD_TITLE_TO_KEY = {
    "The Cure Family": "cure", "The Dominate Chain": "dominate",
    "Conjure by Menu": "conjure-table", "Conjure a Champion": "conjure-single",
    "The Hold Pair": "hold", "Bane & Bless": "bane-bless",
    "The Elemental Blast Template": "blast", "The Suggestion Pair": "suggestion",
    "The Image Ladder": "image", "The Hit-Point Pool Engine": "hp-pool",
    "The Undead Workshop": "undead", "The Locate Series": "locate",
    "The Detect Series": "detect", "The Invisibility Ladder": "invisibility",
    "The Disguise Ladder": "disguise-seeming", "The Polymorph Ladder": "polymorph",
    "The Damage Cantrip Engine": "attack-cantrips", "The Phantom Armory": "phantom-armory",
    "The Dispel Engine": "dispel", "Darkness & Daylight": "darkness-daylight",
    "The Speak-With Series": "speak-with", "The Protection Series": "protection",
    "The Touch-Buff Skeleton": "touch-buffs", "Guidance & Resistance": "guidance-resistance",
}
for s in srd:
    fam_title = fam_of_srd.get(s["name"].lower(), "")
    fam_key = SRD_TITLE_TO_KEY.get(fam_title, "")
    p, how = classify(s["name"], A.spell_text(s), fam_key, OVERRIDES)
    rows.append(dict(game="D&D 5e SRD", name=s["name"], purpose=p, how=how,
                     family=fam_title))

# BG3
import build_bg3_codex as C
for r in C.DPOP:
    fm = C.FAMILY_OF.get(r["id"])
    if not fm:
        for x in C.POP:
            if x["name"] == r["name"] and x["level"] == r["level"] and x["id"] in C.FAMILY_OF:
                fm = C.FAMILY_OF[x["id"]]
                break
    slug = fm["slug"] if fm else ""
    slug = {"hp-pool": "hp-pool-bg3"}.get(slug, slug) if slug == "hp-pool" else slug
    desc = r["desc"] + " " + r["tooltip_damage"] + " " + r["spell_success"]
    p, how = classify(r["name"], desc, slug, OVERRIDES)
    rows.append(dict(game="Baldur's Gate 3", name=r["name"], purpose=p, how=how,
                     family=fm["title"] if fm else ""))

# WoW
wow = json.load(open("wow_spells.json", encoding="utf-8"))
import importlib
bw = importlib.import_module("build_wow_codex")
WOW_FAM_OF = {}
for f in bw.F:
    for m in f["members"]:
        WOW_FAM_OF[m] = f
for r in wow:
    fm = WOW_FAM_OF.get(r["id"])
    slug = fm["slug"] if fm else ""
    slug = {"protection": "protection-wow", "polymorph": "polymorph-wow"}.get(slug, slug)
    p, how = classify(r["name"], r["desc"], slug, OVERRIDES)
    rows.append(dict(game="WoW Classic", name=r["name"], purpose=p, how=how,
                     family=fm["title"] if fm else ""))

# ---------------------------------------------------------------- output
with open("purpose_tagged.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["game", "ability", "purpose", "assigned_by", "family"])
    for r in rows:
        w.writerow([r["game"], r["name"], r["purpose"], r["how"], r["family"]])

games = ["D&D 5e SRD", "Baldur's Gate 3", "WoW Classic"]
mat = defaultdict(lambda: defaultdict(int))
tot = defaultdict(int)
for r in rows:
    mat[r["purpose"]][r["game"]] += 1
    tot[r["game"]] += 1

print(f"{'purpose':<22}" + "".join(f"{g:>18}" for g in games))
for pk, label, user, _ in PURPOSES:
    line = f"{label:<22}"
    for g in games:
        n = mat[pk][g]
        line += f"{n:>7} ({100*n/tot[g]:>4.1f}%)"
    print(line + ("   *user" if user else ""))
print(f"{'TOTAL':<22}" + "".join(f"{tot[g]:>18}" for g in games))
how_counts = defaultdict(int)
for r in rows:
    how_counts[r["how"]] += 1
print("assigned by:", dict(how_counts))

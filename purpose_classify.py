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
    # WoW — current function-primary family slugs
    "tracking": "info", "conjured": "provision", "heals": "heal", "hots": "heal",
    "status-boosts": "offboost", "aspects": "roleshift", "totems": "create",
    "curses": "degrade", "protection-wow": "defboost", "bolts": "damage",
    "dots": "damage", "aoe-damage": "damage", "melee-enhance": "damage",
    "summons": "create", "rez": "heal", "interrupts": "negation",
    "cleanses": "negation", "seals": "offboost", "cc": "disable",
    "snares": "disable", "travel": "mobility", "teleports": "mobility",
    "concealment": "stealth", "threat": "threat", "forms": "roleshift",
    "siphons": "drain", "shards": "drain", "gap-closers": "mobility",
    "static-shell": "defboost", "fieldcraft": "utility",
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

def classify(name, desc, fam_slug, overrides, effect_p=None):
    """Order: override > curated family > mechanical effect data > tooltip keywords."""
    key = name.lower()
    if key in overrides:
        return overrides[key], "override"
    if fam_slug and fam_slug in FAM_PURPOSE:
        return FAM_PURPOSE[fam_slug], "family"
    if effect_p:
        return effect_p, "effect"
    text = (name + " " + desc).lower()
    for purpose, pat in RULES:
        if re.search(pat, text):
            return purpose, "rule"
    return "utility", "fallback"


# ---------------------------------------------------- effect-data classifiers
# WoW: SpellEffect.db2 — effect types and aura codes are the game's mechanics.
WOW_EFFECT = {1: "damage", 2: "damage", 5: "mobility", 8: "drain", 9: "drain", 10: "heal",
              62: "drain",
              17: "damage", 18: "heal", 24: "provision", 28: "create", 30: "provision",
              31: "damage", 33: "utility", 38: "negation", 50: "create", 56: "create",
              58: "damage", 67: "heal", 68: "negation", 75: "threat", 94: "heal",
              112: "create", 113: "heal", 121: "damage"}
WOW_AURA = {3: "damage", 5: "disable", 7: "disable", 8: "heal", 10: "threat",
            11: "threat", 12: "disable", 15: "defboost", 16: "stealth", 18: "stealth",
            19: "info", 20: "heal", 24: "provision", 25: "disable", 26: "disable",
            27: "disable", 31: "mobility", 32: "mobility", 33: "disable",
            34: "defboost", 36: "roleshift", 39: "defboost", 40: "defboost",
            44: "info", 45: "info", 47: "defboost", 49: "defboost", 53: "damage",
            56: "disable", 69: "defboost", 78: "mobility", 85: "provision",
            99: "offboost"}
WOW_AURA_SIGNED = {9, 13, 22, 29, 79}   # buff if positive, degradation if negative
WOW_PRECEDENCE = ["create", "roleshift", "threat", "heal", "mobility", "disable",
                  "negation", "stealth", "info", "drain", "provision", "damage",
                  "degrade", "offboost", "defboost", "utility"]

# WoW-view remap: the D&D map applied to WoW, with WoW-major purposes broken out
# (resource warfare, companion upkeep) and near-empty D&D purposes culled
# (zone -> nearest fit; Banish / Turn Undead play as disables there).
WOW_OVERRIDES = {
    "mana burn": "drain", "drain life": "drain", "drain mana": "drain",
    "drain soul": "drain", "life tap": "drain", "viper sting": "drain",
    "siphon life": "drain", "cannibalize": "drain",
    "call pet": "companion", "tame beast": "companion", "revive pet": "companion",
    "dismiss pet": "companion", "mend pet": "companion", "feed pet": "companion",
    "beast training": "companion", "eyes of the beast": "companion",
    "beast lore": "companion", "health funnel": "companion",
    "banish": "disable", "turn undead": "disable", "nature's grasp": "disable",
}


def load_wow_effects():
    eff = defaultdict(list)
    with open("wow_SpellEffect.csv", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            try:
                eff[int(row["SpellID"])].append(
                    (int(row["Effect"] or 0), int(row["EffectAura"] or 0),
                     float(row["EffectBasePoints"] or 0)))
            except ValueError:
                continue
    return eff


def wow_effect_purpose(spell_ids, eff_table):
    found = set()
    for sid in spell_ids:
        for effect, aura, bp in eff_table.get(sid, []):
            if effect == 6:   # APPLY_AURA — read the aura code
                if aura in WOW_AURA_SIGNED:
                    found.add("degrade" if bp < 0 else
                              ("defboost" if aura == 22 else "offboost"))
                elif aura in WOW_AURA:
                    found.add(WOW_AURA[aura])
            elif effect in WOW_EFFECT:
                found.add(WOW_EFFECT[effect])
    for p in WOW_PRECEDENCE:
        if p in found:
            return p
    return None


# BG3: the stat functors in SpellSuccess/SpellProperties are the mechanics.
BG3_FUNCTORS = [("create", r"\bSummon\("), ("mobility", r"Teleport\w*\("),
                ("negation", r"RemoveStatus\(|RemoveAura"), ("heal", r"RegainHitPoints\(|Resurrect"),
                ("damage", r"DealDamage\("), ("zone", r"CreateSurface\(|SurfaceChange\(")]


def bg3_effect_purpose(success, props, tooltip):
    t = " ".join([success or "", props or "", tooltip or ""])
    for p, pat in BG3_FUNCTORS:
        if re.search(pat, t):
            return p
    return None


def srd_effect_purpose(s):
    if s.get("damage"):
        return "damage"
    if s.get("heal_at_slot_level"):
        return "heal"
    return None

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
    "stealth": "stealth", "prowl": "stealth",
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
    p, how = classify(s["name"], A.spell_text(s), fam_key, OVERRIDES,
                      effect_p=srd_effect_purpose(s))
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
    p, how = classify(r["name"], desc, slug, OVERRIDES,
                      effect_p=bg3_effect_purpose(r["spell_success"], r["properties"],
                                                  r["tooltip_damage"]))
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
WEFF = load_wow_effects()
WOW_ALL_OVERRIDES = {**OVERRIDES, **WOW_OVERRIDES}
for r in wow:
    fm = WOW_FAM_OF.get(r["id"])
    slug = fm["slug"] if fm else ""
    slug = {"protection": "protection-wow", "polymorph": "polymorph-wow"}.get(slug, slug)
    p, how = classify(r["name"], r["desc"], slug, WOW_ALL_OVERRIDES,
                      effect_p=wow_effect_purpose(r["all_ids"], WEFF))
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

"""Shared purpose-taxonomy definitions + lightweight loader for purpose_tagged.csv."""
import csv
import os

# (key, label, user-requested?, one-line definition)
PURPOSES = [
    ("damage",     "Damage",              True,  "reduce enemy hit points"),
    ("offboost",   "Offense boost",       True,  "make allies hit harder or truer"),
    ("defboost",   "Defense boost",       True,  "make allies harder to hurt"),
    ("negation",   "Negation",            True,  "cancel spells, effects, or afflictions (counter, dispel, cleanse)"),
    ("create",     "Creating entities",   True,  "put a new acting thing on the board (creature, weapon, totem-servant)"),
    ("remove",     "Removing entities",   True,  "take a creature off the board without hp damage (banish, turn, rout)"),
    ("disable",    "Disables",            True,  "deny enemy actions: stun, hold, sleep, fear, root, slow, silence"),
    ("degrade",    "Degradation",         False, "weaken without disabling: stat drains, vulnerability, damage-taken up"),
    ("heal",       "Healing & revival",   False, "restore hit points or life"),
    ("mobility",   "Mobility",            False, "move yourself or allies: teleport, speed, flight, charge"),
    ("zone",       "Zone control",        False, "shape space: walls, surfaces, areas that persist"),
    ("info",       "Information",         False, "learn what you could not see: detect, track, scry, identify"),
    ("stealth",    "Deception & stealth", False, "not being seen, or being seen wrongly: invisibility, illusion, disguise"),
    ("provision",  "Provisioning",        False, "manufacture resources for later: food, gems, stones, scrolls"),
    ("threat",     "Threat control",      False, "edit who enemies attack: taunts, feints, aggro dumps"),
    ("drain",      "Resource warfare",    False, "attack or convert the resource system itself: mana burns, drains, life taps"),
    ("companion",  "Companion upkeep",    False, "manage a persistent companion: call, tame, feed, mend, revive"),
    ("roleshift",  "Role shift",          False, "swap your whole kit: forms, stances, exclusive modes"),
    ("utility",    "Utility & world",     False, "everything that touches the world, not the fight"),
]
PLABEL = {p[0]: p[1] for p in PURPOSES}
PEMOJI = {"damage": "💥", "offboost": "⚔️", "defboost": "🛡️", "negation": "🧯",
          "create": "🧞", "remove": "🕳️", "disable": "⛓️", "degrade": "🩸",
          "heal": "❤️‍🩹", "mobility": "🌀", "zone": "🕸️", "info": "👁️",
          "stealth": "🎭", "provision": "🧺", "threat": "😡", "roleshift": "🐻",
          "drain": "🧛", "companion": "🐕", "utility": "🔧"}
PSHORT = {"damage": "DAMAGE", "offboost": "OFF BOOST", "defboost": "DEF BOOST",
          "negation": "NEGATION", "create": "CREATE", "remove": "REMOVE",
          "disable": "DISABLE", "degrade": "DEGRADE", "heal": "HEALING",
          "mobility": "MOBILITY", "zone": "ZONE", "info": "INFO",
          "stealth": "STEALTH", "provision": "PROVISION", "threat": "THREAT",
          "roleshift": "ROLESHIFT", "drain": "DRAIN", "companion": "COMPANION",
          "utility": "UTILITY"}


def load_purposes(game):
    """ability name (lowercase) -> purpose key, for one game, from purpose_tagged.csv."""
    out = {}
    if not os.path.exists("purpose_tagged.csv"):
        return out
    with open("purpose_tagged.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["game"] == game:
                out[r["ability"].lower()] = r["purpose"]
    return out

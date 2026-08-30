"""Decode local SpellEffect rows into wowhead-vocabulary effect labels for every
ability; merge with the wowhead-pulled subset; validate decoder on the overlap.
Writes wow_effects_labels.json (ability id -> labels)."""
import csv
import json
import re
from collections import defaultdict

EFFECT_NAME = {
    1: "Instakill", 2: "School Damage", 3: "Dummy", 5: "Teleport Units",
    6: None,  # Apply Aura -> use aura name
    7: "Environmental Damage", 8: "Power Drain", 9: "Health Leech", 10: "Heal",
    11: "Bind", 16: "Quest Complete", 17: "Weapon Damage (noschool)",
    18: "Resurrect", 19: "Extra Attacks", 20: "Dodge", 21: "Evade", 22: "Parry",
    23: "Block", 24: "Create Item", 26: "Defense", 27: "Persistent Area Aura",
    28: "Summon", 29: "Leap", 30: "Energize", 31: "Weapon % Damage",
    32: "Trigger Missile", 33: "Open Lock", 35: "Apply Area Aura", 36: "Learn Spell",
    38: "Dispel", 39: "Language", 40: "Dual Wield", 41: "Summon Wild",
    42: "Summon Guardian", 44: "Skill Step", 46: "Spawn", 48: "Stealth",
    49: "Detect", 50: "Trans Door", 53: "Enchant Item", 54: "Enchant Item (temporary)",
    55: "Tame Creature", 56: "Summon Pet", 57: "Learn Pet Spell", 58: "Weapon Damage",
    59: "Open Lock (item)", 60: "Proficiency", 61: "Send Event", 62: "Power Burn",
    63: "Threat", 64: "Trigger Spell", 65: "Health Funnel", 66: "Power Funnel",
    114: "Taunt", 30: "Give Power",
    47: "Trade Skill Window", 71: "Pickpocket", 79: "Sanctuary (drop combat)",
    96: "Charge", 101: "Feed Pet", 167: "Sense Undead", 320: "Summon Trap",
    329: "Resurrect",
    67: "Heal Max Health", 68: "Interrupt Cast", 69: "Distract", 70: "Pull",
    75: "Attack Me", 77: "Script Effect", 80: "Add Combo Points", 83: "Duel",
    85: "Summon Player", 88: "Feed Pet", 89: "Dismiss Pet", 94: "Self Resurrect",
    95: "Skinning", 103: "Reputation", 108: "Dispel Mechanic", 109: "Summon Dead Pet",
    110: "Destroy All Totems", 112: "Summon Demon", 113: "Resurrect (new)",
    118: "Skill", 121: "Normalized Weapon Dmg", 126: "Steal Beneficial Buff",
}
AURA_NAME = {
    1: "Bind Sight", 2: "Mod Possess", 3: "Periodic Damage", 4: "Dummy",
    5: "Mod Confuse", 6: "Mod Charm", 7: "Mod Fear", 8: "Periodic Heal",
    9: "Mod Attack Speed", 10: "Mod Threat", 11: "Taunt", 12: "Stun",
    13: "Mod Damage Done", 14: "Mod Damage Taken", 15: "Damage Shield",
    16: "Mod Stealth", 17: "Mod Stealth Detect", 18: "Mod Invisibility",
    19: "Mod Invisibility Detection", 20: "Obs Mod Health", 21: "Obs Mod Power",
    22: "Mod Resistance", 23: "Periodically trigger spell", 24: "Periodically give power",
    25: "Mod Pacify", 26: "Mod Root", 27: "Mod Silence", 28: "Reflect Spells",
    29: "Mod Stat", 30: "Mod Skill", 31: "Mod Increase Speed",
    32: "Mod Increase Mounted Speed", 33: "Mod Decrease Speed",
    34: "Mod Increase Health", 35: "Mod Increase Energy", 36: "Shapeshift",
    37: "Effect Immunity", 38: "State Immunity", 39: "School Immunity",
    40: "Damage Immunity", 41: "Immunity - Debuffs Only", 42: "Proc Trigger Spell",
    43: "Proc Trigger Damage", 44: "Track Creatures", 45: "Track Resources",
    47: "Mod Parry %", 49: "Mod Dodge %", 51: "Mod Block %", 52: "Mod Crit %",
    53: "Periodic Leech", 54: "Mod Hit Chance", 55: "Mod Spell Hit",
    56: "Transform", 57: "Mod Spell Crit", 58: "Increase Swim Speed %",
    61: "Mod Scale", 64: "Periodic Mana Leech", 65: "Mod Casting Speed",
    66: "Feign Death", 67: "Mod Disarm", 68: "Mod Stalked", 69: "School Absorb",
    72: "Mod Power Cost %", 73: "Mod Power Cost", 74: "Reflect School Spells",
    75: "Mod Language", 76: "Far Sight", 77: "Immunity - Mechanic", 78: "Mounted",
    94: "Interrupt Power Decay",
    79: "Mod Damage % Done", 80: "Mod Stat %", 82: "Water Breathing",
    82: "Underwater Breathing",
    84: "Mod Health Regen", 85: "Mod Power Regen", 87: "Mod Damage % Taken",
    89: "Periodic Damage %", 97: "Mana Shield", 99: "Mod Attack Power",
    101: "Mod Resistance %", 103: "Mod Total Threat", 104: "Water Walk",
    105: "Feather Fall", 106: "Hover", 107: "Add Flat Modifier",
    108: "Add Pct Modifier", 110: "Mod Power Regen %", 118: "Mod Healing Received %",
    123: "Mod Target Resistance", 124: "Mod Ranged Attack Power",
    129: "Mod Speed Always", 132: "Mod Increase Energy %", 133: "Mod Increase Health %",
    149: "Decrease Pushback Time by %",
    134: "Mod Manaregen Interrupt", 135: "Mod Healing Done", 138: "Mod Haste",
    86: "Create Soul Shard on Death", 88: "Periodic Health Funnel",
    91: "Mod Detect Range", 92: "Prevent Fleeing", 93: "Unattackable",
    100: "Detect Magic Aura", 113: "Reduce Fall Damage",
    117: "Mod Mechanic Resistance", 120: "Untrackable", 121: "Empathy",
    136: "Mod Healing Done %", 137: "Mod Total Stat %", 144: "Safe Fall",
    161: "Mod Health Regen %", 562: "Split Damage %",
}
STAT = {-1: "All Stats", 0: "Strength", 1: "Agility", 2: "Stamina",
        3: "Intellect", 4: "Spirit"}

rows = defaultdict(list)
with open("wow_SpellEffect.csv", encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        try:
            sid = int(row["SpellID"])
        except ValueError:
            continue
        rows[sid].append((int(row["EffectIndex"] or 0), int(row["Effect"] or 0),
                          int(row["EffectAura"] or 0), int(row["EffectMiscValue_0"] or 0),
                          int(row["EffectTriggerSpell"] or 0)))

unknown = defaultdict(int)
LEARNED_EFFECT = {}
LEARNED_AURA = {}

def decode(sid, school, depth=0, seen=None):
    seen = seen or set()
    if sid in seen or depth > 2:
        return []
    seen.add(sid)
    labels = []
    for _, eff, aura, misc, trig in sorted(rows.get(sid, [])):
        if eff == 6 or eff == 27 or eff == 35:
            nm = AURA_NAME.get(aura) or LEARNED_AURA.get(aura)
            if nm is None:
                unknown[f"aura {aura}"] += 1
                nm = f"Aura #{aura}"
            if aura == 29 and misc in STAT:
                nm += f" ({STAT[misc]})"
            prefix = "Apply Aura: " if eff != 35 else "Apply Area Aura: "
            labels.append(prefix + nm)
            if aura in (23, 42) and trig:   # periodic/proc trigger — follow the payload
                labels += [f"→ {x}" for x in decode(trig, school, depth + 1, seen)]
        else:
            nm = EFFECT_NAME.get(eff) or LEARNED_EFFECT.get(eff)
            if nm is None:
                unknown[f"effect {eff}"] += 1
                nm = f"Effect #{eff}"
            if eff == 2 and school:
                nm += f" ({school.split('/')[0]})"
            labels.append(nm)
            if eff in (64, 32) and trig:    # trigger spell/missile — follow the payload
                labels += [f"→ {x}" for x in decode(trig, school, depth + 1, seen)]
    return labels

recs = json.load(open("wow_spells.json", encoding="utf-8"))
wh = json.load(open("wow_wowhead_effects.json", encoding="utf-8"))

# learn names for unmapped modern ids from the wowhead overlap (position-aligned)
for r in recs:
    whl = (wh.get(str(r["id"])) or {}).get("effects") or []
    local_rows = sorted(rows.get(r["id"], []))
    if not whl or len(whl) != len(local_rows):
        continue
    for (idx, eff, aura, misc, trig), label in zip(local_rows, whl):
        clean = re.sub(r"\s*\(.*?\)", "", label.split("\n")[0]).strip()
        clean = re.sub(r"^Apply (Area )?Aura: ", "", clean)
        if not clean:
            continue
        if eff in (6, 27, 35):
            if aura not in AURA_NAME and aura not in LEARNED_AURA:
                LEARNED_AURA[aura] = clean
        elif eff not in EFFECT_NAME and eff not in LEARNED_EFFECT:
            LEARNED_EFFECT[eff] = clean
if LEARNED_EFFECT or LEARNED_AURA:
    print("learned from wowhead overlap:",
          {f"effect {k}": v for k, v in LEARNED_EFFECT.items()},
          {f"aura {k}": v for k, v in LEARNED_AURA.items()})

merged = {}
pulled = decoded = 0
agree = total = 0
NORM = lambda s: re.sub(r"\s*\(.*?\)", "", s.split("\n")[0]).replace("Apply Area Aura", "Apply Aura").strip().lower()
for r in recs:
    sid = str(r["id"])
    wh_labels = (wh.get(sid) or {}).get("effects") or []
    local = decode(r["id"], r["school"]) or decode(r["all_ids"][0], r["school"])
    if wh_labels:
        merged[sid] = {"name": r["name"], "effects": wh_labels, "source": "wowhead"}
        pulled += 1
        if local:
            total += 1
            a = [NORM(x) for x in wh_labels]
            b = [NORM(x) for x in local]
            if a == b or set(a) == set(b):
                agree += 1
    else:
        merged[sid] = {"name": r["name"], "effects": local, "source": "client-db"}
        decoded += 1

json.dump(merged, open("wow_effects_labels.json", "w", encoding="utf-8"), indent=0,
          ensure_ascii=False)
print(f"{pulled} from wowhead, {decoded} decoded from client SpellEffect")
print(f"decoder validation on wowhead overlap: {agree}/{total} rows match "
      f"({100*agree/max(1,total):.0f}%)")
lab_hit = lab_tot = 0
for r in recs:
    sid = str(r["id"])
    whl = (wh.get(sid) or {}).get("effects") or []
    if whl:
        loc = decode(r["id"], r["school"])
        a, b = {NORM(x) for x in whl}, {NORM(x) for x in loc}
        lab_hit += len(a & b)
        lab_tot += len(a)
print(f"label-level agreement: {lab_hit}/{lab_tot} wowhead labels reproduced "
      f"({100*lab_hit/max(1,lab_tot):.0f}%)")
if unknown:
    print("unknown ids:", dict(sorted(unknown.items(), key=lambda x: -x[1])[:10]))
mismatch = 0
for r in recs[:400]:
    sid = str(r["id"])
    whl = (wh.get(sid) or {}).get("effects") or []
    if whl:
        loc = decode(r["id"], r["school"])
        a, b = [NORM(x) for x in whl], [NORM(x) for x in loc]
        if a != b and set(a) != set(b) and mismatch < 6:
            print(f"  mismatch {r['name']}: wowhead={whl} local={loc}")
            mismatch += 1

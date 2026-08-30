"""Find near-identical spell templates in the D&D 5e SRD spell list.

Approach: normalize each spell description by masking out the "surface"
variables (damage type, dice, numbers, creature/element words), then compute
pairwise sequence similarity. Spells whose normalized text is highly similar
are the same mechanical template with a re-skin.
"""
import json
import re
import csv
from difflib import SequenceMatcher
from itertools import combinations

DAMAGE_TYPES = [
    "acid", "bludgeoning", "cold", "fire", "force", "lightning", "necrotic",
    "piercing", "poison", "psychic", "radiant", "slashing", "thunder",
]
ELEMENT_WORDS = [
    "flame", "flames", "fiery", "frost", "ice", "icy", "freezing", "burning",
    "burns", "burn", "shock", "sparks", "spark", "venom", "venomous",
]
CREATURE_WORDS = [
    "beast", "beasts", "humanoid", "humanoids", "monster", "monsters",
    "celestial", "celestials", "fey", "fiend", "fiends", "undead",
    "elemental", "elementals", "plant", "plants", "animal", "animals",
    "creature", "creatures", "person", "people", "dragon", "dragons",
]
ABILITY_WORDS = [
    "strength", "dexterity", "constitution", "intelligence", "wisdom",
    "charisma",
]


def normalize(text: str) -> str:
    t = text.lower()
    t = re.sub(r"\d+d\d+", " DICE ", t)
    t = re.sub(r"\d+", " N ", t)
    for w in DAMAGE_TYPES:
        t = re.sub(rf"\b{w}\b", " DMG ", t)
    for w in ELEMENT_WORDS:
        t = re.sub(rf"\b{w}\b", " ELEM ", t)
    for w in CREATURE_WORDS:
        t = re.sub(rf"\b{w}\b", " CRT ", t)
    for w in ABILITY_WORDS:
        t = re.sub(rf"\b{w}\b", " ABL ", t)
    t = re.sub(r"[^a-z ]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def spell_text(s: dict) -> str:
    parts = list(s.get("desc", []))
    parts += s.get("higher_level", [])
    return " ".join(parts)


def main():
    spells = json.load(open("spells_2014.json", encoding="utf-8"))
    for s in spells:
        s["_norm"] = normalize(spell_text(s)).split()
        s["_classes"] = sorted(c["name"] for c in s.get("classes", []))

    # --- per-class spell lists -------------------------------------------
    with open("spell_lists_per_class.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["class", "level", "spell", "school", "concentration", "ritual"])
        rows = []
        for s in spells:
            for c in s["_classes"]:
                rows.append([c, int(s["level"]), s["name"],
                             s["school"]["name"], s["concentration"], s["ritual"]])
        rows.sort(key=lambda r: (r[0], r[1], r[2]))
        w.writerows(rows)

    # --- pairwise similarity ---------------------------------------------
    pairs = []
    for a, b in combinations(spells, 2):
        # quick length filter to skip hopeless pairs
        la, lb = len(a["_norm"]), len(b["_norm"])
        if min(la, lb) == 0 or min(la, lb) / max(la, lb) < 0.5:
            continue
        ratio = SequenceMatcher(None, a["_norm"], b["_norm"], autojunk=False).ratio()
        if ratio >= 0.60:
            pairs.append((ratio, a, b))

    pairs.sort(reverse=True, key=lambda p: p[0])
    with open("similar_pairs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["similarity", "spell_a", "lvl_a", "spell_b", "lvl_b",
                    "classes_a", "classes_b"])
        for r, a, b in pairs:
            w.writerow([f"{r:.3f}", a["name"], a["level"], b["name"], b["level"],
                        "/".join(a["_classes"]), "/".join(b["_classes"])])

    # --- cluster with union-find at a high threshold ----------------------
    THRESH = 0.72
    parent = {s["index"]: s["index"] for s in spells}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        parent[find(x)] = find(y)

    for r, a, b in pairs:
        if r >= THRESH:
            union(a["index"], b["index"])

    clusters = {}
    for s in spells:
        clusters.setdefault(find(s["index"]), []).append(s)

    by_index = {s["index"]: s for s in spells}
    out = []
    for root, members in clusters.items():
        if len(members) < 2:
            continue
        members.sort(key=lambda s: (int(s["level"]), s["name"]))
        out.append({
            "spells": [{
                "name": m["name"], "level": int(m["level"]),
                "school": m["school"]["name"], "classes": m["_classes"],
                "range": m.get("range"), "duration": m.get("duration"),
                "concentration": m.get("concentration"),
                "damage_type": (m.get("damage", {}).get("damage_type", {}) or {}).get("name"),
                "dc": (m.get("dc", {}).get("dc_type", {}) or {}).get("name"),
                "desc": spell_text(m),
            } for m in members],
        })
    out.sort(key=lambda c: -len(c["spells"]))
    json.dump(out, open("clusters.json", "w", encoding="utf-8"), indent=1)

    print(f"{len(pairs)} pairs >= 0.60; {len(out)} clusters at >= {THRESH}")
    for c in out:
        names = [f"{s['name']} (L{s['level']})" for s in c["spells"]]
        print("  - " + ", ".join(names))


if __name__ == "__main__":
    main()

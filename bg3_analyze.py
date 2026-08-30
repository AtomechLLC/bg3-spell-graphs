"""Find near-identical spell templates among BG3 spells.

Similarity = 0.6 * masked mechanical signature + 0.4 * masked description.
Container spells are Larian's explicit reskin mechanism and form families outright.
"""
import csv
import json
import re
from difflib import SequenceMatcher
from itertools import combinations

MASK_SUBSTR = [
    "bludgeoning", "piercing", "slashing", "lightning", "necrotic", "radiant",
    "psychic", "thunder", "poison", "force", "acid", "cold", "fire", "frost",
    "flame", "ice", "shock",
    "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma",
]
GUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)

SIG_FIELDS = ["stype", "level", "school", "target_radius", "area_radius",
              "spell_roll", "spell_success", "spell_fail", "properties",
              "tooltip_damage", "status_apply", "attack_save", "use_costs",
              "flags", "intent"]


def mask(t):
    t = GUID.sub("G", t.lower())
    t = re.sub(r"\d+d\d+", " DICE ", t)
    for w in MASK_SUBSTR:
        t = t.replace(w, "X")
    t = re.sub(r"\d+", " N ", t)
    t = re.sub(r"[^a-z0-9X ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def prep(spells):
    for s in spells:
        sig = " | ".join(f"{k}={s[k]}" for k in SIG_FIELDS)
        s["_sig"] = mask(sig).split()
        s["_desc"] = mask(s["desc"] + " " + s["desc_params"]).split()
    return spells


def pair_score(a, b):
    sr = SequenceMatcher(None, a["_sig"], b["_sig"], autojunk=False).ratio()
    dr = SequenceMatcher(None, a["_desc"], b["_desc"], autojunk=False).ratio()
    return 0.6 * sr + 0.4 * dr, sr, dr


def main():
    all_recs = json.load(open("bg3_spells.json", encoding="utf-8"))
    # analysis population: true spells, roots only, containers collapsed
    pop = [r for r in all_recs
           if r["is_spell"] and not r["upcast_variant"] and not r["container"]]
    prep(pop)
    print(f"population: {len(pop)} root spells")

    pairs = []
    for a, b in combinations(pop, 2):
        la, lb = len(a["_sig"]), len(b["_sig"])
        if min(la, lb) / max(la, lb) < 0.5:
            continue
        score, sr, dr = pair_score(a, b)
        if score >= 0.55:
            pairs.append((score, sr, dr, a, b))
    pairs.sort(reverse=True, key=lambda p: p[0])

    with open("bg3_similar_pairs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["score", "sig", "desc", "a", "lvl_a", "b", "lvl_b"])
        for score, sr, dr, a, b in pairs:
            w.writerow([f"{score:.3f}", f"{sr:.3f}", f"{dr:.3f}",
                        a["name"], a["level"], b["name"], b["level"]])

    # union-find clusters
    THRESH = 0.75
    parent = {s["id"]: s["id"] for s in pop}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for score, sr, dr, a, b in pairs:
        if score >= THRESH:
            parent[find(a["id"])] = find(b["id"])

    clusters = {}
    for s in pop:
        clusters.setdefault(find(s["id"]), []).append(s)
    clusters = [sorted(c, key=lambda s: (s["level"], s["name"]))
                for c in clusters.values() if len(c) > 1]
    clusters.sort(key=len, reverse=True)

    print(f"\n{len(pairs)} pairs >= 0.55; {len(clusters)} clusters at >= {THRESH}:")
    for c in clusters:
        print("  - " + ", ".join(f"{s['name']} (L{s['level']})" for s in c))

    print("\ncontainer spells (explicit reskin containers):")
    by_id = {r["id"]: r for r in all_recs}
    for r in sorted(pop, key=lambda r: r["name"]):
        kids = [by_id[k]["name"] for k in r["children"] if k in by_id]
        if kids:
            print(f"  - {r['name']} (L{r['level']}): {', '.join(kids)}")


if __name__ == "__main__":
    main()

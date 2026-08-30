"""Find near-identical ability templates in WoW Classic tooltips.

WoW tooltips are macro-parameterized already ($s1, $d, ${formulas}) — masking
those plus school/element/creature/city words exposes the shared templates.
"""
import csv
import json
import re
from difflib import SequenceMatcher
from itertools import combinations

MASK_WORDS = [
    "fire", "frost", "shadow", "nature", "holy", "arcane", "physical",
    "flame", "flames", "ice", "icy", "lightning", "burning", "burn", "chill",
    "chilled", "frozen",
    "beasts", "humanoids", "undead", "demons", "dragonkin", "elementals",
    "giants", "hidden", "beast", "humanoid", "demon", "elemental", "giant",
    "stormwind", "ironforge", "darnassus", "orgrimmar", "undercity",
    "thunder bluff",
    "agate", "jade", "citrine", "ruby",
    "imp", "voidwalker", "succubus", "felhunter",
    "serpent", "scorpid", "viper",
    "strength", "agility", "intellect", "spirit", "stamina",
]


def mask(t):
    t = t.lower()
    t = re.sub(r"\$\{[^}]*\}", " F ", t)        # ${formulas}
    t = re.sub(r"\$<[^>]*>", " F ", t)
    t = re.sub(r"\$\w+", " V ", t)              # $s1 $d $a1 ...
    for w in MASK_WORDS:
        t = re.sub(rf"\b{re.escape(w)}\b", " X ", t)
    t = re.sub(r"\d+", " N ", t)
    t = re.sub(r"[^a-z ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def main():
    recs = json.load(open("wow_spells.json", encoding="utf-8"))
    for r in recs:
        r["_m"] = mask(r["desc"]).split()

    pairs = []
    for a, b in combinations(recs, 2):
        la, lb = len(a["_m"]), len(b["_m"])
        if min(la, lb) == 0 or min(la, lb) / max(la, lb) < 0.5:
            continue
        s = SequenceMatcher(None, a["_m"], b["_m"], autojunk=False).ratio()
        if s >= 0.60:
            pairs.append((s, a, b))
    pairs.sort(reverse=True, key=lambda p: p[0])

    with open("wow_similar_pairs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sim", "a", "cls_a", "b", "cls_b"])
        for s, a, b in pairs:
            w.writerow([f"{s:.3f}", a["name"], "/".join(a["classes"]),
                        b["name"], "/".join(b["classes"])])

    THRESH = 0.82
    parent = {r["id"]: r["id"] for r in recs}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for s, a, b in pairs:
        if s >= THRESH:
            parent[find(a["id"])] = find(b["id"])

    clusters = {}
    for r in recs:
        clusters.setdefault(find(r["id"]), []).append(r)
    clusters = [sorted(c, key=lambda r: (r["level"], r["name"]))
                for c in clusters.values() if len(c) > 1]
    clusters.sort(key=len, reverse=True)

    print(f"{len(pairs)} pairs >= 0.60; {len(clusters)} clusters at >= {THRESH}:")
    for c in clusters:
        names = ", ".join(f"{r['name']} [{'/'.join(x[:2] for x in r['classes'])}]" for r in c)
        print(f"  ({len(c)}) {names}")


if __name__ == "__main__":
    main()

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


# ------------------------------------------------- mechanical effect signature
def load_effect_sigs():
    """SpellID -> effect-signature tokens from SpellEffect.db2 (mechanics, not prose)."""
    import csv as _csv
    from collections import defaultdict
    rows = defaultdict(list)
    with open("wow_SpellEffect.csv", encoding="utf-8-sig", newline="") as f:
        for row in _csv.DictReader(f):
            try:
                sid = int(row["SpellID"])
            except ValueError:
                continue
            rows[sid].append((int(row["EffectIndex"] or 0),
                              int(row["Effect"] or 0), int(row["EffectAura"] or 0),
                              int(row["EffectMechanic"] or 0),
                              1 if float(row["EffectBasePoints"] or 0) >= 0 else -1,
                              int(row["ImplicitTarget_0"] or 0)))
    sigs = {}
    for sid, es in rows.items():
        toks = []
        for _, eff, aura, mech, sign, tgt in sorted(es):
            toks += [f"E{eff}", f"A{aura}", f"M{mech}", f"S{sign}", f"T{tgt}"]
        sigs[sid] = toks
    return sigs


def prep(recs):
    sigs = load_effect_sigs()
    for r in recs:
        r["_m"] = mask(r["desc"]).split()
        r["_sig"] = (sigs.get(r["id"]) or sigs.get(r["all_ids"][0]) or []) + \
                    ["SCH" + (r["school"] or "")]
    return recs


def pair_score(a, b):
    """0.6 x effect-signature similarity + 0.4 x masked-tooltip similarity."""
    sr = SequenceMatcher(None, a["_sig"], b["_sig"], autojunk=False).ratio()
    dr = SequenceMatcher(None, a["_m"], b["_m"], autojunk=False).ratio() \
        if a["_m"] and b["_m"] else 0.0
    return 0.6 * sr + 0.4 * dr, sr, dr


def main():
    recs = json.load(open("wow_spells.json", encoding="utf-8"))
    prep(recs)

    pairs = []
    for a, b in combinations(recs, 2):
        s, sr, dr = pair_score(a, b)
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

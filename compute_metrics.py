"""Compute the homogeneity index and class-composition profiles for all
three games; writes homogeneity.json and class_comp.json for the atlas."""
import csv
import io
import contextlib
import json
from itertools import combinations

# ---------------------------------------------------------------- homogeneity
# Index: share of a game's kit whose nearest neighbour (same game) scores at
# or above a threshold on that game's mechanical-similarity measure.
# SRD = masked-token text ratio; BG3 = stat-signature blend; WoW = SpellEffect
# blend. Pair files are complete above their storage floors (0.50 / 0.55),
# far below both thresholds, so threshold shares are exact.
T_TWIN, T_REL = 0.85, 0.75

with contextlib.redirect_stdout(io.StringIO()):
    import build_wiki as W          # SRD: BY (masked _norm) + sim()
    import build_bg3_codex as B     # BG3: DPOP (deduped population)

best = {}
srd_ids = list(W.BY)
for a, b in combinations(srd_ids, 2):
    s = W.sim(a, b)
    if s > best.get(a, 0):
        best[a] = s
    if s > best.get(b, 0):
        best[b] = s
srd_nn = [best.get(i, 0.0) for i in srd_ids]

bg3_pop = [r["id"] for r in B.DPOP]
bg3_best = {}
for k, v in json.load(open("cluster_sims.json", encoding="utf-8")).items():
    a, b = k.split("|")
    if v > bg3_best.get(a, 0):
        bg3_best[a] = v
    if v > bg3_best.get(b, 0):
        bg3_best[b] = v
bg3_nn = [bg3_best.get(i, 0.0) for i in bg3_pop]

wow = json.load(open("wow_spells.json", encoding="utf-8"))
wow_rows = wow if isinstance(wow, list) else list(wow.values())
wow_pop = [str(r["id"]) for r in wow_rows]
wow_best = {}
for k, v in json.load(open("wow_cluster_sims.json", encoding="utf-8")).items():
    a, b = k.split("|")
    if v > wow_best.get(a, 0):
        wow_best[a] = v
    if v > wow_best.get(b, 0):
        wow_best[b] = v
wow_nn = [wow_best.get(i, 0.0) for i in wow_pop]

def index(nn):
    n = len(nn)
    return {"n": n,
            "twin": round(100 * sum(1 for v in nn if v >= T_TWIN) / n, 1),
            "rel": round(100 * sum(1 for v in nn if v >= T_REL) / n, 1)}

HOMOG = {
    "D&D 5e SRD": {**index(srd_nn), "measure": "masked spell text"},
    "Baldur's Gate 3": {**index(bg3_nn), "measure": "stat-field signature"},
    "WoW Classic": {**index(wow_nn), "measure": "SpellEffect blend"},
}
json.dump(HOMOG, open("homogeneity.json", "w", encoding="utf-8"), indent=1)

# ---------------------------------------------------------------- class comp
PUR = {}
for r in csv.DictReader(open("purpose_tagged.csv", encoding="utf-8")):
    PUR[(r["game"], r["ability"].lower())] = r["purpose"]

def tally(game, iterable):
    comp = {}
    miss = 0
    for name, classes in iterable:
        p = PUR.get((game, name.lower()))
        if not p:
            miss += 1
            continue
        for c in classes:
            comp.setdefault(c, {}).setdefault(p, 0)
            comp[c][p] += 1
    if miss:
        print(f"{game}: {miss} abilities without purpose rows")
    return comp

srd = json.load(open("spells_2014.json", encoding="utf-8"))
srd_rows = srd if isinstance(srd, list) else list(srd.values())
COMP = {
    "D&D 5e SRD": tally("D&D 5e SRD",
                        ((r["name"], [c["name"] for c in r.get("classes", [])])
                         for r in srd_rows)),
    "Baldur's Gate 3": tally("Baldur's Gate 3",
                             ((r["name"], r.get("classes", [])) for r in B.DPOP)),
    "WoW Classic": tally("WoW Classic",
                         ((r["name"], r.get("classes", [])) for r in wow_rows)),
}
json.dump(COMP, open("class_comp.json", "w", encoding="utf-8"), indent=1)

for g, v in HOMOG.items():
    print(f"{g}: n={v['n']}  twins(>= {T_TWIN}): {v['twin']}%  relatives(>= {T_REL}): {v['rel']}%")
print("class_comp.json:", {g: len(c) for g, c in COMP.items()})

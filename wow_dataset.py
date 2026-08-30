"""Assemble WoW Classic Era class-spell dataset from wago.tools CSVs -> wow_spells.json."""
import csv
import json
import re
from collections import defaultdict

def load(name, key="ID"):
    with open(f"wow_{name}.csv", encoding="utf-8-sig", newline="") as f:
        return {row[key]: row for row in csv.DictReader(f)}

names = load("SpellName")
spells = load("Spell")
skill_lines = load("SkillLine")
misc = {}
for row in load("SpellMisc").values():
    misc[row["SpellID"]] = row
levels = {}
for row in load("SpellLevels").values():
    levels[row["SpellID"]] = row

CLASS_MASK = {1: "Warrior", 2: "Paladin", 4: "Hunter", 8: "Rogue", 16: "Priest",
              64: "Shaman", 128: "Mage", 256: "Warlock", 1024: "Druid"}
SCHOOLS = {1: "Physical", 2: "Holy", 4: "Fire", 8: "Nature", 16: "Frost",
           32: "Shadow", 64: "Arcane"}

def school_of(mask):
    try:
        m = int(mask)
    except (TypeError, ValueError):
        return ""
    return "/".join(v for k, v in SCHOOLS.items() if m & k)

# class skill lines (CategoryID 7), mapped to classes via ClassMask on the ability row
rows = []
with open("wow_SkillLineAbility.csv", encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        sl = skill_lines.get(row["SkillLine"])
        if not sl or sl["CategoryID"] != "7" or sl["DisplayName_lang"] in ("Engraving", "Runes"):
            continue
        if int(row["Spell"]) >= 100000:
            continue   # Season of Discovery / anniversary additions — keep vanilla 1.12 ids
        cm = int(row["ClassMask"] or 0)
        classes = [c for m, c in CLASS_MASK.items() if cm & m]
        if not classes:
            continue
        rows.append((row["Spell"], row["SkillLine"], sl["DisplayName_lang"], classes))

records = {}
for sid, sl_id, sl_name, classes in rows:
    nm = names.get(sid, {}).get("Name_lang", "")
    if not nm or "(OLD)" in nm or "OLD" == nm[:3] or "test" in nm.lower():
        continue
    if "(DND)" in nm or nm.endswith("Passive") or "(NYI)" in nm:
        continue
    sp = spells.get(sid, {})
    mi = misc.get(sid, {})
    lv = levels.get(sid, {})
    if int(lv.get("BaseLevel") or 0) < 1:
        continue   # talents, procs, hidden triggers — trainer spells require a level
    if not sp.get("Description_lang"):
        continue   # hidden proc/aura records
    rec = {
        "id": int(sid),
        "name": nm,
        "rank": sp.get("NameSubtext_lang", ""),
        "desc": sp.get("Description_lang", ""),
        "school": school_of(mi.get("SchoolMask")),
        "level": int(lv.get("BaseLevel") or 0),
        "skillline": sl_name,
        "classes": classes,
    }
    if sid in records:
        records[sid]["classes"] = sorted(set(records[sid]["classes"]) | set(classes))
    else:
        records[sid] = rec

# collapse ranks: group by (name, class-set)
groups = defaultdict(list)
for r in records.values():
    groups[(r["name"], tuple(r["classes"]))].append(r)

def rank_num(r):
    m = re.match(r"Rank (\d+)", r["rank"] or "")
    return int(m.group(1)) if m else 0

out = []
for (nm, cls), rs in groups.items():
    top = max(rs, key=rank_num)
    top = dict(top)
    top["rank_count"] = len({rank_num(r) for r in rs})
    top["all_ids"] = sorted(r["id"] for r in rs)
    out.append(top)

out.sort(key=lambda r: (r["classes"], r["level"], r["name"]))
json.dump(out, open("wow_spells.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

n_rank_entries = sum(r["rank_count"] for r in out)
print(f"{len(records)} class-skill spell entries -> {len(out)} distinct abilities "
      f"({n_rank_entries} rank entries; {n_rank_entries - len(out)} are extra ranks)")
per = defaultdict(set)
for r in out:
    for c in r["classes"]:
        per[c].add(r["name"])
for c in sorted(per):
    print(f"  {c}: {len(per[c])}")
nodesc = sum(1 for r in out if not r["desc"])
print(f"abilities without description (passives etc.): {nodesc}")

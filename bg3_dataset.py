"""Assemble the BG3 spell dataset from extracted game files -> bg3_spells.json.

Pipeline: stats txt (with `using` inheritance) + english.loca (names/descriptions)
+ SpellLists.lsx + Progressions.lsx (class attribution).
"""
import json
import os
import re
import struct
import xml.etree.ElementTree as ET
from collections import defaultdict

D = "bg3_data"
MODS = ["Shared", "SharedDev", "Gustav", "GustavDev", "GustavX"]  # load order

# ---------------------------------------------------------------- stats txt
RAW = {}   # entry name -> {"using": str|None, "data": {k: v}}
for mod in MODS:
    for fn in sorted(os.listdir(D)):
        if fn.startswith(f"Public__{mod}__Stats") and fn.endswith(".txt"):
            text = open(os.path.join(D, fn), encoding="utf-8-sig").read()
            for block in re.split(r"\r?\n\r?\n", text):
                m = re.search(r'new entry "([^"]+)"', block)
                if not m:
                    continue
                name = m.group(1)
                entry = RAW.setdefault(name, {"using": None, "data": {}})
                u = re.search(r'\busing "([^"]+)"', block)
                if u:
                    entry["using"] = u.group(1)
                for k, v in re.findall(r'data "([^"]+)" "([^"]*)"', block):
                    entry["data"][k] = v

def resolve(name, _seen=None):
    """Effective data dict with inheritance applied."""
    _seen = _seen or set()
    if name not in RAW or name in _seen:
        return {}
    _seen.add(name)
    e = RAW[name]
    base = resolve(e["using"], _seen) if e["using"] else {}
    out = dict(base)
    out.update(e["data"])
    return out

# ---------------------------------------------------------------- loca
def load_loca(path):
    buf = open(path, "rb").read()
    assert buf[:4] == b"LOCA"
    num, texts_off = struct.unpack_from("<II", buf, 4)
    table = {}
    pos = 12
    off = texts_off
    for _ in range(num):
        key = buf[pos:pos + 64].split(b"\x00", 1)[0].decode()
        ver, length = struct.unpack_from("<HI", buf, pos + 64)
        table[key] = buf[off:off + length].rstrip(b"\x00").decode("utf-8", "replace")
        pos += 70
        off += length
    return table

LOCA = load_loca(os.path.join(D, "Localization__English__english.loca"))

TAG = re.compile(r"<[^>]+>")
def loc(handle):
    if not handle:
        return ""
    key = handle.split(";")[0]
    return TAG.sub("", LOCA.get(key, "")).strip()

# ---------------------------------------------------------------- spell lists
LISTS = {}   # uuid -> {"name": str, "spells": [ids]}
for mod in MODS:
    fn = os.path.join(D, f"Public__{mod}__Lists__SpellLists.lsx")
    if not os.path.exists(fn):
        continue
    root = ET.parse(fn).getroot()
    for node in root.iter("node"):
        if node.get("id") != "SpellList":
            continue
        a = {x.get("id"): x.get("value") for x in node.iter("attribute")}
        spl = [s for s in re.split(r"[;,]", a.get("Spells", "")) if s]
        LISTS[a["UUID"]] = {"name": a.get("Name", ""), "spells": spl}

# ---------------------------------------------------------------- progressions
SUBCLASS_PARENT = {
    "ArcaneTrickster": "Rogue", "EldritchKnight": "Fighter",
    "WayOfTheFourElements": "Monk", "FourElements": "Monk",
    "LifeDomain": "Cleric", "LightDomain": "Cleric", "TrickeryDomain": "Cleric",
    "KnowledgeDomain": "Cleric", "NatureDomain": "Cleric", "TempestDomain": "Cleric",
    "WarDomain": "Cleric", "DeathDomain": "Cleric",
    "Oathbreaker": "Paladin", "OathOfAncients": "Paladin", "OathOfDevotion": "Paladin",
    "OathOfVengeance": "Paladin", "OathOfTheCrown": "Paladin",
    "CircleOfTheLand": "Druid", "CircleOfTheMoon": "Druid", "CircleOfTheSpores": "Druid",
    "CircleOfTheStars": "Druid",
    "TheFiend": "Warlock", "TheGreatOldOne": "Warlock", "TheArchfey": "Warlock",
    "Hexblade": "Warlock",
    "DraconicBloodline": "Sorcerer", "WildMagic": "Sorcerer", "StormSorcery": "Sorcerer",
    "ShadowMagic": "Sorcerer",
    "CollegeOfLore": "Bard", "CollegeOfValour": "Bard", "CollegeOfSwords": "Bard",
    "CollegeOfGlamour": "Bard",
    "AbjurationSchool": "Wizard", "ConjurationSchool": "Wizard", "DivinationSchool": "Wizard",
    "EnchantmentSchool": "Wizard", "EvocationSchool": "Wizard", "IllusionSchool": "Wizard",
    "NecromancySchool": "Wizard", "TransmutationSchool": "Wizard", "BladesingingSchool": "Wizard",
    "GloomStalker": "Ranger", "BeastMaster": "Ranger", "Hunter": "Ranger",
    "SwarmKeeper": "Ranger", "DrakewardenRanger": "Ranger",
}
CLASSES12 = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin",
             "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]

GUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
class_lists = defaultdict(set)      # class -> set of list uuids
list_source = defaultdict(set)      # uuid -> set of class names that reference it
for mod in MODS:
    fn = os.path.join(D, f"Public__{mod}__Progressions__Progressions.lsx")
    if not os.path.exists(fn):
        continue
    root = ET.parse(fn).getroot()
    for node in root.iter("node"):
        if node.get("id") != "Progression":
            continue
        a = {x.get("id"): x.get("value") for x in node.iter("attribute")}
        name = a.get("Name", "")
        cls = name if name in CLASSES12 else SUBCLASS_PARENT.get(name)
        blob = (a.get("Selectors", "") or "") + ";" + (a.get("Boosts", "") or "")
        for g in GUID.findall(blob):
            if g in LISTS:
                if cls:
                    class_lists[cls].add(g)
                    list_source[g].add(cls)
                else:
                    list_source[g].add(f"({name})")

# ---------------------------------------------------------------- assemble
def is_upcast_variant(name, d):
    if d.get("RootSpellID"):
        return True
    m = re.match(r"^(.+)_(\d+)$", name)
    return bool(m and m.group(1) in RAW)

spell_ids = set()
for cls, uuids in class_lists.items():
    for u in uuids:
        spell_ids.update(LISTS[u]["spells"])

records = {}
for sid in sorted(spell_ids):
    d = resolve(sid)
    if not d or d.get("Level") is None and not d.get("SpellSchool"):
        if not d:
            continue
    name = loc(d.get("DisplayName"))
    if not name:
        continue
    classes = sorted({c for u, cl in
                      ((u, LISTS[u]) for u in LISTS)
                      if sid in cl["spells"]
                      for c in list_source.get(u, set()) if not c.startswith("(")})
    rec = {
        "id": sid,
        "name": name,
        "desc": loc(d.get("Description")),
        "desc_params": d.get("DescriptionParams", ""),
        "level": int(d.get("Level") or 0),
        "school": d.get("SpellSchool", "None"),
        "stype": d.get("SpellType", sid.split("_")[0]),
        "damage_type": d.get("DamageType", ""),
        "tooltip_damage": d.get("TooltipDamageList", ""),
        "attack_save": d.get("TooltipAttackSave", ""),
        "use_costs": d.get("UseCosts", ""),
        "spell_roll": d.get("SpellRoll", ""),
        "spell_success": d.get("SpellSuccess", ""),
        "spell_fail": d.get("SpellFail", ""),
        "properties": d.get("SpellProperties", ""),
        "status_apply": d.get("TooltipStatusApply", ""),
        "target_radius": d.get("TargetRadius", ""),
        "area_radius": d.get("AreaRadius", "") or d.get("ExplodeRadius", ""),
        "flags": d.get("SpellFlags", ""),
        "intent": d.get("VerbalIntent", ""),
        "icon": d.get("Icon", ""),
        "container": d.get("SpellContainerID", ""),
        "children": [c for c in re.split(r"[;,]", d.get("ContainerSpells", "")) if c],
        "upcast_variant": is_upcast_variant(sid, d),
        "classes": classes,
        "is_spell": "IsSpell" in d.get("SpellFlags", ""),
    }
    records[sid] = rec

# containers referenced by lists pull their children in
for sid in list(records):
    for ch in records[sid]["children"]:
        if ch in records:
            continue
        d = resolve(ch)
        nm = loc(d.get("DisplayName"))
        if not d or not nm:
            continue
        r = dict(records[sid])
        r.update(id=ch, name=nm, desc=loc(d.get("Description")),
                 desc_params=d.get("DescriptionParams", ""),
                 damage_type=d.get("DamageType", ""),
                 tooltip_damage=d.get("TooltipDamageList", ""),
                 spell_success=d.get("SpellSuccess", ""),
                 spell_fail=d.get("SpellFail", ""),
                 properties=d.get("SpellProperties", ""),
                 status_apply=d.get("TooltipStatusApply", ""),
                 icon=d.get("Icon", "") or records[sid]["icon"],
                 container=sid, children=[],
                 upcast_variant=is_upcast_variant(ch, d))
        records[ch] = r

json.dump(list(records.values()), open("bg3_spells.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)

roots = [r for r in records.values() if not r["upcast_variant"]]
print(f"{len(records)} spell records ({len(roots)} roots, "
      f"{sum(1 for r in roots if r['container'])} container children, "
      f"{sum(1 for r in roots if r['children'])} containers)")
for c in CLASSES12:
    n = len({r['id'] for r in roots if c in r['classes']})
    print(f"  {c}: {n}")

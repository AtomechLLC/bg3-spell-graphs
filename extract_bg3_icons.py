"""Extract spell icons from the local BG3 install (Game.pak controller UI icons)
and save 64px PNGs to bg3_icons/<srd-slug>.png."""
import io
import json
import os
import re
import sys
from PIL import Image

from bg3pak import read_entries, extract

BG3 = r"Z:\SteamLibrary\steamapps\common\Baldurs Gate 3\Data"
PAKS = ["Game.pak", "GustavX.pak", "Patch8_HotFix9.pak"]  # later paks override

# SRD de-branded / renamed -> BG3 names
RENAME = {
    "Acid Arrow": "Melfs Acid Arrow",
    "Hideous Laughter": "Tashas Hideous Laughter",
    "Floating Disk": "Tensers Floating Disk",
    "Resilient Sphere": "Otilukes Resilient Sphere",
    "Freezing Sphere": "Otilukes Freezing Sphere",
    "Tiny Hut": "Leomunds Tiny Hut",
    "Blindness/Deafness": "Blindness",
    "Jump": "Long Jump",
    "Black Tentacles": "Evards Black Tentacles",
}

SCHOOLS = {"Abjuration", "Conjuration", "Divination", "Enchantment",
           "Evocation", "Illusion", "Necromancy", "Transmutation"}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


# ---- gather icon entries across paks (later paks win) ----------------------
icon_entries = {}   # normalized base name -> (pak_path, entry, raw filename)
pat = re.compile(r"/Assets/ControllerUIIcons/skills_png/Spell_(.+)\.DDS$")
for pakname in PAKS:
    path = os.path.join(BG3, pakname)
    if not os.path.exists(path):
        continue
    try:
        entries = read_entries(path)
    except Exception as e:
        print(f"  ! {pakname}: {e}")
        continue
    n = 0
    for e in entries:
        m = pat.search(e.name)
        if not m:
            continue
        tokens = m.group(1).split("_")
        while tokens and tokens[0] in SCHOOLS:
            tokens.pop(0)
        base = "_".join(tokens)
        icon_entries[norm(base)] = (path, e, base)
        n += 1
    print(f"{pakname}: {n} spell icons")

# ---- match SRD spells ------------------------------------------------------
spells = json.load(open("spells_2014.json", encoding="utf-8"))
os.makedirs("bg3_icons", exist_ok=True)

hits, misses = [], []
for s in spells:
    name = RENAME.get(s["name"], s["name"])
    key = norm(name)
    found = icon_entries.get(key)
    if not found:
        # variant icons like DisguiseSelf_HalfOrc_Female: accept prefix match
        cands = [k for k in icon_entries if k.startswith(key)]
        if cands:
            found = icon_entries[min(cands, key=len)]
    if not found:
        misses.append(s["name"])
        continue
    pak_path, entry, base = found
    try:
        data = extract(pak_path, entry)
        img = Image.open(io.BytesIO(data))
        img = img.convert("RGBA").resize((64, 64), Image.LANCZOS)
        img.save(os.path.join("bg3_icons", s["index"] + ".png"))
        hits.append(s["name"])
    except Exception as ex:
        misses.append(s["name"])
        print(f"  ! {s['name']} ({base}): {ex}")

print(f"\n{len(hits)} icons extracted, {len(misses)} spells unmatched")
print("unmatched:", ", ".join(sorted(misses)))

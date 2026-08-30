"""Extract the exact icon for every BG3 spell record -> bg3_codex_icons/<id>.png."""
import io
import json
import os
import re
from PIL import Image
from bg3pak import read_entries, extract

BG3 = r"Z:\SteamLibrary\steamapps\common\Baldurs Gate 3\Data"
pat = re.compile(r"/Assets/ControllerUIIcons/skills_png/(.+)\.DDS$")

files = {}
for pakname in ["Game.pak", "GustavX.pak", "Patch8_HotFix9.pak"]:
    p = os.path.join(BG3, pakname)
    if not os.path.exists(p):
        continue
    for e in read_entries(p):
        m = pat.search(e.name)
        if m:
            files[m.group(1)] = (p, e)
print(f"{len(files)} icon files indexed")

recs = json.load(open("bg3_spells.json", encoding="utf-8"))
os.makedirs("bg3_codex_icons", exist_ok=True)
hits = misses = 0
for r in recs:
    icon = r.get("icon")
    out = os.path.join("bg3_codex_icons", r["id"] + ".png")
    if not icon or icon not in files:
        misses += 1
        continue
    p, e = files[icon]
    img = Image.open(io.BytesIO(extract(p, e))).convert("RGBA").resize((64, 64), Image.LANCZOS)
    img.save(out)
    hits += 1
print(f"{hits} icons extracted, {misses} records without an icon file")

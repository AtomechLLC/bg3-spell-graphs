"""Targeted icon acquisition for the specific abilities still missing icons."""
import io
import json
import os
import re
import subprocess
import time
import urllib.parse

from PIL import Image

UA = "SpellHomogeneityResearch/1.0 (personal game-design research; low volume, throttled)"
recs = json.load(open("wow_spells.json", encoding="utf-8"))
icon_map = json.load(open("wow_icon_map.json", encoding="utf-8"))
icon_names = json.load(open("wow_icon_names.json", encoding="utf-8"))

HARDCODE = {
    "Inferno": "spell_shadow_summoninfernal",
    "Polymorph: Cow": "spell_nature_polymorph_cow",
    "Slow Fall": "spell_magic_featherfall",
    "Curse of Idiocy": "spell_shadow_mindrot",
    "Aquatic Form (Passive)": "ability_druid_aquaticform",
    "Shadowguard": "spell_nature_lightningshield",
}

def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

def fetch(url):
    try:
        r = subprocess.run(["curl.exe", "-sL", "--max-time", "25", "-A", UA, url],
                           capture_output=True, timeout=45)
        return r.stdout
    except Exception:
        return b""

missing = [r for r in recs if slug(r["name"]) not in icon_map]
names_missing = sorted({r["name"] for r in missing})
print(f"{len(names_missing)} abilities without icons")

got = 0
for name in names_missing:
    ic = HARDCODE.get(name) or icon_names.get(name)
    if not ic:
        print(f"  no icon name known for {name!r}")
        continue
    ic_norm = ic.strip().lower().replace(" ", "_")
    fn = os.path.join("wow_icons", "_" + re.sub(r"[^a-z0-9]+", "_", ic_norm) + ".png")
    if not os.path.exists(fn):
        data = b""
        for url in [
            f"https://warcraft.wiki.gg/wiki/Special:FilePath/{urllib.parse.quote(ic_norm + '.png')}",
            f"https://warcraft.wiki.gg/wiki/Special:FilePath/{urllib.parse.quote(ic_norm + '.jpg')}",
            f"https://wow.zamimg.com/images/wow/icons/large/{ic_norm}.jpg",
        ]:
            data = fetch(url)
            if data[:4] == b"\x89PNG" or data[:2] == b"\xff\xd8":
                break
            data = b""
            time.sleep(0.8)
        if data:
            img = Image.open(io.BytesIO(data)).convert("RGBA")
            img.save(fn)
        time.sleep(0.8)
    if os.path.exists(fn):
        for r in recs:
            if r["name"] == name:
                icon_map[slug(name)] = fn
        got += 1
    else:
        print(f"  still missing: {name} ({ic_norm})")

json.dump(icon_map, open("wow_icon_map.json", "w"), indent=0)
print(f"filled {got}/{len(names_missing)}; map now covers {len(icon_map)} ability slugs")

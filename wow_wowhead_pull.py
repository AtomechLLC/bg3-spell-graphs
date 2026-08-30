"""Pull per-spell effect boxes from wowhead classic for every ability in the
all-spells list. Polite: throttled, cached in wow_wowhead_effects.json."""
import html as H
import json
import os
import re
import subprocess
import time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SpellHomogeneityResearch/1.0 (personal research; throttled)"
CACHE = "wow_wowhead_effects.json"

recs = json.load(open("wow_spells.json", encoding="utf-8"))
cache = json.load(open(CACHE, encoding="utf-8")) if os.path.exists(CACHE) else {}

EFF = re.compile(r"<th>Effect #\d+</th><td[^>]*>(.*?)(?:<small|</td>)", re.S)
TAG = re.compile(r"<[^>]+>")

def parse_effects(html):
    out = []
    for m in EFF.finditer(html):
        label = TAG.sub("", m.group(1))
        label = H.unescape(label).replace("\xa0", " ").strip()
        if label:
            out.append(label)
    return out

todo = [r for r in recs if str(r["id"]) not in cache]
print(f"{len(todo)} abilities to fetch ({len(cache)} cached)", flush=True)
fails = 0
for n, r in enumerate(todo):
    url = f"https://www.wowhead.com/classic/spell={r['id']}"
    effects = None
    for attempt in range(3):
        try:
            res = subprocess.run(["curl.exe", "-sL", "--max-time", "30", "-A", UA, url],
                                 capture_output=True, timeout=60)
            html = res.stdout.decode("utf-8", "replace")
        except Exception:
            html = ""
        if "Effect #" in html:
            effects = parse_effects(html)
            break
        if "429" in html[:400] or "Just a moment" in html[:2000]:
            print(f"  rate-limited at #{n}, backing off 45s", flush=True)
            time.sleep(45)
            continue
        break
    if effects is None:
        effects = []
        fails += 1
    cache[str(r["id"])] = {"name": r["name"], "effects": effects}
    if n % 25 == 0:
        json.dump(cache, open(CACHE, "w", encoding="utf-8"), indent=0)
        print(f"  {n}/{len(todo)} fetched, {fails} without effects", flush=True)
    time.sleep(0.9)

json.dump(cache, open(CACHE, "w", encoding="utf-8"), indent=0)
empty = [v["name"] for v in cache.values() if not v["effects"]]
print(f"done: {len(cache)} cached, {len(empty)} without effect boxes: {', '.join(empty[:15])}")

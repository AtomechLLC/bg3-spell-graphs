"""Fetch ability icons from warcraft.wiki.gg: batch-read page wikitext, extract
the infobox icon name, download the icon file. Polite: batched, throttled."""
import json
import os
import re
import subprocess
import time
import urllib.parse

UA = "SpellHomogeneityResearch/1.0 (personal game-design research; low volume, throttled)"
API = "https://warcraft.wiki.gg/api.php"
recs = json.load(open("wow_spells.json", encoding="utf-8"))
os.makedirs("wow_icons", exist_ok=True)

def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

def api(params):
    url = API + "?" + urllib.parse.urlencode(params)
    r = subprocess.run(["curl.exe", "-sL", "--max-time", "30", "-A", UA, url],
                       capture_output=True, timeout=60)
    return json.loads(r.stdout)

names = sorted({r["name"] for r in recs})
CLASS_OF = {r["name"]: r["classes"][0].lower() for r in recs}
NAMES_CACHE = "wow_icon_names.json"
icon_of = json.load(open(NAMES_CACHE, encoding="utf-8")) if os.path.exists(NAMES_CACHE) else {}

def fetch_batch(titles, label=""):
    got = {}
    d = api({"action": "query", "format": "json", "prop": "revisions",
             "rvprop": "content", "rvslots": "main", "redirects": 1,
             "titles": "|".join(titles)})
    q = d.get("query", {})
    back = {}   # resolved title -> original title
    for m in q.get("normalized", []) + q.get("redirects", []):
        back[m["to"]] = back.get(m["from"], m["from"])
    for p in q.get("pages", {}).values():
        title = p.get("title", "")
        orig = back.get(title, title)
        try:
            txt = p["revisions"][0]["slots"]["main"]["*"]
        except (KeyError, IndexError):
            continue
        m = re.search(r"\|\s*icon\s*=\s*([\w\-'. ]+)", txt)
        if m:
            got[orig] = m.group(1).strip()
    return got

# pass 1: plain titles; pass 2: "(class ability)" for misses
if not icon_of:
    for i in range(0, len(names), 50):
        batch = names[i:i + 50]
        icon_of.update(fetch_batch(batch))
        print(f"  {min(i + 50, len(names))}/{len(names)} pages, {len(icon_of)} icons found", flush=True)
        time.sleep(0.6)
    missing = [n for n in names if n not in icon_of]
    retry = {f"{n} ({CLASS_OF[n]} ability)": n for n in missing}
    for i in range(0, len(retry), 50):
        keys = list(retry)[i:i + 50]
        got = fetch_batch(keys)
        for k, v in got.items():
            icon_of[retry[k]] = v
        time.sleep(0.6)
    json.dump(icon_of, open(NAMES_CACHE, "w", encoding="utf-8"), indent=0)

missing = [n for n in names if n not in icon_of]
print(f"{len(icon_of)}/{len(names)} icon names resolved; missing: {', '.join(missing[:30])}")

# download unique icon files
uniq = sorted(set(icon_of.values()))
have = {}
for k, ic in enumerate(uniq):
    fn = os.path.join("wow_icons", "_" + re.sub(r"[^a-z0-9]+", "_", ic.lower()) + ".png")
    if not os.path.exists(fn):
        f = urllib.parse.quote(ic.replace(" ", "_") + ".png")
        url = f"https://warcraft.wiki.gg/wiki/Special:FilePath/{f}"
        for attempt in range(3):
            r = subprocess.run(["curl.exe", "-sL", "--max-time", "30", "-A", UA, url],
                               capture_output=True, timeout=60)
            if r.stdout[:4] == b"\x89PNG":
                with open(fn, "wb") as fh:
                    fh.write(r.stdout)
                break
            time.sleep(20)   # rate-limited or transient — back off and retry
        time.sleep(1.2)
    if os.path.exists(fn):
        have[ic] = fn
    if k % 40 == 0:
        print(f"  {k}/{len(uniq)} files, {len(have)} ok", flush=True)

# map ability name-slug -> icon file
mapping = {}
for name, ic in icon_of.items():
    if ic in have:
        mapping[slug(name)] = have[ic]
json.dump(mapping, open("wow_icon_map.json", "w"), indent=0)
print(f"{len(have)}/{len(uniq)} icon files downloaded; {len(mapping)} abilities mapped")

"""Extract combat values from decompressed Magicka CharacterTemplate dumps.

Heuristic parser anchored on verified structures:
- id / loc-key: first two 7-bit-length strings after the reader header
- HP: first repeated float pair (current==max) in 50..100000
- resistances: int32 count (1..9) + count * 13-byte entries
  {element flag int32, multiplier float, modifier float, immunity byte}
- AI casts: 'CastSpell' blocks -> weight, condition expression, element
  sequence (count + element flags); 'Melee' blocks -> condition only
Writes magicka_bestiary.json.
"""
import glob
import json
import os
import re
import struct

DUMPS = os.path.join(os.environ.get("XNBTOOL", r"C:\Users\alexy\AppData\Local\Temp\claude"
                     r"\C--Projects-GameDesignSkills-RPGSkillHomogenity"
                     r"\c3da8406-d33d-4751-8599-b0ad67c48758\scratchpad\xnbtool"), "dumps")
ELEM = {1: "earth", 2: "water", 4: "cold", 8: "fire", 16: "lightning",
        32: "arcane", 64: "life", 128: "shield", 256: "ice", 512: "steam"}
KEY = {"earth": "D", "water": "Q", "cold": "R", "fire": "F", "lightning": "A",
       "arcane": "S", "life": "W", "shield": "E", "ice": "QR", "steam": "QF"}

def read7bit(b, i):
    n = shift = 0
    while True:
        v = b[i]; i += 1
        n |= (v & 0x7F) << shift
        if not v & 0x80:
            return n, i
        shift += 7

def read_str(b, i):
    n, i = read7bit(b, i)
    return b[i:i+n].decode("utf-8", "replace"), i + n

def parse(path):
    b = open(path, "rb").read()
    out = {"file": os.path.basename(path)[:-4]}
    # header: 7bit reader-name string, then int32 version, int32 reader-count?; find via the
    # known tail "Culture=neutral" then skip to the first small string
    m = b.find(b"Culture=neutral")
    if m == -1:
        return None
    i = m + len(b"Culture=neutral")
    i += 6  # int32 reader version + int16/7bit object header
    try:
        out["id"], i = read_str(b, i)
        loc, i = read_str(b, i)
        out["loc"] = loc.lstrip("#")
        if not re.fullmatch(r"[\x20-\x7e]{2,40}", out["id"]):
            return None
    except Exception:
        return None
    # HP: first equal float pair spaced 13 bytes (value, ..., value) in range
    hp = None
    for j in range(i, min(len(b) - 17, 4000)):
        f1 = struct.unpack_from("<f", b, j)[0]
        if 50 <= f1 <= 100000 and abs(f1 - round(f1)) < 1e-4:
            f2 = struct.unpack_from("<f", b, j + 13)[0]
            if f1 == f2:
                hp = round(f1)
                break
    out["hp"] = hp
    # resistances: count + count*13 entries
    res = None
    for j in range(i, len(b) - 4):
        cnt = struct.unpack_from("<i", b, j)[0]
        if not 1 <= cnt <= 9:
            continue
        entries = []
        k = j + 4
        ok = True
        for _ in range(cnt):
            if k + 13 > len(b):
                ok = False; break
            flag = struct.unpack_from("<i", b, k)[0]
            mult = struct.unpack_from("<f", b, k + 4)[0]
            mod = struct.unpack_from("<f", b, k + 8)[0]
            imm = b[k + 12]
            if flag not in ELEM or not (-4 <= mult <= 4) or not (-5000 <= mod <= 5000) or imm > 1:
                ok = False; break
            entries.append({"elem": ELEM[flag], "mult": round(mult, 3),
                            "mod": round(mod, 2), "imm": bool(imm)})
            k += 13
        if ok and entries:
            res = entries
            break
    out["resist"] = res or []
    # abilities: CastSpell blocks -> weight, condition, cast mode + element seq
    casts = []
    for m2 in re.finditer(b"CastSpell", b):
        j = m2.end()
        weight = struct.unpack_from("<f", b, j)[0] if j + 4 <= len(b) else 0
        cond = ""
        try:
            c, _ = read_str(b, j + 6)
            if re.fullmatch(r"[\x20-\x7e]{3,80}", c):
                cond = c
        except Exception:
            pass
        # signature scan: mode int, count int, count element flags
        found = None
        for k in range(j, min(j + 170, len(b) - 12)):
            mode = struct.unpack_from("<i", b, k)[0]
            cnt = struct.unpack_from("<i", b, k + 4)[0]
            if mode not in (1, 2, 3, 4) or not 1 <= cnt <= 5:
                continue
            elems = []
            p = k + 8
            ok = True
            for _ in range(cnt):
                if p + 4 > len(b):
                    ok = False; break
                fl = struct.unpack_from("<i", b, p)[0]
                if fl not in ELEM:
                    ok = False; break
                elems.append(ELEM[fl])
                p += 4
            if ok and elems:
                found = (mode, elems)
                break
        if found:
            mode, elems = found
            casts.append({"seq": [KEY[s] for s in elems],
                          "mode": {1: "ranged", 2: "area", 3: "self", 4: "weapon"}.get(mode, str(mode)),
                          "cond": cond,
                          "weight": round(weight, 2) if -1000 < weight < 1000 else 0})
    out["casts"] = casts
    out["melee"] = len(re.findall(b"Melee", b))
    return out

rows = []
for p in sorted(glob.glob(os.path.join(DUMPS, "*.bin"))):
    r = parse(p)
    if r and r.get("id"):
        rows.append(r)

with_hp = sum(1 for r in rows if r["hp"])
with_res = sum(1 for r in rows if r["resist"])
with_casts = sum(1 for r in rows if r["casts"])
print(f"{len(rows)} templates parsed · hp: {with_hp} · resistances: {with_res} · casters: {with_casts}")
json.dump(rows, open("magicka_bestiary.json", "w", encoding="utf-8"), indent=1)
for r in rows:
    if r["file"] in ("Beastman_brute", "Boss_Cult_Cold", "Troll_forest", "Yeti", "Dragon_frost"):
        print(r["file"], "hp:", r["hp"], "res:", r["resist"],
              "casts:", [(c["seq"], c["cond"]) for c in r["casts"]][:3])

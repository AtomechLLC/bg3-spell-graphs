"""Extract BG3 spell stats, spell lists, progressions, and localization to bg3_data/."""
import os
import re
from bg3pak import read_entries, extract

BG3 = r"Z:\SteamLibrary\steamapps\common\Baldurs Gate 3\Data"
WANT = re.compile(
    r"Public/(Shared|SharedDev|Gustav|GustavDev|GustavX)/"
    r"(Stats/Generated/Data/Spell_[A-Za-z]+\.txt|Lists/SpellLists\.lsx|Progressions/Progressions\.lsx)$"
    r"|Localization/English/english\.loca$"
    r"|english\.loca$")
PAKS = ["Shared.pak", "Gustav.pak", "GustavX.pak", "Patch8_HotFix9.pak",
        os.path.join("Localization", "English.pak")]

os.makedirs("bg3_data", exist_ok=True)
for pakname in PAKS:
    path = os.path.join(BG3, pakname)
    if not os.path.exists(path):
        print(f"missing {pakname}")
        continue
    n = 0
    for e in read_entries(path):
        if WANT.search(e.name):
            out = os.path.join("bg3_data", e.name.replace("/", "__"))
            with open(out, "wb") as f:
                f.write(extract(path, e))
            n += 1
    print(f"{pakname}: {n} files")

import sys
import re
from bg3pak import read_entries

pak = sys.argv[1]
pat = re.compile(sys.argv[2], re.I) if len(sys.argv) > 2 else None
entries = read_entries(pak)
print(f"{len(entries)} entries in {pak}")
n = 0
for e in entries:
    if pat is None or pat.search(e.name):
        print(f"  {e.size_raw:9} {e.name}")
        n += 1
        if n >= int(sys.argv[3] if len(sys.argv) > 3 else 40):
            print("  ...")
            break

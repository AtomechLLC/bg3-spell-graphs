"""Cross-class spell list overlap stats for the SRD."""
import json
from collections import defaultdict

spells = json.load(open("spells_2014.json", encoding="utf-8"))
class_lists = defaultdict(set)
share_count = defaultdict(list)
for s in spells:
    cs = sorted(c["name"] for c in s.get("classes", []))
    for c in cs:
        class_lists[c].add(s["name"])
    share_count[len(cs)].append(s["name"])

print("spells per class:")
for c in sorted(class_lists):
    print(f"  {c}: {len(class_lists[c])}")

print("\nhow many class lists each spell appears on:")
for n in sorted(share_count, reverse=True):
    print(f"  on {n} lists: {len(share_count[n])} spells")
print("\nspells on 5+ lists:")
for n in sorted(share_count, reverse=True):
    if n >= 5:
        for name in sorted(share_count[n]):
            print(f"  [{n}] {name}")

print("\noverlap matrix (row: % of row-class list also on column-class list):")
classes = sorted(class_lists)
print("        " + "  ".join(f"{c[:4]:>5}" for c in classes))
for a in classes:
    row = []
    for b in classes:
        if a == b:
            row.append("    -")
        else:
            pct = 100 * len(class_lists[a] & class_lists[b]) / len(class_lists[a])
            row.append(f"{pct:4.0f}%")
    print(f"{a:>8}" + " ".join(f"{x:>5}" for x in row))

total_unique = len({s["name"] for s in spells})
total_slots = sum(len(v) for v in class_lists.values())
print(f"\n{total_unique} unique spells fill {total_slots} class-list slots "
      f"({total_slots/total_unique:.2f} lists per spell on average)")

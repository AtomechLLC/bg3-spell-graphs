import json

d = json.load(open("wow_spells.json", encoding="utf-8"))
mage = [r for r in d if "Mage" in r["classes"]]
print(f"Mage: {len(mage)}")
for r in mage[:45]:
    print(f"{r['level']:3} | {r['name'][:32]:32} | rk{r['rank_count']:2} | "
          f"{r['school']:7} | {r['skillline'][:12]:12} | {(r['desc'] or '')[:60]}")

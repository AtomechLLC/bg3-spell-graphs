import csv
import random

rows = list(csv.DictReader(open("purpose_tagged.csv", encoding="utf-8")))
fb = [r for r in rows if r["assigned_by"] == "fallback"]
random.seed(3)
for r in random.sample(fb, 30):
    print(f"{r['game'][:4]:5} {r['ability']}")
print("\nspot checks:")
for name in ["Fireball", "Web", "Wall of Fire", "Blink", "Charm Person", "Banish",
             "Turn Undead", "Blessing of Salvation", "Bear Form", "Tremor Totem",
             "Moonfire", "Vanish", "Slow Fall", "Detect Magic", "Portal: Stormwind"]:
    hits = [r for r in rows if r["ability"] == name]
    for h in hits:
        print(f"  {h['game'][:4]:5} {h['ability']:24} -> {h['purpose']:10} ({h['assigned_by']})")

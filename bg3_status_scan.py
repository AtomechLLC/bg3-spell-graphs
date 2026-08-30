"""Extract ApplyStatus status IDs from BG3 spell functors and group spells by
shared status — the aura-code trick from the WoW analysis, applied to BG3."""
import json
import re
from collections import defaultdict

recs = json.load(open("bg3_spells.json", encoding="utf-8"))
pop = [r for r in recs if r["is_spell"] and not r["upcast_variant"] and not r["container"]]

STATUS = re.compile(r"ApplyStatus\(\s*([A-Z0-9_]+)")
by_status = defaultdict(set)
for r in pop:
    blob = " ".join([r.get("status_apply", ""), r.get("spell_success", ""),
                     r.get("properties", "")])
    for m in STATUS.finditer(blob):
        by_status[m.group(1)].add(r["name"])

CC_WORDS = ("PRONE", "RESTRAIN", "BLIND", "SLEEP", "CHARM", "FEAR", "FRIGHT",
            "PARALY", "SILENC", "STUN", "SHEEP", "POLYMORPH", "HELD", "HOLD",
            "COMMAND", "CONFUS", "LAUGHTER", "DANCE", "HYPNO", "BANISH", "SLOW",
            "INCAPACITAT", "DOMINAT")
print("--- control-flavored statuses shared by 2+ spells ---")
for st, names in sorted(by_status.items()):
    if len(names) >= 2 and any(w in st for w in CC_WORDS):
        print(f"{st:28} {', '.join(sorted(names))}")

print("\n--- name check for planned family members ---")
have = {r["name"] for r in pop}
for n in ["Fear", "Confusion", "Command", "Tasha's Hideous Laughter",
          "Otto's Irresistible Dance", "Hypnotic Pattern", "Blindness", "Banishment",
          "Slow", "Flame Blade", "Shadow Blade", "Magic Weapon", "Elemental Weapon",
          "Divine Favour", "Crusader's Mantle", "Fly", "Longstrider", "Enhance Leap",
          "Feather Fall", "Freedom of Movement", "Gaseous Form", "Misty Step",
          "Dimension Door", "Speak with Animals", "Speak with Dead", "Detect Thoughts",
          "Knock", "Friends", "Disguise Self", "Feign Death", "Darkvision"]:
    print(f"  {n}: {n in have}")

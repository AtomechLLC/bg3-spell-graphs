import csv

LMOP = ["Aid", "Augury", "Beacon of Hope", "Bless", "Blur", "Burning Hands", "Charm Person",
        "Command", "Comprehend Languages", "Cure Wounds", "Dancing Lights", "Darkness",
        "Detect Magic", "Dispel Magic", "Fireball", "Flaming Sphere", "Fly", "Guidance",
        "Guiding Bolt", "Healing Word", "Hold Person", "Identify", "Inflict Wounds",
        "Invisibility", "Lesser Restoration", "Light", "Lightning Bolt", "Mage Armor",
        "Mage Hand", "Magic Missile", "Mass Healing Word", "Misty Step", "Prayer of Healing",
        "Prestidigitation", "Protection from Energy", "Ray of Frost", "Resistance",
        "Revivify", "Sacred Flame", "Sanctuary", "Shield", "Shield of Faith",
        "Shocking Grasp", "Silence", "Sleep", "Spider Climb", "Spiritual Weapon",
        "Suggestion", "Thaumaturgy", "Thunderwave", "Warding Bond", "Web"]

tags = {}
with open("spells_tagged_by_family.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        tags[row["spell"].lower()] = row

in_fam, no_fam, not_srd = [], [], []
for s in LMOP:
    r = tags.get(s.lower()) or tags.get(s.lower().replace("from", "from"))
    if not r and s == "Protection from Energy":
        r = tags.get("protection from energy")
    if not r:
        not_srd.append(s)
    elif r["family"]:
        in_fam.append(f"{s} -> {r['family_icon']} {r['family']} ({r['tier']})")
    else:
        no_fam.append(s)

print(f"{len(LMOP)} spells: {len(in_fam)} in families, {len(no_fam)} singletons, {len(not_srd)} not in SRD")
print("\nIN FAMILIES:")
for x in in_fam:
    print(" ", x)
print("\nNOT IN SRD:", ", ".join(not_srd))

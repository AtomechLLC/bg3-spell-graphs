"""Azeroth Archetypes: 11 design-school spell archetypes, each expanded into
its real WoW Classic variations with authentic icons -> wow_archetypes.html.

Every listed spell is validated against wow_spells.json at build time;
icons come from the local icon set via build_wow_codex.ICON_MAP.
"""
import base64
import contextlib
import io as iolib
import json
import os
import re

from PIL import Image

with contextlib.redirect_stdout(iolib.StringIO()):
    import build_wow_codex as W

RECS = {r["name"]: r for r in W.RECS}
CLASSCOL = {"Warrior": "#C79C6E", "Paladin": "#F58CBA", "Hunter": "#ABD473",
            "Rogue": "#FFF569", "Priest": "#E8E6EF", "Shaman": "#0070DE",
            "Mage": "#69CCF0", "Warlock": "#9482C9", "Druid": "#FF7D0A"}

def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

ICON_URIS = {}
def icon(name):
    s = slug(name)
    p = W.ICON_MAP.get(s)
    if not p or not os.path.exists(p):
        return None
    if s not in ICON_URIS:
        buf = iolib.BytesIO()
        Image.open(p).convert("RGBA").resize((44, 44), Image.LANCZOS).save(buf, "WEBP", quality=82)
        ICON_URIS[s] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    return s

ARCH = [
    ("Basic Missile", "one bolt of typed damage — the most re-sold design in the game",
     ["Fireball", "Frostbolt", "Shadow Bolt", "Smite", "Wrath", "Starfire",
      "Lightning Bolt", "Arcane Missiles", "Mind Blast"]),
    ("Heal Other", "RegainHitPoints with a class stamp and a delivery knob",
     ["Healing Touch", "Flash Heal", "Greater Heal", "Lesser Heal", "Holy Light",
      "Flash of Light", "Healing Wave", "Lesser Healing Wave", "Chain Heal", "Regrowth"]),
    ("Petrify Monster", "hard crowd control, priced by legal target type",
     ["Polymorph", "Sap", "Hibernate", "Shackle Undead", "Banish", "Freezing Trap",
      "Fear", "Scare Beast", "Turn Undead"]),
    ("Corrupted Ground", "a persistent damaging zone painted on the floor",
     ["Blizzard", "Rain of Fire", "Flamestrike", "Consecration", "Hurricane",
      "Volley", "Hellfire", "Magma Totem"]),
    ("Empower Ally", "a long-duration stat buff sold on every class list",
     ["Power Word: Fortitude", "Mark of the Wild", "Arcane Intellect", "Blessing of Might",
      "Blessing of Wisdom", "Battle Shout", "Divine Spirit", "Thorns"]),
    ("Summon Wolf", "a persistent combat companion from a menu",
     ["Summon Imp", "Summon Voidwalker", "Summon Succubus", "Summon Felhunter",
      "Call Pet", "Tame Beast", "Inferno", "Ritual of Doom"]),
    ("Curse Enemy", "a lasting tag that degrades the target",
     ["Curse of Agony", "Curse of Weakness", "Curse of the Elements", "Curse of Recklessness",
      "Curse of Tongues", "Hunter's Mark", "Faerie Fire", "Demoralizing Shout"]),
    ("Smiting Strike", "weapon hit plus a rider, on every melee list",
     ["Heroic Strike", "Mortal Strike", "Sinister Strike", "Backstab", "Raptor Strike",
      "Stormstrike", "Cleave", "Hamstring", "Mongoose Bite"]),
    ("Emergency Escape", "the panic button — break contact, cheat death",
     ["Blink", "Vanish", "Feign Death", "Divine Shield", "Disengage", "Fade",
      "Ice Block", "Divine Protection"]),
    ("Stealth", "unseen until you strike",
     ["Stealth", "Prowl", "Shadowmeld", "Distract"]),
    ("Create Food", "spell slots become rest-economy resources",
     ["Conjure Food", "Conjure Water", "Create Healthstone", "Create Soulstone",
      "Create Spellstone", "Create Firestone", "Conjure Mana Ruby", "Conjure Mana Jade"]),
]

rows_html = []
missing = []
total = 0
for i, (title, sub, names) in enumerate(ARCH, 1):
    chips = []
    for n in names:
        r = RECS.get(n)
        if not r:
            missing.append(n)
            continue
        total += 1
        cls = r["classes"][0] if r["classes"] else ""
        col = CLASSCOL.get(cls, "#8a879a")
        ic = icon(n)
        img = f'<img src="__I{ic}__" alt="" loading="lazy">' if ic else '<span class="noic"></span>'
        chips.append(f'<span class="sp" style="--c:{col}" title="{cls}">{img}{n}</span>')
    rows_html.append(f'''<div class="arow">
  <div class="hub"><span class="num">{i}</span><span class="ht">{title}
  <small>{sub}</small></span></div>
  <div class="fan">{''.join(chips)}</div>
</div>''')
if missing:
    print("not in trainer data (dropped):", ", ".join(missing))

DISCORD = ('<svg viewBox="0 0 127.14 96.36" width="16" height="12" fill="currentColor" aria-hidden="true">'
           '<path d="M107.7,8.07A105.15,105.15,0,0,0,81.47,0a72.06,72.06,0,0,0-3.36,6.83A97.68,97.68,0,0,'
           '0,49,6.83,72.37,72.37,0,0,0,45.64,0,105.89,105.89,0,0,0,19.39,8.09C2.79,32.65-1.71,'
           '56.6.54,80.21h0A105.73,105.73,0,0,0,32.71,96.36,77.7,77.7,0,0,0,39.6,85.25a68.42,68.42,'
           '0,0,1-10.85-5.18c.91-.66,1.8-1.34,2.66-2a75.57,75.57,0,0,0,64.32,0c.87.71,1.76,1.39,'
           '2.66,2a68.68,68.68,0,0,1-10.87,5.19,77,77,0,0,0,6.89,11.1A105.25,105.25,0,0,0,126.6,'
           '80.22h0C129.24,52.84,122.09,29.11,107.7,8.07ZM42.45,65.69C36.18,65.69,31,60,31,53s5-12.74,'
           '11.43-12.74S54,46,53.89,53,48.84,65.69,42.45,65.69Zm42.24,0C78.41,65.69,73.25,60,73.25,'
           '53s5-12.74,11.44-12.74S96.23,46,96.12,53,91.08,65.69,84.69,65.69Z"/></svg>')
FSC = (f'<a class="fsc" href="http://funsmith.club" target="_blank" rel="noopener" '
       f'title="Funsmith Club — game design community on Discord">{DISCORD}funsmith.club</a>')

HTML = f"""<title>Azeroth Archetypes</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#101016;color:#E8E6EF;font:400 13px/1.5 "IBM Plex Mono",ui-monospace,monospace;
  min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:22px 18px 34px}}
header{{width:100%;max-width:1250px;display:flex;align-items:flex-start;justify-content:space-between;
  gap:12px;flex-wrap:wrap;margin-bottom:16px}}
h1{{font:600 22px Cinzel,Georgia,serif;color:#E3C377;margin:0;letter-spacing:.06em}}
.sub{{color:#A7A4B3;font-size:11.5px}}
.fsc{{display:inline-flex;align-items:center;gap:7px;border:1px solid #3a3647;
  border-radius:999px;padding:4px 12px;font:500 11px "IBM Plex Mono",monospace;color:#C9C6D4;
  text-decoration:none;letter-spacing:.05em}}
.fsc:hover{{border-color:#D4AF5E;color:#E3C377}}
.arow{{width:100%;max-width:1250px;display:flex;gap:0;align-items:stretch;margin-bottom:14px}}
.hub{{flex:0 0 300px;display:flex;align-items:center;gap:0;background:#EDEAF3;border:2px solid #6A63D9;
  border-radius:12px;overflow:hidden;position:relative;z-index:1}}
.num{{flex:0 0 62px;align-self:stretch;display:flex;align-items:center;justify-content:center;
  font:700 22px "IBM Plex Mono",monospace;color:#1B1750;border-right:2px solid #6A63D9;
  border-radius:10px 14px 14px 10px;background:#F5F3F8}}
.ht{{padding:10px 14px;font:700 15px/1.25 "IBM Plex Mono",monospace;color:#1B1750}}
.ht small{{display:block;font:400 10px/1.4 "IBM Plex Mono",monospace;color:#5a5480;margin-top:3px}}
.fan{{flex:1;display:flex;flex-wrap:wrap;gap:6px;align-content:center;padding:8px 0 8px 26px;
  position:relative}}
.fan::before{{content:"";position:absolute;left:0;top:50%;width:26px;height:2px;background:#6A63D9}}
.sp{{display:inline-flex;align-items:center;gap:7px;background:#15131C;border:1px solid #2A2734;
  border-left:3px solid var(--c);border-radius:8px;padding:3px 10px 3px 4px;font-size:11.5px;
  color:#C9C6D4;white-space:nowrap}}
.sp:hover{{border-color:var(--c);color:#E8E6EF}}
.sp img{{width:24px;height:24px;border-radius:5px;display:block}}
.noic{{width:24px;height:24px;border-radius:5px;background:#2A2734;display:inline-block}}
footer{{color:#8a879a;font-size:11px;margin-top:14px;max-width:1250px;text-align:center;line-height:1.8}}
::selection{{background:#D4AF5E44}}
@media (max-width:760px){{.arow{{flex-direction:column}}.hub{{flex:none}}.fan{{padding:10px 0 0}}
.fan::before{{display:none}}}}
</style>
<header>
  <div><h1>Azeroth Archetypes</h1>
  <div class="sub">eleven textbook spell archetypes — and the {total} real WoW Classic abilities
that are each archetype re-sold with a class stamp, from the game's own trainer data</div></div>
  {FSC}
</header>
{chr(10).join(rows_html)}
<footer>chip border = class colour (hover for the class) · icons from the game's own icon set ·
one design, many SKUs: every archetype on this poster shipped at least four times in vanilla —
the homogeneity thesis of the whole study, in one picture · companion pages: the Azeroth Codex
(families &amp; the twin matrix) and Azeroth Constellations ·
World of Warcraft © Blizzard Entertainment; research reference</footer>
"""
for s, uri in ICON_URIS.items():
    HTML = HTML.replace(f"__I{s}__", uri)
with open("wow_archetypes.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"wow_archetypes.html: {os.path.getsize('wow_archetypes.html') / 1024:.0f} KB "
      f"({total} spells across {len(ARCH)} archetypes, {len(ICON_URIS)} icons)")

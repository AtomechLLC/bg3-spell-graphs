# Methodology

**Source.** The game's own client database tables for **WoW Classic Era** (build 1.15.9.69547), fetched as CSV from [wago.tools](https://wago.tools): `SpellName`, `Spell` (tooltips), `SkillLineAbility` + `SkillLine` (class attribution via class masks), `SpellLevels`, `SpellMisc` (school masks). Population: abilities in the nine classes' skill lines with a trainer level requirement — filtering out talents, hidden procs, and Season of Discovery additions (spell ids ≥ 100000, Engraving/Runes lines). **423 distinct abilities** remain, spanning **1388 spellbook entries** once ranks are counted.

**The rank clone farm.** 965 of those entries (70%) are rank duplicates — the same spell re-taught with bigger numbers. Classic's ranks are BG3's upcast clones and D&D's spell-level laddering taken to their logical extreme: two-thirds of the classic spellbook is the same spell again.

**Similarity.** Classic tooltips are already macro-parameterized in the data (`$s1`, `$d`, `${formulas}`) — Blizzard's own template variables. Masking replaces those macros plus schools, elements, creature types, cities, and stat names with tokens; token-level sequence similarity over the masked tooltips then measures how much *sentence* is shared. Highest rank per ability is analyzed; ranks collapse first.

**Icons.** Fetched from [warcraft.wiki.gg](https://warcraft.wiki.gg) (the community wiki), by reading each ability page's infobox `icon=` parameter through the MediaWiki API — batched and throttled. Icons © Blizzard Entertainment, shown for research reference.

**Known limits.** Talents are excluded (trainer spellbook only); pet abilities excluded; Classic Era data includes minor anniversary-era tuning. Cross-era comparison uses the same masks as the SRD and BG3 studies but the population definitions differ slightly per game — the headline percentages are directional, not decimal-precise.

**Reproduce.** `wow_dataset.py` → `wow_analyze.py` → `wow_icons.py` → `build_wow_codex.py`. Companion codices: the D&D 5e SRD and Baldur's Gate 3.

---
*Linked from: [[families/aspects|The Aspect Dial]] · [[families/auras|The Aura Carousel]] · [[families/blessings|The Blessing Rack]] · [[families/bolts|The Bolt Engine]] · [[families/cat-is-rogue|The Druid Costume Shop]] · [[families/cleanses|The Cleanse Counter]] · [[families/conjured|The Conjured Commissary]] · [[families/curses|The Curse Catalogue]] · [[families/dots|The Affliction Engine]] · [[families/fears|The Fear Franchise]] · [[families/group-ladder|The Greater Ladder]] · [[families/heals|One Heal, Nine Names]] · [[families/interrupts|The Interrupt Union]] · [[families/mirror|Amplify & Dampen]] · [[families/poisons|The Numbered Vials]] · [[families/polymorph|The Polymorph Barn]] · [[families/protection|The Protection Rack]] · [[families/rez|The Resurrection Union]] · [[families/seals|The Seal Press]] · [[families/shocks|The Shock Battery]] · [[families/stings|The Sting Clip]] · [[families/summons|The Stable & The Circle]] · [[families/teleports|The Hearth Network]] · [[families/totems|The Totem Foundry]] · [[families/tracking|The Tracking Dial]] · [[findings|The Identical-Spell List]] · [[overview|Overview]]*

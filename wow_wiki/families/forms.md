# <span class="femoji">🐻</span> The Form Rack

<span class="plate"><span class="tier tier-template">Shared template</span><span class="pv"><b>9</b> abilities</span><span class="pv">similarity <b>0.27–1.00</b></span><span class="pv"><b>2</b> classes</span><span class="pv pvc">Druid, Warrior</span></span>

| Ability | Class | Level | School | Ranks | Tooltip |
|---|---|---|---|---|---|
| <img class="sic" data-i="bear-form" alt=""> **Bear Form** | Druid | 10 | Physical | 1 | Shapeshift into a bear, increasing melee attack power by X, armor contribution from items by X%, and health by |
| <img class="sic" data-i="aquatic-form" alt=""> **Aquatic Form** | Druid | 16 | Physical | 1 | Shapeshift into aquatic form, increasing swim speed by X% and allowing the druid to breathe underwater.  Also  |
| <img class="sic" data-i="cat-form" alt=""> **Cat Form** | Druid | 20 | Physical | 1 | Shapeshift into cat form, increasing melee attack power by X plus Agility.  Also protects the caster from Poly |
| <img class="sic" data-i="travel-form" alt=""> **Travel Form** | Druid | 30 | Physical | 1 | Transforms the druid into a travel form, increasing movement speed by X%.  Also protects the caster from Polym |
| <img class="sic" data-i="dire-bear-form" alt=""> **Dire Bear Form** | Druid | 40 | Physical | 1 | Shapeshift into a dire bear, increasing melee attack power by X, armor contribution from items by X%, and heal |
| <img class="sic" data-i="moonkin-form" alt=""> **Moonkin Form** | Druid | 40 | Physical | 1 | Transforms the Druid into Moonkin Form.  While in this form the armor contribution from items is increased by  |
| <img class="sic" data-i="battle-stance" alt=""> **Battle Stance** | Warrior | 1 | Physical | 1 | A balanced combat stance. |
| <img class="sic" data-i="defensive-stance" alt=""> **Defensive Stance** | Warrior | 10 | Physical | 1 | A defensive combat stance.  Decreases damage taken by X% and damage caused by X%.  Increases threat generated. |
| <img class="sic" data-i="berserker-stance" alt=""> **Berserker Stance** | Warrior | 30 | Physical | 1 | An aggressive stance.  Critical hit chance is increased by X% and all damage taken is increased by X%. |

**Shared skeleton.** Every druid form is the identical two-aura package: `Shapeshift (X)` plus `Immunity - Mechanic (Polymorphed)`, all clustering above 0.78. The Warrior's stances run the *same `Shapeshift` aura* with the fur removed — the effect data files Battle, Defensive, and Berserker Stance as forms.

**What varies.** The form or stance, its stat payload, and which kit it unlocks.

**Design read.** One mode-switch chassis across two classes; the abilities each mode unlocks are filed in the function families they belong to (the cat's openers with the [[families/melee-enhance|strikes]], the bear's roar with the [[families/threat|Aggro Ledger]]).

Full list: [[findings|The Identical-Spell List]] · scoring: [[methodology|Methodology]]

---
*Linked from: [[classes/druid|Druid]] · [[classes/warrior|Warrior]] · [[findings|The Identical-Spell List]] · [[spells|All Abilities, Tagged]]*

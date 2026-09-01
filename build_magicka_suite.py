"""Magicka Lenses: the three Magicka views in one page -> magicka.html.

Each lens (element wheel, casting tree, hooks) is embedded whole as a
same-origin srcdoc frame, so swapping tabs never reloads and each view
keeps its own state - a queued sequence in the builder survives a trip
to the wheel and back. The per-page tab rows and their scripts are
stripped from the embedded copies; one sticky bar drives all three.
Run AFTER the three page builders.
"""
import os

VIEWS = [("wheel", "ELEMENT WHEEL", "magicka_map.html"),
         ("tree", "CASTING TREE", "magicka_tree.html"),
         ("hooks", "HOOKS", "magicka_hooks.html"),
         ("bestiary", "BESTIARY", "magicka_bestiary.html")]

def load(fn):
    s = open(fn, encoding="utf-8").read()
    a = s.find('<div class="mtabs"')
    if a != -1:
        b = s.find("</div>", a)
        s = s[:a] + s[b + 6:]
    a = s.find("<script>\n(function () {\n  var CUR")
    if a != -1:
        b = s.find("</script>", a)
        s = s[:a] + s[b + 9:]
    return s.replace("&", "&amp;").replace('"', "&quot;")

frames = "\n".join(
    f'<iframe data-v="{vid}"{" class=on" if i == 0 else ""} title="{lab.title()}" '
    f'srcdoc="{load(fn)}"></iframe>'
    for i, (vid, lab, fn) in enumerate(VIEWS))
tabs = "".join(
    f'<a data-v="{vid}"{" class=on" if i == 0 else ""}>{lab}</a>'
    for i, (vid, lab, fn) in enumerate(VIEWS))

HTML = f"""<title>Magicka Lenses</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#101016}}
.bar{{position:sticky;top:0;z-index:5;display:flex;justify-content:center;
  padding:10px 14px;background:#101016F0;border-bottom:1px solid #2A2734;backdrop-filter:blur(4px)}}
.mtabs{{display:flex;border:1px solid #3a3647;border-radius:7px;overflow:hidden}}
.mtabs a{{color:#A7A4B3;font:500 11.5px "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.08em;
  padding:6px 16px;text-decoration:none;cursor:pointer}}
.mtabs a + a{{border-left:1px solid #3a3647}}
.mtabs a.on{{background:#D4AF5E1f;color:#E3C377;cursor:default}}
.mtabs a:not(.on):hover{{color:#E8E6EF}}
.mtabs a:focus-visible{{outline:2px solid #E3C377;outline-offset:-2px}}
iframe{{display:none;width:100%;border:0}}
iframe.on{{display:block}}
</style>
<div class="bar"><div class="mtabs" role="navigation" aria-label="Magicka views">{tabs}</div></div>
{frames}
<script>
function active() {{ return document.querySelector('iframe.on'); }}
function fit(f) {{
  try {{
    f.style.height = Math.max(600, f.contentDocument.documentElement.scrollHeight + 4) + 'px';
  }} catch (e) {{}}
}}
document.querySelectorAll('iframe').forEach(f =>
  f.addEventListener('load', () => {{ if (f.classList.contains('on')) fit(f); }}));
document.querySelectorAll('.mtabs a').forEach(a => a.addEventListener('click', () => {{
  if (a.classList.contains('on')) return;
  document.querySelectorAll('.mtabs a').forEach(x => x.classList.toggle('on', x === a));
  document.querySelectorAll('iframe').forEach(f =>
    f.classList.toggle('on', f.dataset.v === a.dataset.v));
  setTimeout(() => {{ fit(active()); try {{ active().contentWindow.focus(); }} catch (e) {{}} }}, 0);
  setTimeout(() => fit(active()), 350);
}}));
window.addEventListener('resize', () => fit(active()));
setTimeout(() => fit(active()), 600);
document.addEventListener('keydown', e => {{
  const f = active();
  if (!f || !f.contentDocument) return;
  f.contentDocument.dispatchEvent(new KeyboardEvent('keydown',
    {{key: e.key, bubbles: true, cancelable: true}}));
  if ([' ', 'Backspace', 'ArrowUp', 'ArrowDown'].includes(e.key)) e.preventDefault();
}});
</script>
"""
with open("magicka.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"magicka.html: {os.path.getsize('magicka.html') / 1024:.0f} KB ({len(VIEWS)} lenses, one page)")

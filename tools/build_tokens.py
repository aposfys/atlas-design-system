#!/usr/bin/env python3
"""Regenerate tokens.json from tokens.css. Run from the repository root."""
import json, re, sys

def parse_block(css):
    out = {}
    for m in re.finditer(r'(--[a-zA-Z0-9-]+)\s*:\s*([^;]+);', css):
        name, val = m.group(1)[2:], " ".join(m.group(2).split())
        if val.startswith("var("):        # aliases resolve at use time; export as reference
            out[name] = {"$value": "{" + val[4:-1].strip()[2:] + "}", "$type": "alias"}
        elif re.fullmatch(r'#[0-9a-fA-F]{3,8}', val) or val.startswith(("rgba(", "rgb(")):
            out[name] = {"$value": val, "$type": "color"}
        elif re.fullmatch(r'-?[\d.]+px', val):
            out[name] = {"$value": val, "$type": "dimension"}
        elif re.fullmatch(r'[\d.]+ms', val):
            out[name] = {"$value": val, "$type": "duration"}
        elif val.startswith("cubic-bezier"):
            out[name] = {"$value": val, "$type": "cubicBezier"}
        elif re.fullmatch(r'\d{3}', val):
            out[name] = {"$value": int(val), "$type": "fontWeight"}
        else:
            out[name] = {"$value": val}
    return out

css = open("tokens.css", encoding="utf-8").read()
blocks = re.findall(r'((?::root|\[data-theme="[a-z]+"\])[^{]*)\{(.*?)\n\}', css, re.S)
shared, dark, light = {}, {}, {}
for sel, body in blocks:
    tokens = parse_block(body)
    if "light" in sel and "dark" in sel:  shared.update(tokens)   # the alias block spans both themes
    elif "light" in sel:          light.update(tokens)
    elif "dark" in sel:           dark.update(tokens)
    elif sel.strip().startswith(":root") and "data-theme" not in sel: shared.update(tokens)
    else:                         shared.update(tokens)

doc = {
  "$description": "ATLAS design tokens. Generated from tokens.css by tools/build_tokens.py — edit the CSS, then regenerate; never edit this file.",
  "scale": shared, "dark": dark, "light": light,
}
json.dump(doc, open("tokens.json", "w", encoding="utf-8"), indent=2)
print(f"tokens.json: scale {len(shared)} · dark {len(dark)} · light {len(light)}")

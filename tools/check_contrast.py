#!/usr/bin/env python3
"""The contrast gate. Run from the repository root; exits 1 if any declared
role pair falls under its bar, so the measured claims in NOTES.md cannot
quietly rot. Solid-hex pairs only — glass surfaces are translucent and are
covered by the headroom the text roles keep over --ground."""
import re, sys

CSS = "tokens.css"

# (theme, foreground token, background token, minimum, what the pair is)
PAIRS = [
    ("dark",  "text-primary",     "ground",       4.5, "primary text"),
    ("dark",  "text-secondary",   "ground",       4.5, "secondary text"),
    ("dark",  "text-tertiary",    "ground",       4.5, "tertiary text — the 10px labels"),
    ("dark",  "text-placeholder", "ground",       4.5, "placeholder"),
    ("dark",  "text-accent",      "ground",       4.5, "accent type"),
    ("dark",  "text-on-accent",   "fill-accent",  4.5, "ink on the accent fill"),
    ("dark",  "text-success",     "ground",       4.5, "success text"),
    ("dark",  "text-warning",     "ground",       4.5, "warning text"),
    ("dark",  "text-danger",      "ground",       4.5, "danger text"),
    ("dark",  "text-info",        "ground",       4.5, "info text"),
    ("dark",  "viz-1", "ground", 3.0, "data series 1"),
    ("dark",  "viz-2", "ground", 3.0, "data series 2"),
    ("dark",  "viz-3", "ground", 3.0, "data series 3"),
    ("dark",  "viz-4", "ground", 3.0, "data series 4"),
    ("dark",  "viz-5", "ground", 3.0, "data series 5"),
    ("dark",  "viz-6", "ground", 3.0, "data series 6"),
    ("dark",  "focus-ring", "ground", 3.0, "the focus ring"),
    ("light", "text-primary",     "ground",       4.5, "primary text"),
    ("light", "text-secondary",   "ground",       4.5, "secondary text"),
    ("light", "text-tertiary",    "ground",       4.5, "tertiary text — the 10px labels"),
    ("light", "text-placeholder", "ground",       4.5, "placeholder"),
    ("light", "text-accent",      "ground",       4.5, "accent type"),
    ("light", "text-on-accent",   "fill-accent",  4.5, "ink on the accent fill"),
    ("light", "text-success",     "ground",       4.5, "success text"),
    ("light", "text-warning",     "ground",       4.5, "warning text"),
    ("light", "text-danger",      "ground",       4.5, "danger text"),
    ("light", "text-info",        "ground",       4.5, "info text"),
    ("light", "viz-1", "ground", 3.0, "data series 1"),
    ("light", "viz-2", "ground", 3.0, "data series 2"),
    ("light", "viz-3", "ground", 3.0, "data series 3"),
    ("light", "viz-4", "ground", 3.0, "data series 4"),
    ("light", "viz-5", "ground", 3.0, "data series 5"),
    ("light", "viz-6", "ground", 3.0, "data series 6"),
    ("light", "focus-ring", "ground", 3.0, "the focus ring"),
]

def theme_blocks(css):
    """Split tokens.css into the dark block (:root/[data-theme=dark]) and the
    light block ([data-theme=light]); the shared alias block applies to both."""
    dark_m = re.search(r':root,\s*\[data-theme="dark"\]\s*\{(.*?)\n\}', css, re.S)
    light_m = re.search(r'\[data-theme="light"\]\s*\{(.*?)\n\}', css, re.S)
    shared = re.search(r':root\s*\{(.*?)\n\}', css, re.S)
    def toks(block):
        return {m.group(1)[2:]: " ".join(m.group(2).split())
                for m in re.finditer(r'(--[a-zA-Z0-9-]+)\s*:\s*([^;}]+)[;}]', block)}
    base = toks(shared.group(1)) if shared else {}
    dark = dict(base); dark.update(toks(dark_m.group(1)) if dark_m else {})
    light = dict(dark)  # light is a remap over dark: unremapped primitives persist
    light.update(toks(light_m.group(1)) if light_m else {})
    return {"dark": dark, "light": light}

def resolve(name, toks, depth=0):
    if depth > 12 or name not in toks:
        return None
    v = toks[name]
    if v.startswith("var("):
        return resolve(v[4:-1].strip()[2:], toks, depth + 1)
    return v if re.fullmatch(r'#[0-9a-fA-F]{6}', v) else None

def luminance(hexval):
    r, g, b = (int(hexval[i:i + 2], 16) / 255 for i in (1, 3, 5))
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = lin(r), lin(g), lin(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def main():
    themes = theme_blocks(open(CSS, encoding="utf-8").read())
    failed = 0
    for theme, fg, bg, minimum, why in PAIRS:
        toks = themes[theme]
        a, b = resolve(fg, toks), resolve(bg, toks)
        if a is None or b is None:
            print(f"FAIL  [{theme:5}] --{fg} / --{bg}: token missing or not a resolvable hex")
            failed += 1
            continue
        r = ratio(a, b)
        mark = "ok  " if r >= minimum else "FAIL"
        if r < minimum:
            failed += 1
        print(f"{mark}  [{theme:5}] {r:5.2f}:1  (needs {minimum})  --{fg} on --{bg} — {why}")
    if failed:
        print(f"\n{failed} pair(s) under the bar. The gate is closed.")
        sys.exit(1)
    print(f"\nAll {len(PAIRS)} pairs clear. The gate is open.")

if __name__ == "__main__":
    main()

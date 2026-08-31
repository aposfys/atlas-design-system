# VANE
The interface language for Atlas — a dense, glass-based token system in two themes.

**[Open the showcase →](showcase.html)** — the language applied across palette, type, readout, glass depth, controls, ledger, attention, iconography, geometry and motion, with a theme toggle. `showcase-standalone.html` is the same page with fonts and icons inlined; it opens offline with no network.

![VANE, dark theme](docs/showcase-dark.png)
![VANE, light theme](docs/showcase-light.png)

> **Status: language and tokens only.** The component set — buttons, fields, table, tags, dialog, nav — is the next pass and is not built.

**Rounded glass, two themes.** Dark is navy (#0A1A2F over #061220) with soft chartreuse and blue light blooms behind it, so the blur has something real to refract. Light runs the same device at lower amplitude. One chartreuse (#D4FF4F) carries every action, link and active state. Type is **Gabarito** for the interface and **Spline Sans Mono** for anything numeric; the system's character is the jump between 10px tracked labels and 46px tabular figures with very little in between.

### Using it

```html
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@400;500;600;700&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css" />
<link rel="stylesheet" href="styles.css" />
```

Set `data-theme="dark"` or `"light"` on `<html>`. `styles.css` pulls in `tokens.css` then `base.css`; nothing else is required.

Five rules worth keeping in front of you:

- Use the **semantic** layer only — `--surface`, `--border`, `--text-primary`, `--fill-accent`. Never a primitive.
- `--fill-accent` for backgrounds, `--text-accent` for type. They are not interchangeable.
- Never nest a blurred panel inside another blurred panel.
- One signal per view: one flagged item, one primary button.
- Icons never carry meaning alone and never appear without an accessible name.

### Files

| File | What |
| --- | --- |
| `styles.css` | Entry point. Imports the two token files. |
| `tokens.css` | Colour, type, spacing, geometry, motion. |
| `base.css` | Resets, type defaults, and the `.v-idx` / `.v-panel` / `.v-num` utilities. |
| `showcase.html` | The language applied, with the theme toggle. |
| `showcase-standalone.html` | The showcase as one self-contained file. Compiled output; edit `showcase.html`, never this. |

### More

- [The language, token structure, themes and iconography](docs/LANGUAGE.md)
- [Accessibility, glass caveats and what is still open](docs/NOTES.md)

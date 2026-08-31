# VANE

The interface language for Atlas. A fresh system — the Condos DS was the starting
reference, not the model. Three things were taken from it and everything visual is new.

## Taken from the reference

- **Density.** 12–14px carries the interface. The reference is a dense enterprise system and that is the correct instinct for a data product; nothing here was inflated to a comfortable-looking 16px.
- **The 1.75px base grid.** The reference's spacing scale runs on a 1.75 unit rather than 4 or 8. It is invisible, it is unusual, and it works.
- **Mono numerics.** Every figure, reference and identifier is monospaced and tabular.

Nothing else. The ice-blue, the navy, the cyan primary, the coral, the blue-tinted slate ramp, the rounded PrimeVue chrome — all dropped.

## The language

**Rounded glass, two themes.** The dark theme — what the system was designed in — is navy (#0A1A2F over #061220) with soft chartreuse and blue light blooms behind it, so the blur has something real to refract. The light theme runs the same device at lower amplitude: a pale ground (#F2F5F8 over #E7ECF1), the same blooms faded back, and glass as frosted white at 58% instead of tinted white at 5.5%. One chartreuse (#D4FF4F) carries every action, link and active state; status colours sit at low opacity so they never compete with it. Radii run 6 / 10 / 14 — inner elements, panels and controls, then the app frame. Pill is reserved for tags, progress tracks and avatars.

Three devices do the structural work:

**The index label** — a 10px tracked mono label with a numbered accent prefix and a hairline running to the end of the column. Every block of content opens with one.

**Glass** — panels are translucent white (5.5–12.5%) over the navy with an 18px blur, 30px on the app frame. A 1px gradient sheen along the top edge stands in for elevation; nothing casts a shadow downward. There is no `box-shadow` in the system except the accent glow on a hovered primary button.

**The rule** — inside glass, content separates with hairlines, never with nested cards. Figures sit in one divided panel, not in separate tiles. Tables are the primary surface, with an accent-tint hover instead of striping.

Type is **Gabarito** for the interface and **Spline Sans Mono** for anything numeric. The system's character is the jump between 10px tracked labels and 46px tabular figures with very little in between.

## Files

| File | What |
| --- | --- |
| `styles.css` | Entry point. Imports the two token files. |
| `tokens.css` | Colour, type, spacing, geometry, motion. |
| `base.css` | Resets, type defaults, and the `.v-idx` / `.v-panel` / `.v-num` utilities. |
| `showcase.html` | The language applied across palette, type, readout, glass depth, controls, ledger, attention, iconography, geometry, motion. Carries the theme toggle. |
| `showcase-standalone.html` | The showcase as one self-contained file — fonts and icons inlined, opens offline with no network. Compiled output; edit `showcase.html`, never this. |

## Token structure

Two layers, and the split is load-bearing:

1. **Primitives** — raw values, declared per theme (`--navy-900`, `--lime-400`, `--d-16`). Never referenced by a component.
2. **Semantic** — role names, the only layer components may use: `--ground`, `--surface`, `--border`, `--text-primary`, `--fill-accent`, `--tint-success`, and so on.

A component that reaches past the semantic layer breaks when the theme flips. That is not hypothetical — it is what happened to the accent before it was split into `--fill-accent` (a background) and `--text-accent` (type).

Short aliases (`--ink`, `--ac`, `--glass`) exist at the end of `tokens.css` so older markup keeps working. Every one is a pointer, not a value. New work should use the semantic names.

## Themes

`[data-theme="dark"]` is the default; `[data-theme="light"]` remaps every semantic alias. It is a remap, not an inversion, and three things had to change beyond luminance:

- **Hairlines invert.** On dark, lines are white at 10–26%. On light, white-on-white has no edge, so they become navy at 10–26%.
- **Glass opacity climbs.** 5.5% white over navy reads as glass; 5.5% white over pale grey reads as nothing. Light glass sits at 58–90% — frosted rather than tinted.
- **The accent splits in two.** Chartreuse works as a *fill* in both themes with dark ink on it, but as *text* on a pale ground it measures 1.3:1. So `--fill-accent` (backgrounds) and `--text-accent` (type, icons, the index prefix) are separate tokens; light drops `--text-accent` to a deep lime #4A6606 at 6.0:1. Anything colouring type must use `--text-accent`, never `--fill-accent`.

The showcase carries a toggle and remembers the choice. The toggle itself is a **solid** segmented control, not glass — glass nested inside glass is the one thing the system forbids, and the toggle sits inside the glass masthead.

## Iconography

**Phosphor**, regular weight, from CDN:

```html
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css" />
<i class="ph ph-receipt"></i>
```

- **Regular weight only.** Never mixed with bold, fill or duotone — the mix is the fastest way to make an icon set look borrowed.
- **Sized in em**, so a glyph tracks the label beside it. Standalone sizes are 14 / 16 / 20 / 24px. `.v-icon` sets 1.15em, which is the in-line default.
- **Inherit `currentColor`.** An icon is never given its own colour; it takes the colour of the text it sits with.
- **Never alone without an accessible name.** Icon-only controls carry `aria-label`; decorative glyphs carry `aria-hidden`.
- **Never the sole carrier of meaning.** A state is a tag plus a word. Icons in `.flag` repeat what the copy already says.
- **No emoji.**

## Accessibility

- **Contrast, both themes.** All four text roles clear AA for normal text at 10px, which matters because the system's signature label runs at exactly that size — the labels were never going to be enlarged, so the colours had to carry it. Measured against `--ground` in each theme:

  | Role | Dark | Light |
  | --- | --- | --- |
  | `--text-primary` | 15.7:1 | 16.1:1 |
  | `--text-secondary` | 8.8:1 | 6.6:1 |
  | `--text-tertiary` | 5.9:1 | 5.2:1 |
  | `--text-placeholder` | 4.8:1 | 5.0:1 |
  | `--text-accent` | 15.2:1 | 6.0:1 |

  Status text clears AA in both themes too (light: success 5.0:1, warning 5.4:1, danger 5.4:1; dark: all above 6.3:1). Dark ink on the accent fill measures 14.0:1 dark / 12.8:1 light. Both sets keep headroom for the light blooms, which raise background luminance under the text. The light theme's tertiary, placeholder and status tones were all re-derived — the first pass failed at 4.35:1, 4.06:1 and below.
- **Focus.** A 2px chartreuse outline at 2px offset on every interactive element, never removed.
- **Colour is never the only carrier.** Trend direction pairs the colour with a sign, tags pair the tint with a word, invalid fields pair the border with error copy and `aria-invalid`.
- **Touch targets** floor at 44px (`--touch`); the 34px control height is for pointer surfaces only.
- **Motion** respects `prefers-reduced-motion`, which collapses both durations to 1ms.

## Glass caveats

Backdrop blur is the whole visual premise, so two things matter. It needs light behind it — `body::before` paints the blooms, and a glass panel dropped onto a flat fill will read as grey mush. And it is GPU work: keep the number of simultaneously visible blurred layers low, and never nest a blurred panel inside another one. The light theme is the more fragile of the two — frosted white has far less contrast against its ground than tinted white has against navy, so a light-theme panel needs its hairline to define the edge. `base.css` carries an `@supports not (backdrop-filter)` fallback that raises the fill opacity where blur is unavailable.

## Using it

```html
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@400;500;600;700&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css" />
<link rel="stylesheet" href="styles.css" />
```

Set `data-theme="dark"` or `"light"` on `<html>`. `styles.css` pulls in `tokens.css` then `base.css`; nothing else is required.

Rules worth keeping in front of you:

- Use the **semantic** layer only — `--surface`, `--border`, `--text-primary`, `--fill-accent`. Never a primitive.
- `--fill-accent` for backgrounds, `--text-accent` for type. They are not interchangeable.
- Never nest a blurred panel inside another blurred panel.
- One signal per view: one flagged item, one primary button.
- Icons never carry meaning alone and never appear without an accessible name.

## Open

- **Content is placeholder.** The showcase is shaped like a ledger because that is the component structure carried over from the reference. The personal project has no name or description on record, so copy, navigation and screens can't be made real yet.
- **No components built.** This is the language and the token system. The component set (buttons, fields, table, tags, dialog, nav) and the screens are the next pass.
- **Fonts are CDN-linked.** Gabarito and Spline Sans Mono load from Google Fonts; Phosphor from unpkg. Self-host them before production.
- **Known nit.** `base.css` sets `border-radius: var(--r-sm)` inside the shared `:focus-visible` rule, which snaps pill and frame-radius elements to 6px while focused. The rule uses `:where()` so any component can override it, but the focus style should be moved to `outline` alone when the component layer lands.

## Not carried over

Trimmed from the working folder when this was published, recoverable from the original if wanted:

- `chooser.html` — the live picker used to settle radius and type. Its decisions are already baked into `tokens.css`.
- `reference/fig-tokens.css` — all 2,174 variables extracted from the Figma file, kept for lookup only. Superseded by `tokens.css`.
- `reference/fig-typography.css` — a stub; the Figma file carried no text or effect styles.

# The language

ATLAS is a fresh system — the Condos DS was the starting reference, not the model. Three
things were taken from it and everything visual is new.

## Coverage

ATLAS is a product interface system, not a brand, so two of the sections a brand book carries
do not apply to it — there is no logotype and no photography. Measured against the rest:

| | Section | Status |
|---|---|---|
| 01 | Philosophy — the three devices the system is built on | Documented |
| 02 | Logotype | Not applicable |
| 03 | Colour — semantic layer over per-theme primitives | Documented |
| 04 | Typography — Gabarito and Spline Sans Mono | Documented |
| 05 | Photography / illustration | Not applicable |
| 06 | Iconography — Phosphor regular, six rules | Documented |
| 07 | Grid & layout — the 1.75px unit, radii 6/10/14 | Documented |
| 08 | Application — the component set | **Not built** |

## Taken from the reference

- **Density.** 12–14px carries the interface. The reference is a dense enterprise system and
  that is the correct instinct for a data product; nothing here was inflated to a
  comfortable-looking 16px.
- **The 1.75px base grid.** The reference's spacing scale runs on a 1.75 unit rather than 4
  or 8. It is invisible, it is unusual, and it works.
- **Mono numerics.** Every figure, reference and identifier is monospaced and tabular.

Nothing else. The ice-blue, the navy, the cyan primary, the coral, the blue-tinted slate
ramp, the rounded PrimeVue chrome — all dropped.

## The three structural devices

**The index label** — a 10px tracked mono label with a numbered accent prefix and a hairline
running to the end of the column. Every block of content opens with one.

**Glass** — panels are translucent white (5.5–12.5%) over the navy with an 18px blur, 30px
on the app frame. A 1px gradient sheen along the top edge stands in for elevation; nothing
casts a shadow downward. There is no `box-shadow` in the system except the accent glow on a
hovered primary button.

**The rule** — inside glass, content separates with hairlines, never with nested cards.
Figures sit in one divided panel, not in separate tiles. Tables are the primary surface,
with an accent-tint hover instead of striping.

Radii run 6 / 10 / 14 — inner elements, panels and controls, then the app frame. Pill is
reserved for tags, progress tracks and avatars.

## Token structure

Two layers, and the split is load-bearing:

1. **Primitives** — raw values, declared per theme (`--navy-900`, `--lime-400`, `--d-16`).
   Never referenced by a component.
2. **Semantic** — role names, the only layer components may use: `--ground`, `--surface`,
   `--border`, `--text-primary`, `--fill-accent`, `--tint-success`, and so on.

A component that reaches past the semantic layer breaks when the theme flips. That is not
hypothetical — it is what happened to the accent before it was split into `--fill-accent`
(a background) and `--text-accent` (type).

Short aliases (`--ink`, `--ac`, `--glass`) exist at the end of `tokens.css` so older markup
keeps working. Every one is a pointer, not a value. New work should use the semantic names.

## Themes

`[data-theme="dark"]` is the default; `[data-theme="light"]` remaps every semantic alias. It
is a remap, not an inversion, and three things had to change beyond luminance:

- **Hairlines invert.** On dark, lines are white at 10–26%. On light, white-on-white has no
  edge, so they become navy at 10–26%.
- **Glass opacity climbs.** 5.5% white over navy reads as glass; 5.5% white over pale grey
  reads as nothing. Light glass sits at 58–90% — frosted rather than tinted.
- **The accent splits in two.** Chartreuse works as a *fill* in both themes with dark ink on
  it, but as *text* on a pale ground it measures 1.3:1. So `--fill-accent` (backgrounds) and
  `--text-accent` (type, icons, the index prefix) are separate tokens; light drops
  `--text-accent` to a deep lime #4A6606 at 6.0:1. Anything colouring type must use
  `--text-accent`, never `--fill-accent`.

The showcase carries a toggle and remembers the choice. The toggle itself is a **solid**
segmented control, not glass — glass nested inside glass is the one thing the system
forbids, and the toggle sits inside the glass masthead.

## Iconography

**Phosphor**, regular weight, from CDN:

```html
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css" />
<i class="ph ph-receipt"></i>
```

- **Regular weight only.** Never mixed with bold, fill or duotone — the mix is the fastest
  way to make an icon set look borrowed.
- **Sized in em**, so a glyph tracks the label beside it. Standalone sizes are
  14 / 16 / 20 / 24px. `.a-icon` sets 1.15em, which is the in-line default.
- **Inherit `currentColor`.** An icon is never given its own colour; it takes the colour of
  the text it sits with.
- **Never alone without an accessible name.** Icon-only controls carry `aria-label`;
  decorative glyphs carry `aria-hidden`.
- **Never the sole carrier of meaning.** A state is a tag plus a word. Icons in `.flag`
  repeat what the copy already says.
- **No emoji.**

# Accessibility, caveats and open items

## Accessibility

**Contrast, both themes.** All four text roles clear AA for normal text at 10px, which
matters because the system's signature label runs at exactly that size — the labels were
never going to be enlarged, so the colours had to carry it. Measured against `--ground` in
each theme:

| Role | Dark | Light |
| --- | --- | --- |
| `--text-primary` | 15.7:1 | 16.1:1 |
| `--text-secondary` | 8.8:1 | 6.6:1 |
| `--text-tertiary` | 5.9:1 | 5.2:1 |
| `--text-placeholder` | 4.8:1 | 5.0:1 |
| `--text-accent` | 15.2:1 | 6.0:1 |

Status text clears AA in both themes too (light: success 5.0:1, warning 5.4:1, danger 5.4:1;
dark: all above 6.3:1). Dark ink on the accent fill measures 14.0:1 dark / 12.8:1 light.
Both sets keep headroom for the light blooms, which raise background luminance under the
text. The light theme's tertiary, placeholder and status tones were all re-derived — the
first pass failed at 4.35:1, 4.06:1 and below.

- **Focus.** A 2px chartreuse outline at 2px offset on every interactive element, never
  removed.
- **Colour is never the only carrier.** Trend direction pairs the colour with a sign, tags
  pair the tint with a word, invalid fields pair the border with error copy and
  `aria-invalid`.
- **Touch targets** floor at 44px (`--touch`); the 34px control height is for pointer
  surfaces only.
- **Motion** respects `prefers-reduced-motion`, which collapses both durations to 1ms.

## Glass caveats

Backdrop blur is the whole visual premise, so two things matter. It needs light behind it —
`body::before` paints the blooms, and a glass panel dropped onto a flat fill will read as
grey mush. And it is GPU work: keep the number of simultaneously visible blurred layers low,
and never nest a blurred panel inside another one.

The light theme is the more fragile of the two — frosted white has far less contrast against
its ground than tinted white has against navy, so a light-theme panel needs its hairline to
define the edge. `base.css` carries an `@supports not (backdrop-filter)` fallback that
raises the fill opacity where blur is unavailable.

## Open

- **Content is placeholder.** The showcase, the component specimen and both case screens
  use invented product data — a ledger, a sensor fleet, a month close. None of it is a
  factual statement about any real business.
- **Fonts are CDN-linked.** Gabarito and Spline Sans Mono load from Google Fonts; Phosphor
  from unpkg. Self-host them before production.
- **Resolved.** The old focus-ring nit — `border-radius: var(--r-sm)` inside the shared
  `:focus-visible` rule, which snapped pill and frame-radius elements to 6px while
  focused — was fixed when the component layer landed: the rule now sets the outline
  alone, and outlines follow the element's own radius.

## Not carried over

Trimmed from the working folder when this was published, recoverable from the original if
wanted:

- `chooser.html` — the live picker used to settle radius and type. Its decisions are already
  baked into `tokens.css`.
- `reference/fig-tokens.css` — all 2,174 variables extracted from the Figma file, kept for
  lookup only. Superseded by `tokens.css`.
- `reference/fig-typography.css` — a stub; the Figma file carried no text or effect styles.

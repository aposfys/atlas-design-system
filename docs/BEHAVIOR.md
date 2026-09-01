# The behavior contract

ATLAS ships as CSS, so the markup and the keyboard are the implementer's to
build — but they are not the implementer's to design. This file is the
contract: the roles, states and keystrokes every interactive component carries,
in the order `components.css` defines them. The stylesheet already keys its
styling to these attributes (`aria-selected`, `aria-pressed`, `aria-invalid`,
`aria-current`), so markup that honors the contract gets the correct rendering
for free — and markup that skips it renders visibly wrong, which is the point.

Two rules from the README apply everywhere and are not repeated below: the
focus ring (2px accent outline, 2px offset) is never removed, and an icon never
appears without an accessible name.

## Buttons — `.a-btn`

A `<button>`. Space and Enter activate; that is the element's own behavior, so
never rebuild a button from a `<div>`. Icon-only buttons (`.a-btn--icon`) carry
`aria-label`. Disabled uses the `disabled` attribute — if a control must stay
discoverable while unavailable, use `aria-disabled="true"`, keep it focusable,
and swallow the activation.

## Fields — `.a-input`, `.a-select`, `.a-textarea`

- Every field has a `<label>` wired with `for`/`id`. The `.a-label` style is
  how it looks; the association is what it is.
- Help text (`.a-help`) is tied in with `aria-describedby`.
- An invalid field carries `aria-invalid="true"` — the stylesheet keys the
  danger border and tint to exactly this attribute, never to a class — and its
  `.a-error` line is referenced by `aria-describedby`. The error is a sentence
  that says how to fix it; the tint is never the only signal.

## Selection — `.a-check`, `.a-radio`, `.a-switch`

Native `<input type="checkbox">` / `<input type="radio">` inside their
`<label>`; the label text is the accessible name. Radios in a set share a
`name` and arrow keys move between them — native behavior, kept. The switch is
a checkbox with `role="switch"`; Space toggles it. State lives in
`:checked`, never in a class.

## Tabs — `.a-tabs` / `.a-tab`

- Container: `role="tablist"` with an `aria-label`.
- Each tab: a `<button role="tab">` with `aria-selected`, `aria-controls`
  pointing at its panel, and a roving tabindex — the selected tab is `0`,
  the rest `-1`.
- Each panel: `role="tabpanel"`, `aria-labelledby` back at its tab, and
  `tabindex="0"` when it contains no focusable element.
- Keyboard: Left/Right move and select (automatic activation), Home/End jump.
  Tab leaves the tablist for the panel — it never walks the tabs.

## Segmented — `.a-seg`

An exclusive choice rendered as buttons. Container: `role="group"` with an
`aria-label`. Each button carries `aria-pressed` — the stylesheet keys the
active fill to it. One button is pressed at all times; activating another
releases the previous.

## Dialog — `.a-overlay` / `.a-dialog`

- `role="dialog"` and `aria-modal="true"`, labelled by its `<h3>` via
  `aria-labelledby`.
- Opening moves focus to the first focusable element inside (or the panel
  itself, `tabindex="-1"`). Tab and Shift+Tab cycle inside the dialog and do
  not leave it. Escape closes. Closing returns focus to the opener.
- The overlay click may close; it is never the only way out — the footer
  always carries a real button.

## Flags — `.a-flag`

Static flags in the page flow need no role. A flag inserted in response to an
action carries `role="status"` (ok, info) or `role="alert"` (danger) so it is
announced. The icon repeats what the copy says and carries `aria-hidden` —
severity is in the words, never only in the color.

## The ledger table — `.a-table`

A real `<table>` with `<th scope="col">` (and `scope="row"` where the first
cell names the row). Sortable headers are buttons inside the `<th>`, with
`aria-sort` on the sorted column. The accent-tint row hover is a pointer
affordance only; anything clickable in a row is its own focusable element.

## Navigation — `.a-nav`

A `<nav>` with an `aria-label`. The current page carries
`aria-current="page"` — the stylesheet keys the active state to it.

## Progress — `.a-progress`

`role="progressbar"` with `aria-valuemin` / `aria-valuemax` / `aria-valuenow`,
and an `aria-label` naming what is progressing. An indeterminate track omits
`aria-valuenow`.

## Density, motion, touch

`.a-dense` changes spacing, never type — nothing here changes the contract.
Motion honors `prefers-reduced-motion` at the token layer (both durations
collapse to 1ms). Touch surfaces floor targets at `--touch` (44px); the 34px
control height is for pointer surfaces only.

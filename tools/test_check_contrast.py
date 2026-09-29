"""Tests for the contrast gate. Run from the repository root with
python3 -m unittest discover -s tools"""
import io
import os
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(__file__))
import check_contrast as cc  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def themes():
    with open(os.path.join(ROOT, "tokens.css"), encoding="utf-8") as f:
        return cc.theme_blocks(f.read())


def measure(theme, fg, stack):
    return cc.measure(fg, stack, themes()[theme])


class Compositing(unittest.TestCase):
    def test_opaque_colour_covers_the_backdrop(self):
        self.assertEqual(cc.over((10, 20, 30, 1.0), (200, 200, 200)), (10, 20, 30))

    def test_half_alpha_is_the_midpoint(self):
        self.assertEqual(cc.to_hex(cc.over((0, 0, 0, 0.5), (255, 255, 255))), "#808080")

    def test_backdrop_needs_an_opaque_bottom(self):
        toks = themes()["light"]
        self.assertIsNone(cc.backdrop("surface", toks))
        self.assertIsNotNone(cc.backdrop("ground+surface", toks))

    def test_solid_pairs_measure_as_plain_hex(self):
        # Compositing an opaque colour over one opaque token must give the
        # same ratio as comparing the two hex values directly.
        for theme, fg, bg, _, _ in cc.PAIRS:
            if "+" in bg:
                continue
            toks = themes()[theme]
            a, b = cc.resolve_rgba(fg, toks), cc.resolve_rgba(bg, toks)
            self.assertEqual(a[3], 1.0)
            self.assertEqual(cc.measure(fg, bg, toks),
                             cc.ratio(cc.to_hex(a[:3]), cc.to_hex(b[:3])))


class PrimaryButtonBoundary(unittest.TestCase):
    def test_light_border_clears_three_to_one(self):
        # The documented values in NOTES.md.
        self.assertAlmostEqual(measure("light", "border-primary", "ground"), 6.01, delta=0.005)
        self.assertAlmostEqual(measure("light", "border-primary", "ground+surface"), 6.35, delta=0.005)

    def test_light_border_pairs_are_gated(self):
        gated = {(t, fg, bg) for t, fg, bg, _, _ in cc.PAIRS}
        measured = {(t, fg, bg) for t, fg, bg, _ in cc.MEASURED}
        for stack in ("ground", "ground+surface"):
            self.assertIn(("light", "border-primary", stack), gated)
            self.assertNotIn(("light", "border-primary", stack), measured)

    def test_accent_border_is_left_as_it_was(self):
        # Tags, the grid demo and the close case still use --border-accent.
        self.assertAlmostEqual(measure("light", "border-accent", "ground"), 1.50, places=2)
        self.assertEqual(themes()["dark"]["border-primary"], "var(--border-accent)")

    def test_dark_fill_carries_the_boundary(self):
        self.assertGreaterEqual(measure("dark", "fill-accent", "ground"), 3.0)


class Gate(unittest.TestCase):
    def run_gate(self, css):
        tmp = os.path.join(ROOT, "tools", "_gate_test_tokens.css")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(css)
        old, cc.CSS = cc.CSS, tmp
        out = io.StringIO()
        try:
            with redirect_stdout(out):
                cc.main()
            return 0, out.getvalue()
        except SystemExit as e:
            return e.code, out.getvalue()
        finally:
            cc.CSS = old
            os.remove(tmp)

    def test_committed_tokens_open_the_gate(self):
        with open(os.path.join(ROOT, "tokens.css"), encoding="utf-8") as f:
            code, out = self.run_gate(f.read())
        self.assertEqual(code, 0)
        self.assertIn("ok    [light]  6.01:1  (needs 3.0)  --border-primary on --ground ", out)
        self.assertIn("ok    [light]  6.35:1  (needs 3.0)  --border-primary on --ground+--surface ", out)
        self.assertIn(f"All {len(cc.PAIRS)} gated pairs clear.", out)

    def test_a_broken_token_closes_the_gate(self):
        with open(os.path.join(ROOT, "tokens.css"), encoding="utf-8") as f:
            css = f.read().replace("--lime-700: #4A6606;", "--lime-700: #8FB31A;")
        code, out = self.run_gate(css)
        self.assertEqual(code, 1)
        self.assertIn("FAIL  [light]", out)

    def test_a_faint_primary_border_closes_the_gate(self):
        with open(os.path.join(ROOT, "tokens.css"), encoding="utf-8") as f:
            css = f.read().replace("--border-primary: var(--lime-700);",
                                   "--border-primary: var(--border-accent);")
        code, out = self.run_gate(css)
        self.assertEqual(code, 1)
        self.assertIn("FAIL  [light]  1.53:1  (needs 3.0)  --border-primary on --ground+--surface", out)


if __name__ == "__main__":
    unittest.main()

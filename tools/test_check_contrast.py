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
    toks = themes()[theme]
    bg = cc.backdrop(stack, toks)
    return cc.ratio(cc.to_hex(cc.over(cc.resolve_rgba(fg, toks), bg)), cc.to_hex(bg))


class Compositing(unittest.TestCase):
    def test_opaque_colour_covers_the_backdrop(self):
        self.assertEqual(cc.over((10, 20, 30, 1.0), (200, 200, 200)), (10, 20, 30))

    def test_half_alpha_is_the_midpoint(self):
        self.assertEqual(cc.to_hex(cc.over((0, 0, 0, 0.5), (255, 255, 255))), "#808080")

    def test_backdrop_needs_an_opaque_bottom(self):
        toks = themes()["light"]
        self.assertIsNone(cc.backdrop("surface", toks))
        self.assertIsNotNone(cc.backdrop("ground+surface", toks))


class PrimaryButtonBoundary(unittest.TestCase):
    def test_light_border_is_measured_below_three_to_one(self):
        # The documented value in NOTES.md. If a token change lifts it past
        # 3:1, move the pair into PAIRS and update NOTES.md.
        self.assertAlmostEqual(measure("light", "border-accent", "ground"), 1.50, places=2)
        self.assertLess(measure("light", "border-accent", "ground+surface"), 3.0)

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
        self.assertIn("info  [light]  1.50:1  --border-accent on ground", out)

    def test_a_broken_token_closes_the_gate(self):
        with open(os.path.join(ROOT, "tokens.css"), encoding="utf-8") as f:
            css = f.read().replace("--lime-700: #4A6606;", "--lime-700: #8FB31A;")
        code, out = self.run_gate(css)
        self.assertEqual(code, 1)
        self.assertIn("FAIL  [light]", out)


if __name__ == "__main__":
    unittest.main()

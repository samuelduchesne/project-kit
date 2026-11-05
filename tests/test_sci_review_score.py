"""Tests for the seeded-fixture scorer of sci-review (tests/fixtures/sci-review/seeded-repo/score.py).

The scorer reads two manifest formats: the sci-review fixture's own (`defects`, `lookalikes`, `contested`) and the
entry format of the idfkit building-energy fixture (`entries` with `kind`). Both must load, and the SC-012
attribution criterion must count only findings raised by the named perspective.
"""

from __future__ import annotations

import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORE_PATH = ROOT / "tests" / "fixtures" / "sci-review" / "seeded-repo" / "score.py"

spec = importlib.util.spec_from_file_location("sci_review_score", SCORE_PATH)
score = importlib.util.module_from_spec(spec)
sys.modules["sci_review_score"] = score
spec.loader.exec_module(score)

ENTRY_MANIFEST = {
    "fixture": "building-energy",
    "entries": [
        {
            "id": "py-defect",
            "file": "src/bem/units.py",
            "line": 6,
            "anchor": "X",
            "description": "d",
            "language": "python",
            "kind": "defect",
        },
        {
            "id": "idf-defect",
            "file": "models/office.idf",
            "line": 73,
            "anchor": "Y",
            "description": "d",
            "language": "idf",
            "kind": "defect",
        },
        {
            "id": "py-lookalike",
            "file": "src/bem/units.py",
            "line": 21,
            "anchor": "Z",
            "description": "d",
            "language": "python",
            "kind": "lookalike",
        },
    ],
}


def finding(fid: str, file: str, line: int, raised_by: list[str]) -> dict:
    return {
        "id": fid,
        "file": file,
        "line_start": line,
        "line_end": line,
        "dimension": "physical-modelling-and-units",
        "severity": "high",
        "summary": "s",
        "trigger": "t",
        "wrong_output": "w",
        "fix": "f",
        "raised_by": raised_by,
        "label": "consensus",
    }


class TestScore(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dir, True)

    def write(self, name: str, data: dict) -> Path:
        path = self.dir / name
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_fixture_manifest_loads(self) -> None:
        manifest = score.load_manifest(score.DEFAULT_MANIFEST)
        self.assertTrue(manifest.defects)
        self.assertTrue(all(d.dimension for d in manifest.defects))

    def test_entry_manifest_loads(self) -> None:
        manifest = score.load_manifest(self.write("manifest.json", ENTRY_MANIFEST))
        self.assertEqual([d.id for d in manifest.defects], ["py-defect", "idf-defect"])
        self.assertEqual([e.id for e in manifest.lookalikes], ["py-lookalike"])
        self.assertEqual(manifest.contested, ())
        self.assertIsNone(manifest.defects[0].dimension)

    def test_unknown_kind_is_unreadable(self) -> None:
        bad = json.loads(json.dumps(ENTRY_MANIFEST))
        bad["entries"][0]["kind"] = "bug"
        with self.assertRaises(score.UnreadableInput):
            score.load_manifest(self.write("bad.json", bad))

    def test_domain_attribution(self) -> None:
        manifest = self.write("manifest.json", ENTRY_MANIFEST)
        report = self.write(
            "report.json",
            {
                "findings": [
                    finding("F1", "src/bem/units.py", 6, ["theorist", "building-physicist"]),
                    finding("F2", "models/office.idf", 73, ["theorist"]),
                ]
            },
        )
        out = io.StringIO()
        with redirect_stdout(out):
            code = score.main([str(report), "--manifest", str(manifest), "--domain-perspective", "building-physicist"])
        self.assertEqual(code, 0)
        text = out.getvalue()
        self.assertIn("SC-001: PASS (2/2 detected)", text)
        self.assertIn("language idf: 1/1", text)
        self.assertNotIn("dimension ", text)
        self.assertIn("SC-012: FAIL (1/2 reported with building-physicist as a raiser)", text)
        self.assertIn("reported as F2 without building-physicist", text)

    def test_domain_attribution_leaves_out_general_defects(self) -> None:
        """SC-012 counts only domain defects; SC-001 still counts every defect."""
        data = json.loads(json.dumps(ENTRY_MANIFEST))
        data["entries"].append(
            {
                "id": "py-general",
                "file": "src/bem/units.py",
                "line": 27,
                "anchor": "W",
                "description": "d",
                "language": "python",
                "kind": "defect",
                "domain": False,
            }
        )
        manifest = self.write("manifest.json", data)
        report = self.write(
            "report.json",
            {
                "findings": [
                    finding("F1", "src/bem/units.py", 6, ["building-physicist"]),
                    finding("F2", "models/office.idf", 73, ["building-physicist"]),
                    finding("F3", "src/bem/units.py", 27, ["computer-scientist"]),
                ]
            },
        )
        text = self.run_score(str(report), "--manifest", str(manifest), "--domain-perspective", "building-physicist")
        self.assertIn("SC-001: PASS (3/3 detected)", text)
        self.assertIn("py-general                         not a domain defect; left out", text)
        self.assertIn("SC-012: PASS (2/2 reported with building-physicist as a raiser)", text)

    def run_score(self, *args: str) -> str:
        out = io.StringIO()
        with redirect_stdout(out):
            code = score.main(list(args))
        self.assertEqual(code, 0)
        return out.getvalue()

    def test_lookalike_needs_overlap(self) -> None:
        """A finding about adjacent code, within the tolerance but not on the look-alike's line, is not counted."""
        manifest = self.write("manifest.json", ENTRY_MANIFEST)
        adjacent = finding("F7", "src/bem/units.py", 24, ["methodologist"]) | {"line_end": 27}
        report = self.write("report.json", {"findings": [adjacent]})
        self.assertIn(
            "SC-002: PASS (0 false positive(s) at look-alikes)",
            self.run_score(str(report), "--manifest", str(manifest)),
        )
        on_line = finding("F8", "src/bem/units.py", 21, ["theorist"])
        report = self.write("report.json", {"findings": [on_line]})
        text = self.run_score(str(report), "--manifest", str(manifest))
        self.assertIn("SC-002: FAIL (1 false positive(s) at look-alikes)", text)
        self.assertIn("reported as F8", text)

    def test_candidate_credited_through_merge(self) -> None:
        """A candidate outside the tolerance is credited with the defect of the merged finding that absorbed it."""
        manifest = self.write("manifest.json", ENTRY_MANIFEST)
        report = self.write(
            "report.json",
            {
                "findings": [
                    finding("F1", "src/bem/units.py", 6, ["theorist", "building-physicist"]),
                    finding("F2", "models/office.idf", 73, ["theorist"]),
                ]
            },
        )
        run = self.dir / "run"
        (run / "candidates").mkdir(parents=True)
        (run / "merge").mkdir()
        candidates = {
            "perspective": "building-physicist",
            "findings": [
                {"id": "building-physicist-1", "file": "src/bem/units.py", "line_start": 14, "line_end": 16},
                {"id": "building-physicist-2", "file": "models/office.idf", "line_start": 73, "line_end": 73},
                {"id": "building-physicist-3", "file": "src/bem/units.py", "line_start": 40, "line_end": 40},
            ],
        }
        (run / "candidates" / "building-physicist.json").write_text(json.dumps(candidates), encoding="utf-8")
        merge = {
            "batch": 1,
            "findings": [
                {"id": "F1", "members": ["building-physicist-1"]},
                {"id": "F2", "members": ["building-physicist-2"]},
            ],
        }
        (run / "merge" / "batch-1.json").write_text(json.dumps(merge), encoding="utf-8")
        text = self.run_score(str(report), "--manifest", str(manifest), "--run", str(run))
        self.assertIn("building-physicist       2/2 detected, 1 false positive(s) of 3 finding(s)", text)
        self.assertIn("building-physicist-3", text)
        self.assertNotIn("building-physicist-1 ", text)
        self.assertIn("SC-009: PASS (1/1 false positives removed)", text)


if __name__ == "__main__":
    unittest.main()

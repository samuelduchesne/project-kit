"""Tests for the verify protocol of sci-review (spec 009).

Covers the verdict adjudication rules, the automatic merge, the ingest of verification messages, the
Workflow script's automatic merge (parity with panel.py) and a simulated verify-protocol Workflow run.

Run with: uv run --no-project --python 3.12 python -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from test_sci_review_panel import GOLDEN, RunDirMixin, panel, run_panel
from test_sci_review_workflow_build import NODE, PLUGIN, SIMULATION_HARNESS, WORKFLOW, section

FULL = GOLDEN / "full"


def merged(fid: str = "F1", raised_by: tuple[str, ...] = ("theorist",), concrete: bool = True) -> panel.MergedFinding:
    return panel.MergedFinding(
        id=fid,
        members=tuple(f"{r}-1" for r in raised_by),
        raised_by=raised_by,
        batch=1,
        file="src/a.py",
        line_start=1,
        line_end=2,
        dimension="numerical-stability",
        severity="high",
        summary="A defect.",
        trigger="x = 0" if concrete else None,
        wrong_output="nan" if concrete else None,
        fix="Guard x.",
    )


def verdict(kind: str, fid: str = "F1", verifier: str = "v1", assumption: str | None = None) -> panel.VerdictRecord:
    return panel.VerdictRecord(
        finding_id=fid,
        verdict=kind,
        reason=f"{verifier} {kind}",
        argument_for=f"{verifier} for",
        argument_against=f"{verifier} against",
        deciding_assumption=assumption,
        no_trigger_reason=None,
        verifier=verifier,
    )


def verification(batch: int, verifier: str, verdicts: dict[str, str]) -> dict:
    return {
        "batch": batch,
        "verifier": verifier,
        "verdicts": [
            {
                "finding_id": fid,
                "verdict": kind,
                "evidence": "reproduced",
                "refutation_search": "Read the module docstring and the callers.",
                "reason": f"{verifier} judged {fid} {kind}.",
                "argument_for": f"{verifier}: the scenario follows from the code.",
                "argument_against": f"{verifier}: none found.",
                "deciding_assumption": "Whether inputs stay small." if kind == "uncertain" else None,
                "no_trigger_reason": "No trigger was established." if fid == "F2" else None,
                "reach": "Read the settings module and the environment file; the inputs come from users.",
                "trigger_class": "unreachable" if kind == "refute" else "user-action",
                "value_corrections": [],
                "reproduction": f"python3 -B repro_{fid.lower()}.py  # prints the wrong output",
                "extent": [],
            }
            for fid, kind in verdicts.items()
        ],
    }


class TestVerifyOutcome(unittest.TestCase):
    def label(self, finding: panel.MergedFinding, *kinds: str) -> tuple[str | None, str | None]:
        outcome = panel.verify_outcome(finding, [verdict(k, verifier=f"v{i + 1}") for i, k in enumerate(kinds)])
        return outcome.label, outcome.rejection

    def test_single_confirming_verifier_gives_consensus_with_its_raiser(self) -> None:
        self.assertEqual(self.label(merged(), "confirm"), ("consensus", None))

    def test_refutations_outnumbering_confirmations_reject(self) -> None:
        self.assertEqual(self.label(merged(), "refute"), (None, "refuted"))
        self.assertEqual(self.label(merged(), "confirm", "refute", "refute"), (None, "refuted"))

    def test_a_tie_or_uncertainty_is_contested(self) -> None:
        self.assertEqual(self.label(merged(), "confirm", "refute"), ("contested", None))
        self.assertEqual(self.label(merged(), "uncertain"), ("contested", None))

    def test_confirmations_with_an_uncertain_verdict_give_majority(self) -> None:
        self.assertEqual(self.label(merged(), "confirm", "uncertain"), ("majority", None))
        self.assertEqual(self.label(merged(), "confirm", "confirm", "refute"), ("majority", None))

    def test_no_concrete_scenario_is_at_most_contested(self) -> None:
        self.assertEqual(self.label(merged(concrete=False), "confirm", "confirm"), ("contested", None))
        self.assertEqual(self.label(merged(concrete=False), "refute"), (None, "refuted"))

    def test_confirmation_without_evidence_counts_as_uncertain(self) -> None:
        unproven = panel.dataclasses.replace(verdict("confirm"), evidence="none")
        self.assertEqual(panel.verify_outcome(merged(), [unproven]).label, "contested")
        proven = panel.dataclasses.replace(verdict("confirm", verifier="v2"), evidence="traced")
        self.assertEqual(panel.verify_outcome(merged(), [unproven, proven]).label, "majority")

    def test_unverified_finding_is_contested(self) -> None:
        self.assertEqual(self.label(merged()), ("contested", None))


class VerifyRunMixin(RunDirMixin):
    def verify_run(self, verifiers: int = 1) -> Path:
        """The golden `full` scenario as a verify-protocol run: no debate and no notes."""
        run_dir = self.init_run()
        for name in ("candidates", "merge"):
            shutil.copytree(FULL / name, run_dir / name)
        shutil.copy(FULL / "scope.json", run_dir / "scope.json")
        state = json.loads((FULL / "panel.json").read_text(encoding="utf-8"))
        state["panel"].update(protocol="verify", verifiers=verifiers, rebuttal_rounds=0)
        (run_dir / "panel.json").write_text(json.dumps(state), encoding="utf-8")
        return run_dir

    def write_verdicts(self, run_dir: Path, batch: int, verifier: str, verdicts: dict[str, str]) -> None:
        path = run_dir / "verify" / f"batch-{batch}" / f"{verifier}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        message = verification(batch, verifier, verdicts)
        self.assertEqual(panel.validate_message("verification", message), [])
        path.write_text(json.dumps(message), encoding="utf-8")


class TestVerifyAdjudication(VerifyRunMixin):
    def test_labels_rejections_and_notes_from_verdicts(self) -> None:
        run_dir = self.verify_run(verifiers=2)
        self.write_verdicts(run_dir, 1, "v1", {"F1": "confirm", "F2": "confirm", "F5": "refute", "F6": "uncertain"})
        self.write_verdicts(run_dir, 1, "v2", {"F1": "confirm", "F2": "confirm", "F5": "refute", "F6": "uncertain"})
        self.write_verdicts(run_dir, 2, "v1", {"F3": "confirm", "F4": "confirm"})
        self.write_verdicts(run_dir, 2, "v2", {"F3": "confirm", "F4": "uncertain"})
        result = run_panel("adjudicate", "--run", str(run_dir))
        self.assertEqual(result.code, 0, result.err)
        data = json.loads((run_dir / "adjudication.json").read_text(encoding="utf-8"))
        labels = {f["id"]: f["label"] for f in data["findings"]}
        self.assertEqual(
            labels, {"F1": "consensus", "F2": "contested", "F3": "consensus", "F4": "majority", "F6": "contested"}
        )
        self.assertEqual([r["finding_id"] for r in data["rejected"]], ["F5"])
        self.assertEqual(data["rejected"][0]["reason"], "v1 judged F5 refute.")
        f6 = next(f for f in data["findings"] if f["id"] == "F6")
        self.assertEqual(f6["deciding_assumption"], "Whether inputs stay small.")
        f2 = next(f for f in data["findings"] if f["id"] == "F2")
        self.assertEqual(f2["no_trigger_reason"], "No trigger was established.")
        self.assertEqual(len(data["verdicts"]), 12)
        self.assertEqual(data["records"], [])

    def test_report_states_the_verify_protocol(self) -> None:
        run_dir = self.verify_run()
        self.write_verdicts(run_dir, 1, "v1", {"F1": "confirm", "F2": "confirm", "F5": "confirm", "F6": "confirm"})
        self.write_verdicts(run_dir, 2, "v1", {"F3": "confirm", "F4": "confirm"})
        self.assertEqual(run_panel("adjudicate", "--run", str(run_dir)).code, 0)
        result = run_panel("report", "--run", str(run_dir), "--format", "markdown")
        self.assertEqual(result.code, 0, result.err)
        self.assertIn("Protocol: verify.", result.out)
        self.assertIn("1 verifier per batch", result.out)
        self.assertNotIn("Defender", result.out)
        json_result = run_panel("report", "--run", str(run_dir), "--format", "json")
        self.assertEqual(json_result.code, 0, json_result.err)
        report = json.loads((run_dir / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(panel.validate_message("report", report), [])

    def test_finding_beyond_the_end_of_its_file_is_not_reported(self) -> None:
        run_dir = self.verify_run()
        self.write_verdicts(run_dir, 1, "v1", {"F1": "confirm", "F2": "confirm", "F5": "confirm", "F6": "confirm"})
        self.write_verdicts(run_dir, 2, "v1", {"F3": "confirm", "F4": "confirm"})
        self.assertEqual(run_panel("adjudicate", "--run", str(run_dir)).code, 0)
        f1 = json.loads((run_dir / "merge" / "batch-1.json").read_text(encoding="utf-8"))["findings"][0]
        short = self.project / f1["file"]
        short.parent.mkdir(parents=True, exist_ok=True)
        short.write_text("x = 1\n" * (f1["line_start"] - 1), encoding="utf-8")
        result = run_panel("report", "--run", str(run_dir), "--format", "json")
        self.assertEqual(result.code, 0, result.err)
        report = json.loads((run_dir / "report.json").read_text(encoding="utf-8"))
        self.assertNotIn("F1", [f["id"] for f in report["findings"]])
        self.assertTrue(any("F1 cites lines" in n for n in report["notices"]), report["notices"])

    def test_missing_verifications_leave_findings_contested_with_a_notice(self) -> None:
        run_dir = self.verify_run()
        self.write_verdicts(run_dir, 1, "v1", {"F1": "confirm", "F2": "confirm", "F5": "confirm", "F6": "confirm"})
        self.assertEqual(run_panel("adjudicate", "--run", str(run_dir)).code, 0)
        data = json.loads((run_dir / "adjudication.json").read_text(encoding="utf-8"))
        self.assertEqual({f["id"]: f["label"] for f in data["findings"]}["F3"], "contested")
        self.assertTrue(any("F3 was not verified" in n for n in data["notices"]))


class TestAutoMerge(VerifyRunMixin):
    def test_singleton_batches_are_merged_by_the_script(self) -> None:
        run_dir = self.verify_run()
        shutil.rmtree(run_dir / "merge")
        result = run_panel("auto-merge", "--run", str(run_dir))
        self.assertEqual(result.code, 0, result.err)
        self.assertEqual(json.loads(result.out), {"written": [1], "moderator": [2]})
        ruling = json.loads((run_dir / "merge" / "batch-1.json").read_text(encoding="utf-8"))
        self.assertEqual(panel.validate_message("merge-ruling", ruling), [])
        self.assertEqual([f["id"] for f in ruling["findings"]], ["F1", "F2", "F5", "F6"])
        candidate = json.loads((run_dir / "candidates" / "experimentalist.json").read_text(encoding="utf-8"))[
            "findings"
        ][0]
        first = ruling["findings"][0]
        self.assertEqual((first["members"], first["raised_by"]), ([candidate["id"]], [candidate["raised_by"]]))
        for key in (
            "file",
            "line_start",
            "line_end",
            "dimension",
            "severity",
            "summary",
            "trigger",
            "wrong_output",
            "fix",
        ):
            self.assertEqual(first[key], candidate[key], key)
        self.assertFalse((run_dir / "merge" / "batch-2.json").exists())

    def test_a_debate_keeps_the_moderator_merge(self) -> None:
        run_dir = self.verify_run()
        shutil.rmtree(run_dir / "merge")
        state = json.loads((run_dir / "panel.json").read_text(encoding="utf-8"))
        state["panel"]["protocol"] = "debate"
        (run_dir / "panel.json").write_text(json.dumps(state), encoding="utf-8")
        result = run_panel("auto-merge", "--run", str(run_dir))
        self.assertEqual(json.loads(result.out), {"written": [], "moderator": [1, 2]})
        self.assertFalse((run_dir / "merge").exists())


class TestIngestVerification(VerifyRunMixin):
    def test_verification_entries_are_written_and_unsafe_ids_dropped(self) -> None:
        run_dir = self.verify_run()
        result_file = run_dir / "workflow-result.json"
        good = verification(1, "v1", {"F1": "confirm"})
        bad = verification(1, "v1", {"F1": "confirm"})
        bad["verifier"] = "../v1"
        result_file.write_text(json.dumps({"verify": [{"batch": 1, "message": good}, {"batch": 1, "message": bad}]}))
        result = run_panel("ingest", "--run", str(run_dir), str(result_file))
        self.assertEqual(result.code, 0, result.err)
        self.assertTrue((run_dir / "verify" / "batch-1" / "v1.json").is_file())
        notices = json.loads((run_dir / "notices.json").read_text(encoding="utf-8"))
        self.assertTrue(any("verification" in n and "dropped" in n for n in notices), notices)


AUTO_HARNESS = """
const input = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'))
const clusters = clusterCandidates(input.candidates)
const batches = batchClusters(clusters, input.max_batches)
const byId = new Map(input.candidates.map(c => [c.id, c]))
process.stdout.write(JSON.stringify(batches.map(b => autoRuling(b, clusters, byId))))
"""


@unittest.skipIf(NODE is None, "node is not installed, so the Workflow tests cannot run")
class TestWorkflowVerify(unittest.TestCase):
    def test_auto_ruling_matches_panel(self) -> None:
        candidates = [
            f
            for p in sorted((FULL / "candidates").glob("*.json"))
            for f in json.loads(p.read_text(encoding="utf-8"))["findings"]
        ]
        work = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, work, True)
        (work / "input.json").write_text(json.dumps({"candidates": candidates, "max_batches": 2}), encoding="utf-8")
        pure = section(WORKFLOW.read_text(encoding="utf-8"), "// BEGIN PURE", "// END PURE")
        (work / "harness.js").write_text(pure + AUTO_HARNESS, encoding="utf-8")
        result = subprocess.run(
            [NODE, str(work / "harness.js"), str(work / "input.json")], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        js = json.loads(result.stdout)
        records = [panel.CandidateFinding.from_json(c) for c in candidates]
        plan = panel.merge_plan(records, 2)
        by_id = {c.id: c for c in records}
        expected = [panel.auto_ruling(b, plan.clusters, by_id) for b in plan.batches]
        self.assertEqual(js, [r.to_json() if r else None for r in expected])

    def simulate(self, extra: dict) -> dict:
        golden = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, golden, True)
        for name in ("candidates", "merge"):
            shutil.copytree(FULL / name, golden / name)
        for batch, ids in ((1, ["F1", "F2", "F5", "F6"]), (2, ["F3", "F4"])):
            for verifier in ("v1", "v2"):
                path = golden / "verify" / f"batch-{batch}" / f"{verifier}.json"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(verification(batch, verifier, dict.fromkeys(ids, "confirm"))))
        harness = SIMULATION_HARNESS.replace(
            "  if (kind === 'merge') return read(`merge/${a}.json`)",
            "  if (kind === 'merge') return read(`merge/${a}.json`)\n"
            "  if (kind === 'verify') return read(`verify/${a}/${b}.json`)",
        )
        state = json.loads((FULL / "panel.json").read_text(encoding="utf-8"))
        args = {
            "scope": json.loads((FULL / "scope.json").read_text(encoding="utf-8")),
            "perspectives": [p["id"] for p in state["panel"]["perspectives"]],
            "extensions": [],
            "max_batches": 2,
            "skill_dir": str(PLUGIN / "skills" / "scientific-review"),
            **extra,
        }
        work = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, work, True)
        as_text = args.pop("_as_text", False)
        (work / "args.json").write_text(json.dumps(json.dumps(args) if as_text else args), encoding="utf-8")
        (work / "harness.js").write_text(harness, encoding="utf-8")
        result = subprocess.run(
            [NODE, str(work / "harness.js"), str(golden), str(work / "args.json"), str(WORKFLOW)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_verify_protocol_runs_finders_one_moderator_and_the_verifiers(self) -> None:
        output = self.simulate({"protocol": "verify", "verifiers": 2})
        calls = sorted(output["calls"])
        self.assertEqual(len([c for c in calls if c.startswith("independent:")]), 5)
        # Batch 1 holds only single-candidate clusters, so only batch 2 needs the moderator.
        self.assertEqual([c for c in calls if c.startswith("merge:")], ["merge:batch-2"])
        self.assertEqual(
            [c for c in calls if c.startswith("verify:")],
            ["verify:batch-1:v1", "verify:batch-1:v2", "verify:batch-2:v1", "verify:batch-2:v2"],
        )
        self.assertFalse([c for c in calls if c.startswith(("debate:", "notes:"))])
        self.assertEqual(len(calls), 10)
        result = output["result"]
        self.assertEqual(len(result["verify"]), 4)
        auto = next(m for m in result["merge"] if m["batch"] == 1)
        self.assertEqual([f["id"] for f in auto["findings"]], ["F1", "F2", "F5", "F6"])

    def test_finder_prompts_carry_the_focus_and_no_protocol(self) -> None:
        perspectives = [
            {"id": "theorist", "dimensions": ["mathematical-derivations", "physical-modelling-and-units"]},
            {"id": "numerical-analyst", "dimensions": ["numerical-stability", "algorithmic-correctness"]},
            {"id": "methodologist", "dimensions": ["statistical-integrity"]},
        ]
        output = self.simulate({"protocol": "verify", "verifiers": 1, "perspectives": perspectives})
        prompt = output["prompts"]["independent:theorist:p1"]
        self.assertIn("Your focus dimensions: mathematical-derivations, physical-modelling-and-units.", prompt)
        self.assertIn("statistical-integrity.md", prompt)  # named, to load on demand
        self.assertNotIn("<protocol>", prompt)
        self.assertNotIn("# Panel protocol", prompt)
        verify_prompt = output["prompts"]["verify:batch-1:v1"]
        self.assertIn("# Verifier", verify_prompt)
        self.assertNotIn("theorist-1", verify_prompt.split("<merged-findings>")[0])

    def test_arguments_given_as_json_text_are_parsed(self) -> None:
        # The Workflow tool can deliver a large argument object as its JSON text.
        output = self.simulate({"protocol": "verify", "verifiers": 1, "_as_text": True})
        self.assertEqual(len([c for c in output["calls"] if c.startswith("independent:")]), 5)

    def test_a_caller_without_protocol_gets_the_debate(self) -> None:
        calls = self.simulate({"rebuttal_rounds": 2})["calls"]
        self.assertTrue([c for c in calls if c.startswith("debate:")])
        self.assertFalse([c for c in calls if c.startswith("verify:")])


if __name__ == "__main__":
    unittest.main()

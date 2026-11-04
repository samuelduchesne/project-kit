"""Tests for the generated Workflow script of sci-review.

1. Drift: build_workflow.py --check passes on the committed script and fails, with a diff, when a source changes.
2. Parity: the script's PURE section, run under Node.js, clusters, batches and stops debates exactly as panel.py does
   on the shared fixtures.
3. Simulation: the whole script, run under Node.js with stub agents that replay the golden panel messages, returns a
   PanelRun that panel.py ingests into the golden report.

The Node.js classes are skipped, with the reason, when `node` is not installed.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "sci-review"
WORKFLOW = PLUGIN / "workflows" / "scientific-review.js"
BUILD = PLUGIN / "scripts" / "build_workflow.py"
MESSAGES = ROOT / "tests" / "fixtures" / "sci-review" / "messages"
GOLDEN = MESSAGES / "golden" / "full"
NODE = shutil.which("node")

spec = importlib.util.spec_from_file_location("sci_review_panel_wf", PLUGIN / "scripts" / "panel.py")
panel = importlib.util.module_from_spec(spec)
sys.modules["sci_review_panel_wf"] = panel
spec.loader.exec_module(panel)


def run(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False)


def section(text: str, begin: str, end: str) -> str:
    return text[text.index(begin) + len(begin) : text.rindex(end)]


class TestDrift(unittest.TestCase):
    def test_committed_script_is_current(self) -> None:
        result = run([sys.executable, str(BUILD), "--check"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def copy_plugin(self) -> Path:
        target = Path(tempfile.mkdtemp()) / "sci-review"
        self.addCleanup(shutil.rmtree, target.parent, True)
        shutil.copytree(PLUGIN, target)
        return target

    def test_edited_brief_is_detected(self) -> None:
        plugin = self.copy_plugin()
        brief = plugin / "skills" / "scientific-review" / "roles" / "theorist.md"
        brief.write_text(brief.read_text(encoding="utf-8") + "\nAn added sentence.\n", encoding="utf-8")
        script = plugin / "scripts" / "build_workflow.py"
        workflow = plugin / "workflows" / "scientific-review.js"
        before = workflow.read_text(encoding="utf-8")

        check = run([sys.executable, str(script), "--check"])
        self.assertEqual(check.returncode, 1)
        self.assertIn("An added sentence.", check.stdout)

        dry = run([sys.executable, str(script), "--dry-run"])
        self.assertEqual(dry.returncode, 0)
        self.assertIn("An added sentence.", dry.stdout)
        self.assertEqual(before, workflow.read_text(encoding="utf-8"))

        self.assertEqual(run([sys.executable, str(script)]).returncode, 0)
        self.assertEqual(run([sys.executable, str(script), "--check"]).returncode, 0)

    def test_marker_text_inside_a_source_is_harmless(self) -> None:
        plugin = self.copy_plugin()
        protocol = plugin / "skills" / "scientific-review" / "protocol.md"
        protocol.write_text(
            protocol.read_text(encoding="utf-8") + "\nQuoted marker: // END GENERATED\n", encoding="utf-8"
        )
        script = plugin / "scripts" / "build_workflow.py"
        self.assertEqual(run([sys.executable, str(script)]).returncode, 0)
        self.assertEqual(run([sys.executable, str(script)]).returncode, 0)
        self.assertEqual(run([sys.executable, str(script), "--check"]).returncode, 0)
        text = (plugin / "workflows" / "scientific-review.js").read_text(encoding="utf-8")
        self.assertEqual(text.count("// BEGIN PURE"), 1)
        self.assertTrue(text.rstrip().endswith("return run"))

    def test_missing_markers_exit_3(self) -> None:
        plugin = self.copy_plugin()
        workflow = plugin / "workflows" / "scientific-review.js"
        workflow.write_text(workflow.read_text(encoding="utf-8").replace("// BEGIN GENERATED", ""), encoding="utf-8")
        result = run([sys.executable, str(plugin / "scripts" / "build_workflow.py"), "--check"])
        self.assertEqual(result.returncode, 3)
        self.assertIn("error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_missing_role_briefs_exit_3(self) -> None:
        plugin = self.copy_plugin()
        shutil.rmtree(plugin / "skills" / "scientific-review" / "roles")
        result = run([sys.executable, str(plugin / "scripts" / "build_workflow.py")])
        self.assertEqual(result.returncode, 3)
        self.assertIn("error: no role briefs or schemas", result.stderr)

    def test_every_source_is_embedded(self) -> None:
        generated = section(WORKFLOW.read_text(encoding="utf-8"), "// BEGIN GENERATED", "// END GENERATED")
        skill = PLUGIN / "skills" / "scientific-review"
        sources = [skill / "protocol.md", *sorted((skill / "roles").glob("*.md"))]
        sources += sorted((skill / "dimensions").glob("*.md"))
        for path in sources:
            with self.subTest(path=path.name):
                self.assertIn(json.dumps(path.read_text(encoding="utf-8"), ensure_ascii=False), generated)
        for path in sorted((skill / "schemas").glob("*.schema.json")):
            with self.subTest(path=path.name):
                name = path.name.removesuffix(".schema.json")
                self.assertIn(json.dumps(name) + ": {", generated)


PARITY_HARNESS = """
const fs = require('fs')
const input = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'))
const out = { merge: {}, debate: {} }
for (const [name, c] of Object.entries(input.merge)) {
  const clusters = clusterCandidates(c.candidates)
  out.merge[name] = { clusters, batches: batchClusters(clusters, c.max_batches) }
}
for (const [name, c] of Object.entries(input.debate)) {
  let stop = Math.min(c.rebuttal_rounds, Math.max(c.rounds.length - 1, 0))
  for (let k = 1; k <= Math.min(c.rebuttal_rounds, c.rounds.length - 1); k++) {
    if (debateStopped(c.rounds, k)) { stop = k; break }
  }
  const changed = []
  const calls = []
  for (let k = 1; k < c.rounds.length; k++) {
    changed.push(changedMembers(c.rounds, k))
    calls.push(membersToCall(c.rounds, k))
  }
  out.debate[name] = { stop, changed, calls }
}
process.stdout.write(JSON.stringify(out))
"""


@unittest.skipIf(NODE is None, "node is not installed, so the Workflow parity test cannot run")
class TestParity(unittest.TestCase):
    def test_pure_section_matches_panel(self) -> None:
        pure = section(WORKFLOW.read_text(encoding="utf-8"), "// BEGIN PURE", "// END PURE")
        merge = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((MESSAGES / "merge").glob("*.json"))}
        debate = {
            p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((MESSAGES / "debate").glob("*.json"))
        }
        work = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, work, True)
        (work / "input.json").write_text(json.dumps({"merge": merge, "debate": debate}), encoding="utf-8")
        (work / "harness.js").write_text(pure + PARITY_HARNESS, encoding="utf-8")
        result = run([NODE, str(work / "harness.js"), str(work / "input.json")])
        self.assertEqual(result.returncode, 0, result.stderr)
        js = json.loads(result.stdout)

        for name, case in merge.items():
            with self.subTest(merge=name):
                candidates = [panel.CandidateFinding.from_json(c) for c in case["candidates"]]
                clusters = panel.cluster_candidates(candidates)
                batches = panel.batch_clusters(clusters, case["max_batches"])
                self.assertEqual(js["merge"][name]["clusters"], [c.to_json() for c in clusters])
                self.assertEqual(js["merge"][name]["batches"], [b.to_json() for b in batches])
        for name, case in debate.items():
            with self.subTest(debate=name):
                rounds = [[panel.Position.from_json(p) for p in r] for r in case["rounds"]]
                self.assertEqual(js["debate"][name]["stop"], panel.stop_round(rounds, case["rebuttal_rounds"]))
                self.assertEqual(js["debate"][name]["stop"], case["expected_stop_round"])
                expected_changed = [panel.changed_members(rounds, k) for k in range(1, len(rounds))]
                self.assertEqual(js["debate"][name]["changed"], expected_changed)
                expected_calls = [panel.members_to_call(rounds, k) for k in range(1, len(rounds))]
                self.assertEqual(js["debate"][name]["calls"], expected_calls)


SIMULATION_HARNESS = """
const fs = require('fs')
const path = require('path')
const golden = process.argv[2]
const read = p => JSON.parse(fs.readFileSync(path.join(golden, p), 'utf8'))
const exists = p => fs.existsSync(path.join(golden, p))
const calls = []
const prompts = {}
async function agent(prompt, opts) {
  calls.push(opts.label)
  prompts[opts.label] = prompt
  if (!opts.schema || opts.schema.type !== 'object') throw new Error('missing schema for ' + opts.label)
  const [kind, a, b, c] = opts.label.split(':')
  if (kind === 'independent') return read(`candidates/${a}.json`)
  if (kind === 'merge') return read(`merge/${a}.json`)
  if (kind === 'notes') return read(`notes/${a}.json`)
  if (kind === 'debate') {
    const file = `debate/${a}/${b}/${c}.json`
    if (exists(file)) return read(file)
    // A member with no recorded position in this round repeats its latest recorded positions.
    const round = Number(b.split('-')[1])
    let k = round
    while (k > 0 && !exists(`debate/${a}/round-${k}/${c}.json`)) k--
    const latest = read(`debate/${a}/round-${k}/${c}.json`)
    return { member: c, round, positions: latest.positions.map(p => ({ ...p, round, answers: [] })) }
  }
  throw new Error('unexpected agent ' + opts.label)
}
async function parallel(thunks) { return Promise.all(thunks.map(t => t().catch(() => null))) }
async function pipeline(items, ...stages) {
  return Promise.all(items.map(async (item, index) => {
    let value = item
    for (const stage of stages) {
      try {
        value = await stage(value, item, index)
      } catch (e) {
        process.stderr.write(String(e.stack) + '\\n')
        return null
      }
    }
    return value
  }))
}
const phase = () => {}
const log = () => {}
const scriptArgs = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'))
let source = fs.readFileSync(process.argv[4], 'utf8').replace('export const meta', 'const meta')
const names = ['args', 'agent', 'parallel', 'pipeline', 'phase', 'log']
const body = new Function(...names, 'return (async () => {' + source + '})()')
body(scriptArgs, agent, parallel, pipeline, phase, log).then(result => {
  process.stdout.write(JSON.stringify({ result, calls, prompts }))
}).catch(e => { process.stderr.write(String(e.stack)); process.exit(1) })
"""


@unittest.skipIf(NODE is None, "node is not installed, so the Workflow simulation cannot run")
class TestSimulation(unittest.TestCase):
    def simulate(self, extra_args: dict | None = None, golden: Path = GOLDEN) -> dict:
        state = json.loads((GOLDEN / "panel.json").read_text(encoding="utf-8"))
        script_args = {
            "scope": json.loads((GOLDEN / "scope.json").read_text(encoding="utf-8")),
            "perspectives": [p["id"] for p in state["panel"]["perspectives"]],
            "extensions": [],
            "rebuttal_rounds": 2,
            "max_batches": 2,
            "skill_dir": str(PLUGIN / "skills" / "scientific-review"),
            **(extra_args or {}),
        }
        work = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, work, True)
        (work / "args.json").write_text(json.dumps(script_args), encoding="utf-8")
        (work / "harness.js").write_text(SIMULATION_HARNESS, encoding="utf-8")
        result = run([NODE, str(work / "harness.js"), str(golden), str(work / "args.json"), str(WORKFLOW)])
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_independent_prompts_hold_no_other_output(self) -> None:
        output = self.simulate()
        for label, prompt in output["prompts"].items():
            if not label.startswith("independent:"):
                continue
            own = label.split(":")[1]
            for other in ("theorist-1", "numerical-analyst-1", "methodologist-1", "experimentalist-1"):
                if not other.startswith(own):
                    self.assertNotIn(other, prompt, f"{label} received {other} (SC-011)")

    def test_debate_stops_and_calls_only_the_members_the_rule_names(self) -> None:
        calls = self.simulate()["calls"]
        batch1_round1 = sorted(c.split(":")[3] for c in calls if c.startswith("debate:batch-1:round-1:"))
        self.assertEqual(len(batch1_round1), 6)
        batch1_round2 = sorted(c.split(":")[3] for c in calls if c.startswith("debate:batch-1:round-2:"))
        self.assertEqual(batch1_round2, ["numerical-analyst"])
        self.assertFalse([c for c in calls if c.startswith("debate:batch-2:round-2:")])
        self.assertIn("notes:batch-1", calls)
        self.assertIn("notes:batch-2", calls)

    def test_panel_run_reproduces_golden_report(self) -> None:
        result = self.simulate()["result"]
        self.assertEqual(result["dropped"], [])
        project = Path(tempfile.mkdtemp(prefix="sci-review-project-"))
        self.addCleanup(shutil.rmtree, project, True)
        init = run([sys.executable, str(PLUGIN / "scripts" / "panel.py"), "init", "--project", str(project)])
        run_dir = Path(init.stdout.strip())
        self.addCleanup(shutil.rmtree, run_dir, True)
        shutil.copy(GOLDEN / "scope.json", run_dir / "scope.json")
        shutil.copy(GOLDEN / "panel.json", run_dir / "panel.json")
        (run_dir / "workflow-result.json").write_text(json.dumps(result), encoding="utf-8")
        script = str(PLUGIN / "scripts" / "panel.py")
        for argv in (
            ["ingest", "--run", str(run_dir), str(run_dir / "workflow-result.json")],
            ["adjudicate", "--run", str(run_dir)],
        ):
            step = run([sys.executable, script, *argv])
            self.assertEqual(step.returncode, 0, step.stderr)
        report = run([sys.executable, script, "report", "--run", str(run_dir)])
        self.assertEqual(report.returncode, 0, report.stderr)
        self.assertEqual(report.stdout, (GOLDEN / "expected-report.md").read_text(encoding="utf-8"))

    def test_reversed_line_ranges_are_normalised(self) -> None:
        golden = Path(tempfile.mkdtemp()) / "full"
        self.addCleanup(shutil.rmtree, golden.parent, True)
        shutil.copytree(GOLDEN, golden)
        path = golden / "candidates" / "theorist.json"
        message = json.loads(path.read_text(encoding="utf-8"))
        first = message["findings"][0]
        first["line_start"], first["line_end"] = first["line_end"], first["line_start"]
        path.write_text(json.dumps(message), encoding="utf-8")
        result = self.simulate(golden=golden)["result"]
        theorist = next(m for m in result["candidates"] if m["perspective"] == "theorist")
        for finding in theorist["findings"]:
            self.assertLessEqual(finding["line_start"], finding["line_end"])
        self.assertFalse(panel.validate_message("candidate-findings", theorist))

    def test_project_root_is_stated_in_every_prompt(self) -> None:
        root = "/reviewed/project"
        prompts = self.simulate({"project": root})["prompts"]
        self.assertTrue(prompts)
        for label, prompt in prompts.items():
            self.assertIn(f"The reviewed project is {root}.", prompt, label)

    def test_single_perspective_is_raised_to_two(self) -> None:
        output = self.simulate({"perspectives": ["theorist"]})
        independent = sorted(c.split(":")[1] for c in output["calls"] if c.startswith("independent:"))
        self.assertEqual(independent, ["numerical-analyst", "theorist"])
        self.assertTrue(output["result"]["candidates"])

    def test_empty_scope_returns_without_agents(self) -> None:
        output = self.simulate({"scope": {"files": [], "note": "nothing"}})
        self.assertEqual(output["calls"], [])

    def test_harness_is_dedented(self) -> None:
        self.assertEqual(textwrap.dedent(SIMULATION_HARNESS), SIMULATION_HARNESS)


if __name__ == "__main__":
    unittest.main()

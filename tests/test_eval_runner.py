from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER = REPO_ROOT / "scripts" / "run_evals.py"
SPEC = importlib.util.spec_from_file_location("run_evals", RUNNER)
assert SPEC and SPEC.loader
run_evals = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(run_evals)


class EvalRunnerTests(unittest.TestCase):
    def test_case_selection_and_arm_validation(self) -> None:
        cases = [{"id": 1, "name": "one"}, {"id": 2, "name": "two"}]
        self.assertEqual([cases[0]], run_evals._select_cases(cases, "1"))
        self.assertEqual([cases[1]], run_evals._select_cases(cases, "two"))
        self.assertEqual("no_skill", run_evals._parse_arms(["no_skill"])[0]["name"])
        with self.assertRaises(run_evals.EvalError):
            run_evals._select_cases(cases, "missing")
        with self.assertRaises(run_evals.EvalError):
            run_evals._parse_arms(["candidate=/does/not/exist"])

    def test_codex_command_keeps_prompt_as_one_argument(self) -> None:
        prompt = "Review $(touch should-not-run); `whoami`; and spaces"
        command = run_evals._codex_command(
            prompt=prompt,
            workspace=Path("/tmp/work space"),
            output_file=Path("/tmp/final output"),
            model="gpt-5.4-mini",
            reasoning="low",
            schema_file=None,
        )
        self.assertIsInstance(command, list)
        self.assertEqual(prompt, command[-1])
        self.assertNotIn("shell=True", RUNNER.read_text(encoding="utf-8"))

    def test_event_usage_and_probe_markers_are_deterministic(self) -> None:
        events = "\n".join(
            [
                json.dumps({"type": "item.completed"}),
                json.dumps(
                    {
                        "type": "turn.completed",
                        "usage": {"input_tokens": 12, "output_tokens": 3},
                    }
                ),
            ]
        )
        self.assertEqual(
            {"input_tokens": 12, "output_tokens": 3},
            run_evals._usage_from_events(events),
        )
        output = "answer\n<probe:task-state-with-files>\n<probe:agent-harness-design>"
        self.assertEqual(
            ["agent-harness-design", "task-state-with-files"],
            sorted(set(run_evals.PROBE_PATTERN.findall(output))),
        )

    def test_atomic_json_writer_replaces_only_the_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "nested" / "result.json"
            run_evals._write_json(target, {"ok": True})
            self.assertEqual({"ok": True}, json.loads(target.read_text()))


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
from pathlib import Path
import subprocess
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

    def test_host_commands_keep_prompt_as_one_argument(self) -> None:
        prompt = "Review $(touch should-not-run); `whoami`; and spaces"
        for adapter in (run_evals.CodexHost(), run_evals.ZCodeHost()):
            command = adapter.build_command(
                prompt=prompt,
                workspace=Path("/tmp/work space"),
                output_file=Path("/tmp/final output"),
                model=None,
                reasoning=None,
                schema_file=None,
                restrict_tools=True,
            )
            self.assertIsInstance(command, list)
            self.assertIn(prompt, command)
            self.assertNotIn(";", [item for item in command if item != prompt])
        self.assertNotIn("shell=True", RUNNER.read_text(encoding="utf-8"))

    def test_codex_argv_preserves_the_isolation_flags(self) -> None:
        adapter = run_evals.CodexHost()
        command = adapter.build_command(
            prompt="p",
            workspace=Path("/tmp/ws"),
            output_file=Path("/tmp/final.txt"),
            model="gpt-5.4-mini",
            reasoning="low",
            schema_file=Path("/tmp/schema.json"),
            restrict_tools=True,
        )
        expected_prefix = [
            "codex",
            "exec",
            "--ephemeral",
            "--ignore-user-config",
            "--ignore-rules",
            "--skip-git-repo-check",
            "--sandbox",
            "read-only",
            "--disable",
            "plugins",
            "--disable",
            "memories",
            "--disable",
            "hooks",
            "--disable",
            "apps",
            "--model",
            "gpt-5.4-mini",
            "--config",
            'model_reasoning_effort="low"',
            "--json",
            "--color",
            "never",
            "--output-last-message",
            "/tmp/final.txt",
            "--cd",
            "/tmp/ws",
            "--output-schema",
            "/tmp/schema.json",
        ]
        self.assertEqual(expected_prefix, command[:-1])

    def test_zcode_argv_reflects_the_verified_headless_surface(self) -> None:
        adapter = run_evals.ZCodeHost()
        common = adapter.build_command(
            prompt="p",
            workspace=Path("/tmp/ws"),
            output_file=Path("/tmp/final.txt"),
            model=None,
            reasoning=None,
            schema_file=None,
            restrict_tools=False,
        )
        self.assertEqual(
            ["zcode", "--prompt", "p", "--json", "--no-color", "--cwd", "/tmp/ws",
             "--mode", "yolo"],
            common,
        )
        restricted = adapter.build_command(
            prompt="p",
            workspace=Path("/tmp/ws"),
            output_file=Path("/tmp/final.txt"),
            model=None,
            reasoning=None,
            schema_file=None,
            restrict_tools=True,
        )
        self.assertEqual(len(common) + 2, len(restricted))
        self.assertEqual(common, restricted[:-2])
        self.assertEqual("--disallowed-tools", restricted[-2])
        self.assertIn("Bash", restricted[-1])
        self.assertIn("Write", restricted[-1])

    def test_probe_skills_install_into_each_hosts_own_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            self.assertEqual(
                home / ".agents" / "skills" / "probe-a",
                run_evals.CodexHost().probe_skill_root(home) / "probe-a",
            )
            self.assertEqual(
                home / ".zcode" / "skills" / "probe-a",
                run_evals.ZCodeHost().probe_skill_root(home) / "probe-a",
            )
            self.assertTrue((home / ".zcode" / "skills").is_dir())

    def test_zcode_config_is_referenced_by_symlink_and_never_copied(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "real-home" / ".zcode" / "cli" / "config.json"
            source.parent.mkdir(parents=True)
            source.write_text("{}", encoding="utf-8")
            adapter = run_evals.ZCodeHost()
            old = dict(run_evals.os.environ)
            run_evals.os.environ["ZCODE_CONFIG"] = str(source)
            try:
                home = root / "eval-home"
                home.mkdir()
                adapter.link_configuration(home)
            finally:
                run_evals.os.environ.clear()
                run_evals.os.environ.update(old)
            linked = home / ".zcode" / "cli" / "config.json"
            self.assertTrue(linked.is_symlink())
            self.assertEqual(source.resolve(), linked.resolve())

    def test_zcode_config_link_requires_an_existing_source(self) -> None:
        adapter = run_evals.ZCodeHost()
        old = dict(run_evals.os.environ)
        run_evals.os.environ["ZCODE_CONFIG"] = "/does/not/exist/config.json"
        try:
            with tempfile.TemporaryDirectory() as temporary:
                home = Path(temporary)
                with self.assertRaises(run_evals.EvalError):
                    adapter.link_configuration(home)
        finally:
            run_evals.os.environ.clear()
            run_evals.os.environ.update(old)

    def test_model_and_reasoning_overrides_are_refused_or_defaulted_per_host(self) -> None:
        codex = run_evals.CodexHost()
        self.assertEqual("gpt-5.4-mini", codex.resolve_model(None))
        self.assertEqual("low", codex.resolve_reasoning(None))
        self.assertEqual("high", codex.resolve_reasoning("high"))
        with self.assertRaises(run_evals.EvalError):
            codex.resolve_reasoning("extreme")
        zcode = run_evals.ZCodeHost()
        self.assertIsNone(zcode.resolve_model(None))
        self.assertIsNone(zcode.resolve_reasoning(None))
        with self.assertRaises(run_evals.EvalError):
            zcode.resolve_model("glm-9")
        with self.assertRaises(run_evals.EvalError):
            zcode.resolve_reasoning("low")

    def test_structured_output_methods_are_declared_truthfully(self) -> None:
        codex = run_evals.CodexHost()
        zcode = run_evals.ZCodeHost()
        self.assertEqual("output_schema", codex.structured_output_method)
        self.assertEqual("prompt_json_validated", zcode.structured_output_method)
        self.assertIsNone(codex.structured_output_instructions({"type": "object"}))
        instructions = zcode.structured_output_instructions(
            {"type": "object", "properties": {"winner": {"type": "string"}}}
        )
        assert instructions is not None
        self.assertIn('"winner"', instructions)
        self.assertIn("no prose", instructions)

    def test_model_json_parse_tolerates_fences_and_prose(self) -> None:
        self.assertEqual({"a": 1}, run_evals._parse_model_json('{"a": 1}'))
        self.assertEqual(
            {"a": 1}, run_evals._parse_model_json('```json\n{"a": 1}\n```')
        )
        self.assertEqual(
            {"a": 1}, run_evals._parse_model_json('Verdict:\n{"a": 1}\nDone.')
        )
        with self.assertRaises(json.JSONDecodeError):
            run_evals._parse_model_json("no object at all")

    def test_zcode_execution_parse_maps_usage_and_errors(self) -> None:
        adapter = run_evals.ZCodeHost()
        completed = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout=json.dumps(
                {
                    "response": " answer ",
                    "usage": {
                        "inputTokens": 12,
                        "outputTokens": 3,
                        "reasoningTokens": 1,
                        "cacheReadTokens": 9,
                        "modelRequestCount": 2,
                    },
                }
            ),
            stderr="",
        )
        parsed = adapter.parse_execution(
            completed=completed, root=Path("/tmp/x"), output_file=Path("/tmp/x/f")
        )
        self.assertEqual("ok", parsed["status"])
        self.assertEqual("answer", parsed["final_output"])
        self.assertEqual(
            {
                "input_tokens": 12,
                "output_tokens": 3,
                "reasoning_tokens": 1,
                "cache_read_tokens": 9,
                "model_requests": 2,
            },
            parsed["usage"],
        )
        missing = adapter.parse_execution(
            completed=subprocess.CompletedProcess(
                args=[], returncode=0, stdout="{}", stderr=""
            ),
            root=Path("/tmp/x"),
            output_file=Path("/tmp/x/f"),
        )
        self.assertEqual("error", missing["status"])
        self.assertEqual("no_final_message", missing["error"])
        crashed = adapter.parse_execution(
            completed=subprocess.CompletedProcess(
                args=[], returncode=1, stdout="", stderr="quota exhausted"
            ),
            root=Path("/tmp/x"),
            output_file=Path("/tmp/x/f"),
        )
        self.assertEqual("usage_or_rate_limit", crashed["error"])

    def test_rate_limit_patterns_are_recognized_for_every_host(self) -> None:
        for adapter in (run_evals.CodexHost(), run_evals.ZCodeHost()):
            self.assertTrue(adapter.is_rate_limited("You've hit your usage limit.", ""))
            self.assertTrue(adapter.is_rate_limited("", "HTTP 429 too many requests"))
            self.assertFalse(adapter.is_rate_limited("plain failure", "other"))

    def test_zcode_run_evidence_reads_only_rollout_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rollout = root / "home" / ".zcode" / "cli" / "rollout"
            rollout.mkdir(parents=True)
            record = {
                "model": {"modelId": "GLM-5.2", "providerId": "builtin:test"},
                "request": {
                    "body": {
                        "thinking": {"type": "enabled", "budget_tokens": 32000},
                        "output_config": {"effort": "max"},
                    }
                },
            }
            (rollout / "model-io-sess_1.jsonl").write_text(
                json.dumps(record) + "\n", encoding="utf-8"
            )
            evidence = run_evals.ZCodeHost().extra_run_evidence(root)
            self.assertEqual(
                {
                    "observed_model": {
                        "model_id": "GLM-5.2",
                        "provider": "builtin:test",
                        "thinking": {"type": "enabled", "budget_tokens": 32000},
                        "effort": "max",
                    }
                },
                evidence,
            )

    def test_observed_configuration_replaces_host_resolved_placeholders(self) -> None:
        result = {
            "configuration": {"model": None, "reasoning": None},
            "runs": [
                {
                    "observed_model": {
                        "model_id": "GLM-5.2",
                        "provider": "builtin:bigmodel-coding-plan",
                        "thinking": {"type": "enabled", "budget_tokens": 32000},
                        "effort": "max",
                    }
                }
            ],
        }
        run_evals._fill_observed_configuration(result)
        self.assertEqual(
            "builtin:bigmodel-coding-plan/GLM-5.2", result["configuration"]["model"]
        )
        self.assertEqual(
            "effort=max thinking=enabled(32000)", result["configuration"]["reasoning"]
        )
        pinned = {
            "configuration": {"model": "gpt-5.4-mini", "reasoning": "low"},
            "runs": [],
        }
        run_evals._fill_observed_configuration(pinned)
        self.assertEqual("gpt-5.4-mini", pinned["configuration"]["model"])

    def test_host_registry_names_the_extension_contract(self) -> None:
        codex = run_evals._build_host("codex", None)
        self.assertEqual("codex", codex.name)
        zcode = run_evals._build_host("zcode", ["/opt/zcode"])
        self.assertEqual(["/opt/zcode"], zcode.binary)
        for known in run_evals.KNOWN_HOSTS_WITHOUT_ADAPTERS:
            with self.assertRaises(run_evals.EvalError) as caught:
                run_evals._build_host(known, None)
            self.assertIn("HostAdapter", str(caught.exception))
        with self.assertRaises(run_evals.EvalError):
            run_evals._build_host("unknown-host", None)

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

    def test_tree_digest_is_stable_across_text_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            lf = root / "lf"
            crlf = root / "crlf"
            lf.mkdir()
            crlf.mkdir()
            (lf / "SKILL.md").write_bytes(b"first\nsecond\n")
            (crlf / "SKILL.md").write_bytes(b"first\r\nsecond\r\n")
            self.assertEqual(run_evals._tree_digest(lf), run_evals._tree_digest(crlf))

    def test_tree_digest_uses_case_sensitive_relative_path_order(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            (root / "agents").mkdir()
            (root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (root / "agents" / "openai.yaml").write_text("agent\n", encoding="utf-8")
            expected = hashlib.sha256()
            for name, content in (
                ("SKILL.md", b"skill\n"),
                ("agents/openai.yaml", b"agent\n"),
            ):
                expected.update(name.encode("utf-8"))
                expected.update(b"\0")
                expected.update(content)
                expected.update(b"\0")
            self.assertEqual(expected.hexdigest(), run_evals._tree_digest(root))

    def test_atomic_json_writer_replaces_only_the_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "nested" / "result.json"
            run_evals._write_json(target, {"ok": True})
            self.assertEqual({"ok": True}, json.loads(target.read_text()))


if __name__ == "__main__":
    unittest.main()

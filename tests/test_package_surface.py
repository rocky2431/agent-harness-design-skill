from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "agent-harness-design"
SKILL_ROOT = PLUGIN_ROOT / "skills" / "agent-harness-design"


def skill_digest() -> str:
    digest = hashlib.sha256()
    files = [
        path
        for path in SKILL_ROOT.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    ]
    for path in sorted(
        files, key=lambda item: item.relative_to(SKILL_ROOT).as_posix()
    ):
        digest.update(path.relative_to(SKILL_ROOT).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes().replace(b"\r\n", b"\n"))
        digest.update(b"\0")
    return digest.hexdigest()


class PackageSurfaceTests(unittest.TestCase):
    def test_plugin_marketplace_and_skill_identity_match(self) -> None:
        plugin = json.loads(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(
                encoding="utf-8"
            )
        )
        marketplace = json.loads(
            (REPO_ROOT / ".agents" / "plugins" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        entry = marketplace["plugins"][0]
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertEqual("agent-harness-design", plugin["name"])
        self.assertEqual(plugin["name"], entry["name"])
        self.assertEqual("./skills/", plugin["skills"])
        self.assertEqual("./plugins/agent-harness-design", entry["source"]["path"])
        self.assertIn("name: agent-harness-design", skill)
        self.assertEqual(["Skills"], plugin["interface"]["capabilities"])
        self.assertLessEqual(len(plugin["interface"]["defaultPrompt"]), 128)
        openai = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        prompt = re.search(r'(?m)^  default_prompt: "([^"]+)"$', openai)
        short = re.search(r'(?m)^  short_description: "([^"]+)"$', openai)
        self.assertIsNotNone(prompt)
        self.assertIsNotNone(short)
        self.assertEqual(plugin["interface"]["defaultPrompt"], prompt.group(1))
        self.assertEqual(plugin["interface"]["shortDescription"], short.group(1))

    def test_version_is_consistent(self) -> None:
        plugin = json.loads(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(
                encoding="utf-8"
            )
        )
        version = plugin["version"]
        self.assertIn(
            f'metadata:\n  author: rocky2431\n  version: "{version}"',
            (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            f'VERSION = "{version}"',
            (REPO_ROOT / "scripts" / "install_user.py").read_text(
                encoding="utf-8"
            ),
        )

    def test_skill_encodes_calibration_without_old_universal_gates(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("**Invariant**", skill)
        self.assertIn("**Default**", skill)
        self.assertIn("**Conditional pattern**", skill)
        self.assertIn("capability-preserving determinism", skill)
        self.assertIn("Keep a denial local", skill)
        self.assertIn("Do not silently downgrade", skill)
        self.assertIn("capability tax", skill)
        self.assertIn("multiple agents", skill)
        self.assertIn("without an incident", skill)
        self.assertIn("## Keep activation scoped", skill)
        self.assertIn("backward\n  compatibility", skill)
        self.assertIn("in band, in the artifact, and in the trace", skill)
        self.assertIn("Separate authority gates from resource governors", skill)
        self.assertIn("soft in-band\n  tier before its hard ceiling", skill)
        self.assertIn("Re-test on upgrade; do not remove on upgrade", skill)
        for reference in (
            "references/harness-vs-software.md",
            "references/failure-visibility.md",
        ):
            self.assertIn(reference, skill)
            self.assertTrue((SKILL_ROOT / reference).is_file())
        self.assertNotIn("only after the simpler live path has failed", skill)
        self.assertNotIn("Parallelize only independent, read-only", skill)
        self.assertLess(len(skill.splitlines()), 220)

        description = re.search(r'(?m)^description: "([^"]+)"$', skill)
        self.assertIsNotNone(description)
        self.assertLessEqual(len(description.group(1)), 380)
        self.assertIn("not for ordinary coding", description.group(1))

    def test_eval_set_covers_activation_and_anti_dogma_cases(self) -> None:
        data = json.loads(
            (SKILL_ROOT / "evals" / "evals.json").read_text(encoding="utf-8")
        )
        names = {case["name"] for case in data["evals"]}
        arms = data["comparison_arms"]
        self.assertGreaterEqual(len(arms), 2)
        self.assertEqual(len(arms), len(set(arms)))
        self.assertIn("no_skill", arms)
        self.assertIn("agent-harness-design", arms)
        self.assertGreaterEqual(len(data["evals"]), 10)
        self.assertEqual(len(data["evals"]), len(names))
        for required in (
            "preventive_regulated_controls_without_incident",
            "multi_agent_can_be_first_choice",
            "parallel_isolated_writes",
            "validated_model_grader_can_gate",
            "denied_effect_does_not_cripple_reasoning",
            "silent_capability_reduction_is_not_a_control",
            "provider_neutral_allows_native_adapters",
            "retire_stale_model_compensation",
            "long_task_pauses_without_fake_completion",
            "root_agents_file_is_a_map",
            "measure_capability_tax_with_ablation",
            "ordinary_task_does_not_activate",
            "success_shaped_fallback_is_a_defect",
            "compatibility_must_not_hide_capability_loss",
            "two_tier_budget_not_a_bare_step_cap",
            "no_fixed_number_on_semantic_quantities",
            "long_thread_versus_consolidated_restart",
            "retest_scaffolding_rather_than_remove_it",
            "completion_must_close_on_the_environment",
            "disputed_practice_needs_a_criterion",
        ):
            self.assertIn(required, names)

    def test_trigger_set_covers_routing_and_adjacent_skills(self) -> None:
        data = json.loads(
            (SKILL_ROOT / "evals" / "trigger-evals.json").read_text(encoding="utf-8")
        )
        cases = data["evals"]
        self.assertEqual(len(cases), len({case["name"] for case in cases}))
        self.assertTrue({"positive", "negative", "ambiguous", "coexistence"} <= {case["kind"] for case in cases})
        expected = {skill for case in cases for skill in case["expected_skills"]}
        self.assertTrue(
            {"agent-harness-design", "task-state-with-files", "agent-delegation"}
            <= expected
        )
        coexistence = next(
            case for case in cases if case["name"] == "coexistence_delegate_harness_audit"
        )
        self.assertEqual(2, len(coexistence["accepted_skill_sets"]))

    def test_release_evidence_matches_the_current_skill(self) -> None:
        """Release evidence must exist for the declared version and be internally
        consistent. Counts are derived from the recorded configuration rather than
        pinned, so any host, case count, or trial count stays valid."""
        version = json.loads(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )["version"]
        evidence = REPO_ROOT / "eval-results"
        behavior_path = evidence / f"v{version}-behavior.json"
        trigger_path = evidence / f"v{version}-trigger.json"
        for path in (behavior_path, trigger_path):
            self.assertTrue(
                path.is_file(),
                f"missing release evidence for v{version}: {path.name}",
            )

        behavior = json.loads(behavior_path.read_text(encoding="utf-8"))
        trigger = json.loads(trigger_path.read_text(encoding="utf-8"))
        digest = skill_digest()

        candidate = next(
            arm
            for arm in behavior["configuration"]["arms"]
            if arm["name"] == "agent-harness-design"
        )
        self.assertEqual(digest, candidate["source_sha256"])
        self.assertEqual(digest, trigger["configuration"]["skill_source_sha256"])

        configuration = behavior["configuration"]
        trials = configuration["trials"]
        arms = configuration["arms"]
        cases = configuration["selected_cases"]
        self.assertEqual(len(cases) * len(arms) * trials, len(behavior["runs"]))
        if behavior.get("grades"):
            self.assertEqual(len(cases) * trials, len(behavior["grades"]))

        trigger_configuration = trigger["configuration"]
        self.assertEqual(
            len(trigger_configuration["selected_cases"]) * trigger_configuration["trials"],
            len(trigger["runs"]),
        )

        # Evidence means completed runs. A file full of failures is not a release record.
        for name, payload in (("behavior", behavior), ("trigger", trigger)):
            failed = [run for run in payload["runs"] if run.get("status") != "ok"]
            self.assertEqual(
                [], failed[:3], f"{name} evidence contains unsuccessful runs"
            )

        # The host that produced the evidence must be recorded, whichever host it was.
        recorded_host = {
            key: value
            for key, value in configuration.items()
            if key.endswith("_cli") or key in {"host", "model"}
        }
        self.assertTrue(recorded_host, "evidence must record the host and model used")

    def test_research_basis_uses_many_primary_sources(self) -> None:
        research = (SKILL_ROOT / "references" / "research-basis.md").read_text(
            encoding="utf-8"
        )
        self.assertGreaterEqual(research.count("https://"), 18)
        for source in ("agentskills.io", "developers.openai.com", "anthropic.com"):
            self.assertIn(source, research)
        self.assertIn("arxiv.org/abs/2406.12045", research)
        self.assertIn("arxiv.org/abs/2503.18813", research)
        self.assertIn("2026-07-28", research)
        self.assertNotIn("specification/2025-11-25", research)
        self.assertIn("outgrow the benefits of **collaboration**", research)
        self.assertNotIn("outgrow the benefits of multi-agent systems", research)
        self.assertIn("## Commonly miscited", research)
        self.assertNotIn("/research/building-effective-agents", research)

    def test_package_has_no_hooks_mcp_or_machine_specific_paths(self) -> None:
        package_files = [
            path
            for path in REPO_ROOT.rglob("*")
            if path.is_file()
            and ".git" not in path.relative_to(REPO_ROOT).parts
            and "__pycache__" not in path.relative_to(REPO_ROOT).parts
        ]
        relative = {path.relative_to(REPO_ROOT).as_posix() for path in package_files}
        self.assertFalse(any("hooks/" in path for path in relative))
        self.assertFalse(any(path.endswith(".mcp.json") for path in relative))

        offenders: list[str] = []
        machine_path = "/Users/" + "rocky243"
        unfinished_marker = "[TO" + "DO:"
        for path in package_files:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if machine_path in text or unfinished_marker in text:
                offenders.append(path.relative_to(REPO_ROOT).as_posix())
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()

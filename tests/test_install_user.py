from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "scripts" / "install_user.py"
SPEC = importlib.util.spec_from_file_location("install_user", INSTALLER)
assert SPEC and SPEC.loader
install_user = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(install_user)


class UserInstallerTests(unittest.TestCase):
    def run_installer(
        self,
        home: Path,
        command: str,
        *extra: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(INSTALLER),
                command,
                "--home",
                str(home),
                *extra,
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_host_destinations_match_supported_cli_locations(self) -> None:
        home = Path("/tmp/example-home")
        expected = {
            "hermes": home / ".hermes/skills/agent-harness-design",
            "claude": home / ".claude/skills/agent-harness-design",
            "codex": home / ".agents/skills/agent-harness-design",
            "kimi": home / ".kimi/skills/agent-harness-design",
            "zcode": home / ".zcode/skills/agent-harness-design",
            "opencode": home / ".config/opencode/skills/agent-harness-design",
        }
        self.assertEqual(
            {
                host: install_user._skill_destination(home, host)
                for host in install_user.SUPPORTED_HOSTS
            },
            expected,
        )

    def test_install_doctor_update_and_uninstall_all_hosts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            first_backup = home / "backups" / "first"
            second_backup = home / "backups" / "second"
            remove_backup = home / "backups" / "remove"

            first = self.run_installer(
                home, "install", "--backup-dir", str(first_backup)
            )
            doctor = self.run_installer(home, "doctor", "--json")
            second = self.run_installer(
                home, "install", "--backup-dir", str(second_backup)
            )
            uninstall = self.run_installer(
                home, "uninstall", "--backup-dir", str(remove_backup)
            )

            self.assertEqual(0, first.returncode, first.stderr)
            self.assertEqual(0, doctor.returncode, doctor.stderr)
            report = json.loads(doctor.stdout)
            self.assertTrue(report["ok"])
            self.assertEqual(set(install_user.SUPPORTED_HOSTS), set(report["hosts"]))
            self.assertTrue(
                all(status["skill"] == "ok" for status in report["hosts"].values())
            )
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertEqual(0, uninstall.returncode, uninstall.stderr)

            for host in install_user.SUPPORTED_HOSTS:
                destination = install_user._skill_destination(home, host)
                self.assertFalse(destination.exists(), host)
                self.assertTrue((second_backup / host / "skill" / "SKILL.md").is_file())
                self.assertTrue((remove_backup / host / "skill" / "SKILL.md").is_file())

    def test_unmanaged_destination_fails_before_any_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            codex = install_user._skill_destination(home, "codex")
            codex.mkdir(parents=True)
            (codex / "SKILL.md").write_text("owner copy\n", encoding="utf-8")

            result = self.run_installer(
                home,
                "install",
                "--hosts",
                "hermes,codex",
                "--backup-dir",
                str(home / "backup"),
            )

            self.assertEqual(2, result.returncode)
            self.assertIn("Refusing to replace unmanaged Skill", result.stderr)
            self.assertFalse(
                install_user._skill_destination(home, "hermes").exists()
            )
            self.assertEqual(
                "owner copy\n", (codex / "SKILL.md").read_text(encoding="utf-8")
            )

    def test_explicit_replacement_backs_up_unmanaged_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            claude = install_user._skill_destination(home, "claude")
            claude.mkdir(parents=True)
            (claude / "SKILL.md").write_text("local edits\n", encoding="utf-8")
            backup = home / "backup"

            result = self.run_installer(
                home,
                "install",
                "--hosts",
                "claude",
                "--replace-existing",
                "--backup-dir",
                str(backup),
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue(install_user._is_managed(claude))
            self.assertEqual(
                "local edits\n",
                (backup / "claude" / "skill" / "SKILL.md").read_text(
                    encoding="utf-8"
                ),
            )

    def test_doctor_detects_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            install = self.run_installer(home, "install", "--hosts", "opencode")
            destination = install_user._skill_destination(home, "opencode")
            with (destination / "SKILL.md").open("a", encoding="utf-8") as handle:
                handle.write("\nchanged\n")
            doctor = self.run_installer(
                home, "doctor", "--hosts", "opencode", "--json"
            )

            self.assertEqual(0, install.returncode, install.stderr)
            self.assertEqual(1, doctor.returncode)
            report = json.loads(doctor.stdout)
            self.assertEqual("drifted", report["hosts"]["opencode"]["skill"])


if __name__ == "__main__":
    unittest.main()

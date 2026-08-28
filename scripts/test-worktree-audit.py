#!/usr/bin/env python3

import json
import os
import pathlib
import subprocess
import tempfile
import unittest


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
AUDIT = SCRIPT_DIR / "worktree-audit.py"


def run(*args: str, cwd: pathlib.Path) -> None:
    subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True)


class WorktreeAuditTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name) / "repo"
        self.root.mkdir()
        run("git", "init", "-b", "main", cwd=self.root)
        run("git", "config", "user.email", "test@example.com", cwd=self.root)
        run("git", "config", "user.name", "Test", cwd=self.root)
        (self.root / "seed.txt").write_text("seed\n")
        run("git", "add", "seed.txt", cwd=self.root)
        run("git", "commit", "-m", "seed", cwd=self.root)
        self.active = pathlib.Path(self.temp.name) / "active"
        self.clean = pathlib.Path(self.temp.name) / "clean"
        self.dirty = pathlib.Path(self.temp.name) / "dirty"
        run("git", "worktree", "add", "-b", "active", str(self.active), cwd=self.root)
        run("git", "worktree", "add", "-b", "clean", str(self.clean), cwd=self.root)
        run("git", "worktree", "add", "-b", "dirty", str(self.dirty), cwd=self.root)
        (self.dirty / "uncommitted.txt").write_text("keep me\n")

    def tearDown(self):
        self.temp.cleanup()

    def test_classifies_active_clean_unowned_and_dirty_unowned(self):
        env = os.environ.copy()
        env["DUET_WORKTREE_AGENTS_JSON"] = json.dumps(
            [{"name": "dev1", "cwd": str(self.active)}]
        )
        result = subprocess.run(
            [str(AUDIT), str(self.root)],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 3)
        self.assertIn(f"ACTIVE\tdev1\t{self.active.resolve()}", result.stdout)
        self.assertIn(f"CLEAN_UNOWNED\t-\t{self.clean.resolve()}", result.stdout)
        self.assertIn(f"DIRTY_UNOWNED\t-\t{self.dirty.resolve()}", result.stdout)

    def test_reads_local_herdr_agent_list_without_federation(self):
        fake_herdr = pathlib.Path(self.temp.name) / "herdr"
        fake_herdr.write_text(
            "#!/usr/bin/env python3\n"
            "import json\n"
            f"print(json.dumps({{'result': {{'agents': [{{'name': 'dev1', 'cwd': {str(self.active)!r}}}]}}}}))\n"
        )
        fake_herdr.chmod(0o755)
        env = os.environ.copy()
        env.pop("DUET_WORKTREE_AGENTS_JSON", None)
        env["HERDR_BIN"] = str(fake_herdr)

        result = subprocess.run(
            [str(AUDIT), str(self.root)],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 3)
        self.assertIn(f"ACTIVE\tdev1\t{self.active.resolve()}", result.stdout)


if __name__ == "__main__":
    unittest.main()

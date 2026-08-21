#!/usr/bin/env python3

import os
import pathlib
import stat
import subprocess
import tempfile
import textwrap
import unittest


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
START = SCRIPT_DIR / "herdr-agent-start.sh"


class HerdrAgentStartTest(unittest.TestCase):
    def run_start(self, process_environment: str) -> tuple[subprocess.CompletedProcess[str], str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = pathlib.Path(temp_dir)
            fake_herdr = temp_path / "herdr"
            fake_ps = temp_path / "ps"
            call_log = temp_path / "calls.txt"
            fake_herdr.write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env python3
                    import json, os, pathlib, sys
                    args = sys.argv[1:]
                    with pathlib.Path(os.environ["CALL_LOG"]).open("a") as stream:
                        stream.write(" ".join(args) + "\\n")
                    core = args[2:] if args[:2] == ["--session", "default"] else args
                    if core[:2] == ["pane", "get"]:
                        print(json.dumps({"result": {"pane": {"cwd": "/tmp"}}}))
                    elif core[:2] == ["pane", "process-info"]:
                        print(json.dumps({"result": {"process_info": {"foreground_processes": [{"name": "codex", "pid": 123}]}}}))
                    else:
                        print(json.dumps({"result": {"type": "ok"}}))
                    """
                )
            )
            fake_ps.write_text(f"#!/bin/sh\nprintf '%s\\n' '{process_environment}'\n")
            for executable in (fake_herdr, fake_ps):
                executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
            env = os.environ.copy()
            env.update({"HERDR_BIN": str(fake_herdr), "PS_BIN": str(fake_ps), "CALL_LOG": str(call_log)})
            result = subprocess.run(
                [str(START), "dev1", "codex", "w1:p1", "resume", "native-session"],
                cwd=SCRIPT_DIR.parent,
                env=env,
                text=True,
                capture_output=True,
                timeout=10,
                check=False,
            )
            return result, call_log.read_text()

    def test_resume_prepares_color_environment_before_start(self):
        result, calls = self.run_start("codex TERM=xterm-256color COLORTERM=truecolor")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("color=ok", result.stdout)
        self.assertLess(calls.index("pane run"), calls.index("agent start"))
        self.assertIn("unset NO_COLOR CODEX_CI", calls)
        self.assertIn("agent start dev1 --kind codex --pane w1:p1 --timeout 120000 -- resume native-session", calls)

    def test_resume_pins_codex_to_the_pane_worktree(self):
        result, calls = self.run_start("codex TERM=xterm-256color COLORTERM=truecolor")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "agent start dev1 --kind codex --pane w1:p1 --timeout 120000 -- "
            "resume native-session --cd /tmp",
            calls,
        )

    def test_live_codex_with_no_color_is_rejected(self):
        result, _ = self.run_start(
            "codex NO_COLOR=1 CODEX_CI=1 TERM=xterm-256color COLORTERM=truecolor"
        )
        self.assertEqual(result.returncode, 4)
        self.assertIn("failed color preflight", result.stderr)


if __name__ == "__main__":
    unittest.main()

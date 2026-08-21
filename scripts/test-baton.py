#!/usr/bin/env python3

import os
import pathlib
import stat
import subprocess
import tempfile
import textwrap
import unittest


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
BATON = SCRIPT_DIR / "baton.sh"


class BatonTest(unittest.TestCase):
    def test_idle_codex_prompt_requires_state_confirmation_and_readback(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = pathlib.Path(temp_dir)
            fake_herdr = temp_path / "herdr"
            prompt_log = temp_path / "prompt.txt"
            args_log = temp_path / "args.txt"
            fake_herdr.write_text(
                textwrap.dedent(
                    """\
                    #!/usr/bin/env python3
                    import json
                    import os
                    import pathlib
                    import sys

                    args = sys.argv[1:]
                    with pathlib.Path(os.environ["FAKE_ARGS_LOG"]).open("a") as log_file:
                        log_file.write(" ".join(args) + "\\n")
                    core = args[2:] if args[:2] == ["--session", "test-session"] else args
                    if core == ["session", "list", "--json"]:
                        print(json.dumps({"sessions": [{"name": "test-session", "running": True}]}))
                    elif core == ["workspace", "list"]:
                        print(json.dumps({"result": {"workspaces": [{"workspace_id": "w1", "label": "test"}]}}))
                    elif core == ["agent", "list"]:
                        print(json.dumps({"result": {"agents": [{
                            "name": "codex-idle", "workspace_id": "w1", "pane_id": "w1:p1",
                            "terminal_id": "term-1", "agent": "codex", "agent_status": "idle",
                            "foreground_cwd": "/tmp/test"
                        }]}}))
                    elif core == ["pane", "process-info", "--pane", "w1:p1"]:
                        print(json.dumps({"result": {"process_info": {"foreground_process_group_id": 101}}}))
                    elif core[:3] == ["agent", "prompt", "codex-idle"]:
                        pathlib.Path(os.environ["FAKE_PROMPT_LOG"]).write_text(core[3])
                        print(json.dumps({"result": {"agent": {"name": "codex-idle", "agent_status": "working"}}}))
                    elif core[:3] == ["agent", "read", "codex-idle"]:
                        log = pathlib.Path(os.environ["FAKE_PROMPT_LOG"])
                        print(log.read_text() if log.exists() else "")
                    else:
                        print(json.dumps({"error": {"message": "unexpected: " + repr(args)}}))
                        raise SystemExit(1)
                    """
                )
            )
            fake_herdr.chmod(fake_herdr.stat().st_mode | stat.S_IXUSR)
            env = os.environ.copy()
            env.update(
                {
                    "PATH": f"{temp_dir}:{env['PATH']}",
                    "HERDR_BIN": str(fake_herdr),
                    "FAKE_PROMPT_LOG": str(prompt_log),
                    "FAKE_ARGS_LOG": str(args_log),
                }
            )
            result = subprocess.run(
                [str(BATON), "send", "codex-idle", "owner", "test assignment"],
                cwd=SCRIPT_DIR.parent,
                env=env,
                text=True,
                capture_output=True,
                timeout=10,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("baton delivered", result.stdout)
            self.assertIn("[delivery:", prompt_log.read_text())
            prompt_args = args_log.read_text()
            self.assertIn(
                "agent prompt codex-idle", prompt_args
            )
            self.assertIn(
                "--wait --until working --until idle --until done --until blocked --timeout 10000",
                prompt_args,
            )
            self.assertIn("agent read codex-idle", prompt_args)


if __name__ == "__main__":
    unittest.main()

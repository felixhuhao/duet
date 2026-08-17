#!/usr/bin/env python3

import importlib.util
import pathlib
import unittest
from unittest import mock


MODULE_PATH = pathlib.Path(__file__).with_name("herdr-federation.py")
SPEC = importlib.util.spec_from_file_location("herdr_federation", MODULE_PATH)
assert SPEC and SPEC.loader
FEDERATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FEDERATION)


class FederationTest(unittest.TestCase):
    def test_run_json_rejects_api_error_payload(self):
        completed = mock.Mock(returncode=0, stdout='{"error":{"message":"offline"}}', stderr="")
        with mock.patch.object(FEDERATION.subprocess, "run", return_value=completed):
            with self.assertRaises(FEDERATION.FederationError):
                FEDERATION.run_json(["agent", "list"])

    def test_discover_aggregates_only_running_sessions(self):
        def fake_run(args):
            responses = {
                ("session", "list", "--json"): {
                    "sessions": [
                        {"name": "btrack", "running": True},
                        {"name": "etrack", "running": True},
                        {"name": "old", "running": False},
                    ]
                },
                ("--session", "btrack", "workspace", "list"): {
                    "result": {"workspaces": [{"workspace_id": "w1", "label": "B"}]}
                },
                ("--session", "btrack", "agent", "list"): {
                    "result": {
                        "agents": [
                            {
                                "name": "b-spec",
                                "workspace_id": "w1",
                                "pane_id": "w1:p1",
                                "agent": "codex",
                                "agent_status": "idle",
                                "cwd": "/b",
                            }
                        ]
                    }
                },
                ("--session", "etrack", "workspace", "list"): {
                    "result": {"workspaces": [{"workspace_id": "w2", "label": "E"}]}
                },
                ("--session", "etrack", "agent", "list"): {
                    "result": {
                        "agents": [
                            {
                                "name": "e-delivery",
                                "workspace_id": "w2",
                                "pane_id": "w2:p2",
                                "agent": "opencode",
                                "agent_status": "working",
                                "foreground_cwd": "/e",
                            }
                        ]
                    }
                },
            }
            return responses[tuple(args)]

        with mock.patch.object(FEDERATION, "run_json", side_effect=fake_run):
            agents = FEDERATION.discover()
        self.assertEqual([agent["name"] for agent in agents], ["b-spec", "e-delivery"])
        self.assertEqual(agents[1]["workspace_label"], "E")
        self.assertEqual(agents[1]["status"], "working")

    def test_resolve_global_and_session_qualified_names(self):
        agents = [
            {"name": "spec", "session": "btrack"},
            {"name": "spec", "session": "etrack"},
        ]
        with self.assertRaises(FEDERATION.FederationError):
            FEDERATION.resolve(agents, "spec")
        self.assertEqual(FEDERATION.resolve(agents, "etrack/spec")["session"], "etrack")
        with self.assertRaises(FEDERATION.FederationError):
            FEDERATION.resolve(agents, "missing")


if __name__ == "__main__":
    unittest.main()

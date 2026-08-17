#!/usr/bin/env python3
"""Discover and resolve named agents across all running Herdr sessions."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any


HERDR = os.environ.get("HERDR_BIN", "herdr")


class FederationError(RuntimeError):
    pass


def run_json(args: list[str]) -> dict[str, Any]:
    proc = subprocess.run(
        [HERDR, *args],
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )
    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip() or f"exit {proc.returncode}"
        raise FederationError(f"{' '.join(args)}: {detail}")
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise FederationError(f"{' '.join(args)}: invalid JSON") from exc
    if "error" in payload:
        error = payload["error"]
        raise FederationError(f"{' '.join(args)}: {error.get('message', error)}")
    return payload


def discover() -> list[dict[str, Any]]:
    sessions = run_json(["session", "list", "--json"]).get("sessions", [])
    agents: list[dict[str, Any]] = []
    for session in sessions:
        if not session.get("running"):
            continue
        name = session["name"]
        workspace_result = run_json(["--session", name, "workspace", "list"])
        workspace_labels = {
            workspace.get("workspace_id"): workspace.get("label", "")
            for workspace in workspace_result.get("result", {}).get("workspaces", [])
        }
        agent_result = run_json(["--session", name, "agent", "list"])
        for raw in agent_result.get("result", {}).get("agents", []):
            agent_name = raw.get("name") or raw.get("agent_name")
            if not agent_name:
                continue
            workspace_id = raw.get("workspace_id", "")
            agents.append(
                {
                    "name": agent_name,
                    "session": name,
                    "workspace": workspace_id,
                    "workspace_label": workspace_labels.get(workspace_id, ""),
                    "pane": raw.get("pane_id", ""),
                    "kind": raw.get("agent", "unknown"),
                    "status": raw.get("agent_status", "unknown"),
                    "cwd": raw.get("foreground_cwd") or raw.get("cwd", ""),
                }
            )
    return sorted(agents, key=lambda item: (item["session"], item["name"]))


def resolve(agents: list[dict[str, Any]], target: str) -> dict[str, Any]:
    session_name = None
    agent_name = target
    if "/" in target:
        session_name, agent_name = target.split("/", 1)
    matches = [
        agent
        for agent in agents
        if agent["name"] == agent_name
        and (session_name is None or agent["session"] == session_name)
    ]
    if not matches:
        raise FederationError(f"agent not found: {target}")
    if len(matches) > 1:
        locations = ", ".join(f"{item['session']}/{item['name']}" for item in matches)
        raise FederationError(
            f"agent name is not globally unique: {target} ({locations}); "
            "use <session>/<name> or rename the duplicate"
        )
    return matches[0]


def print_table(agents: list[dict[str, Any]]) -> None:
    headers = ("NAME", "SESSION", "WORKSPACE", "RUNTIME", "STATUS", "PANE", "CWD")
    rows = [
        (
            item["name"],
            item["session"],
            item["workspace_label"] or item["workspace"],
            item["kind"],
            item["status"],
            item["pane"],
            item["cwd"],
        )
        for item in agents
    ]
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(str(value)))
    print("  ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    for row in rows:
        print("  ".join(str(value).ljust(widths[index]) for index, value in enumerate(row)))


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    peers_parser = subparsers.add_parser("peers")
    peers_parser.add_argument("--json", action="store_true")
    resolve_parser = subparsers.add_parser("resolve")
    resolve_parser.add_argument("target")
    args = parser.parse_args()

    try:
        agents = discover()
        if args.command == "peers":
            if args.json:
                print(json.dumps(agents, ensure_ascii=False))
            else:
                print_table(agents)
            return 0
        print(json.dumps(resolve(agents, args.target), ensure_ascii=False))
        return 0
    except (FederationError, subprocess.TimeoutExpired) as exc:
        print(f"HERDR FEDERATION ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

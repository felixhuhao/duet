#!/usr/bin/env python3
"""Discover and resolve named agents across all running Herdr sessions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from typing import Any


HERDR = os.environ.get("HERDR_BIN", "herdr")


class FederationError(RuntimeError):
    pass


STATUS_MAP = {
    "working": "working",
    "idle": "idle",
    "blocked": "blocked",
    "done": "idle",
    "dead": "dead",
    "exited": "dead",
}


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


def process_identity(session: str, name: str, raw: dict[str, Any]) -> dict[str, Any]:
    """Build an opaque incarnation from the live terminal and foreground process."""
    pane = raw.get("pane_id", "")
    process_id: int | str = ""
    if pane:
        try:
            result = run_json(["--session", session, "pane", "process-info", "--pane", pane])
            process = result.get("result", {}).get("process_info", {})
            process_id = process.get("foreground_process_group_id", "")
        except FederationError:
            pass

    agent_session = raw.get("agent_session") or {}
    agent_session_id = agent_session.get("value", "")
    terminal_id = raw.get("terminal_id", "")
    if not terminal_id or not process_id:
        return {"instance_id": "", "process_id": process_id, "agent_session_id": agent_session_id}

    material = "\0".join((session, name, terminal_id, str(process_id))).encode()
    instance_id = "i-" + hashlib.sha256(material).hexdigest()[:12]
    return {
        "instance_id": instance_id,
        "process_id": process_id,
        "agent_session_id": agent_session_id,
    }


def semantic_status(raw_status: str, instance_id: str) -> str:
    status = STATUS_MAP.get(raw_status, "unknown")
    if status in {"working", "idle", "blocked"} and not instance_id:
        return "unknown"
    return status


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
            identity = process_identity(name, agent_name, raw)
            raw_status = raw.get("agent_status", "unknown")
            agents.append(
                {
                    "name": agent_name,
                    "session": name,
                    "workspace": workspace_id,
                    "workspace_label": workspace_labels.get(workspace_id, ""),
                    "pane": raw.get("pane_id", ""),
                    "kind": raw.get("agent", "unknown"),
                    "status": semantic_status(raw_status, identity["instance_id"]),
                    "raw_status": raw_status,
                    "cwd": raw.get("foreground_cwd") or raw.get("cwd", ""),
                    **identity,
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


def verify(agents: list[dict[str, Any]], target: str, instance_id: str) -> dict[str, Any]:
    current = resolve(agents, target)
    if not instance_id or current.get("instance_id") != instance_id:
        actual = current.get("instance_id") or "unverified"
        raise FederationError(
            f"stale agent instance: {target} expected {instance_id or 'unverified'}, got {actual}"
        )
    return current


def print_table(agents: list[dict[str, Any]]) -> None:
    headers = ("NAME", "SESSION", "WORKSPACE", "RUNTIME", "STATUS", "INSTANCE", "PANE", "CWD")
    rows = [
        (
            item["name"],
            item["session"],
            item["workspace_label"] or item["workspace"],
            item["kind"],
            item["status"],
            item["instance_id"] or "unverified",
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
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("target")
    verify_parser.add_argument("instance_id")
    args = parser.parse_args()

    try:
        agents = discover()
        if args.command == "peers":
            if args.json:
                print(json.dumps(agents, ensure_ascii=False))
            else:
                print_table(agents)
            return 0
        if args.command == "resolve":
            result = resolve(agents, args.target)
        else:
            result = verify(agents, args.target, args.instance_id)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (FederationError, subprocess.TimeoutExpired) as exc:
        print(f"HERDR FEDERATION ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

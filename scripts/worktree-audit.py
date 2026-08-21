#!/usr/bin/env python3
"""One-shot audit for linked worktrees versus live Herdr agent ownership."""

import json
import os
import pathlib
import subprocess
import sys


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent


def run(args, cwd):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"{' '.join(args)}: {detail}")
    return result.stdout


def worktrees(repo):
    output = run(["git", "worktree", "list", "--porcelain"], repo)
    records = []
    for block in output.strip().split("\n\n"):
        record = {"branch": "DETACHED"}
        for line in block.splitlines():
            if line.startswith("worktree "):
                record["path"] = line.removeprefix("worktree ")
            elif line.startswith("branch refs/heads/"):
                record["branch"] = line.removeprefix("branch refs/heads/")
        if "path" in record:
            records.append(record)
    return records


def agents():
    injected = os.environ.get("DUET_WORKTREE_AGENTS_JSON")
    if injected is not None:
        return json.loads(injected)
    output = run(
        [sys.executable, str(SCRIPT_DIR / "herdr-federation.py"), "peers", "--json"],
        SCRIPT_DIR.parent,
    )
    return json.loads(output)


def main():
    if len(sys.argv) != 2:
        print("usage: worktree-audit.py <repo-root>", file=sys.stderr)
        return 2
    repo = pathlib.Path(sys.argv[1]).resolve()
    records = worktrees(repo)
    if not records:
        print("no worktrees found", file=sys.stderr)
        return 2
    live_agents = agents()
    print("STATE\tAGENT\tPATH\tBRANCH")
    violations = 0
    for record in records[1:]:
        tree = pathlib.Path(record["path"]).resolve()
        owners = sorted(
            agent.get("name", "")
            for agent in live_agents
            if pathlib.Path(agent.get("cwd", "/nonexistent")).resolve() == tree
            and agent.get("name")
        )
        if owners:
            state = "ACTIVE"
            owner = ",".join(owners)
        else:
            dirty = bool(run(["git", "status", "--porcelain"], tree).strip())
            state = "DIRTY_UNOWNED" if dirty else "CLEAN_UNOWNED"
            owner = "-"
            violations += 1
        print(f"{state}\t{owner}\t{tree}\t{record['branch']}")
    return 3 if violations else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"worktree audit failed: {error}", file=sys.stderr)
        raise SystemExit(2)

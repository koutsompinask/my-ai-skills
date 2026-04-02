#!/usr/bin/env python3
"""Suggest a Conventional Commit message from git changes.

Heuristics are intentionally simple and deterministic:
- Prefer staged changes when present, or when --staged-only is passed.
- Infer type from changed paths and diff keywords.
- Infer scope from top-level path dominance.
"""

import argparse
import collections
import re
import subprocess
import sys


def run_git(args):
    proc = subprocess.run(["git"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "git {} failed".format(" ".join(args)))
    return proc.stdout


def get_status_lines():
    out = run_git(["status", "--short"])
    return [line for line in out.splitlines() if line.strip()]


def has_staged_changes(status_lines):
    for line in status_lines:
        # XY path ; staged if X != space and X != ?
        if len(line) >= 2 and line[0] not in {" ", "?"}:
            return True
    return False


def parse_paths(name_status):
    paths = []
    for line in name_status.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) >= 2:
            paths.append(parts[-1])
    return paths


def top_scope(paths):
    if not paths:
        return None
    counts = collections.Counter()
    for path in paths:
        top = path.split("/", 1)[0]
        if top and top not in {".", ".."}:
            counts[top] += 1
    if not counts:
        return None
    scope = counts.most_common(1)[0][0]
    if re.match(r"^[a-zA-Z0-9_.-]+$", scope):
        return scope.lower()
    return None


def infer_type(paths, patch):
    lowered_paths = [p.lower() for p in paths]
    patch_l = patch.lower()

    if any(".gitea/workflows/" in p or ".github/workflows/" in p for p in lowered_paths):
        return "ci"
    if lowered_paths and all(
        p.endswith((".md", ".rst", ".txt", ".adoc")) or p.startswith(("docs/", "doc/"))
        for p in lowered_paths
    ):
        return "docs"
    if lowered_paths and all(
        "test" in p or p.endswith(("_test.py", ".spec.ts", ".test.ts", "test.java"))
        for p in lowered_paths
    ):
        return "test"
    if any(
        p in {
            "package.json",
            "pnpm-lock.yaml",
            "yarn.lock",
            "pom.xml",
            "build.gradle",
            "build.gradle.kts",
            "settings.gradle.kts",
        }
        for p in lowered_paths
    ):
        return "build"
    if any(k in patch_l for k in ["fix", "bug", "error", "exception", "nullpointer", "npe"]):
        return "fix"
    if any(k in patch_l for k in ["perf", "optimiz", "faster", "latency"]):
        return "perf"
    if any(k in patch_l for k in ["refactor", "cleanup", "rename", "extract method"]):
        return "refactor"
    return "chore"


def build_subject(commit_type, scope, paths):
    if not paths:
        summary = "update repository"
    elif len(paths) == 1:
        summary = "update {}".format(paths[0])
    else:
        summary = "update {} files".format(len(paths))

    if scope:
        return "{}({}): {}".format(commit_type, scope, summary)
    return "{}: {}".format(commit_type, summary)


def load_snapshot(staged_only):
    status_lines = get_status_lines()
    staged = staged_only or has_staged_changes(status_lines)
    if staged:
        name_status = run_git(["diff", "--cached", "--name-status"])
        patch = run_git(["diff", "--cached"])
    else:
        name_status = run_git(["diff", "--name-status"])
        patch = run_git(["diff"])

    paths = parse_paths(name_status)
    return {"paths": paths, "status_lines": status_lines, "patch": patch}


def main():
    parser = argparse.ArgumentParser(description="Suggest Conventional Commit message")
    parser.add_argument("--staged-only", action="store_true", help="Use only staged changes")
    parser.add_argument("--include-body", action="store_true", help="Print a body template")
    args = parser.parse_args()

    try:
        snapshot = load_snapshot(staged_only=args.staged_only)
    except RuntimeError as err:
        print("ERROR: {}".format(err), file=sys.stderr)
        return 2

    if not snapshot["paths"]:
        print("No diff detected. Stage or modify files first.")
        return 1

    commit_type = infer_type(snapshot["paths"], snapshot["patch"])
    scope = top_scope(snapshot["paths"])
    subject = build_subject(commit_type, scope, snapshot["paths"])

    print(subject)

    if args.include_body:
        print()
        print("Explain what changed and why.")
        print("Mention notable behavior, risk, or migration notes.")

    if "breaking change" in snapshot["patch"].lower():
        print()
        print("BREAKING CHANGE: describe the incompatible behavior change")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

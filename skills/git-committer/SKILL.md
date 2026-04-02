---
name: git-committer
description: Analyze git changes and generate high-quality commit messages that follow Conventional Commits 1.0.0. Use when a user asks to write, improve, validate, or standardize commit messages from staged or unstaged diffs, including selecting type/scope, concise summary, body details, and breaking-change footers.
---

# Git Committer

## Overview

Inspect repository changes and produce informative commit messages that conform to Conventional Commits.
Use deterministic checks to map change patterns to commit `type`, optional `scope`, summary, body, and footers.

## Workflow

1. Inspect changes with `git status --short`, `git diff --stat`, and `git diff --name-status`.
2. Prefer staged content via `git diff --cached` when staged files exist.
3. Determine the primary intent of the change and choose one Conventional Commit type.
4. Infer optional scope from dominant module/path when useful.
5. Draft a concise subject line: `<type>(<scope>): <description>` or `<type>: <description>`.
6. Add body paragraphs only when they improve clarity.
7. Add `BREAKING CHANGE:` footer when behavior/API compatibility changes.
8. Return one recommended message plus 1-2 alternatives only when ambiguity is high.

## Type Selection

Select the dominant type by intent:

- `feat`: introduce new user-facing behavior or capability
- `fix`: correct a defect
- `refactor`: change internals without feature or fix intent
- `perf`: improve performance
- `docs`: documentation-only change
- `test`: add or modify tests only
- `build`: build system or dependency tooling change
- `ci`: CI workflow or automation change
- `chore`: maintenance that does not fit above
- `revert`: explicitly revert prior commit(s)

If a diff combines multiple unrelated intents, recommend split commits.

## Message Quality Rules

- Keep subject imperative and specific.
- Prefer lowercase type and scope for consistency.
- Keep subject short; avoid trailing punctuation.
- Mention significant side effects in body.
- Use footers for issue references and breaking changes.
- Follow the strict syntax defined in [references/conventional-commits-v1.0.0.md](references/conventional-commits-v1.0.0.md).

## Script Usage

Use `scripts/suggest_commit_message.py` to generate a first-pass message from current repo diffs, then refine manually.

```bash
python3 scripts/suggest_commit_message.py
python3 scripts/suggest_commit_message.py --staged-only
python3 scripts/suggest_commit_message.py --include-body
```

## Output Contract

Return:

1. Final commit message in a fenced block.
2. One-line reason for chosen `type` and `scope`.
3. Optional warning if changes should be split into multiple commits.

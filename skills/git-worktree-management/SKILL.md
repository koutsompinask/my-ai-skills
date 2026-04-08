---
name: git-worktree-management
description: Create, inspect, merge, and clean up Git worktrees safely. Use when Codex needs to isolate work on a branch in a separate checkout, verify worktree or branch state, merge a worktree branch back into the main branch, or remove temporary worktrees without disturbing unrelated local changes in the main checkout.
---

# Git Worktree Management

Use this skill to manage short-lived Git worktrees safely when the user wants isolated branch work without stashing or disturbing their current checkout.

## Core Rules

- Inspect repository state before creating, merging, or removing a worktree.
- Prefer sibling worktree paths such as `../repo-feature-name` unless the user specifies another location.
- Create a dedicated branch for the worktree unless the user explicitly asks to attach a detached HEAD.
- Never assume the main checkout is clean; check for modified and untracked files first.
- Before merging, verify whether incoming paths overlap with untracked files in the target checkout.
- Prefer `git merge --ff-only <branch>` when the worktree branch is directly ahead of the target branch.
- Remove the worktree before deleting its branch.
- Do not delete branches, remove worktrees, or push unless the user asked for that cleanup step.

## Quick Workflow

### 1. Inspect state

Run:

```bash
git worktree list
git branch --show-current
git status --short
git log --oneline --decorate -n 10
```

Use these to answer:
- Which branch is the current checkout on?
- Does a worktree for this task already exist?
- Is the main checkout dirty?
- Is the target worktree branch already merged or still ahead?

### 2. Create the worktree

Default pattern:

```bash
git worktree add ../repo-task-name -b task-branch-name <base-branch>
```

Guidance:
- Use the current integration branch as the base unless the user specifies another base.
- Choose names that make the directory and branch relationship obvious.
- If `.git` writes are sandbox-restricted, request approval rather than working around Git metadata updates.

### 3. Work inside the worktree

Inside the worktree:

```bash
git status --short
git branch --show-current
```

Then make the requested changes, run validation there, and commit on the worktree branch.

### 4. Merge back safely

Before merging into the main checkout:

```bash
git status --short
git diff --name-only <target-branch>..<worktree-branch>
find <overlap-prone-paths> -type f
```

Check for overlap between:
- files added by the worktree branch
- untracked files already present in the target checkout

If the branch is linear on top of the target branch, prefer:

```bash
git merge --ff-only <worktree-branch>
```

If a fast-forward is not possible:
- inspect why first
- do not create a merge commit silently unless the user asked for it or the repo workflow clearly requires it

### 5. Clean up

Cleanup order:

```bash
git worktree remove ../repo-task-name
git branch -d task-branch-name
```

Optional final step:

```bash
git push origin <target-branch>
```

Do not attempt `git branch -d` before removing the worktree if that branch is still checked out there.

## Decision Rules

### When the main checkout is dirty

- Keep the work in a separate worktree.
- Avoid commands that would rewrite or clean the main checkout.
- Merge only after confirming the incoming paths do not overwrite untracked local work.

### When a merge is requested

- First determine whether it is a fast-forward, rebase, or true merge situation.
- Prefer the least surprising path:
  - `git merge --ff-only` for linear history
  - ask before using a non-fast-forward merge if it changes history shape or may create conflicts

### When cleanup is requested

- Remove the worktree first.
- Delete the branch second.
- Leave pre-existing unrelated branches alone unless the user explicitly asks to prune them too.

## Common Commands

Create:

```bash
git worktree add ../repo-fix-auth -b fix-auth master
```

Inspect:

```bash
git worktree list
git status --short
git log --oneline --decorate -n 5
```

Merge:

```bash
git merge --ff-only fix-auth
```

Cleanup:

```bash
git worktree remove ../repo-fix-auth
git branch -d fix-auth
```

## Pitfalls To Catch

- A dirty main checkout does not block using a worktree, but it does raise merge risk.
- Untracked files can block or endanger merges even when tracked files have no conflicts.
- `git worktree add` and merge operations update `.git` metadata; request approval if the environment blocks those writes.
- Removing a worktree with local uncommitted changes may fail; inspect that worktree first.
- Deleting a branch still attached to a worktree will fail until the worktree is removed.

## Response Style

When helping with worktrees:
- tell the user which checkout and branch you are operating on
- state whether the merge is fast-forward or not
- call out any overlap risk with local untracked files
- explain the remaining cleanup steps after merge in one short list

# Conventional Commits 1.0.0 (Local Reference)

Source: https://www.conventionalcommits.org/en/v1.0.0/
License note from source: Creative Commons CC BY 3.0.

## Summary

Conventional Commits defines a lightweight structure for commit messages so humans and tools can infer change intent. It aligns commit semantics with SemVer-style release automation.

Canonical shape:

```text
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

## Structural Elements

- `fix` communicates a bug fix (patch-level intent).
- `feat` communicates a new feature (minor-level intent).
- `BREAKING CHANGE` footer or `!` in header communicates incompatible changes (major-level intent).
- Additional types are allowed (`build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf`, `test`, etc.).
- Scope is optional and appears in parentheses after type.
- Footers can include metadata and issue references using trailer-like syntax.

## Specification Rules (Implementation-Oriented)

1. Prefix commit with type, optional scope, optional `!`, then required `: ` separator.
2. Use `feat` when adding a feature.
3. Use `fix` when fixing a bug.
4. Scope may be provided and should name the impacted area.
5. Put short description immediately after `: `.
6. Body may be added after one blank line.
7. Body may contain multiple paragraphs.
8. Footers may be added one blank line after body.
9. Each footer uses token + `: ` value, or token + ` #` value.
10. Footer tokens should use `-` instead of spaces.
11. Exception: `BREAKING CHANGE` token is explicitly allowed with space.
12. Footer values may span lines until next valid footer token.
13. Mark breaking changes with `!` in header or with breaking-change footer.
14. If using footer form, use uppercase `BREAKING CHANGE: <description>`.
15. If using `!`, breaking footer may be omitted.
16. Types beyond `feat` and `fix` are valid.
17. Parsers should treat units as case-insensitive, except `BREAKING CHANGE` token must remain uppercase.
18. `BREAKING-CHANGE` is synonymous with `BREAKING CHANGE` as footer token.

## SemVer Mapping

- `fix` -> PATCH
- `feat` -> MINOR
- Any commit with breaking change -> MAJOR

## Examples

```text
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

```text
feat!: send an email to the customer when a product is shipped
```

```text
feat(api)!: send an email to the customer when a product is shipped
```

```text
chore!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

```text
docs: correct spelling of CHANGELOG
```

```text
feat(lang): add Polish language
```

```text
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Reviewed-by: Z
Refs: #123
```

## Why Use It

- Generate changelogs automatically.
- Derive version bumps automatically.
- Communicate change intent clearly to collaborators.
- Trigger build/release workflows from commit metadata.
- Improve contributor onboarding through predictable history.

## FAQ Highlights

- Early-stage projects should still use the convention.
- Type casing can vary; consistency is recommended.
- If one commit contains multiple intents, split into multiple commits when possible.
- Convention supports fast development by improving long-term maintainability.
- Team-specific types/extensions are acceptable.
- If the wrong type is used before merge/release, interactive rebase can fix history.
- If a non-spec type slips in, tooling may ignore it, but repository remains valid.
- Not every contributor must write perfect Conventional Commits if maintainers squash/rewrite on merge.

## Revert Guidance

Spec does not strictly define revert semantics. A common practice is:

```text
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

Tooling can implement project-specific policies for revert handling.

# Git Workflow

## What This Doc Is

This doc describes the recommended git workflow for `meikipop`.

Read this before creating branches, making commits, or preparing a PR.

## Branching

- Start feature or fix work from `main` unless there is an explicit reason not to.
- Use a short-lived branch for each focused piece of work.
- Prefer descriptive branch names over ticket-only names.

Recommended branch name patterns:
- `feat/native-shell-skeleton`
- `feat/native-overlay-spike`
- `fix/popup-focus-regression`
- `docs/native-migration-plan`
- `refactor/lookup-service-boundary`

## Commit Scope

- Keep each commit coherent and reviewable.
- Prefer commits that represent one logical step.
- Separate pure documentation, refactors, and behavior changes when practical.
- Do not mix unrelated cleanup into the same commit.

Good commit boundaries:
- add a new planning doc
- refactor one subsystem without intended behavior change
- implement one user-visible behavior change
- add one focused verification or build fix

## Commit Messages

Use short, imperative commit subjects.

Recommended style:
- `Add native migration planning docs`
- `Document recommended git workflow`
- `Refactor lookup result formatting`
- `Fix popup focus restoration on macOS`

Guidelines:
- Start with a verb.
- Keep the subject concise.
- Describe the change, not the debugging story.
- Avoid vague messages like `stuff`, `updates`, or `fixes`.

Optional body guidance:
- Add a body when the reason is not obvious from the diff.
- Explain important tradeoffs, constraints, or follow-up work.

Example:

```text
Add native overlay planning doc

Document the recommended split between highlight overlay and popup
so future native implementation work does not carry forward the Qt
popup/capture lock coupling.
```

## Pull Requests

- Prefer PRs with a focused scope.
- Make the PR title readable as a changelog-quality summary.
- Include manual verification notes when runtime behavior changed.
- Call out packaging-sensitive changes explicitly.

Useful PR description points:
- what changed
- why it changed
- how it was verified
- risks or open questions

## Suggested Workflow

1. Branch from `main`.
2. Make one focused set of changes.
3. Commit in logical steps.
4. Re-read the diff before opening a PR.
5. Summarize verification honestly.
6. Open a PR back to `main`.

## Repo-Specific Notes

- PR CI builds packaged artifacts for `main`, but that does not prove runtime correctness.
- Changes involving OCR providers, `.spec` files, packaging, popup timing, input, or capture deserve extra care.
- Documentation-only changes can usually stay in a single commit if they are tightly related.
- For larger implementation work, a small sequence of clean commits is better than one opaque dump commit.

## What This Repo Does Not Currently Enforce

There is currently no documented enforced rule here for:
- conventional commits
- squash-only merges
- strict branch naming
- ticket-number prefixes

Until that changes, optimize for clarity and reviewability.

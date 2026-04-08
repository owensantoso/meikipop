# CURRENT_STATE.md

## What This Doc Is

This is a repo-reality snapshot for future agents.

Read this before broad refactors, packaging work, provider changes, or when deciding how much verification is needed.

This doc supports risk assessment, task planning, and safe-change scoping.

## Production-Critical Paths

Fact:
- The main user-facing path is the runtime pipeline in `src/meikipop/main.py`, `src/meikipop/gui/`, `src/meikipop/screenshot/`, `src/meikipop/ocr/`, and `src/meikipop/dictionary/`.
- Frozen distribution appears to matter operationally because CI and releases focus on PyInstaller artifacts for Linux, macOS, and Windows.
- Dictionary bootstrap is production-critical because the app downloads `dictionary.pkl` at runtime if it is missing.

## What Looks In Progress Or Actively Curated

Fact:
- Version is currently `2.0.0rc3` in both `pyproject.toml` and `src/meikipop/config/config.py`.
- Release automation is present and reasonably maintained.
- Dictionary automation runs weekly through `.github/workflows/build-dictionary.yml`.
- OCR provider support is active enough to include multiple backends plus custom-provider guidance.

Inference:
- The repo is maintained primarily around shipping binaries and dictionary updates rather than around deep automated validation.

## What Looks Brittle, Confusing, Or Stale

### Verification Surface Is Thin

Fact:
- There are no tests, lint jobs, or typecheck jobs in the repo.
- PR CI only builds packaged artifacts.

Implication:
- Runtime regressions can ship if packaging still succeeds.

### Dynamic Runtime Vs Static Packaging

Fact:
- Providers are discovered dynamically from `src/meikipop/ocr/providers/`.
- All three `.spec` files manually list provider files and hidden imports.

Implication:
- Source changes can work locally but disappear from packaged builds.

### Broad Exception Handling

Fact:
- Core loops in input, screenshot, OCR, hit scanning, and lookup use broad exception handling and continue running.

Implication:
- Broken behavior may degrade silently instead of failing fast.

### Stale Doc Surface

Fact:
- `docs/CUSTOM_OCR_PROVIDER.md` existed before this pass but had stale path references.
- README is strong for end-user setup, but it is not sufficient as the source of truth for agent-safe repo changes.

### Multi-Monitor Fragility

Fact:
- `src/meikipop/screenshot/screenmanager.py` has an explicit note that monitor changes are not handled correctly.

## Notable Footguns

- `LatestValueQueue` is intentionally lossy.
- `config` is global and mutable from several runtime areas.
- Popup timing and screenshot timing are coordinated through `screen_lock`.
- OCR provider output ordering matters to hit scanning.
- The Google Lens provider contains a hardcoded API key and remote endpoint.
- Generated protobuf/betterproto files are checked in and should not be hand-edited.

## What Needs Human Confirmation

Unverified:
- Whether the app currently starts and behaves correctly on this machine.
- Whether all packaged artifacts launch successfully after build.
- Whether first-run dictionary download still succeeds reliably.
- Whether Screen AI setup paths are acceptable on macOS in practice.
- Whether the hardcoded Google Lens path and key are intentionally supported long-term.

## Recommended Agent Stance

- Treat runtime changes as high-verification work, especially in input, screenshot, OCR, hit-scan, popup, and packaging code.
- Assume cross-platform behavior differs until proven otherwise.
- Do not trust packaging success as proof of correctness.
- Read the focused component docs before changing shared runtime behavior.

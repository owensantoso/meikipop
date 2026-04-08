# AGENTS.md

## What This Repo Is

- `meikipop` is a single-package Python desktop app that shows a popup Japanese dictionary for text anywhere on screen.
- The runtime is a thread-based pipeline: input -> screenshot -> OCR -> hit-scan -> dictionary lookup -> popup render.
- OCR is pluggable at runtime through provider packages under `src/meikipop/ocr/providers/`, but packaged builds still require manual PyInstaller spec updates.
- Dictionary data is an external artifact in the user data directory, not a tracked repo asset.
- CI mostly proves the app can be packaged on Linux, macOS, and Windows; it does not prove runtime behavior.

## Top-Level Structure

- `src/meikipop/main.py`: composition root and CLI entrypoint.
- `src/meikipop/gui/`: popup, tray, settings, input polling, region selection, Magpie integration.
- `src/meikipop/screenshot/`: screen capture and scan-area ownership.
- `src/meikipop/ocr/`: provider interface, provider discovery, OCR worker, hit scanning.
- `src/meikipop/dictionary/`: dictionary loading, deconjugation, lookup/ranking.
- `src/meikipop/scripts/`: dictionary build and Yomitan import utilities.
- `.github/workflows/`: packaging and release automation.
- `meikipop.*.spec`: PyInstaller specs for each platform.
- `docs/agents/`: deeper agent-facing operating map.
- `docs/native/`: native macOS architecture, migration, overlay, and platform planning docs.
- `DESIGN.md`: visual and interaction guidance for the future native app.

## Essential Commands

```bash
pip install -e .
meikipop
meikipop build-dict
meikipop import-yomitan-dict-html path/to/dict.zip
meikipop import-yomitan-dict-text path/to/dict.zip
```

Packaging commands used in CI:

```bash
pyinstaller meikipop.macos.spec
xvfb-run pyinstaller meikipop.linux.x64.spec
pyinstaller meikipop.win.x64.spec
```

## Non-Obvious Rules And Gotchas

- Runtime provider discovery is dynamic, but frozen packaging is static. Adding or renaming a provider also requires updating all three `.spec` files.
- `LatestValueQueue` is intentionally lossy. It keeps only the latest pending value, which is core to the app's responsiveness.
- `config` is a singleton shared across UI, OCR, screenshot, and input code. Small config changes can have system-wide effects.
- `screen_lock` coordinates popup visibility and screenshot capture. Changes around popup timing or capture timing can cause self-capture regressions.
- The repo has no automated tests. Packaging success is not equivalent to runtime correctness.
- Existing `docs/CUSTOM_OCR_PROVIDER.md` is useful, but verify paths and packaging implications before following it blindly.

## Read This Next

- Repo layout or package boundaries: `docs/agents/repo-map.md`
- Build, package, or release work: `docs/agents/build-test-release.md`
- Branches, commits, and PR workflow: `docs/agents/git-workflow.md`
- Runtime flow or threading questions: `ARCHITECTURE.md`
- Current risks, stale areas, or unverified assumptions: `CURRENT_STATE.md`
- Native macOS architecture direction: `docs/native/architecture.md`
- Native macOS migration phases: `docs/native/migration-plan.md`
- Native overlay/highlighting constraints: `docs/native/overlay-highlighting.md`
- macOS-specific implementation notes: `docs/native/macos-platform-notes.md`
- Native design system and visual rules: `DESIGN.md`
- Popup, tray, input, or scan-area changes: `docs/agents/components/gui-and-input.md`
- OCR providers or OCR pipeline changes: `docs/agents/components/ocr-pipeline.md`
- Lookup, dictionary, or deconjugation changes: `docs/agents/components/dictionary-and-hit-scanning.md`
- Config paths, data locations, or first-run behavior: `docs/agents/components/configuration-and-paths.md`
- Safe UI edits: `docs/agents/runbooks/make-a-safe-ui-change.md`
- Adding or modifying an OCR provider: `docs/agents/runbooks/add-or-modify-an-ocr-provider.md`
- Dictionary rebuild/import workflows: `docs/agents/runbooks/update-dictionary-assets.md`
- Release packaging details: `docs/agents/runbooks/packaging-and-release.md`

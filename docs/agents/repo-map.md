# Repo Map

## What This Doc Is

This is the repo topology and task-routing map.

Read this before making any code change if you do not already know where a responsibility lives.

This doc supports fast orientation, scoping changes, and deciding what other files to load next.

## What Lives Where

- `pyproject.toml`: package metadata, dependencies, console script entrypoint, dictionary utility entrypoints.
- `README.md`: public product and user setup documentation.
- `AGENTS.md`: lightweight always-worth-loading entrypoint for future agents.
- `ARCHITECTURE.md`: system shape and runtime flow.
- `CURRENT_STATE.md`: risks, brittleness, and unverified assumptions.
- `.github/workflows/`: build, release, and dictionary automation.
- `meikipop.macos.spec`, `meikipop.linux.x64.spec`, `meikipop.win.x64.spec`: frozen packaging rules.
- `src/meikipop/main.py`: composition root and CLI dispatch.
- `src/meikipop/config/`: config singleton, app constants, platform flags.
- `src/meikipop/utils/`: paths, logging, latest-value queue.
- `src/meikipop/gui/`: popup, tray, input, region selector, settings dialog, Magpie helper.
- `src/meikipop/screenshot/`: screenshot capture and scan geometry ownership.
- `src/meikipop/ocr/`: OCR contract, OCR worker, hit scan logic, providers, line-grouping postprocessing.
- `src/meikipop/dictionary/`: dictionary loading, deconjugation, lookup and ranking.
- `src/meikipop/scripts/`: offline dictionary build/import tooling.
- `src/meikipop/resources/`: icons bundled into the app.

## Execution Entrypoints

### GUI App

- Console script: `meikipop`
- Entry function: `meikipop.main:main`
- GUI path: default branch of `main()` calls `run_gui()`

### Dictionary Utility Commands

- `meikipop build-dict`
- `meikipop import-yomitan-dict-html <zip>`
- `meikipop import-yomitan-dict-text <zip>`

### Packaging Entrypoints

- `pyinstaller meikipop.macos.spec`
- `xvfb-run pyinstaller meikipop.linux.x64.spec`
- `pyinstaller meikipop.win.x64.spec`

## Runtime Pipeline

```text
InputLoop
  -> ScreenManager
  -> OcrProcessor
  -> HitScanner
  -> Lookup
  -> Popup
```

Supporting surfaces:
- `TrayIcon` reconfigures runtime state and settings.
- `config` is shared across the whole pipeline.
- `screen_lock` coordinates popup visibility and screenshot capture.

## Boundary Guide

### Usually Safe To Work In Relative Isolation

- `src/meikipop/ocr/providers/*`
- `src/meikipop/dictionary/*`
- `src/meikipop/scripts/*`
- `src/meikipop/utils/logger.py`

Even here, still check:
- `.spec` files if you add or rename providers/resources
- docs if you change exposed workflows

### Read Surrounding Modules First

- `src/meikipop/gui/*`
- `src/meikipop/screenshot/*`
- `src/meikipop/ocr/hit_scan.py`
- `src/meikipop/config/config.py`
- `src/meikipop/main.py`

Reason:
- These areas coordinate via shared state, timing, locks, and user config.

## Cross-Cutting State

- `SharedState` in `src/meikipop/main.py`
- `config` singleton in `src/meikipop/config/config.py`
- `paths` singleton in `src/meikipop/utils/paths.py`
- `LatestValueQueue` in `src/meikipop/utils/lastest_queue.py`

## Platform-Specific Hotspots

- `src/meikipop/gui/input.py`
- `src/meikipop/gui/magpie_manager.py`
- `src/meikipop/ocr/providers/screenai/provider.py`
- `.github/workflows/build-*.yml`
- `meikipop.*.spec`

## Change Planning Footguns

- Provider names are persisted in config and shown in the tray UI.
- Provider discovery is dynamic, but packaging is manual.
- Hit scanning assumes OCR token order and `full_text` alignment are coherent.
- Queue semantics are intentionally lossy.
- Popup and screenshot behavior interact through timing and locking.

## Read This Next By Task

- Add or change an OCR provider: `docs/agents/runbooks/add-or-modify-an-ocr-provider.md`
- Change popup appearance or behavior: `docs/agents/components/gui-and-input.md`
- Change scan mode, hotkeys, or region selection: `docs/agents/components/gui-and-input.md`
- Change OCR flow or provider normalization: `docs/agents/components/ocr-pipeline.md`
- Change lookup ranking, kanji entries, or dictionary loading: `docs/agents/components/dictionary-and-hit-scanning.md`
- Change paths, config schema, or first-run behavior: `docs/agents/components/configuration-and-paths.md`
- Change packaging or releases: `docs/agents/build-test-release.md`

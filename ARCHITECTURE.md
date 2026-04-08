# ARCHITECTURE.md

## What This Doc Is

This is the system-shape map for `meikipop` as the repo exists today.

Read this when you need to understand the runtime pipeline, thread model, ownership boundaries, or where a change is likely to have side effects.

This doc supports changes to runtime behavior, UI flow, OCR provider work, lookup behavior, and packaging-sensitive refactors.

## System Shape

Fact:
- The app is composed in `src/meikipop/main.py`.
- `run_gui()` creates shared coordination state, a Qt app, the popup/tray/UI helpers, and five daemon worker threads: `Lookup`, `HitScanner`, `OcrProcessor`, `ScreenManager`, and `InputLoop`.
- `TrayIcon` stays on the Qt side and acts as the main runtime control surface for settings, scan mode, scan region, provider selection, pause/resume, and quit.

Fact:
- The shared coordination model is intentionally small:
  - `screenshot_trigger_event`
  - `ocr_queue`
  - `hit_scan_queue`
  - `lookup_queue`
  - `screen_lock`
- All three queues are `LatestValueQueue`, not FIFO queues.

Inference:
- The app is optimized for freshness and responsiveness, not for processing every intermediate state. Fast cursor movement or repeated scan triggers intentionally collapse work.

## End-To-End Runtime Flow

Fact:
1. `InputLoop` polls mouse position and hotkey state.
2. `ScreenManager` captures the configured region or screen and pushes a PIL image into `ocr_queue`.
3. `OcrProcessor` runs the selected OCR backend and pushes normalized paragraphs into `hit_scan_queue`.
4. `HitScanner` resolves the cursor position against OCR boxes and pushes a lookup suffix into `lookup_queue`.
5. `Lookup` resolves dictionary entries and writes the latest popup payload.
6. `Popup` polls that payload on a Qt timer, renders rich-text HTML, and moves/hides/shows itself near the cursor.

Inference:
- The architecture separates expensive OCR refreshes from cheaper re-hit-scans against the last OCR result. That is why mouse movement can update lookups without forcing OCR every time.

## Core Invariants

Fact:
- OCR providers must emit `Paragraph`, `Word`, and normalized `BoundingBox` objects from `src/meikipop/ocr/interface.py`.
- OCR output must preserve coherent `full_text` and `words` ordering, because hit scanning computes a character index and slices `full_text[index:]`.
- Popup visibility and screenshot capture are coordinated through `screen_lock`.
- Dictionary data is loaded from the user data directory and can be downloaded on first run if missing.
- Runtime config is a process-wide singleton from `src/meikipop/config/config.py`.

Implication:
- If a provider changes output ordering or normalization, hit scanning and lookup quality can break without obvious type errors.

## Component Boundaries

### Composition Root

Fact:
- `src/meikipop/main.py` owns startup, shutdown, signal wiring, and CLI dispatch for dictionary-related subcommands.

When to read:
- Before changing initialization order, thread ownership, shutdown behavior, or adding new long-lived runtime components.

### GUI And Input

Fact:
- `src/meikipop/gui/input.py` handles platform-specific hotkey detection and mouse polling.
- `src/meikipop/gui/popup.py` renders the popup and decides when it should be visible.
- `src/meikipop/gui/tray.py` mutates config and delegates runtime actions.
- `src/meikipop/gui/settings_dialog.py` exposes more config editing.
- `src/meikipop/gui/magpie_manager.py` adjusts coordinate transforms for Windows Magpie compatibility.

Risk:
- This area is tightly coupled to cursor position, popup timing, scan behavior, and platform-specific APIs.

### Screenshot Ownership

Fact:
- `src/meikipop/screenshot/screenmanager.py` owns scan area selection, screenshot capture, OCR throttling, unchanged-frame suppression, and handoff to OCR.
- Region selection happens via `RegionSelector`.

Risk:
- Saved monitor/region state is fragile. The file already contains a note that monitor changes are not handled well.

### OCR Pipeline

Fact:
- `src/meikipop/ocr/ocr.py` discovers providers dynamically from `src/meikipop/ocr/providers/`.
- `src/meikipop/ocr/hit_scan.py` maps normalized OCR boxes back to the current cursor position.
- Provider implementations normalize their own outputs before downstream logic sees them.

Important provider types:
- `meikiocr (local)`: external library, likely model-managed outside this repo.
- `Google Lens (remote)`: direct network OCR.
- `owocr (Websocket)`: local websocket bridge to another process.
- `Chrome Screen AI (local)`: local native library and model bundle.

### Dictionary Engine

Fact:
- `src/meikipop/dictionary/customdict.py` loads `dictionary.pkl`, validates shape, and auto-downloads it from GitHub Releases if missing.
- `src/meikipop/dictionary/lookup.py` performs cache-aware prefix scanning, deconjugation, fallback lookup, result merging, and ranking.
- Deconjugation rules are embedded in the serialized dictionary payload and come from the dictionary build pipeline.

Inference:
- Lookup is designed around hover suffixes, not general-purpose segmentation. It expects the hit scanner to start near the intended word boundary.

### Offline Dictionary Tooling

Fact:
- `src/meikipop/scripts/build_dictionary.py` creates the main serialized dictionary artifact.
- `src/meikipop/scripts/import_yomitan_dict_html.py` and `src/meikipop/scripts/import_yomitan_dict_text.py` replace the default dictionary with imported Yomitan data.

## Threading Model

Fact:
- `LatestValueQueue.put()` overwrites the pending value.
- `LatestValueQueue.trigger()` wakes the waiting worker without changing the stored value.

Why it matters:
- `HitScanner` can recompute against the most recent OCR result without a new OCR pass.
- Replacing `LatestValueQueue` with FIFO semantics would change latency, throughput, and CPU behavior in meaningful ways.

## External Integration Surface

Fact:
- Network use exists in:
  - Google Lens OCR requests
  - first-run dictionary bootstrap from GitHub Releases
  - dictionary build script downloads
- Frozen packaging is handled by PyInstaller specs at repo root, not by automatic module discovery alone.

Operational consequence:
- Runtime extension points and packaged extension points are not the same. Source-only changes can still fail in frozen builds.

## Facts Vs Inference

Fact:
- The runtime pipeline, queue semantics, config singleton, and provider discovery behavior are directly visible in source.

Inference:
- Timing interactions, provider output ordering quirks, and lock timing behavior were not runtime-verified in this pass.

## Read Next

- Task routing and code boundaries: `docs/agents/repo-map.md`
- Build/package/release details: `docs/agents/build-test-release.md`
- GUI-specific operational notes: `docs/agents/components/gui-and-input.md`
- OCR-specific operational notes: `docs/agents/components/ocr-pipeline.md`
- Dictionary-specific operational notes: `docs/agents/components/dictionary-and-hit-scanning.md`

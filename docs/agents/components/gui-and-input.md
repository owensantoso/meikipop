# GUI And Input

## What This Doc Is

This doc covers the user-facing runtime surfaces: popup, tray, settings, hotkeys, mouse polling, and scan-area selection.

Read this before changing UI behavior, input behavior, popup timing, or scan mode semantics.

## Main Files

- `src/meikipop/gui/popup.py`
- `src/meikipop/gui/tray.py`
- `src/meikipop/gui/settings_dialog.py`
- `src/meikipop/gui/input.py`
- `src/meikipop/gui/region_selector.py`
- `src/meikipop/gui/magpie_manager.py`

## Responsibilities

### `popup.py`

Fact:
- Owns popup rendering, popup visibility decisions, popup positioning, HTML generation, and popup calibration.
- Polls `_latest_data` on a 10 ms Qt timer instead of subscribing to worker-thread signals.
- Uses `screen_lock` while visible to coordinate with screenshot capture.

Agent caution:
- Popup changes can affect capture behavior, not just visuals.

### `tray.py`

Fact:
- Owns tray icon menu, scan mode selection, scan area selection, OCR provider selection, pause/resume, quit, and settings dialog access.
- Persists configuration changes directly through the global `config`.

Agent caution:
- Tray actions can have runtime side effects immediately and also change future startup behavior via saved config.

### `settings_dialog.py`

Fact:
- Exposes most editable config fields, including OCR provider, theme, popup content, and scan behavior.

Agent caution:
- If you add config fields, check whether they need UI exposure, tray updates, or reapply logic.

### `input.py`

Fact:
- Polls mouse position and hotkey state every 10 ms.
- Linux uses X11/Xlib logic.
- macOS uses Quartz/AppKit modifier checks.
- Windows uses the `keyboard` package.

Agent caution:
- This file is highly platform-sensitive.
- Behavior that looks simple in shared logic can break differently on each OS.

### `region_selector.py`

Fact:
- Owns interactive selection of a custom scan rectangle.

### `magpie_manager.py`

Fact:
- Provides optional coordinate transforms for Magpie on Windows.
- Non-Windows behavior is effectively no-op.

## Key Behavioral Rules

- Manual mode: hotkey-down triggers screenshot capture.
- Auto mode: entering auto mode triggers an initial capture.
- Auto mode can trigger rescans on mouse movement.
- Mouse movement can trigger hit scanning even when OCR is not rerun.
- Popup visibility depends on both latest lookup data and virtual-hotkey state.

## Common Mistakes

- Treating popup work as pure presentation. It interacts with capture locking and cursor timing.
- Changing input polling or auto mode without checking screenshot/OCR rearm behavior.
- Forgetting that provider names shown in UI are persisted config values.

## Safe Change Checklist

- Read `ARCHITECTURE.md` first if the change touches timing or visibility behavior.
- Check whether `config.save()` is needed or already happening.
- Check whether the tray, settings dialog, and startup defaults all need to stay consistent.
- Manually verify popup placement and visibility behavior if you change any of:
  - cursor logic
  - hotkey logic
  - scan mode logic
  - popup show/hide timing

## Related Docs

- Runtime pipeline: `ARCHITECTURE.md`
- Safe UI workflow: `docs/agents/runbooks/make-a-safe-ui-change.md`

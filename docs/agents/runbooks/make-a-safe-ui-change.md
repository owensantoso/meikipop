# Make A Safe UI Change

## What This Doc Is

This runbook is for popup, tray, settings, input, and scan-area changes.

Read this before editing `src/meikipop/gui/*` unless the change is purely cosmetic and obviously isolated.

## Before You Edit

- Read `AGENTS.md`
- Read `ARCHITECTURE.md`
- Read `docs/agents/components/gui-and-input.md`
- If the change affects capture timing or popup visibility, also read `src/meikipop/screenshot/screenmanager.py`

## Change Checklist

1. Identify whether the change affects:
   - popup visibility
   - popup placement
   - input polling
   - scan triggering
   - config persistence
   - provider or scan-area selection
2. Check whether the same setting exists in:
   - defaults in `config.py`
   - tray behavior
   - settings dialog
   - popup or input reapply logic
3. If the change touches timing or visibility, review `screen_lock` behavior.
4. If the change is platform-sensitive, read the relevant branch in `input.py` or `magpie_manager.py`.

## Manual Verification Suggestions

- Launch the app.
- Confirm popup visibility still matches expected hotkey or auto-scan behavior.
- Confirm the popup does not capture itself in screenshots.
- Confirm tray actions still update runtime behavior.
- Confirm settings persistence survives restart.

## Common Failure Modes

- Popup stuck visible or stuck hidden
- Auto mode becoming too aggressive or too quiet
- Region selection not persisting correctly
- Platform-specific hotkey regressions
- Popup placement drifting because cursor and screen coordinates no longer align

# Add Or Modify An OCR Provider

## What This Doc Is

This runbook covers the practical workflow for adding or changing OCR providers safely.

Read this before touching `src/meikipop/ocr/providers/*`.

## Before You Edit

- Read `docs/agents/components/ocr-pipeline.md`
- Read `docs/CUSTOM_OCR_PROVIDER.md`
- Read the provider contract in `src/meikipop/ocr/interface.py`

## Safe Workflow

1. Start from an existing provider or the dummy template.
2. Ensure the provider returns normalized `Paragraph` data with coherent `full_text` and `words`.
3. Pick a stable, user-facing `NAME`.
4. Verify the provider package is discoverable under `src/meikipop/ocr/providers/<provider_name>/`.
5. If the provider should ship in packaged apps, update all three `.spec` files.
6. Update docs if setup requirements or operational caveats changed.

## Packaging Rule

Do not stop after runtime discovery works in source mode.

If the provider should be available in packaged builds, update:

- `meikipop.macos.spec`
- `meikipop.linux.x64.spec`
- `meikipop.win.x64.spec`

## Provider-Specific Questions To Ask

- Is this local, remote, or bridged through another process?
- Does it need extra models, binaries, sockets, or credentials?
- Does it return word-level or character-level boxes?
- Could output ordering break hit scanning?
- Does it introduce new first-run or offline behavior?

## Verification Suggestions

- Confirm the provider appears in the tray or settings UI.
- Confirm selection persists through config.
- Confirm hit scanning still targets the intended character.
- Confirm packaged builds include the provider if required.

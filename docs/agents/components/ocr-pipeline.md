# OCR Pipeline

## What This Doc Is

This doc covers OCR provider discovery, OCR normalization, hit scanning, and the main integration differences between OCR backends.

Read this before changing provider logic, provider packaging, OCR normalization, or cursor-to-text behavior.

## Main Files

- `src/meikipop/ocr/interface.py`
- `src/meikipop/ocr/ocr.py`
- `src/meikipop/ocr/hit_scan.py`
- `src/meikipop/ocr/providers/*`
- `src/meikipop/ocr/providers/postprocessing.py`

## Provider Contract

Fact:
- Providers must implement `OcrProvider.scan(image) -> Optional[List[Paragraph]]`.
- Downstream code expects normalized coordinates in `BoundingBox`.
- Downstream hit scanning expects `Paragraph.full_text` and `Paragraph.words` to align coherently.

## Discovery And Selection

Fact:
- `OcrProcessor` scans `src/meikipop/ocr/providers/` for provider packages and imports concrete `OcrProvider` subclasses.
- The selected provider name comes from config.
- If the configured provider is unavailable, startup falls back to the first discovered provider.

Agent caution:
- Provider `NAME` values are user-facing and persisted in config.

## Provider Landscape

### `meikiocr (local)`

Fact:
- Uses the external `meikiocr` library.
- Converts OCR output to character-level `Word` entries, then groups lines into paragraphs.

Inference:
- Model download/session behavior may occur inside the external library rather than this repo.

### `Google Lens (remote)`

Fact:
- Sends protobuf payloads to `https://lensfrontend-pa.googleapis.com/v1/crupload`.
- Uses a hardcoded API key and request session headers.

Agent caution:
- This is both a network dependency and a security/compliance consideration.

### `owocr (Websocket)`

Fact:
- Connects to `ws://127.0.0.1:7331`.
- Expects a local companion process and retries once after connection loss.

### `Chrome Screen AI (local)`

Fact:
- Loads a local native library and model bundle from `~/.config/screen_ai/resources`.
- Uses checked-in generated protobuf bindings.

Agent caution:
- Do not hand-edit the generated protobuf files.

## Hit Scanning

Fact:
- `HitScanner` maps cursor coordinates into normalized capture-space coordinates.
- It finds the paragraph under the cursor, then the word box under the cursor, then estimates a character offset inside that word box.
- It returns `full_text[final_char_index:]` as the lookup suffix.

Implication:
- Provider token ordering and box quality have a direct effect on lookup quality.

## Packaging Footgun

Fact:
- Runtime provider discovery is dynamic.
- Packaged apps only include provider modules listed in the `.spec` files.

Rule:
- If you add or rename a provider, update:
  - `meikipop.macos.spec`
  - `meikipop.linux.x64.spec`
  - `meikipop.win.x64.spec`

## Safe Change Checklist

- Verify provider `NAME` stability.
- Verify normalization and token ordering assumptions.
- Update specs if the frozen app should include the provider.
- Re-read `docs/CUSTOM_OCR_PROVIDER.md` and `docs/agents/runbooks/add-or-modify-an-ocr-provider.md`.

## Related Docs

- Custom provider guide: `docs/CUSTOM_OCR_PROVIDER.md`
- Provider workflow: `docs/agents/runbooks/add-or-modify-an-ocr-provider.md`
- Runtime map: `ARCHITECTURE.md`

# Glossary

## What This Doc Is

This is a quick vocabulary guide for repo-specific terms.

Read this when variable names or architecture docs use project jargon that is not obvious from the code alone.

## Terms

- `auto scan mode`: mode where screenshots and OCR can be triggered without manually pressing the hotkey each time.
- `hit scan`: the step that maps cursor position back onto OCR output and chooses the lookup suffix under the pointer.
- `lookup suffix`: the text slice starting at the inferred hovered character, passed into the dictionary engine.
- `LatestValueQueue`: a one-slot overwrite queue used to keep only the freshest work item.
- `Magpie compatibility`: Windows-specific coordinate adjustment for users running the Magpie upscaler.
- `OCR provider`: a concrete backend implementation under `src/meikipop/ocr/providers/` that returns normalized `Paragraph` data.
- `Paragraph`: normalized OCR output block containing `full_text`, `words`, a bounding box, and writing direction.
- `Word`: OCR token used by hit scanning. In practice this may be a full word or a single character depending on provider output.
- `screen lock`: shared lock preventing popup visibility and screenshot capture from interfering with each other.
- `scan region`: either an interactive user-selected rectangle or an entire monitor index saved in config.
- `dictionary.pkl`: serialized dictionary artifact loaded at runtime from the user data directory.
- `dictionary-latest`: GitHub release tag used by the scheduled dictionary build workflow.
- `deconjugation`: grammar-aware normalization of Japanese word forms before dictionary lookup.
- `KanjiEntry`: supplemental leading-character kanji card that can be appended to normal word lookup results.

## Related Docs

- Runtime behavior: `ARCHITECTURE.md`
- OCR details: `docs/agents/components/ocr-pipeline.md`
- Dictionary details: `docs/agents/components/dictionary-and-hit-scanning.md`

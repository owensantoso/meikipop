# Dictionary And Hit Scanning

## What This Doc Is

This doc explains how hovered OCR text becomes ranked dictionary results.

Read this before changing lookup behavior, kanji cards, dictionary loading, deconjugation usage, or dictionary build/import tooling.

## Main Files

- `src/meikipop/ocr/hit_scan.py`
- `src/meikipop/dictionary/lookup.py`
- `src/meikipop/dictionary/customdict.py`
- `src/meikipop/dictionary/deconjugator.py`
- `src/meikipop/scripts/build_dictionary.py`
- `src/meikipop/scripts/import_yomitan_dict_html.py`
- `src/meikipop/scripts/import_yomitan_dict_text.py`

## Runtime Lookup Flow

1. `HitScanner` computes the lookup suffix from OCR geometry plus the current cursor position.
2. `Lookup` trims the suffix to `max_lookup_length`.
3. Lookup stops at Japanese separators.
4. Lookup checks a cache.
5. Lookup scans prefixes, applies deconjugation, checks fallback spellings, merges duplicate display forms, and ranks results.
6. If enabled, a leading-character kanji card may be appended.

## Dictionary Loading

Fact:
- Runtime dictionary data lives outside the repo as `dictionary.pkl` in the user data directory.
- If it is missing, the app downloads `dictionary.zip` from the `dictionary-latest` GitHub release and extracts `dictionary.pkl`.
- The dictionary payload also carries the deconjugation rules used at runtime.

Agent caution:
- First-run behavior depends on network availability unless the dictionary is already present.

## Lookup Behavior Notes

Fact:
- Lookup is prefix-based and optimized for a suffix that starts near the hovered character.
- Result ranking combines match length and a priority heuristic that includes frequency and deconjugation factors.
- Duplicate `(written_form, reading)` pairs are merged before final sorting.

Inference:
- This is not a general tokenizer. It depends on hit scanning to hand it a good starting point.

## Build And Import Tooling

### `build_dictionary.py`

Fact:
- Builds the default serialized dictionary artifact from external sources and local processing.
- Uses cache directories for downloaded source data.

Agent caution:
- The script contains some silent `pass` branches and minimal request validation, so output quality should be checked, not assumed.

### Yomitan Import Scripts

Fact:
- Import commands overwrite the default dictionary with imported Yomitan-derived output.
- HTML and text import flows are separate scripts with different formatting tradeoffs.

## Safe Change Checklist

- If you change hit scanning, verify cursor-to-text alignment assumptions.
- If you change lookup ranking, inspect whether kanji cards, deconjugation, or duplicate merging still make sense.
- If you change dictionary serialization shape, verify runtime load and validation logic.
- If you change build/import tooling, verify the generated `dictionary.pkl` rather than trusting command success alone.

## Related Docs

- Runtime flow: `ARCHITECTURE.md`
- Dictionary workflow: `docs/agents/runbooks/update-dictionary-assets.md`

# Configuration And Paths

## What This Doc Is

This doc explains where persistent state lives and how config and resource paths are resolved.

Read this before changing config schema, path logic, bundled resource lookup, or first-run behavior.

## Main Files

- `src/meikipop/config/config.py`
- `src/meikipop/utils/paths.py`
- `src/meikipop/dictionary/customdict.py`

## Config Model

Fact:
- Runtime config is a singleton.
- It loads from an INI file at `paths.config_path`.
- Missing values fall back to defaults from `_SCHEMA`.
- Saving rewrites the INI file with the current in-memory values.

Current config areas:
- input and scan behavior
- OCR provider selection
- auto-scan behavior
- Magpie compatibility
- popup position/theme/content options

Agent caution:
- Config changes can affect both current runtime behavior and future startups.

## Path Model

Fact:
- Paths are resolved through `platformdirs`.
- `config_path`: user config directory
- `dictionary_path`: user data directory
- `cache_dir`: user cache directory
- `main_dir`: source tree path in dev, `_MEIPASS/meikipop` when frozen

## Important Persistent Assets

- `config.ini`
- `dictionary.pkl`
- cached downloads used by dictionary build tooling
- packaged icon resources

## First-Run Behavior

Fact:
- If `dictionary.pkl` is missing, `customdict.py` attempts to download `dictionary.zip` from GitHub Releases and extract it automatically.

Operational consequence:
- Offline startup can fail if the dictionary has never been bootstrapped locally.

## Config-Change Checklist

- Update defaults in `_SCHEMA`.
- Check whether settings UI should expose the new field.
- Check whether tray reapply logic or runtime reconfiguration is needed.
- Check whether docs should mention the new setting.

## Related Docs

- Runtime behavior: `ARCHITECTURE.md`
- Build/import details: `docs/agents/components/dictionary-and-hit-scanning.md`

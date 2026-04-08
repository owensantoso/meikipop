# Packaging And Release

## What This Doc Is

This runbook covers frozen builds, release automation, and packaging-specific footguns.

Read this before changing `.spec` files, GitHub workflows, versioning, or bundled resources.

## Packaging Surfaces

- `meikipop.macos.spec`
- `meikipop.linux.x64.spec`
- `meikipop.win.x64.spec`
- `.github/workflows/build-linux.yml`
- `.github/workflows/build-macos.yml`
- `.github/workflows/build-windows.yml`
- `.github/workflows/pr-build.yml`
- `.github/workflows/release.yml`
- `.github/workflows/build-dictionary.yml`

## Current Release Model

- PRs to `main` build Linux, macOS, and Windows artifacts.
- Tag pushes matching `v*` build artifacts and publish a GitHub release.
- A separate workflow rebuilds `dictionary-latest` weekly and on demand.

## Packaging Checklist

1. If you add or rename a provider, update all `.spec` files.
2. If you add bundled resources, check whether they must be added to `.spec` `datas`.
3. Keep `pyproject.toml` and `src/meikipop/config/config.py` version values aligned.
4. If you change packaging behavior, check whether the README or agent docs should mention it.

## Verification Guidance

- Packaging jobs prove frozen artifact creation, not runtime correctness.
- If the change affects runtime loading, provider inclusion, or resource resolution, a build-only check is incomplete.

## Known Packaging Footguns

- Dynamic provider discovery does not automatically carry over to PyInstaller bundles.
- macOS bundle versioning depends on `APP_VERSION` in `config.py`.
- Linux packaging depends on CI-only system packages and headless X support.

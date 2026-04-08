# Build, Test, Release

## What This Doc Is

This doc explains how the repo is built and released today, and what verification is actually available.

Read this before running validation, touching packaging, or assuming CI covers a behavior.

This doc supports local setup, packaging work, and release changes.

## Local Development Commands

Recommended source install path:

```bash
pip install -e .
```

Run the app:

```bash
meikipop
```

Dictionary utility commands:

```bash
meikipop build-dict
meikipop import-yomitan-dict-html path/to/dict.zip
meikipop import-yomitan-dict-text path/to/dict.zip
```

## What The Repo Does Not Provide

Fact:
- No test suite
- No lint command
- No typecheck command
- No formatter command
- No `tox`, `nox`, or `make` workflow

Implication:
- Local verification is mostly manual unless you add your own temporary checks.

## Packaging Workflows

### Linux

CI path:

```bash
pip install -e .
pip install pyinstaller
xvfb-run pyinstaller meikipop.linux.x64.spec
```

Artifact:
- `dist/meikipop.linux.x64.tar.gz`

Notes:
- Linux build depends on `xvfb` and several X/Qt-related apt packages in CI.

### macOS

CI path:

```bash
pip install -e .
pip install pyinstaller
pyinstaller meikipop.macos.spec
```

Artifact:
- `dist/meikipop.macos.arm64.dmg`

Notes:
- The macOS spec parses `APP_VERSION` from `src/meikipop/config/config.py` for bundle versioning.

### Windows

CI path:

```bash
pip install -e .
pip install pyinstaller
pyinstaller meikipop.win.x64.spec
```

Artifact:
- `dist/meikipop.windows.x64.zip`

## CI Coverage Reality

Fact:
- Pull requests to `main` run the reusable Linux, macOS, and Windows packaging workflows.
- Tag pushes matching `v*` build artifacts and publish a GitHub release.
- A separate scheduled/manual workflow rebuilds and republishes the dictionary as `dictionary-latest`.

What CI proves:
- Editable install plus PyInstaller packaging works on the configured runners.

What CI does not prove:
- The app launches correctly.
- OCR providers behave correctly.
- Hit scanning still works.
- Popup behavior still works.
- Input permissions and OS integration still work.
- Dictionary build/import logic is semantically correct.

## Validation Guidance For Agents

If you change:

- input logic
- screenshot flow
- OCR providers
- hit scanning
- popup behavior
- packaging specs

Then prefer at least one of:

- manual runtime smoke test
- packaging build for the affected platform
- targeted script run if working in dictionary tooling

## Versioning Notes

Fact:
- Version currently appears in both `pyproject.toml` and `src/meikipop/config/config.py`.
- macOS packaging reads `APP_VERSION` from `config.py`.

Implication:
- Version bumps should keep both files in sync.

## Packaging Footguns

- Adding a provider package requires `.spec` updates for all packaged platforms.
- Adding bundled resources may also require `.spec` updates.
- Frozen builds and source runs do not discover code/assets the same way.

## Related Docs

- Task routing: `docs/agents/repo-map.md`
- Packaging details: `docs/agents/runbooks/packaging-and-release.md`
- Current risk profile: `CURRENT_STATE.md`

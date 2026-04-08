# Update Dictionary Assets

## What This Doc Is

This runbook covers default dictionary rebuilds and Yomitan import workflows.

Read this before changing dictionary generation scripts or replacing the runtime dictionary.

## Main Commands

```bash
meikipop build-dict
meikipop import-yomitan-dict-html path/to/dict.zip
meikipop import-yomitan-dict-text path/to/dict.zip
```

## Important Behavior

- `build-dict` rebuilds the default serialized dictionary.
- Import commands overwrite the default runtime dictionary with imported output.
- Runtime uses `dictionary.pkl` from the user data directory, not a repo-tracked asset.

## Safe Workflow

1. Decide whether you are rebuilding the default dictionary or intentionally replacing it with imported data.
2. Check whether cached source data might affect reproducibility.
3. Run the command.
4. Verify the resulting dictionary actually loads and produces sensible lookup results.
5. If you changed script behavior, update docs and mention any new data assumptions.

## Risks

- Upstream source downloads can change over time.
- The scripts contain some silent error-skipping branches.
- Successful command completion is not enough to prove dictionary quality.

## Related Docs

- Dictionary architecture: `docs/agents/components/dictionary-and-hit-scanning.md`
- Build/release surface: `docs/agents/build-test-release.md`

# Open Questions

## What This Doc Is

This tracks uncertainty, inferred behavior, and areas that would benefit from human confirmation or runtime verification.

Read this before making broad assumptions from code alone.

## Current Open Questions

- Is the hardcoded Google Lens API path and key an intentional long-term integration, or only a pragmatic fallback?
- Is `~/.config/screen_ai/resources` the intended setup path on macOS as well as Linux, or just an implementation shortcut?
- Which OCR providers are considered supported in packaged builds versus source-only workflows?
- Are provider-specific model downloads from `meikiocr` expected during first run, and is that behavior acceptable for offline users?
- How often do multi-monitor changes break saved scan state in real use?
- Are the broad `except:` blocks intentionally tolerated for resilience, or are they known technical debt awaiting cleanup?
- Is there a preferred manual smoke-test checklist for releases?
- Is there a documented regeneration path for the checked-in protobuf/betterproto files outside this repo?

## Unverified In This Pass

- Actual runtime timing and lock behavior
- Startup success on this machine
- Packaged app launch behavior
- Provider-specific output quirks
- Dictionary build health against current upstream data

## Good Human Follow-Ups

- Confirm which providers are officially supported and expected to keep working.
- Confirm release acceptance criteria beyond “all three packaging jobs pass”.
- Confirm whether the Google Lens integration has policy or maintenance constraints.

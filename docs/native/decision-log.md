# Native Decision Log

## Status

This log records architecture decisions for the planned mac-native app.

Each item is marked as one of:
- `Recommended`
- `Needs confirmation`
- `Open`

## Decisions

### D-001: Native UI stack

Status:
- `Recommended`

Decision:
- use SwiftUI for standard app UI and AppKit for specialized overlay/window behavior

Why:
- the hardest problems are window activation, overlay levels, event pass-through, and focus stability

### D-002: Popup ownership

Status:
- `Recommended`

Decision:
- do not preserve the current Qt popup in the long-term mac-native app

Why:
- current popup behavior is tightly coupled to focus restoration and capture locking

### D-003: Highlight architecture

Status:
- `Recommended`

Decision:
- create a dedicated native highlight overlay separate from the popup

Why:
- highlight feedback needs a faster and more stable lifecycle than popup content

### D-004: OCR and dictionary ownership for phase 1

Status:
- `Recommended`

Decision:
- keep OCR and dictionary logic in Python initially behind an explicit service boundary

Why:
- this preserves working domain logic while native work focuses on the biggest UX/platform gaps

### D-005: Migration style

Status:
- `Recommended`

Decision:
- use incremental migration with a native shell plus Python core, not a full rewrite first

Why:
- it produces earlier user-visible value with lower product risk

### D-006: Capture stack

Status:
- `Recommended`

Decision:
- prefer ScreenCaptureKit for native capture work

Why:
- it is the platform-native path and better matches the future product shape

### D-007: Product shape

Status:
- `Needs confirmation`

Decision:
- ship as a menu-bar-first utility with settings window

Why:
- it matches the current product interaction model

Need from human:
- confirm whether a dock-presence mode is also desired

### D-008: Config migration

Status:
- `Needs confirmation`

Decision:
- native preferences do not have to preserve the current Python `config.ini` format unless continuity is important

Why:
- a clean native settings model may be better than carrying old structure forward

Need from human:
- confirm whether settings migration compatibility matters

### D-009: Provider scope

Status:
- `Open`

Decision:
- determine which OCR providers are in-scope for the first native milestone

Why:
- supporting every current provider from day one may slow the native rewrite materially

### D-010: Remote OCR support

Status:
- `Open`

Decision:
- determine whether Google Lens OCR remains a supported first-party path

Why:
- it is a product, compliance, and maintenance question, not just a technical one

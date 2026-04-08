# Native Migration Plan

## Recommendation Summary

Recommended path: incremental migration to a native mac app, with the first major cut being a native shell plus native overlay stack and a preserved Python OCR/dictionary core.

Do not start with a full rewrite.
Do not keep the current Qt popup as part of the long-term mac-native product.

## Option Comparison

### 1. Full Native Rewrite

Description:
- rewrite OCR orchestration, lookup engine, popup, settings, and menu bar entirely in Swift

Pros:
- cleanest end state
- simplest packaging once finished
- no long-lived multi-runtime bridge

Cons:
- highest delivery risk
- recreates working dictionary/deconjugation logic immediately
- slows time-to-value on the most urgent UX fixes
- forces simultaneous decisions on UI, OCR, dictionary, and packaging

Verdict:
- not recommended as the first implementation phase

### 2. Hybrid Native Shell + Python Core

Description:
- native mac app owns all user-facing macOS behavior
- Python process owns OCR and dictionary work behind a stable IPC boundary

Pros:
- fixes the most important UX problems first
- preserves proven OCR and lookup logic
- creates clean migration seams
- lets native work focus on overlays, focus behavior, capture, and permissions

Cons:
- requires careful IPC and process management
- distribution becomes a bundled multi-runtime app
- some latency/debug complexity remains

Verdict:
- recommended initial architecture

### 3. Incremental Migration Inside The Existing App

Description:
- improve the Python/Qt app step by step while slowly replacing parts

Pros:
- smallest initial code motion
- preserves current packaging and mental model

Cons:
- keeps the product trapped in the current focus/windowing model
- encourages more investment in the wrong UI stack for the target platform
- makes the final native transition messier

Verdict:
- useful only for tiny short-term stabilizations, not as the main strategy

## What To Preserve Initially

Preserve:
- OCR provider contract in `src/meikipop/ocr/interface.py`
- provider-specific normalization logic where still operationally useful
- hit-scan algorithm ideas from `src/meikipop/ocr/hit_scan.py`
- dictionary loading and validation from `src/meikipop/dictionary/customdict.py`
- lookup, deconjugation, ranking, and kanji card logic from `src/meikipop/dictionary/lookup.py`
- dictionary build/import scripts

Do not preserve as-is:
- Qt popup/window model
- Qt region selector
- polling-heavy input/window coordination as the long-term architecture
- `screen_lock` as the core correctness mechanism

## Phased Roadmap

### Phase 0: Planning And Contracts

Goals:
- document target native architecture
- define service contract between Swift and Python
- identify which current providers are in-scope for native milestone one

Deliverables:
- native architecture docs
- IPC schema draft
- risk register

### Phase 1: Native Shell Skeleton

Goals:
- create mac-native app shell
- implement menu bar app lifecycle
- implement settings shell and permissions onboarding
- launch and manage background Python worker process

Milestone:
- native app boots, shows menu bar UI, reports service health, and stores preferences

### Phase 2: Native Capture And Region Selection

Goals:
- implement native scan region and display selection
- adopt native capture path
- persist geometry safely across display changes

Milestone:
- native app can select a region and produce captured frames for service requests

### Phase 3: Native Highlight Overlay

Goals:
- implement non-activating, non-interactive word highlighting
- render stable hover state without popup dependency
- update highlight independently from popup content

Milestone:
- hovered OCR token can be highlighted smoothly without focus churn or visible flicker

### Phase 4: Native Popup

Goals:
- implement non-activating popup surface
- render lookup results with native component styling
- tune placement, animation, and resize stability

Milestone:
- native popup replaces Qt popup behavior for the primary lookup experience

### Phase 5: End-To-End Native Runtime

Goals:
- connect capture, OCR service, hit-testing, highlight, and popup into a stable loop
- preserve lossy freshness semantics from the current app
- harden failure handling and degraded states

Milestone:
- user can run the native app for real lookups on macOS

### Phase 6: Core Migration Decisions

Goals:
- evaluate whether Python OCR and lookup should remain long-term
- migrate selected logic to Swift only where it clearly improves product or operations

Possible work:
- port hit scanning first
- port dictionary lookup later
- leave dictionary build tooling in Python regardless

## Suggested Early Spikes

These are worthwhile, but should be explicit and small:

1. Overlay spike
   Validate a non-activating highlight window and a non-activating popup window on macOS without focus restoration hacks.

2. Capture spike
   Validate ScreenCaptureKit region capture performance and behavior under continuous hover-driven updates.

3. Bridge spike
   Validate one end-to-end request from native capture -> Python OCR/lookup -> native popup rendering.

## Exit Criteria For The First Native Milestone

- No focus stealing during highlight or popup display.
- No popup hide/show flicker during normal hover movement.
- Region selection works across multiple displays.
- Permissions flow is understandable and recoverable.
- OCR/lookup latency feels at least competitive with the current app in normal use.

## Human Confirmation Needed

- Whether menu-bar-only is the intended default product shape.
- Whether all current OCR providers must survive phase 1.
- Whether shipping a bundled Python runtime is acceptable for the first native release.

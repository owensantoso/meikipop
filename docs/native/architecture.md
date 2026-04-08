# Native Architecture Plan

## Purpose

This document proposes the target architecture for a mac-native `meikipop`.

It is based on the current Python app as it exists in this repo today and is intended to guide future implementation work.

## Current Repo Facts

- The current app is composed in `src/meikipop/main.py` and runs a thread-based pipeline: input -> screenshot -> OCR -> hit-scan -> lookup -> popup.
- `InputLoop` polls mouse position and hotkey state every 10 ms.
- `ScreenManager` captures the selected region or screen with `mss`.
- OCR providers normalize output into `Paragraph`, `Word`, and `BoundingBox` objects from `src/meikipop/ocr/interface.py`.
- `HitScanner` maps the cursor into normalized OCR space and returns a suffix string starting at the hovered character.
- `Lookup` loads `dictionary.pkl`, performs prefix lookup and deconjugation, and writes popup-ready result objects.
- The popup is a top-level Qt window and currently coordinates with screenshot capture through `screen_lock`.

## Core Recommendation

Recommend a hybrid-native architecture first:
- native macOS app shell in Swift using SwiftUI plus AppKit,
- native overlay/highlight/popup/windowing/input-permissions stack,
- existing OCR and dictionary logic preserved in Python initially behind a local service boundary,
- incremental movement of pure logic into Swift only after the native shell is stable.

Reasoning:
- The biggest current product problem is macOS windowing/focus behavior, not dictionary ranking.
- The current OCR and lookup code already has useful internal contracts.
- A full rewrite would create the most simultaneous risk in the most performance-sensitive areas.
- A thin native shell with a Qt or Python popup would not solve the main UX issue.

## Target System Shape

### Native Mac App

Own in Swift:
- app lifecycle
- menu bar item and menu
- settings/preferences UI
- permissions onboarding
- region selection UI
- cursor tracking and global event monitoring
- non-activating popup window
- non-activating highlight overlay
- screen capture orchestration
- service orchestration and health state

### OCR / Lookup Core

Keep in Python initially:
- OCR provider abstraction
- existing provider implementations where still useful
- OCR normalization into paragraphs/words/boxes
- hit-scanning logic or its algorithmic equivalent
- dictionary loading and lookup ranking
- deconjugation
- dictionary build/import tooling

### Bridge Layer

Introduce a small, explicit contract between native and Python:
- request: capture image plus pointer context plus scan metadata
- response: OCR paragraphs, hit target, lookup results, confidence, timing
- transport: local process boundary over JSON or MessagePack IPC

The contract should be versioned and testable independently of UI.

## Native Module Breakdown

### `AppCore`

Responsibilities:
- app state machine
- startup/shutdown
- dependency graph
- coordinating native services and Python worker process

### `CaptureService`

Responsibilities:
- screen capture requests
- region/screen ownership
- capture throttling
- frame deduping

Preferred mac-native approach:
- use ScreenCaptureKit for capture rather than screenshotting through a general-purpose library.

### `PointerService`

Responsibilities:
- current pointer position
- modifier or hotkey state
- optional event tap integration
- hover timing

### `OverlayService`

Responsibilities:
- highlight lifecycle
- popup lifecycle
- placement decisions
- animation coordination
- non-activating window behavior

This should be AppKit-owned even if popup content is SwiftUI-hosted.

### `SelectionService`

Responsibilities:
- custom region selection overlay
- monitor-aware geometry persistence
- invalidation when displays change

### `LookupServiceClient`

Responsibilities:
- marshal requests to Python service
- cache last result
- collapse stale requests
- surface health/failure state to the app

### `Preferences`

Responsibilities:
- durable settings storage
- migration from current config if desired
- defaults and validation

Recommended storage:
- `UserDefaults` for most settings
- app support directory for structured state and caches

## Windowing Strategy

### Recommendation

Use AppKit for all specialized window behavior:
- `NSPanel` or custom `NSWindow` subclasses for non-activating popup surfaces
- dedicated borderless overlay windows for highlighting
- SwiftUI views embedded inside those windows where helpful

### Why Not SwiftUI Alone

Inference:
- SwiftUI is strong for settings and conventional app UI.
- The critical problem space here is activation policy, event pass-through, screen levels, and overlay behavior.
- Those are AppKit concerns first on macOS and should be owned there to avoid fighting framework abstractions.

## Overlay And Popup Separation

Recommend two independent surfaces:

### Highlight Overlay

Responsibilities:
- render hovered word bounds
- remain visible during small pointer movement inside the same token
- never intercept input
- never activate the app

### Lookup Popup

Responsibilities:
- render dictionary content
- anchor near the highlighted token or pointer
- update content independently from highlight visibility
- remain non-activating

This separation is important because the current app couples popup visibility to capture correctness through `screen_lock`.
That should not survive into the native architecture.

## OCR Integration Strategy

### Phase 1 Recommendation

Keep OCR in Python.

Why:
- provider abstraction already exists in `src/meikipop/ocr/interface.py`
- multiple providers already normalize to a shared output format
- OCR backends have different packaging and runtime requirements
- the native rewrite's highest-value early work is not OCR model work

### Phase 2 Options

Possible later directions:
- keep Python as the long-term OCR host
- move local OCR providers one by one to native if operationally worthwhile
- replace some providers entirely with mac-native or bundled-core alternatives

## Dictionary Strategy

### Phase 1 Recommendation

Keep dictionary lookup in Python.

Why:
- `src/meikipop/dictionary/lookup.py` is relatively self-contained
- deconjugation and ranking are domain-specific and already working
- dictionary tooling is already Python-based

### Phase 2 Recommendation

Only migrate dictionary lookup to Swift if one of these becomes true:
- Python startup or IPC overhead is materially user-visible
- packaging/distribution becomes too fragile
- deeper native integration needs a fully in-process engine

## Lifecycle Model

### App Startup

1. Launch menu bar app.
2. Check required permissions.
3. Start Python service if enabled by configuration.
4. Restore prior scan region and runtime settings.
5. Begin pointer monitoring and capture scheduling only when the app is active.

### Runtime Loop

1. Pointer/hotkey state changes.
2. Native scheduler decides whether a fresh capture is needed.
3. Native capture service acquires frame/region.
4. Request goes to Python OCR/lookup service.
5. Native overlay service updates highlight first, popup second.
6. Stale in-flight work is dropped in favor of fresher work.

### Shutdown

1. Hide overlays.
2. Stop capture and event monitors.
3. Terminate Python worker gracefully.
4. Persist state.

## Performance Principles

- Preserve the current “freshness over completeness” behavior.
- Keep lossy latest-value semantics at service boundaries.
- Prefer hit-testing against the latest OCR result over rerunning OCR on every pointer move.
- Debounce popup geometry changes more aggressively than highlight changes.
- Separate capture cadence from overlay animation cadence.

## Human Confirmation Needed

- Whether the first native milestone should still support all current OCR providers.
- Whether remote Google Lens OCR should remain a supported first-party option.
- Whether compatibility with the existing `config.ini` matters, or if native preferences can replace it.
- Whether the native app should remain menu-bar only or also expose a dock/settings presence by default.

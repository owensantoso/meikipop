# Overlay And Highlighting Notes

## Purpose

This document focuses on the hardest part of the native migration:
- non-focus-stealing overlays
- word highlighting
- popup stability
- pointer-driven updates on macOS

## Current Repo Facts

- The current app has no separate highlight layer.
- The popup is a top-level Qt window that is shown and hidden near the cursor.
- On macOS, the popup stores the previously active app and tries to restore focus after hiding.
- Screenshot capture and popup visibility are coordinated through a shared lock so the popup does not get captured.

## Problem Statement

The future native app needs:
- visible hovered-word feedback,
- a popup that does not activate the app,
- no flicker from repeated hide/show cycles,
- and no focus churn when OCR/highlighting updates rapidly.

## Recommendation

Treat highlighting and popup rendering as separate systems.

### Highlight Layer

Use a dedicated overlay window:
- borderless
- non-activating
- ignores mouse events
- high enough window level to remain visible above the target app
- lightweight, fast, and geometry-driven

The highlight layer should render:
- current word bounds
- optional paragraph bounds in debug mode only
- confidence-aware smoothing if needed

### Popup Layer

Use a separate non-activating panel/window:
- borderless or panel-like
- anchored relative to highlighted geometry or pointer
- content-hosting surface for SwiftUI view hierarchy
- independent animation timing from highlight updates

## Behavioral Rules

- Highlight should update more often than popup layout.
- Minor pointer movement inside the same OCR token should not relayout the popup.
- If OCR changes but the hovered token is still plausibly the same, prefer a smooth geometry transition.
- If OCR becomes unavailable temporarily, hold the last highlight briefly before fading out.
- If lookup data is stale but still relevant, keep the popup visible until a better result or a clear miss arrives.

## Hit Testing Strategy

Recommended approach:

1. Native side tracks pointer position continuously.
2. Native side keeps the last OCR result model.
3. Pointer movement within the same OCR result triggers native hit testing first.
4. Fresh OCR capture is requested only when the scheduler decides the frame is likely stale.

This preserves one of the best ideas from the current app:
- do not rerun OCR on every hover update if the last OCR geometry is still good enough.

## Cursor Tracking And Event Handling

Use native pointer/event APIs rather than window-relative view hover tracking.

Rationale:
- the user is hovering over other apps, not over `meikipop` views
- the app needs global pointer awareness
- global modifier state and activation-sensitive behavior are platform concerns

Inference:
- AppKit plus a global event monitor or event tap is the right ownership layer for this behavior
- SwiftUI should not be the primary owner of this subsystem

## Capture Interaction

The current lock-based design exists to stop the popup from appearing in screenshots.

For the native design, prefer one or more of these instead:
- capture pipeline that excludes the app's own windows where the platform allows it
- temporarily hide only the popup layer during capture, not the highlight layer
- capture before popup update when scheduling allows it
- use overlay surfaces that are not part of the captured content path

Do not carry forward a single global lock that tightly couples popup visibility to capture correctness unless testing proves it is necessary.

## Failure Modes To Design For

- OCR result geometry shifts slightly frame to frame.
- The pointer rides the boundary between adjacent characters.
- The target app scrolls under the cursor.
- A display is added, removed, or rearranged.
- Permissions are missing or revoked while the app is running.
- The Python service lags, restarts, or returns partial results.

## Suggested Native Data Model

Keep an in-memory model like:
- `CaptureFrame`
- `OcrParagraph`
- `OcrToken`
- `HoverMatch`
- `LookupPayload`
- `OverlayPresentationState`

The overlay system should consume stable geometry models, not raw provider output directly.

## Spike Recommendation

Before implementation, a small spike is justified here:

- create a non-activating highlight overlay
- create a non-activating popup panel
- validate that both can update while another app stays frontmost
- validate that no focus restoration hack is required

If that spike fails, revisit the windowing strategy before larger implementation work starts.

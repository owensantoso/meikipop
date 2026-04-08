# macOS Platform Notes

## Purpose

This document captures platform constraints and architecture guidance specific to the future native mac app.

It is not a complete API guide. It is a planning note for future implementation work.

## Current Repo Facts

- The current Python app already depends on macOS-specific frameworks through PyObjC for Quartz/Cocoa access.
- The current macOS hotkey path checks modifier state through `NSEvent.modifierFlags()`.
- The current popup stores the frontmost application and re-activates it after hiding.
- The README instructs users to grant Input Monitoring, Screen Recording, and Accessibility permissions on macOS.

## Platform Recommendations

### App Framework Split

Use:
- SwiftUI for settings, onboarding, and conventional app UI
- AppKit for overlays, panels, event monitoring, activation policy, and menu-bar integration details when needed

This should be treated as the default assumption, not as an exception.

### Menu Bar App

Recommended product shape:
- menu bar app first
- optional settings window
- no main document window by default

Implementation options:
- `MenuBarExtra` if it stays sufficient
- `NSStatusItem` if more control is required

### Permissions

Likely required:
- Screen Recording
- Accessibility
- possibly Input Monitoring depending on the final event monitoring approach

Recommendations:
- centralize permission checks
- show explicit onboarding and recovery guidance
- detect revoked permissions at runtime
- avoid silent degraded behavior where practical

### Capture

Preferred direction:
- ScreenCaptureKit for screen or region capture

Why:
- it is the mac-native capture stack
- it gives more control than a generic cross-platform screenshot library
- it aligns better with a future high-frequency capture loop

### Global Input And Pointer State

Needed capabilities:
- global pointer position
- modifier or shortcut state
- possibly event tap monitoring for richer interactions

Design guidance:
- keep this in a dedicated native service
- do not bury permission-sensitive behavior inside view code

### Windows And Overlays

Needed behavior:
- stay visible without taking focus
- ignore mouse events when appropriate
- support multiple displays
- survive rapid updates

Design guidance:
- create explicit AppKit window/controller types for:
  - highlight overlay
  - lookup popup
  - region selector

## SwiftUI Sufficiency

Recommendation:
- SwiftUI is not sufficient by itself for the critical overlay/window behavior.

Why:
- the specialized problems are activation policy, window level, input pass-through, and global event behavior
- those are platform-window concerns first, not declarative view-composition concerns

Use SwiftUI inside AppKit-owned windows when it improves maintainability.

## Things To Validate In Early Native Work

- Whether capture can reliably avoid including app-owned overlay windows.
- Which permission combination is truly required for the desired shortcut and hover behavior.
- Whether highlighted-word geometry should be based on OCR token bounds, expanded hit boxes, or smoothed display boxes.
- Whether menu-bar-only lifecycle has any practical drawbacks for onboarding or debugging.

## Human Confirmation Needed

- Whether a dock icon should appear during onboarding or preferences.
- Whether remote OCR providers remain acceptable in the native product.
- Whether the native app may depend on a bundled Python runtime in early releases.

# DESIGN.md

## Purpose

This document defines the visual and interaction direction for a future mac-native `meikipop`.

It is intentionally implementation-aware:
- it should help future agents build a polished native app,
- it should keep visual ambition practical,
- and it should prevent the app from drifting into a generic web-like style.

## Design Goals

- Feel native on macOS first, not cross-platform by accident.
- Stay lightweight, quiet, and utility-like.
- Make hover lookup feel stable and immediate.
- Use translucency and motion to support legibility and spatial clarity, not decoration.
- Keep the OCR/highlight/popup loop visually calm under frequent updates.

## Product Character

- Desktop-first utility, not document editor.
- Calm, precise, and readable.
- Fast enough to feel ambient.
- Polished enough to disappear into the reading experience.

## Visual Direction

### Materials

- Prefer native materials over custom glass reimplementations.
- Use macOS materials for popup chrome, settings sidebars, and menu-adjacent surfaces where they improve depth and integration.
- Keep highlight overlays simpler than the popup. Highlights should read as guidance, not as windows.
- Avoid stacking too many blur layers. One strong material layer is better than several weak ones.

### Color

- Default palette should be neutral and paper-like rather than neon.
- Accent color should support Japanese text emphasis without overwhelming the source content.
- Highlights should use one primary accent for the matched word and one softer support accent for reading/furigana metadata when needed.
- Prefer slightly warm neutrals over pure blue-gray UI chrome.

Suggested baseline direction:
- Background surfaces: warm graphite or soft parchment-tinted material, depending on appearance mode.
- Primary text: high-contrast neutral.
- Word emphasis: cool cyan or teal.
- Reading/support text: moss, jade, or muted sky.
- Warning/destructive actions: system semantic colors only.

### Typography

- Use native typography defaults unless there is a strong reason not to.
- Prioritize excellent Japanese rendering and mixed Japanese/Latin balance.
- The popup should clearly separate:
  - looked-up headword
  - reading
  - definitions
  - metadata
- Header text should feel anchored, not oversized.
- Definition text should optimize for scan speed over density.

Recommended stance:
- Use the system font stack by default for chrome and controls.
- For Japanese-heavy content, allow a curated text face choice only if it materially improves readability.
- Avoid “designer” fonts in the core popup.

## Interaction Principles

### Hover And Highlighting

- Highlight should appear before or with the popup, not after a noticeable lag.
- Highlight should be non-activating and non-intercepting.
- Hover state should be stable under tiny cursor motion within a word box.
- The popup and highlight should be separate surfaces with separate lifecycles.
- Losing OCR confidence should degrade gracefully by fading or shrinking the highlight, not by rapid show/hide flicker.

### Popup Behavior

- Popup should never steal focus.
- Popup motion should be subtle and mostly positional, not bouncy.
- Content updates should avoid resizing thrash when only secondary details change.
- When possible, keep the popup anchored to a stable point near the highlighted token rather than chasing every cursor pixel.
- Favor slight fade and position interpolation over sudden teleportation.

### Menu Bar Behavior

- The menu bar item should feel like the control center, not a leftover tray port.
- Common actions should be one click away:
  - enable or pause lookup
  - choose scan mode
  - choose scan region
  - open settings
  - quit
- Runtime state should be visible with concise labels and icon treatment.

### Settings

- Settings should be native and preference-like.
- Group by user intent, not by implementation.
- Recommended top-level groupings:
  - General
  - Lookup
  - OCR
  - Appearance
  - Permissions
  - Advanced
- Avoid exposing every debug option in the main path.

## Motion

- Use motion to explain state transitions, not to impress.
- Keep durations short and consistent.
- Prefer opacity and small translation transitions.
- Treat highlight updates as ultra-lightweight motion.
- Disable or reduce non-essential animation when system accessibility preferences request it.

Recommended defaults:
- Popup show: 120-160 ms fade/translate.
- Popup content transition: 80-120 ms crossfade for text sections when practical.
- Highlight change: 60-100 ms morph or fade.
- Region selection overlay: immediate response, no decorative animation.

## Component Rules

### Highlight Overlay

- Render as a dedicated non-activating overlay surface.
- The overlay must ignore mouse events.
- Shape should fit text bounds with minimal padding.
- Rounded rectangles are preferred over hard boxes.
- Use a single soft stroke and restrained fill.
- Avoid thick borders, glows, or game-like targeting UI.

### Lookup Popup

- Structure:
  - headword row
  - reading row or inline reading
  - definitions block
  - optional metadata / kanji details
- Use clear spacing rather than visible dividers when possible.
- If separators are needed, use hairlines or subtle spacing changes, not heavy borders.
- Keep corner radius moderate and Mac-like.

### Settings Window

- SwiftUI is appropriate for most settings content.
- Use native list, form, split view, and toolbar patterns.
- Do not style the settings window like a custom web dashboard.

## What To Avoid

- Web-card aesthetics with oversized shadows and generic rounded panels everywhere.
- Constant blur plus transparency plus borders on every surface.
- Cursor-chasing popup motion that feels jittery.
- Bright purple/blue “AI app” palettes.
- Overly dense debug information in the primary popup.
- Focus restoration hacks as a substitute for correct non-activating window behavior.
- Full-SwiftUI ownership of specialized overlay windows if AppKit solves the problem more directly.

## Implementation Guidance

- SwiftUI should own standard app UI where it improves velocity and maintainability.
- AppKit should own specialized windows, event taps, overlay levels, and activation-sensitive behavior.
- Prefer a small design token layer:
  - spacing
  - corner radius
  - typography roles
  - highlight colors
  - material choices
  - animation timings
- Keep the popup component visually stable even if its data source changes implementation later.

## Review Checklist

- Does the interaction remain calm during continuous hover updates?
- Does any surface steal focus or appear to?
- Does the app still feel native when all custom styling is removed?
- Is translucency improving depth, or just making text harder to read?
- Would this still feel good after hours of reading?

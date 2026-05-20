---
name: ui-ux-pro-max
description: UI/UX design optimization skill. Handles icon systems, visual hierarchy, interaction patterns, and design-polish for web interfaces.
---

# UI-UX-Pro-Max

Expert UI/UX optimization skill. Focuses on elevating interface design quality through systematic improvements.

## Core Capabilities

### 1. Icon System
- **Never use emojis as functional UI icons.** Emojis render inconsistently across platforms and look unprofessional in management dashboards.
- Use one of these approaches (ranked by preference):
  - **Inline SVG icons** — crisp at any size, fully controllable with CSS `fill: currentColor`, zero HTTP requests.
  - **Unicode geometric symbols** — `●` `◆` `▲` `■` `⬡` `▸` `◎` `◉` as minimal abstract markers.
  - **CSS-only icons** — borders, transforms, pseudo-elements for arrows, checkmarks, dots.
- Icons must match the design system: monochrome, geometric, consistent stroke width.
- For Nike-style dashboards: prefer minimal geometric shapes over illustrative icons.

### 2. Sidebar & Navigation Polish
- Active state: solid fill (`background: var(--ink); color: var(--on-primary)`) — high contrast pill.
- Inactive state: muted text, no background, subtle hover to `var(--soft-cloud)`.
- Icons: 18-20px inline SVG or Unicode geometric markers aligned with text.
- Spacing: 10-12px gap between icon and label.
- Group headers: 11px uppercase, letter-spacing 0.5px, `var(--stone)` color, minimal padding.

### 3. Visual Hierarchy Rules
- Primary actions: black pill (`btn-primary`), exactly ONE per viewport fold.
- Secondary actions: `var(--soft-cloud)` pill, never competing with primary.
- Data emphasis: Futura-display numbers at 48px for KPIs, 12px muted labels above.
- Dividers: only 1px `var(--hairline-soft)`, never decorative borders.

### 4. Interaction
- All clickable: `cursor: pointer`, `transition: all 0.15s`.
- Active/pressed: Nike-style `scale(0.98)` collapse with `opacity: 0.7`.
- Focus: subtle ring, never loud outlines.

### 5. Anti-patterns to Fix
- Emojis as navigation icons → replace with SVG or Unicode symbols.
- Inconsistent icon sizes → normalize to 18-20px viewBox.
- Decorative colors in chrome → monochrome only, color reserved for data signals.
- Center-aligned sidebar text → left-align with consistent indent.
- Missing active states → every nav item must have active/inactive distinction.
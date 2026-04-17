# Add Keyboard Diagram UI for Keybinding Analysis

## Summary
Introduce a visual keyboard diagram to display keybinding consensus, conflicts, and recommendations across characters and specs.

This feature is inspired by the KeyBind addon’s keyboard layout visualisation but should be implemented using organiseMyAlts' data-driven architecture.

---

## Goals

- Provide a clear visual representation of keybindings
- Highlight inconsistencies across characters/specs
- Show consensus recommendations directly on keys
- Improve usability of the keybinding analysis system

---

## Reference

The KeyBind addon provides a useful example of:
- keyboard layout definition
- rendering keys as UI elements
- modifier key toggles (Shift / Ctrl / Alt)
- scalable UI layout

This should be used as a **design reference only**, not copied directly.

---

## Desired Behaviour

Each key in the diagram should display:

- Key label (e.g. R, 1, Q)
- Assigned category (interrupt, builder, etc.)
- Consensus key mapping
- Confidence level
- Current binding (for active character)

---

## Visual Indicators

Use colour to represent state:

- Green → matches consensus
- Yellow → low-confidence consensus
- Red → conflict / mismatch
- Grey → unused

---

## Interaction

- Hover → show tooltip:
  - spell name
  - category
  - consensus key
  - confidence
- Click (future):
  - inspect ability details
  - suggest reassignment

---

## Proposed Implementation

### Phase 1 – Layout System
- Create keyboard layout table (key positions, sizes)
- Define reusable key UI element

### Phase 2 – Rendering
- Build keyboard frame
- Render keys using layout table
- Populate with current character bindings

### Phase 3 – Data Integration
- Integrate consensus data
- Colour keys based on match/mismatch
- Display category labels

### Phase 4 – Controls
- Add modifier toggles (Shift / Ctrl / Alt)
- Add scaling option (optional)

### Phase 5 – Enhancements
- Tooltips
- Click interactions
- Filtering (by category, conflicts)

---

## Data Requirements

Use existing systems:

- keybind snapshots
- consensus engine
- conflict detection

No direct reliance on raw API-only data for display.

---

## Acceptance Criteria

- [ ] Keyboard layout rendered correctly
- [ ] Keys display current bindings
- [ ] Keys display consensus mapping
- [ ] Conflicts are visually highlighted
- [ ] Tooltips provide detailed info
- [ ] Modifier toggles work correctly

---

## Future Enhancements

- Drag-and-drop key reassignment
- Profile save/load
- Integration with action bar UI
- One-handed accessibility mode

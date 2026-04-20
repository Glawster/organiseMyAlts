# Standardise Keybindings Across Characters and Specs (Consensus-Based)

## Summary
Keybindings currently vary between characters and talent specialisations, which reduces muscle memory efficiency and slows down gameplay.

This feature aims to standardise keybindings so that:
- Common abilities across characters use the same keys
- Core abilities across different specs of the same class remain consistent
- A consensus model is built across the entire account

---

## Goals

- Improve muscle memory and reaction time
- Reduce cognitive load when switching characters or specs
- Provide a consistent and optimised key layout
- Derive optimal bindings from real usage across all characters

---

## User Context

Preferred key layout:

- Main keys: 1, 2, 3, 4, 5
- Function keys: F1, F2, F3, F4
- Utility keys: Q, E, R, T, Y
- Special: 1 used for single-button assist

---

## Design Principle

The addon should not assume one character has the “correct” layout.

Instead, it should:
- capture layouts broadly across all characters and specs
- identify common patterns
- recommend a consensus key layout

---

## Data Capture Scope

Keybinding and action bar snapshots should be collected across:

- all characters
- all specs / talent builds
- all captured layouts over time

Each snapshot should include:
- character
- spec / talent loadout
- action bar slot → spell
- keybinding → action button
- timestamp

---

## Consensus Model

Build recommendations using layered consensus:

### Priority Order

1. Same character across specs  
2. Same class across characters/specs  
3. Account-wide role consensus  

---

## Desired Behaviour

### 1. Cross-Character Consistency
Abilities with similar roles should map to the same key across all characters.

Examples:
- Interrupt → same key (e.g. R)
- Movement ability → same key (e.g. Q)
- Defensive cooldown → same key (e.g. E)

---

### 2. Cross-Spec Consistency
Within a class, abilities should stay on the same keys between specs where possible.

Examples:
- Builder abilities → same key
- Spenders → same key
- Cooldowns → consistent positions

---

### 3. Ability Classification System
Introduce a classification layer:

- builder
- spender
- interrupt
- defensive
- movement
- cooldown
- utility

Each category maps to a preferred key.

---

## Proposed Implementation

### Phase 1 – Data Collection
- Capture keybindings and action bar layouts across all characters and specs
- Store snapshots with timestamps

### Phase 2 – Classification
- Map spells to categories
- Allow manual overrides

### Phase 3 – Consensus Engine
- Aggregate data across snapshots
- Determine most common key per role
- Identify inconsistencies

### Phase 4 – Recommendation Engine
- Suggest optimal layouts
- Highlight mismatches

### Phase 5 – Optional Enforcement
- Apply layouts automatically (optional)
- Export/import profiles

---

## In-Game Character Overview UI

Use `/oma ui` to toggle the character overview panel.

The panel shows:

- current character summary line: active spec, talent loadout ID, and whether the current spec/talent combo has a keybind snapshot
- a column table listing **all tracked characters** with:

| Column    | Description                                        |
|-----------|----------------------------------------------------|
| Character | Character name                                     |
| Class     | WoW class token                                    |
| Spec      | Active spec from last scan                         |
| Lvl       | Character level                                    |
| iLvl      | Equipped item level from last scan                 |
| KB Scan   | YES (green) / NO (red) — keybind snapshot present  |
| Last Scan | Date/time of last `/oma scan` run                  |

The current character's row is highlighted in yellow.

The panel refreshes automatically when `/oma scan` or `/oma keybinds` runs while it is open.

---

## Example Mapping

| Category  | Suggested Key |
|-----------|---------------|
| Assist    | 1             |
| Builder   | 2–3           |
| Spender   | 4–5           |
| Interrupt | R / backtick    |
| Defensive | E             |
| Movement  | Q             |
| Cooldown  | T / Y         |
| Utility   | F1–F4         |

---

## Logging Considerations

Log analysis events:

```
event=keybind.scan char=Name spec=Spec abilities=24
event=keybind.consensus_summary categories=8 char=Name-Realm
event=keybind.analysis conflicts=3 suggestions=5
```

---

## Acceptance Criteria

- [ ] Keybinding data captured across all characters and specs  
- [ ] Snapshot system implemented  
- [ ] Ability classification system implemented  
- [ ] Consensus engine produces stable key mappings  
- [ ] Recommendations generated based on consensus  
- [ ] Clear mapping between ability types and keys  

---

## Future Enhancements

- Visual layout editor UI
- One-handed accessibility optimisation
- Machine-learning-based suggestions
- Cross-account sync

# Filter Professions to Latest Expansion

## Summary
Profession data currently includes all expansion tiers, leading to noisy and misleading output.

## Problem
- Multiple tiers per profession
- Incorrect representation of progress
- Confusing UI and logs

## Desired Behaviour
- Only show latest expansion profession tier
- Maintain clean and relevant data

## Proposed Solution
- Filter professions by expansion ID
- Store only relevant tier data

## Acceptance Criteria
- [ ] Only latest expansion professions are stored
- [ ] UI reflects correct profession levels
- [ ] Logs reflect accurate counts

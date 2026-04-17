# Prevent Duplicate Keybinding Snapshots

## Summary
Keybinding snapshots are currently captured during both character scan and manual commands, which can result in duplicate or redundant snapshots being stored.

## Problem
- Multiple snapshots may be identical
- Snapshot history becomes noisy
- Consensus calculations become biased

## Desired Behaviour
- Only store snapshots when the layout has changed
- Avoid duplicate entries for same character/spec

## Proposed Solution
- Generate a hash of snapshot data
- Compare with latest snapshot
- Skip insert if identical

## Acceptance Criteria
- [ ] Duplicate snapshots are not stored
- [ ] Snapshot count remains stable during repeated scans
- [ ] Consensus results improve due to cleaner data

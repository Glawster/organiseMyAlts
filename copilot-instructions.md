# Copilot Instructions for organiseMyAlts

## Project purpose
organiseMyAlts is a World of Warcraft addon designed to guide solo players through an efficient weekly gameplay loop across multiple characters.

The addon is aimed at players who:
- play mainly solo
- focus on Delves, Prey, gear, and crafting
- play multiple alts
- want low-friction weekly planning

The addon should act as a **"what should I do next?" engine + checklist**, not just a passive data dump.

## Current architecture
The addon currently loads from the repository root with this layout:

- `organiseMyAlts.toc`
- `core/`
- `data/`

Current files include:
- `core/init.lua`
- `core/logger.lua`
- `data/characters.lua`
- `data/resets.lua`
- `data/tasks.lua`

Keep this root-level addon structure unless explicitly asked to change it.

## Coding style
When adding or editing code:
- prefer small, focused Lua modules
- use clear naming and keep code easy to scan
- favour simple, explicit logic over clever abstractions
- build incrementally in phases
- preserve a clean path toward future expansion

For this addon specifically:
- use `local oma = organiseMyAlts` within modules
- keep saved variable access through `oma.db`
- prefer helper methods on `oma` over scattered globals
- keep slash command handling simple and readable
- avoid introducing heavy frameworks unless explicitly requested

## Functional priorities
Prioritise features in this order unless asked otherwise:
1. character tracking
2. daily and weekly reset handling
3. manual task tracking
4. recommendation logic for current character
5. alt overview and scoring
6. Delves / Prey / crafting templates
7. UI panels and widgets

## Gameplay assumptions
Assume the target user:
- has around 2 hours per day
- plays mostly solo
- prefers Delves and Prey over Mythic+
- values gear progression and crafting
- uses alts for variety and profession coverage

Design decisions should support:
- minimal decision fatigue
- high-value actions surfaced first
- alt-friendly workflows
- graceful fallback when game APIs do not expose enough information

## Task model guidance
Tasks should support:
- daily, weekly, and manual reset types
- category, priority, completion state, and character ownership
- future expansion to Delves, Prey, crafting cooldowns, and profession tasks

When Blizzard APIs are limited, prefer a hybrid approach:
- auto-detect what is reliable
- allow manual overrides for the rest

## UI guidance
When building UI:
- optimise for fast scanning rather than decoration
- keep a compact and practical layout
- support a current-character view and an all-alts view
- keep minimap and widget features optional

## Safety for future edits
Do not:
- rename the addon without being asked
- move the addon into a nested subfolder without being asked
- replace the modular file layout with one huge file unless explicitly requested
- add Mythic+ assumptions into the recommendation model by default

## Good commit themes
Use commit scopes like:
- `phase 1: ...`
- `phase 2: ...`
- `docs: ...`
- `ui: ...`
- `engine: ...`

Keep changes cohesive and easy to review.

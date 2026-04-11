# organiseMyAlts

organiseMyAlts is a World of Warcraft addon designed to guide solo players through an efficient weekly gameplay loop across multiple characters.

---

## 🎯 Purpose

organiseMyAlts helps you answer:

> **“What should I do next?”**

It is designed for:
- solo players
- alt-heavy playstyles
- limited playtime (~2 hours/day)
- focus on gear + crafting
- Delves and Prey (not Mythic+)

---

## 🧠 Core Concept

The addon is a:

**decision engine + checklist**

It:
- tracks weekly and daily tasks
- monitors progress across alts
- highlights high-value actions
- reduces decision fatigue

---

## 🧩 Current Features (Phase 1)

- character tracking
- saved variables setup
- daily + weekly reset handling
- manual task creation
- per-character task tracking
- basic “next tasks” output
- slash commands:

# organiseMyAlts — Requirements and Development Phases

## Overview

**organiseMyAlts** is a World of Warcraft addon designed to help solo players manage multiple alts through a clear, efficient weekly gameplay loop.

The addon is aimed at players who:

- mainly play solo
- have limited playtime, such as around 2 hours per day
- focus on gear progression and crafting
- prefer Delves and Prey over Mythic+
- play multiple alts for variety and profession coverage

The addon should act as a:

> **"what should I do next?" engine + checklist**

It should reduce decision fatigue, keep alt data organised, and support both in-game use and out-of-game analysis.

---

## Core Product Goals

### Primary goals

- reduce decision fatigue on login
- show the best next action for the current character
- help manage multiple alts efficiently
- support solo-first gameplay
- keep track of weekly and daily opportunities
- support crafting and profession workflows
- encourage consistency across characters

### Secondary goals

- provide a strong data foundation for future analysis
- support action bar and keybind consistency across alts
- expose data in a form that can be processed outside the game with Python
- make cached alt data easy to compare and review

---

## Design Principles

- solo-first, not Mythic+-first
- alt-first, not main-only
- fast scanning over decorative UI
- small, modular Lua files
- explicit data structures over vague blobs
- graceful fallback when WoW APIs do not expose enough information
- hybrid model: auto-detect what is reliable, allow manual input for the rest
- data collection in-game, deeper analysis optionally out-of-game

---

## Functional Requirements

## 1. Character Registry

The addon must maintain an account-wide registry of known characters.

Each character record should support:

- character name
- realm
- class
- level
- last login timestamp
- last scan timestamp
- optional role tags
- optional notes

This registry should be updated whenever a character logs in.

---

## 2. Altoholic-Style Character Snapshot Cache

The addon must use a **last known snapshot** model for character data.

Character information should be scanned and cached when that character is logged in, rather than assumed to be live across the whole account.

Each character snapshot should support:

- class
- level
- current specialization
- average item level
- equipped items by slot
- professions
- optional bag summary
- optional currencies
- last login timestamp
- last scan timestamp

The addon should clearly distinguish cached data from live current-character data.

### Freshness requirements

Where cached character data is displayed, the addon should be able to show:

- updated today
- updated X days ago
- never scanned

---

## 3. Task System

The addon must support a flexible task system.

### Task reset types

- daily
- weekly
- manual

### Task fields

Each task should support:

- unique id
- name
- category
- character ownership
- reset type
- priority
- completion state
- optional progress value
- optional notes
- optional source or template key
- created timestamp
- completed timestamp

### Default task categories

- Delves
- Prey
- Crafting
- Professions
- Solo Gear
- Outdoor
- Currency
- Custom

### Default priority levels

- critical
- high
- medium
- low

---

## 4. Manual Task Support

The addon must allow manual task creation and manual completion toggles.

This is required because some gameplay systems may not be fully exposed through WoW APIs.

The user should be able to:

- create a manual task
- mark a task complete
- unmark a task if needed later
- create custom recurring tasks in future phases
- pin tasks in future phases
- hide tasks in future phases

---

## 5. Built-In Task Templates

The addon should support predefined task templates for core weekly and daily gameplay loops.

Initial built-in templates should include:

- Complete Prey Weekly
- Complete Delves (Weekly)
- Run 1 Delve
- Use Crafting Cooldowns

Templates should be created per character and must not duplicate if they already exist.

---

## 6. Recommendation Engine

The addon must recommend useful actions rather than only listing raw data.

It should support:

- best next action for the current character
- top 3 recommended actions
- best alt to switch to in later phases
- likely highest-value unfinished task

### Default recommendation priority

1. incomplete weekly tasks
2. high-value solo progression
3. daily crafting cooldowns
4. profession progression
5. optional or filler activities

The initial implementation may use a simple sort order before evolving into a scoring engine.

---

## 7. Reset Handling

The addon must support reset-aware task handling.

It should detect and store:

- daily reset state
- weekly reset state

When a reset occurs, relevant tasks should be refreshed automatically.

---

## 8. Crafting and Profession Tracking

The addon should support profession tracking across alts.

Each character should support:

- profession 1
- profession 2
- optional profession role tags
- crafting-related task visibility

Future phases should support:

- daily crafting sweep
- profession-specific weekly tasks
- profession role tags such as crafter, gatherer, consumables, gear crafting

---

## 9. Warband Equipment Awareness

The addon should support awareness of Warband-available equipment for alt progression.

This should be built as a **cached visibility system**, not as an assumption of always-live account-wide access.

### The addon should support

- scanning Warbound or Warband-transferable items in current bags
- scanning visible Warband Bank contents when the Warband Bank is open
- caching visible candidate items for later comparison
- comparing cached item opportunities against cached alt equipment snapshots
- flagging likely usable or upgraded gear for specific alts

### Important design rule

The UI must clearly distinguish:

- live visible data
- cached previously seen data

---

## 10. Keybind and Action Bar Consistency

This is a future feature, but the requirements should be captured now.

The addon should eventually help maintain consistent ability placement and keybind usage across:

- multiple alts
- different specs within the same class
- common gameplay roles

### Goal

Keep common ability roles in the same place where possible, for example:

- builder on key 1
- spender on key 2
- interrupt on F
- defensive on R

### Future system design

This should be based on:

- spell or ability classification
- action bar slot snapshots
- keybinding snapshots
- layout comparison
- optional suggested or user-triggered fixes

### Recommended model

Do not treat this as only a spell-to-key mapping system.

Prefer:

> role → preferred slot → preferred keybind

Examples of roles:

- builder
- spender
- interrupt
- defensive
- movement
- major cooldown

---

## 11. Out-of-Game Analysis Support

The addon should be designed so that its SavedVariables can be analysed outside the game with Python.

This is a first-class design requirement.

### In-game responsibilities

The addon should focus on:

- collecting data
- caching snapshots
- lightweight displays
- simple recommendations
- user-triggered actions

### Out-of-game responsibilities

Python tools may later perform:

- alt comparison
- task optimisation
- warband upgrade analysis
- keybind consistency analysis
- action bar drift detection
- recommendation generation
- markdown, JSON, or CSV report generation

### Data design requirements

The addon should store data in a way that is friendly to later Python analysis.

Preferred characteristics:

- stable keys
- explicit fields
- raw IDs as well as display text where useful
- timestamps for freshness
- clear separation between character data, tasks, layouts, and warband caches

Example areas of saved data:

- characters
- tasks
- resets
- warband
- layouts
- settings
- analysis outputs in future phases

---

## 12. UI Requirements

The UI should evolve over phases.

### Early phase UI

- slash commands
- chat output
- simple testing commands

### Later phase UI

- current character view
- alt overview view
- task summary view
- crafting sweep view
- optional widget
- optional minimap launcher

The UI should always optimise for:

- fast scanning
- practical use
- low clutter

---

## 13. Non-Functional Requirements

- lightweight and fast to load
- modular code structure
- easy to extend
- easy to review in Git
- suitable for phased development
- safe under WoW combat and protected frame restrictions
- explicit about stale cached data
- usable even if only part of the data model is populated

---

## Data Model Requirements

The exact schema may evolve, but the intended structure should resemble:

```lua
organiseMyAltsDB = {
    characters = {},
    tasks = {},
    resets = {},
    warband = {},
    layouts = {},
    settings = {},
    uiState = {},
}

characters["Name-Realm"] = {
    name = "Name",
    realm = "Realm",
    class = "MAGE",
    level = 80,
    specName = "Frost",
    specID = 64,
    averageItemLevel = 612.4,
    professions = {
        primary1 = "Tailoring",
        primary2 = "Enchanting",
    },
    equipment = {
        HEAD = {
            itemID = 12345,
            itemLink = "...",
            itemLevel = 610,
        },
    },
    lastLogin = time(),
    lastScan = time(),
}

tasks["prey_weekly_Name-Realm"] = {
    id = "prey_weekly_Name-Realm",
    name = "Complete Prey Weekly",
    category = "prey",
    character = "Name-Realm",
    resetType = "weekly",
    priority = "critical",
    completed = false,
    templateKey = "prey_weekly",
    createdAt = time(),
}

Development Phases
Phase 1 — Foundation
Goals
establish addon skeleton
create saved variables
register characters
add reset handling
add initial task storage
provide basic slash command testing
Scope
organiseMyAlts.toc
core/init.lua
core/logger.lua
data/characters.lua
data/resets.lua
data/tasks.lua
Status
addon appears in addon list
slash-command based smoke testing
basic character registration
basic task plumbing
Phase 2 — Task Engine
Goals
turn task storage into a real structured task system
add built-in task templates
add task categories and priorities
improve next-action logic
Scope
template tasks for Delves, Prey, and crafting
priority-based sorting
task bootstrap per character
better /oma next output
Sub-phases
Phase 2a — Character Scan Cache
add altoholic-style character scan cache
store spec, item level, equipment, professions
add /oma scan
add current character summary output
Phase 2b — Warband Item Cache
scan visible warbound gear in bags
scan visible Warband Bank contents when open
cache candidate items for later analysis
Phase 2c — Basic Upgrade Matching
compare cached gear opportunities to cached alt equipment
flag likely upgrades or useful items
Phase 3 — Alt Decision Engine
Goals
score alts for usefulness
show which alt should be played next
surface high-value unfinished opportunities account-wide
Scope
alt scoring model
best-alt recommendation
crafting sweep logic
stale scan visibility
better account-wide views
Phase 4 — UI Layer
Goals
move from chat-only interaction to a practical addon UI
support fast scanning of current character and all alts
Scope
current character panel
alt overview panel
weekly summary panel
crafting overview panel
optional lightweight checklist widget
optional minimap launcher
Phase 5 — Layout and Keybind Consistency
Goals
support action bar and keybind consistency across alts and specs
compare current layouts to preferred patterns
eventually suggest or apply fixes out of combat
Scope
action bar snapshot capture
keybind snapshot capture
role-based layout model
comparison view
suggestion engine
optional user-triggered apply logic in later sub-phases
Recommended sub-phases
Phase 5a
snapshot and compare only
Phase 5b
suggest fixes
Phase 5c
optional apply logic
Phase 6 — Out-of-Game Analysis Tooling
Goals
process SavedVariables data in Python
generate reports and recommendations outside the game
Scope
Python parser for SavedVariables
alt comparison reports
warband upgrade analysis
keybind consistency analysis
markdown / JSON / CSV outputs
optional analysis companion Lua file in later phases
Suggested Future File Layout

The exact file layout may evolve, but the intended modular direction is:

organiseMyAlts/
├── organiseMyAlts.toc
├── core/
│   ├── init.lua
│   ├── logger.lua
│   ├── constants.lua
│   └── utils.lua
├── data/
│   ├── characters.lua
│   ├── characterScan.lua
│   ├── resets.lua
│   ├── tasks.lua
│   ├── taskTemplates.lua
│   ├── warbandCache.lua
│   └── layouts.lua
├── engine/
│   ├── priorityEngine.lua
│   ├── altScoring.lua
│   └── gearAdvisor.lua
├── ui/
│   ├── mainFrame.lua
│   ├── currentPanel.lua
│   ├── altPanel.lua
│   ├── craftingPanel.lua
│   └── widget.lua
└── tools/
    └── python/
Recommended Near-Term Priorities

The next best implementation order is:

fix and validate phase 1 loading and slash command behaviour
phase 2a character scan cache
phase 2 task templates and priority engine
phase 2b warband item cache
phase 3 alt decision engine
Summary

organiseMyAlts should become a lightweight but powerful planning layer for solo alt play in WoW.

It should:

cache reliable character data
guide weekly and daily priorities
support Delves, Prey, crafting, and Warband opportunities
reduce alt-management friction
support consistent gameplay patterns across characters
expose structured data for deeper Python analysis outside the game
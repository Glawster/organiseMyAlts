# organiseMyAlts

organiseMyAlts is a World of Warcraft addon designed to guide solo players through an efficient weekly gameplay loop across multiple characters.

---

## 🎯 Purpose

organiseMyAlts helps you answer:

> **“What should I do next?”**

It is designed for:

* solo players
* alt-heavy playstyles
* limited playtime (~2 hours/day)
* focus on gear + crafting
* Delves and Prey (not Mythic+)

---

## 🧠 Core Concept

The addon is a:

**decision engine + checklist**

It:

* tracks weekly and daily tasks
* monitors progress across alts
* highlights high-value actions
* reduces decision fatigue

---

## 🧩 Current Features (Phase 1)

* character tracking
* saved variables setup
* daily + weekly reset handling
* manual task creation
* per-character task tracking
* basic “next tasks” output
* keybind snapshot capture + consensus suggestions
* character overview panel (`/oma ui`) with column table showing all alts, scan status, and item level

## How To Use It

Start with the practical user guide:

* [How To Use organiseMyAlts](documentation/how-to-use.md)

### Slash commands

```
/oma
/oma chars
/oma tasks
/oma next
/oma keybinds
/oma ui
```

---

# 📘 Requirements & Design

## Overview

organiseMyAlts is designed to help solo players manage multiple alts through a clear, efficient weekly loop.

It supports both:

* in-game guidance
* out-of-game analysis (Python tooling)

---

## 🎯 Core Goals

### Primary

* reduce decision fatigue
* guide next actions
* manage alts efficiently
* support solo gameplay
* track weekly + daily progression

### Secondary

* support crafting workflows
* enable keybind consistency
* provide structured data for analysis

---

## 🧱 Design Principles

* solo-first
* alt-first
* fast scanning > decoration
* modular Lua files
* explicit data structures
* hybrid model (auto + manual)
* data collection in-game, analysis optional outside

---

# ⚙️ Functional Requirements

## Character Registry

* account-wide character tracking
* updated on login
* includes class, level, timestamps

---

## Character Snapshot Cache (Altoholic-style)

Each character stores:

* class, spec, level
* item level + equipment
* professions
* timestamps

Data is:

* cached per character
* not assumed live

---

## Task System

Supports:

### Reset types

* daily
* weekly
* manual

### Fields

* id
* name
* category
* character
* reset type
* priority
* completion state

---

## Task Categories

* Delves
* Prey
* Crafting
* Professions
* Solo Gear
* Outdoor
* Currency
* Custom

---

## Priority Levels

* critical
* high
* medium
* low

---

## Built-in Tasks (planned)

* Complete Prey Weekly
* Complete Delves
* Run 1 Delve
* Crafting cooldowns

---

## Recommendation Engine

The addon must:

* suggest next actions
* prioritise high-value tasks
* evolve into scoring system

---

## Reset Handling

* detect daily reset
* detect weekly reset
* refresh tasks automatically

---

## Crafting Tracking

* professions per character
* cooldown visibility
* future: crafting sweep

---

## Warband Equipment (future)

* detect warbound gear
* scan bags + bank when visible
* cache opportunities
* compare against alt gear

---

## Keybind & Action Bar Consistency

Goal:

> consistent ability placement across alts

Model:

```
spell → classification → preferred key role → finding
```

Current Strafe Mode prototype roles:

* assist → 1
* self-heal / sustain → 2
* rotation → 3 / 4 / 5 / 6 / F1 / F2
* offensive → Q / E / R / T / Y / U
* interrupt → F3
* defensive → F5 / F6 / F7
* movement → F8
* utility → `
* system / reserved → H / J / K / L

Current support:

* capture action slot → spell and key → action button snapshots
* store snapshots with character, spec, talent loadout, and timestamp
* classify captured abilities (built-in + manual override support)
* build layered consensus (character → class → account)
* show recommendations with `/oma keybinds`
* prototype consensus-aware Findings model in the Python UI harness

---

## In-Game Lua UI Direction

The addon should have a simple in-game Lua UI for normal use.

Slash commands remain available for expert users, debugging, macros, and fast command-line workflows, but the main player workflow should be available through buttons and panels.

The planned Lua UI should expose the same actions as the slash commands:

* character summary
* character list
* current character scan
* keybind snapshot capture
* keybind scan status
* task list
* next tasks
* task complete / undo
* daily and weekly task creation
* alt rankings
* best alt recommendation
* logs and debug controls
* Findings / keybind consistency view

Initial UI goal:

* one compact main window
* clear action buttons for common commands
* status area for command output
* tabs or sections for Characters, Tasks, Keybinds, and Debug
* slash commands preserved as the expert interface

---

## Out-of-Game Analysis

Data must support Python tooling.

### In-game

* collect data
* cache snapshots
* display lightweight info

### Out-of-game

* compare alts
* analyse gear
* optimise tasks
* generate reports

---

# 📊 Data Model

```lua
organiseMyAltsDB = {
    characters = {},
    tasks = {},
    resets = {},
    warband = {},
    layouts = {},
    keybinds = {
        snapshots = {},
        classificationOverrides = {},
    },
    settings = {},
}
```

---

# 🚀 Development Phases

## Phase 1 — Foundation And Command Coverage (current)

* addon skeleton
* saved variables
* character tracking
* character scan cache
* reset handling
* basic task system
* slash commands for all core actions

---

## Phase 2 — Simple Lua Control Panel

* build a compact in-game main window
* expose existing slash-command actions as UI buttons
* show command results in a status/output area
* add sections for Characters, Tasks, Keybinds, and Debug
* keep slash commands as expert shortcuts

---

## Phase 3 — Keybind Findings Foundation

* port the Python findings model into Lua
* add preferred key roles and Strafe Mode profile data
* build Lua consensus helpers
* compare captured bindings against preferred roles
* display simple match/mismatch findings in the Lua UI

---

## Phase 4 — Keyboard Findings Window

* port the keyboard diagram into WoW Frames
* show key role colours
* show current spell assignments
* add tooltips with spell, role, category, consensus, and confidence
* integrate with real `/oma keybinds` snapshots

---

## Phase 5 — Task And Alt Decision Engine

* task templates
* priorities
* better next-action logic
* alt scoring
* best alt recommendation
* account-wide optimisation

---

## Phase 6 — Recommendations And Polish

* keybind consistency scoring
* concrete keybind recommendations
* spell classification management
* import/export
* SavedVariables parsing/reporting tools
* optional Python reports and deeper analysis

---

# 📁 Project Structure

```
organiseMyAlts/
├── uiTestHarness/
│   ├── src/
│   ├── tests/
│   ├── pytest.ini
│   └── requirements-dev.txt
├── core/
├── data/
├── engine/
└── documentation/
```

---

# 🧭 Roadmap (short-term)

1. build a simple Lua main window that exposes the existing slash-command workflows
2. add reusable UI helpers for buttons, rows, section panels, and status output
3. wire scan, keybind capture, task list, next task, alt ranking, and debug actions into the UI
4. port the Python keybind findings model into Lua
5. add the in-game Findings / keyboard view

---

# 🧠 Summary

organiseMyAlts is a:

> lightweight planning layer for solo alt gameplay

It aims to:

* organise your week
* reduce friction
* improve consistency
* support deeper analysis

---

## Status

Early development — core systems in progress.

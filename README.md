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
* keybind scan status UI panel

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
role → slot → keybind
```

Categories:

* assist → 1
* builder → 2 / 3
* spender → 4 / 5
* interrupt → R / `
* defensive → E
* movement → Q
* cooldown → T / Y
* utility → F1-F4

Current support:

* capture action slot → spell and key → action button snapshots
* store snapshots with character, spec, talent loadout, and timestamp
* classify captured abilities (built-in + manual override support)
* build layered consensus (character → class → account)
* show recommendations with `/oma keybinds`

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

## Phase 1 — Foundation (current)

* addon skeleton
* character tracking
* reset handling
* basic task system

---

## Phase 2 — Task Engine

* task templates
* priorities
* better next-action logic

### Sub-phases

* 2a: character scan cache
* 2b: warband cache
* 2c: upgrade matching

---

## Phase 3 — Alt Decision Engine

* alt scoring
* best alt recommendation
* account-wide optimisation

---

## Phase 4 — UI Layer

* dashboard
* alt overview
* task panels
* optional widget

---

## Phase 5 — Layout Consistency

* action bar tracking
* keybind tracking
* suggestion system

---

## Phase 6 — Python Tooling

* SavedVariables parsing
* reports + analysis
* upgrade recommendations

---

# 📁 Project Structure

```
organiseMyAlts/
├── organiseMyAlts.toc
├── core/
├── data/
├── engine/
├── ui/
└── tools/
```

---

# 🧭 Roadmap (short-term)

1. fix phase 1 loading + commands
2. add character scan cache
3. implement task templates
4. add warband item tracking
5. build alt scoring system

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

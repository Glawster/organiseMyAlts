# How To Use organiseMyAlts

This guide covers the addon as it works today, plus the Python UI prototype that is being used to design the future keybind Findings window.

organiseMyAlts currently has two parts:

- The in-game WoW addon, controlled with `/oma` commands.
- The Python UI test harness, used to prototype the keyboard and Findings workflow before it is rebuilt in Lua.

Planned direction:

- A simple in-game Lua UI will become the normal way to use the addon.
- Slash commands will remain available for expert users, debugging, macros, and quick actions.

## In-Game Addon

### 1. Load The Addon

Put the addon folder in your WoW retail AddOns directory:

```text
World of Warcraft/_retail_/Interface/AddOns/organiseMyAlts
```

In game, reload the UI:

```text
/reload
```

Then run:

```text
/oma
```

You should see the help menu.

## First-Time Setup

### 1. Log In To Each Character

Log in to each character you want organiseMyAlts to know about.

On login, the addon registers:

- character name
- realm
- class
- level
- last login time

### 2. Scan Each Character

On each character, run:

```text
/oma scan
```

This updates the cached character snapshot, including current spec and item level data.

### 3. Capture Keybinds

On each character and spec you care about, set up your action bars and run:

```text
/oma keybinds
```

This captures a keybind snapshot for the current character/spec/talent loadout.

For the best future consensus results, repeat this on:

- each character
- each spec
- each important talent loadout

The addon stores snapshots in `organiseMyAltsDB.keybinds.snapshots`.

## Useful Commands

### General

```text
/oma
```

Shows the help menu.

```text
/oma char
```

Shows the current character summary.

```text
/oma chars
```

Lists tracked characters.

```text
/oma scan
```

Rescans the current character.

### Tasks

```text
/oma tasks
```

Shows numbered tasks for the current character.

```text
/oma next
```

Shows the next recommended tasks.

```text
/oma done <number>
```

Marks a visible task complete.

```text
/oma undo <number>
```

Marks a visible task incomplete.

```text
/oma daily <name>
```

Adds a custom daily task.

```text
/oma weekly <name>
```

Adds a custom weekly task.

```text
/oma reset
```

Resets task completion for the current character.

```text
/oma reset all
```

Resets task completion for all characters.

### Alt Scoring

```text
/oma alts
```

Shows alt rankings.

```text
/oma best
```

Shows the best alt to play according to the current scoring logic.

### Keybinds

```text
/oma keybinds
```

Captures the current keybind snapshot and prints current consensus/recommendation output.

```text
/oma ui
```

Toggles the in-game character overview panel.

The panel shows tracked characters, class, spec, item level, scanned specs, and last scan information.

### Debugging

```text
/oma debug
```

Toggles debug logging.

```text
/oma logs
```

Shows recent logs.

```text
/oma logreset
```

Clears stored logs.

## Planned In-Game UI

The next major usability step is a simple Lua control panel that performs the same actions as the slash commands.

The goal is that normal use does not require remembering commands.

Planned main window sections:

| Section | Purpose |
| --- | --- |
| Characters | Show tracked characters, current character summary, scan status, and scan button |
| Tasks | Show current tasks, next tasks, mark done, undo, reset |
| Keybinds | Capture keybind snapshot, show scan coverage, open Findings |
| Alts | Show alt rankings and best alt recommendation |
| Debug | Toggle debug, view logs, clear logs |

Planned first version:

1. Open a compact organiseMyAlts window.
2. Click buttons for the common actions currently handled by `/oma`.
3. See output in a simple status/results area.
4. Use slash commands only when you want fast expert control.

The first UI does not need to be beautiful. It should be reliable, readable, and easy to migrate into richer panels later.

## Current Keybind Workflow

The current in-game keybind workflow is scan-first:

1. Log in to a character.
2. Select the spec/talent loadout you want to capture.
3. Make sure your action bars are set up.
4. Run `/oma keybinds`.
5. Repeat for other specs and characters.
6. Use `/oma ui` to check which characters/specs have been scanned.

The addon currently captures:

- action bar slot
- action button
- key bound to that button
- spell ID
- spell name
- character
- class
- spec
- talent loadout ID
- timestamp

## Consensus And Strafe Mode

The prototype is moving toward a consensus model.

The goal is for the addon to learn patterns like:

```text
Death Strike appears on 2 across Death Knight specs.
Therefore, 2 is probably your self-heal/sustain key.
```

The current prototype includes a Strafe Mode profile based on this playstyle:

- hold strafe right on `D`
- use right mouse button for facing
- spam single-button assist on `1`
- use self-heal/sustain on `2`
- use nearby rotation keys such as `3`, `4`, `F1`, and `F2`

Current prototype key roles:

| Key | Role |
| --- | --- |
| `1` | Assist |
| `2` | Self-heal / sustain |
| `3`, `4`, `5`, `6` | Rotation |
| `F1`, `F2` | Reachable rotation |
| `Q`, `E`, `R`, `T`, `Y`, `U` | Offensive |
| `F3` | Interrupt |
| `F5`, `F6`, `F7` | Defensive |
| `F8` | Movement |
| `` ` `` | Utility |
| `H`, `J`, `K`, `L` | System/reserved |

## Python UI Prototype

The Python harness is not the in-game addon UI. It is a fast way to design and test the future Lua UI.

### Install Python Dependencies

From the addon folder:

```text
cd uiTestHarness
python3 -m pip install -r requirements-dev.txt
```

### Run The Prototype

From `uiTestHarness`:

```text
python3 -m src.app
```

The main window opens first.

Use:

```text
Show Findings
```

This opens the Findings prototype and hides the main window.

### Use The Findings Window

In the Findings window:

1. Choose a character.
2. Choose a spec.
3. Review the keyboard diagram.
4. Key colour shows the preferred role.
5. Spell text shows the current assignment.
6. Hover a key to see details.
7. Right-click a key to change its role.
8. Double-click a key to edit the displayed spell name.
9. Close the Findings window to return to the main window.

The current prototype includes sample data for:

- Hunter Marksmanship
- Mage Arcane
- Death Knight Death Strike consensus examples

### Run The Test Suite

From `uiTestHarness`:

```text
pytest -q
```

## What Is Implemented Today

Implemented in the Lua addon:

- character registry
- character scans
- task commands
- keybind snapshot capture
- early spell classification
- early consensus/recommendation output
- character overview panel

Implemented in the Python prototype:

- main window
- Findings window
- physical keyboard diagram
- role colours
- key selection
- spell display names
- tooltips
- role editing
- inline spell-name editing
- consensus-aware findings service
- Strafe Mode profile

## What Is Not Implemented Yet

Not yet complete in the in-game Lua addon:

- simple main control panel for all common slash-command actions
- full Findings window
- full keyboard diagram UI
- profile editor
- spell classification management UI
- robust comparison engine
- scoring engine for keybind consistency
- recommendation engine with concrete suggested moves
- import/export

## Recommended Day-To-Day Use For Now

For actual WoW data collection:

1. Log in to each character.
2. Run `/oma scan`.
3. For each spec, run `/oma keybinds`.
4. Use `/oma ui` to check scan coverage.

Once the planned Lua control panel exists, use it for these actions and keep slash commands for expert shortcuts.

For UI and keybind model development:

1. Run the Python harness.
2. Open Show Findings.
3. Review how the keyboard model feels.
4. Adjust roles and spell examples in the prototype.
5. Run `pytest -q` before migrating behavior into Lua.

# Improve Logging System (Structured, Useful, Bounded)

## Summary
The current logging system in **organiseMyAlts** mirrors user-facing console output rather than providing meaningful diagnostic information. This makes debugging difficult and causes unnecessary log growth.

We should refactor logging to be:
- Structured
- Informative (focus on *what happened and why*)
- Bounded (prevent unbounded growth)
- Separate from UI output

---

## Current Problems

### 1. Logs mirror UI output
Examples:
```
/oma chars     - list characters
1. [todo] Complete Delves (Weekly)
```

These are not useful for debugging and duplicate chat output.

---

### 2. Lack of context (“why”)
Example:
```
task reset: Complete Delves (Weekly)
```

Missing:
- Why it reset (daily/weekly rollover?)
- Which period triggered it
- Previous state

---

### 3. Repeated / noisy entries
Logs frequently include repeated sequences:
```
loaded
commands: ...
profession scan...
```

Suggests:
- Multiple init triggers
- No filtering or deduplication

---

### 4. No log retention policy
Logs are stored in SavedVariables and grow indefinitely:

```lua
logs = { ... }
```

This will eventually:
- Slow loading
- Bloat SavedVariables file

---

## Desired Behaviour

### 1. Structured logging
Use consistent key=value format:

```
event=task.complete id=prey_weekly_Annson-AeriePeak char=Annson-AeriePeak source=slash_done
```

---

### 2. Log levels
Introduce simple levels:

- DEBUG – internal flow  
- INFO – normal operations  
- WARN – unexpected but handled  
- ERROR – failures  

---

### 3. Separate logging from UI
- `self:print()` → user-facing  
- `self:log()` → internal only  

Never log UI/help/command output.

---

### 4. Log trimming
Limit log size (e.g. last 200 entries):
- Prevent SavedVariables bloat  
- Maintain performance  

---

### 5. Reset logs command
Add:
```
/oma logreset
```

Clears stored logs.

---

## Proposed Implementation

### Logging function
```lua
function OMA:log(level, msg)
    if not self.db.logs then self.db.logs = {} end

    table.insert(self.db.logs, {
        ts = date("%Y-%m-%d %H:%M:%S"),
        level = level,
        msg = msg
    })

    self:trimLogs()
end
```

---

### Log trimming
```lua
local MAX_LOGS = 200

function OMA:trimLogs()
    local logs = self.db.logs
    if #logs > MAX_LOGS then
        local excess = #logs - MAX_LOGS
        for i = 1, excess do
            table.remove(logs, 1)
        end
    end
end
```

---

### Reset logs
```lua
function OMA:resetLogs()
    self.db.logs = {}
    self:print("logs cleared")
end
```

---

## Example Improvements

### Before
```
task completed: Complete Prey Weekly
```

### After
```
event=task.complete id=prey_weekly_Annson-AeriePeak char=Annson-AeriePeak source=slash_done
```

---

### Before
```
scan complete: Annson-AeriePeak
```

### After
```
event=scan.complete char=Annson-AeriePeak ilvl=103 tasks=4 professions=2
```

---

### Before
```
no task found for selection: 5
```

### After
```
event=task.lookup.failed selection=5 available=4 source=next_list
```

---

## Benefits

- Easier debugging of task logic and resets  
- Clear understanding of system behaviour  
- Prevents SavedVariables bloat  
- Cleaner separation of concerns (UI vs logic)  

---

## Optional Enhancements (Future)

- Debug mode toggle (`/oma debug`)  
- Session markers (`event=session.start`)  
- Log filtering in `/oma logs`  

---

## Acceptance Criteria

- [ ] Logs no longer include UI/command output  
- [ ] Logs use structured key=value format  
- [ ] Log size is capped (e.g. 200 entries)  
- [ ] `/oma logreset` command works  
- [ ] Key events (scan, task complete, reset, errors) are logged with context  

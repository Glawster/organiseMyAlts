local addonName, addon = ...

organiseMyAlts = organiseMyAlts or {}
local oma = organiseMyAlts

oma.name = addonName
oma.version = "0.2.2"
oma.keybindDefaultMaxSnapshots = 120

oma.eventFrame = CreateFrame("Frame")
oma.lastNextTaskIds = {}

local function dispatchEvent(_, event, ...)
    if type(oma[event]) == "function" then
        oma[event](oma, ...)
    end
end

oma.eventFrame:SetScript("OnEvent", dispatchEvent)
oma.eventFrame:RegisterEvent("ADDON_LOADED")
oma.eventFrame:RegisterEvent("PLAYER_LOGIN")
oma.eventFrame:RegisterEvent("PLAYER_ENTERING_WORLD")

function oma:ADDON_LOADED(name)
    if name ~= addonName then
        return
    end

    organiseMyAltsDB = organiseMyAltsDB or {}
    organiseMyAltsDB.characters = organiseMyAltsDB.characters or {}
    organiseMyAltsDB.tasks = organiseMyAltsDB.tasks or {}
    organiseMyAltsDB.resets = organiseMyAltsDB.resets or {}
    organiseMyAltsDB.warband = organiseMyAltsDB.warband or {}
    organiseMyAltsDB.layouts = organiseMyAltsDB.layouts or {}
    organiseMyAltsDB.keybinds = organiseMyAltsDB.keybinds or {}
    local keybindsDB = organiseMyAltsDB.keybinds
    keybindsDB.snapshots = keybindsDB.snapshots or {}
    keybindsDB.classificationOverrides = keybindsDB.classificationOverrides or {}
    keybindsDB.maxSnapshots = keybindsDB.maxSnapshots or self.keybindDefaultMaxSnapshots
    organiseMyAltsDB.settings = organiseMyAltsDB.settings or {}
    organiseMyAltsDB.uiState = organiseMyAltsDB.uiState or {}

    self.db = organiseMyAltsDB
    organiseMyAltsDB.logs = organiseMyAltsDB.logs or {}
    if self.trimLogs then
        self:trimLogs()
    end
end

function oma:PLAYER_LOGIN()
    local charKey = self:getCurrentCharacterKey() or "unknown"
    self:registerCharacter()
    self:scanCurrentCharacter()
    self:initialiseResets()
    self:refreshTaskResets()
    self:ensureTemplateTasks()
    self:log("INFO", string.format("event=session.start char=%s", charKey))
end

function oma:PLAYER_ENTERING_WORLD()
    self:registerCharacter()
end

SLASH_ORGANISEMYALTS1 = "/oma"

SlashCmdList["ORGANISEMYALTS"] = function(msg)
    oma:handleSlash(msg or "")
end

function oma:printHelp()
    self:printSection("commands...")

    self:print("/oma chars     - list characters")
    self:print("/oma char      - current character summary")
    self:print("/oma tasks     - list all numbered tasks")
    self:print("/oma next      - show top numbered tasks")
    self:print("/oma scan      - rescan current character")

    self:print("/oma done <n>  - complete numbered task")
    self:print("/oma undo <n>  - undo numbered task")

    self:print("/oma daily     - add custom daily task")
    self:print("/oma weekly    - add custom weekly task")

    self:print("/oma alts      - show alt rankings")
    self:print("/oma best      - best alt to play")
    self:print("/oma keybinds  - capture + show keybind consensus")

    self:print("/oma debug     - toggle debug logging")
    self:print("/oma logs      - show recent logs")
    self:print("/oma logreset  - clear stored logs")

    self:print("/oma reset     - reset task completion for current character")
    self:print("/oma reset all - reset task completion for all characters")
end

function oma:handleSlash(msg)
    local command, rest = msg:match("^(%S+)%s*(.-)$")
    command = command and string.lower(command) or ""

    if command == "" or command == "help" then
        self:printHelp()

    elseif command == "chars" then
        self:printCharacters()

    elseif command == "char" then
        self:printCurrentCharacterSummary()

    elseif command == "tasks" then
        self:printTasksForCurrentCharacter()

    elseif command == "next" then
        self:printNextTasks()

    elseif command == "scan" then
        self:scanCurrentCharacter()
        self:printCurrentCharacterSummary()

    elseif command == "done" then
        self:markTaskByVisibleIndex(rest, true)

    elseif command == "undo" then
        self:markTaskByVisibleIndex(rest, false)

    elseif command == "daily" then
        if rest == "" then
            self:print("usage: /oma daily <name>")
        else
            self:createTask(rest, "daily")
        end

    elseif command == "weekly" then
        if rest == "" then
            self:print("usage: /oma weekly <name>")
        else
            self:createTask(rest, "weekly")
        end

    elseif command == "alts" then
        self:printAltScores()
    
    elseif command == "best" then
        self:printBestAlt()
    
    elseif command == "keybinds" then
        self:captureKeybindingSnapshot()
        self:printKeybindRecommendations()

    elseif command == "debug" then
        self.db.settings.debug = not self.db.settings.debug
        self:print("debug logging:", self.db.settings.debug and "ON" or "OFF")
        self:log(
            "INFO",
            string.format(
                "event=logging.debug_toggle enabled=%s source=slash_debug",
                self.db.settings.debug and "true" or "false"
            )
        )

    elseif command == "logs" then
        self:printSection("recent logs...")

        local logs = self.db.logs or {}
        local start = math.max(1, #logs - 10)

        for i = start, #logs do
            local entry = logs[i]
            self:print(entry.ts, entry.level or "INFO", entry.msg)
        end

    elseif command == "logreset" then
        self:resetLogs()

    elseif command == "reset" then
        self:resetTasks(rest)

    else
        self:printHelp()
    end
end

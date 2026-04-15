local oma = organiseMyAlts

-- Keep logs useful for debugging without growing SavedVariables indefinitely.
local MAX_LOG_ENTRIES = 200
local VALID_LEVELS = {
    DEBUG = true,
    INFO = true,
    WARN = true,
    ERROR = true,
}

function oma:print(...)
    print("|cff00ff98[organiseMyAlts]|r", ...)
end

function oma:printSection(title)
    print("|cff00ff98[organiseMyAlts]|r", "|cffffff00" .. title .. "|r")
end

function oma:log(level, msg)
    if not self.db then
        return
    end

    if type(level) ~= "string" then
        return
    end

    level = string.upper(level)
    if not VALID_LEVELS[level] then
        return
    end

    if type(msg) ~= "string" then
        return
    end

    self.db.logs = self.db.logs or {}

    table.insert(self.db.logs, {
        ts = date("%Y-%m-%d %H:%M:%S"),
        level = level,
        msg = msg,
    })

    self:trimLogs()
end

function oma:trimLogs()
    if not self.db then
        return
    end

    self.db.logs = self.db.logs or {}
    local logs = self.db.logs

    if #logs > MAX_LOG_ENTRIES then
        local excess = #logs - MAX_LOG_ENTRIES
        local newSize = MAX_LOG_ENTRIES

        for i = 1, newSize do
            logs[i] = logs[i + excess]
        end

        for i = #logs, newSize + 1, -1 do
            logs[i] = nil
        end
    end
end

function oma:logDebug(...)
    if not self.db or not self.db.settings or not self.db.settings.debug then
        return
    end

    local parts = {}
    for i = 1, select("#", ...) do
        table.insert(parts, tostring(select(i, ...)))
    end

    self:log("DEBUG", string.format("event=debug.message text=%q", table.concat(parts, " ")))
end

function oma:resetLogs()
    if not self.db then
        return
    end

    self.db.logs = {}
    self:print("logs cleared")
end

local oma = organiseMyAlts

local MAX_LOG_ENTRIES = 500

function oma:print(...)
    print("|cff00ff98[organiseMyAlts]|r", ...)
    self:log(...)
end

function oma:printSection(title)
    print("|cff00ff98[organiseMyAlts]|r", "|cffffff00" .. title .. "|r")
end

local function now()
    return date("%Y-%m-%d %H:%M:%S")
end

function oma:log(...)
    if not self.db or not self.db.logs then
        return
    end

    local parts = {}
    for i = 1, select("#", ...) do
        local v = select(i, ...)
        table.insert(parts, tostring(v))
    end

    local message = table.concat(parts, " ")

    table.insert(self.db.logs, {
        ts = now(),
        msg = message,
    })

    -- prevent unbounded growth
    if #self.db.logs > MAX_LOG_ENTRIES then
        table.remove(self.db.logs, 1)
    end
end

function oma:logDebug(...)
    if not self.db.settings or not self.db.settings.debug then
        return
    end

    self:log("[DEBUG]", ...)
end
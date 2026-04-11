local addonName, addon = ...

organiseMyAlts = organiseMyAlts or {}
local oma = organiseMyAlts

oma.name = addonName
oma.version = "0.2.0"

oma.eventFrame = CreateFrame("Frame")

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
    organiseMyAltsDB.settings = organiseMyAltsDB.settings or {}

    self.db = organiseMyAltsDB
end

function oma:PLAYER_LOGIN()
    self:registerCharacter()
    self:scanCurrentCharacter()
    self:initialiseResets()
    self:refreshTaskResets()
    self:print("loaded")
end

function oma:PLAYER_ENTERING_WORLD()
    self:registerCharacter()
end

SLASH_ORGANISEMYALTS1 = "/oma"

SlashCmdList["ORGANISEMYALTS"] = function(msg)
    oma:handleSlash(msg or "")
end

function oma:handleSlash(msg)
    local command, rest = msg:match("^(%S+)%s*(.-)$")
    command = command and string.lower(command) or ""

    if command == "" or command == "help" then
        self:print("commands: /oma chars | char | tasks | next | scan")
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
    else
        self:print("commands: /oma chars | char | tasks | next | scan")
    end
end
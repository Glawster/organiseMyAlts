local addonName, addon = ...

organiseMyAlts = organiseMyAlts or {}
local oma = organiseMyAlts

oma.name = addonName
oma.version = "0.1.0"

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
    if name ~= addonName then return end

    organiseMyAltsDB = organiseMyAltsDB or {}
    organiseMyAltsDB.characters = organiseMyAltsDB.characters or {}
    organiseMyAltsDB.tasks = organiseMyAltsDB.tasks or {}
    organiseMyAltsDB.resets = organiseMyAltsDB.resets or {}

    self.db = organiseMyAltsDB
end

function oma:PLAYER_LOGIN()
    self:registerCharacter()
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
    if msg == "chars" then
        self:printCharacters()
    elseif msg == "tasks" then
        self:printTasksForCurrentCharacter()
    elseif msg == "next" then
        self:printNextTasks()
    else
        self:print("commands: /oma chars | tasks | next")
    end
end

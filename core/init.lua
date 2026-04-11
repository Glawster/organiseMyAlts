local addonName, addon = ...

organiseMyAlts = {}
local oma = organiseMyAlts

oma.name = addonName

-- Event Frame
oma.eventFrame = CreateFrame("Frame")

-- Register Events
oma.eventFrame:RegisterEvent("ADDON_LOADED")
oma.eventFrame:RegisterEvent("PLAYER_LOGIN")

oma.eventFrame:SetScript("OnEvent", function(self, event, ...)
    if oma[event] then
        oma[event](oma, ...)
    end
end)

-- SavedVariables Init
function oma:ADDON_LOADED(name)
    if name ~= addonName then return end

    if not organiseMyAltsDB then
        organiseMyAltsDB = {
            characters = {}
        }
    end

    self.db = organiseMyAltsDB
end

-- Player Ready
function oma:PLAYER_LOGIN()
    self:registerCharacter()
    self:print("Loaded")
end

-- Slash Command
SLASH_ORGANISEMYALTS1 = "/oma"

SlashCmdList["ORGANISEMYALTS"] = function(msg)
    oma:handleSlash(msg)
end

function oma:handleSlash(msg)
    if msg == "chars" then
        self:printCharacters()
    else
        self:print("Commands: /oma chars")
    end
end
local oma = organiseMyAlts

function oma:getCurrentCharacterKey()
    local name = UnitName("player")
    local realm = GetNormalizedRealmName() or GetRealmName()

    if not name or not realm then
        return nil
    end

    return name .. "-" .. realm
end

function oma:registerCharacter()
    local key = self:getCurrentCharacterKey()
    if not key then
        return
    end

    self.db.characters[key] = self.db.characters[key] or {}

    local char = self.db.characters[key]
    char.name = UnitName("player")
    char.realm = GetNormalizedRealmName() or GetRealmName()
    char.class = select(2, UnitClass("player"))
    char.level = UnitLevel("player")
    char.lastLogin = time()
end

function oma:printCharacters()
    local foundAny = false

    for key, char in pairs(self.db.characters) do
        foundAny = true
        local specName = char.specName or "unknown spec"
        local ilvl = char.equippedItemLevel or char.averageItemLevel or "?"
        self:print(key, char.level or "?", char.class or "UNKNOWN", specName, "ilvl", ilvl)
    end

    if not foundAny then
        self:print("no characters tracked")
    end
end
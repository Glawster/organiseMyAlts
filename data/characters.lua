local oma = organiseMyAlts

function oma:getCurrentCharacterKey()
    local name = UnitName("player")
    local realm = GetNormalizedRealmName()
    return name .. "-" .. realm
end

function oma:registerCharacter()
    local key = self:getCurrentCharacterKey()

    self.db.characters[key] = self.db.characters[key] or {}

    local char = self.db.characters[key]
    char.name = UnitName("player")
    char.class = select(2, UnitClass("player"))
    char.level = UnitLevel("player")
    char.lastLogin = time()
end

function oma:printCharacters()
    for key, char in pairs(self.db.characters) do
        self:print(key, char.level, char.class)
    end
end

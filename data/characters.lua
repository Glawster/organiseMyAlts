local oma = organiseMyAlts

function oma:registerCharacter()
    local name = UnitName("player")
    local realm = GetNormalizedRealmName()
    local key = name .. "-" .. realm

    if not self.db.characters[key] then
        self.db.characters[key] = {}
    end

    local char = self.db.characters[key]

    char.name = name
    char.realm = realm
    char.class = select(2, UnitClass("player"))
    char.level = UnitLevel("player")
    char.lastLogin = time()

    self:print("Registered character:", key)
end

function oma:printCharacters()
    for key, char in pairs(self.db.characters) do
        self:print(key, "Level", char.level, char.class)
    end
end
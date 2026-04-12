local oma = organiseMyAlts

local equipmentSlots = {
    { key = "HEAD", slotId = INVSLOT_HEAD },
    { key = "NECK", slotId = INVSLOT_NECK },
    { key = "SHOULDER", slotId = INVSLOT_SHOULDER },
    { key = "CHEST", slotId = INVSLOT_CHEST },
    { key = "WAIST", slotId = INVSLOT_WAIST },
    { key = "LEGS", slotId = INVSLOT_LEGS },
    { key = "FEET", slotId = INVSLOT_FEET },
    { key = "WRIST", slotId = INVSLOT_WRIST },
    { key = "HANDS", slotId = INVSLOT_HAND },
    { key = "FINGER1", slotId = INVSLOT_FINGER1 },
    { key = "FINGER2", slotId = INVSLOT_FINGER2 },
    { key = "TRINKET1", slotId = INVSLOT_TRINKET1 },
    { key = "TRINKET2", slotId = INVSLOT_TRINKET2 },
    { key = "BACK", slotId = INVSLOT_BACK },
    { key = "MAINHAND", slotId = INVSLOT_MAINHAND },
    { key = "OFFHAND", slotId = INVSLOT_OFFHAND },
}

local function professionLabel(profession)
    if not profession then
        return "none"
    end

    local name = profession.name or profession.professionName or "unknown"
    local skillLevel = profession.skillLevel or 0
    local maxSkillLevel = profession.maxSkillLevel or 0

    return string.format("%s (%d/%d)", name, skillLevel, maxSkillLevel)
end

function oma:getCurrentSpecInfo()
    local specIndex = GetSpecialization and GetSpecialization()
    if not specIndex then
        return nil, nil
    end

    local specID, specName = GetSpecializationInfo(specIndex)
    return specID, specName
end

function oma:getCurrentProfessions()
    local professions = {
        primary1 = nil,
        primary2 = nil,
        archaeology = nil,
        fishing = nil,
        cooking = nil,
        all = {},
    }

    local profession1, profession2, archaeology, fishing, cooking = GetProfessions()
    local indices = {
        primary1 = profession1,
        primary2 = profession2,
        archaeology = archaeology,
        fishing = fishing,
        cooking = cooking,
    }

    for key, index in pairs(indices) do
        if index then
            local name, icon, skillLevel, maxSkillLevel, numAbilities, spellOffset, skillLine, skillModifier, specializationIndex, specializationOffset, skillLineName = GetProfessionInfo(index)

            local entry = {
                index = index,
                name = name,
                icon = icon,
                skillLevel = skillLevel,
                maxSkillLevel = maxSkillLevel,
                numAbilities = numAbilities,
                spellOffset = spellOffset,
                skillLine = skillLine,
                skillModifier = skillModifier,
                specializationIndex = specializationIndex,
                specializationOffset = specializationOffset,
                skillLineName = skillLineName,
            }

            professions[key] = entry
            table.insert(professions.all, entry)
        end
    end

    return professions
end

function oma:scanCurrentEquipment()
    local equipment = {}

    for _, entry in ipairs(equipmentSlots) do
        local itemLink = GetInventoryItemLink("player", entry.slotId)
        local itemID = GetInventoryItemID("player", entry.slotId)

        if itemLink or itemID then
            local itemName, _, _, itemLevel, _, itemType, itemSubType, _, itemEquipLoc = GetItemInfo(itemLink or itemID)

            equipment[entry.key] = {
                itemID = itemID,
                itemLink = itemLink,
                itemName = itemName,
                itemLevel = itemLevel,
                itemType = itemType,
                itemSubType = itemSubType,
                itemEquipLoc = itemEquipLoc,
                slotId = entry.slotId,
            }
        end
    end

    return equipment
end

function oma:scanCurrentCharacter()
    local characterKey = self:getCurrentCharacterKey()
    self:printSection("scan...")

    if not characterKey then
        self:print("unable to identify current character")
        return
    end

    local character = self.db.characters[characterKey] or {}
    local specID, specName = self:getCurrentSpecInfo()
    local avgItemLevel, equippedItemLevel = GetAverageItemLevel()

    character.name = UnitName("player")
    character.realm = GetNormalizedRealmName() or GetRealmName() or "UnknownRealm"
    character.class = select(2, UnitClass("player"))
    character.level = UnitLevel("player") or 0
    character.specID = specID
    character.specName = specName
    character.averageItemLevel = avgItemLevel
    character.equippedItemLevel = equippedItemLevel
    character.professions = self:getCurrentProfessions()
    character.equipment = self:scanCurrentEquipment()
    character.lastLogin = time()
    character.lastScan = time()

    self.db.characters[characterKey] = character

    local p1 = character.professions and character.professions.primary1 or nil
    local p2 = character.professions and character.professions.primary2 or nil

    self:print("profession scan:", professionLabel(p1), "/", professionLabel(p2))
    self:print("scan complete:", characterKey)
end

function oma:printCurrentCharacterSummary()
    local characterKey = self:getCurrentCharacterKey()
    self:printSection("this character...")

    if not characterKey then
        self:print("unable to identify current character")
        return
    end

    local character = self.db.characters[characterKey]
    if not character then
        self:print("no cached data for current character")
        return
    end

    self:print("character:", characterKey)
    self:print("class:", character.class or "unknown")
    self:print("level:", character.level or 0)
    self:print("spec:", character.specName or "unknown")
    self:print("equipped ilvl:", character.equippedItemLevel or "unknown")
    self:print("average ilvl:", character.averageItemLevel or "unknown")

    local p1 = character.professions and character.professions.primary1 or nil
    local p2 = character.professions and character.professions.primary2 or nil

    self:print("professions:")
    self:print("  ", professionLabel(p1))
    self:print("  ", professionLabel(p2))
end
local oma = organiseMyAlts

local slotGroups = {
    { token = "ACTIONBUTTON", slotStart = 1, count = 12 },
    { token = "MULTIACTIONBAR1BUTTON", slotStart = 13, count = 12 },
    { token = "MULTIACTIONBAR2BUTTON", slotStart = 25, count = 12 },
    { token = "MULTIACTIONBAR3BUTTON", slotStart = 37, count = 12 },
    { token = "MULTIACTIONBAR4BUTTON", slotStart = 49, count = 12 },
}

oma.keybindCategoryOrder = {
    "assist",
    "builder",
    "spender",
    "interrupt",
    "defensive",
    "movement",
    "cooldown",
    "utility",
}

oma.keybindCategoryDefaults = {
    assist = { "1" },
    builder = { "2", "3" },
    spender = { "4", "5" },
    interrupt = { "R", "`" },
    defensive = { "E" },
    movement = { "Q" },
    cooldown = { "T", "Y" },
    utility = { "F1", "F2", "F3", "F4" },
}

local builtinSpellCategoryByID = {
    [6552] = "interrupt", -- Pummel
    [1766] = "interrupt", -- Kick
    [2139] = "interrupt", -- Counterspell
    [57994] = "interrupt", -- Wind Shear
    [96231] = "interrupt", -- Rebuke
    [183752] = "interrupt", -- Consume Magic
    [187707] = "interrupt", -- Muzzle
    [106839] = "movement", -- Skull Bash
    [102280] = "defensive", -- Dampen Harm
}

local function normaliseBindingKey(key)
    if type(key) ~= "string" then
        return nil
    end

    local trimmed = strtrim(key)
    if trimmed == "" then
        return nil
    end

    return string.upper(trimmed)
end

local function getPreferredCategoryByKey(key)
    for category, keys in pairs(oma.keybindCategoryDefaults) do
        for _, preferredKey in ipairs(keys) do
            if preferredKey == key then
                return category
            end
        end
    end

    return nil
end

local function getSpellNameFromAction(actionType, actionID, fallbackName)
    if actionType ~= "spell" or not actionID then
        return fallbackName
    end

    local name = GetSpellInfo(actionID)
    return name or fallbackName
end

local function captureActionSlots()
    local actionSlots = {}
    local buttonBySlot = {}
    local bindingByButton = {}
    local bindingByKey = {}

    for _, group in ipairs(slotGroups) do
        for index = 1, group.count do
            local slot = group.slotStart + index - 1
            local buttonName = string.format("%s%d", group.token, index)
            local actionType, actionID, actionSubType = GetActionInfo(slot)
            local actionName = GetActionText(slot)
            local spellName = getSpellNameFromAction(actionType, actionID, actionName)
            local key1, key2 = GetBindingKey(buttonName)
            local keys = {}

            for _, key in ipairs({ key1, key2 }) do
                local normalised = normaliseBindingKey(key)
                if normalised then
                    table.insert(keys, normalised)
                    bindingByButton[buttonName] = bindingByButton[buttonName] or {}
                    table.insert(bindingByButton[buttonName], normalised)
                    bindingByKey[normalised] = buttonName
                end
            end

            actionSlots[slot] = {
                slot = slot,
                button = buttonName,
                actionType = actionType,
                actionID = actionID,
                actionSubType = actionSubType,
                spellID = actionType == "spell" and actionID or nil,
                spellName = spellName,
                keys = keys,
            }

            buttonBySlot[slot] = buttonName
        end
    end

    return actionSlots, buttonBySlot, bindingByButton, bindingByKey
end

function oma:getCurrentTalentLoadoutID()
    if C_ClassTalents and C_ClassTalents.GetActiveConfigID then
        return C_ClassTalents.GetActiveConfigID()
    end

    return nil
end

function oma:getSpellCategory(spellID, spellName, key)
    local overrides = self.db.keybinds and self.db.keybinds.classificationOverrides or nil
    if overrides and spellID and overrides[spellID] then
        return overrides[spellID], "manual_override"
    end

    if spellID and builtinSpellCategoryByID[spellID] then
        return builtinSpellCategoryByID[spellID], "builtin"
    end

    local inferred = getPreferredCategoryByKey(key)
    if inferred then
        return inferred, "key_preference"
    end

    if spellName and string.find(string.lower(spellName), "assist", 1, true) then
        return "assist", "name_inference"
    end

    return "utility", "fallback"
end

function oma:setSpellCategoryOverride(spellID, category)
    if not spellID or not category or not self.db.keybinds then
        return
    end

    self.db.keybinds.classificationOverrides = self.db.keybinds.classificationOverrides or {}
    self.db.keybinds.classificationOverrides[spellID] = category
end

function oma:captureKeybindingSnapshot()
    if not self.db or not self.db.keybinds then
        return nil
    end

    local characterKey = self:getCurrentCharacterKey()
    if not characterKey then
        return nil
    end

    local specID, specName = self:getCurrentSpecInfo()
    local actionSlots, buttonBySlot, bindingByButton, bindingByKey = captureActionSlots()
    local snapshot = {
        ts = time(),
        character = characterKey,
        class = select(2, UnitClass("player")),
        specID = specID,
        specName = specName,
        talentLoadoutID = self:getCurrentTalentLoadoutID(),
        actionSlots = actionSlots,
        slotToButton = buttonBySlot,
        buttonToKeys = bindingByButton,
        keyToButton = bindingByKey,
        abilities = {},
    }

    for _, slotEntry in pairs(actionSlots) do
        if slotEntry.spellID and slotEntry.keys and slotEntry.keys[1] then
            local key = slotEntry.keys[1]
            local category, source = self:getSpellCategory(slotEntry.spellID, slotEntry.spellName, key)

            table.insert(snapshot.abilities, {
                spellID = slotEntry.spellID,
                spellName = slotEntry.spellName,
                key = key,
                slot = slotEntry.slot,
                category = category,
                categorySource = source,
            })
        end
    end

    self.db.keybinds.snapshots = self.db.keybinds.snapshots or {}
    table.insert(self.db.keybinds.snapshots, snapshot)

    local maxSnapshots = self.db.keybinds.maxSnapshots or 120
    while #self.db.keybinds.snapshots > maxSnapshots do
        table.remove(self.db.keybinds.snapshots, 1)
    end

    self:log(
        "INFO",
        string.format(
            "event=keybind.scan char=%s spec=%s abilities=%d",
            characterKey,
            specName or "unknown",
            #snapshot.abilities
        )
    )

    return snapshot
end

local function addVote(votes, category, key)
    if not votes[category] then
        votes[category] = {}
    end

    votes[category][key] = (votes[category][key] or 0) + 1
end

local function getBestKeyForCategory(categoryVotes, preferredKeys)
    local bestKey = nil
    local bestVotes = -1
    local totalVotes = 0

    for key, count in pairs(categoryVotes or {}) do
        totalVotes = totalVotes + count
        if count > bestVotes then
            bestVotes = count
            bestKey = key
        elseif count == bestVotes and preferredKeys then
            for _, preferred in ipairs(preferredKeys) do
                if key == preferred then
                    bestKey = key
                    break
                end
            end
        end
    end

    return bestKey, bestVotes, totalVotes
end

function oma:getKeybindConsensusForCharacter(characterKey)
    local snapshots = self.db.keybinds and self.db.keybinds.snapshots or {}
    local char = self.db.characters and self.db.characters[characterKey]
    local currentClass = char and char.class or nil

    local charVotes = {}
    local classVotes = {}
    local accountVotes = {}

    for _, snapshot in ipairs(snapshots) do
        for _, ability in ipairs(snapshot.abilities or {}) do
            if ability.category and ability.key then
                addVote(accountVotes, ability.category, ability.key)
                if currentClass and snapshot.class == currentClass then
                    addVote(classVotes, ability.category, ability.key)
                end
                if snapshot.character == characterKey then
                    addVote(charVotes, ability.category, ability.key)
                end
            end
        end
    end

    local consensus = {}
    for _, category in ipairs(self.keybindCategoryOrder or {}) do
        local preferred = self.keybindCategoryDefaults[category] or {}
        local key, votes, total = getBestKeyForCategory(charVotes[category], preferred)
        local source = "character"

        if not key then
            key, votes, total = getBestKeyForCategory(classVotes[category], preferred)
            source = "class"
        end

        if not key then
            key, votes, total = getBestKeyForCategory(accountVotes[category], preferred)
            source = "account"
        end

        if not key then
            key = preferred[1]
            votes = 0
            total = 0
            source = "default"
        end

        consensus[category] = {
            key = key,
            source = source,
            votes = votes or 0,
            total = total or 0,
            confidence = (total and total > 0) and (votes / total) or 0,
        }
    end

    return consensus
end

function oma:getLatestKeybindSnapshot(characterKey)
    local snapshots = self.db.keybinds and self.db.keybinds.snapshots or {}
    for index = #snapshots, 1, -1 do
        local snapshot = snapshots[index]
        if snapshot and snapshot.character == characterKey then
            return snapshot
        end
    end
    return nil
end

function oma:getKeybindRecommendations(characterKey)
    local consensus = self:getKeybindConsensusForCharacter(characterKey)
    local latest = self:getLatestKeybindSnapshot(characterKey)
    local conflicts = {}

    if latest then
        for _, ability in ipairs(latest.abilities or {}) do
            local recommendation = consensus[ability.category]
            if recommendation and recommendation.key and ability.key ~= recommendation.key then
                table.insert(conflicts, {
                    spellID = ability.spellID,
                    spellName = ability.spellName,
                    category = ability.category,
                    currentKey = ability.key,
                    suggestedKey = recommendation.key,
                })
            end
        end
    end

    return {
        character = characterKey,
        consensus = consensus,
        latestSnapshot = latest,
        conflicts = conflicts,
    }
end

function oma:printKeybindRecommendations()
    local characterKey = self:getCurrentCharacterKey()
    if not characterKey then
        self:print("unable to identify current character")
        return
    end

    local result = self:getKeybindRecommendations(characterKey)
    local suggestionCount = 0
    self:printSection("keybind recommendations...")

    for _, category in ipairs(self.keybindCategoryOrder or {}) do
        local entry = result.consensus and result.consensus[category]
        if entry then
            suggestionCount = suggestionCount + 1
            self:log(
                "INFO",
                string.format(
                    "event=keybind.consensus role=%s key=%s confidence=%.2f",
                    category,
                    entry.key or "none",
                    entry.confidence or 0
                )
            )
            self:print(
                string.format(
                    "%s -> %s (%s, confidence %.2f)",
                    category,
                    entry.key or "none",
                    entry.source or "unknown",
                    entry.confidence or 0
                )
            )
        end
    end

    self:print("mismatches:", #result.conflicts)
    self:log(
        "INFO",
        string.format(
            "event=keybind.analysis conflicts=%d suggestions=%d",
            #result.conflicts,
            suggestionCount
        )
    )
end

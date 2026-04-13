local oma = organiseMyAlts

local function getAgeInDays(timestamp)
    if not timestamp then
        return 999
    end

    local ageSeconds = time() - timestamp
    return math.floor(ageSeconds / 86400)
end

local function countTasksForCharacter(tasks, characterKey)
    local counts = {
        weeklyTodo = 0,
        dailyTodo = 0,
        craftingTodo = 0,
        totalTodo = 0,
    }

    for _, task in pairs(tasks or {}) do
        if task.character == characterKey and not task.completed then
            counts.totalTodo = counts.totalTodo + 1

            if task.resetType == "weekly" then
                counts.weeklyTodo = counts.weeklyTodo + 1
            elseif task.resetType == "daily" then
                counts.dailyTodo = counts.dailyTodo + 1
            end

            if task.category == "crafting" then
                counts.craftingTodo = counts.craftingTodo + 1
            end
        end
    end

    return counts
end

function oma:scoreCharacter(characterKey)
    local character = self.db.characters and self.db.characters[characterKey]
    if not character then
        return nil
    end

    local taskCounts = countTasksForCharacter(self.db.tasks, characterKey)
    local scanAgeDays = getAgeInDays(character.lastScan)

    local score = 0
    local reasons = {}

    if taskCounts.weeklyTodo > 0 then
        score = score + (taskCounts.weeklyTodo * 30)
        table.insert(reasons, string.format("%d weekly task(s) left", taskCounts.weeklyTodo))
    end

    if taskCounts.dailyTodo > 0 then
        score = score + (taskCounts.dailyTodo * 10)
        table.insert(reasons, string.format("%d daily task(s) left", taskCounts.dailyTodo))
    end

    if taskCounts.craftingTodo > 0 then
        score = score + (taskCounts.craftingTodo * 8)
        table.insert(reasons, "crafting cooldowns available")
    end

    if scanAgeDays == 0 then
        score = score + 5
    elseif scanAgeDays > 7 then
        score = score - 10
        table.insert(reasons, "scan data is stale")
    end

    if character.equippedItemLevel and tonumber(character.equippedItemLevel) then
        local ilvl = tonumber(character.equippedItemLevel)
        if ilvl < 237 then
            table.insert(reasons, "high upgrade potential")
        elseif ilvl < 250 then
            table.insert(reasons, "moderate upgrade potential")
        elseif ilvl < 263 then
            table.insert(reasons, "some upgrade potential")
        else
            score = score - 3
            table.insert(reasons, "low upgrade potential")
        end

        local ilvl = tonumber(character.equippedItemLevel)
        if ilvl < 700 then
            score = score + 5
            table.insert(reasons, "gear upgrades likely for this character")
        end
    end

    if #reasons == 0 then
        table.insert(reasons, "done for now")
    end

    return {
        key = characterKey,
        name = character.name or characterKey,
        class = character.class or "UNKNOWN",
        specName = character.specName or "unknown",
        level = character.level or 0,
        equippedItemLevel = character.equippedItemLevel or character.averageItemLevel or "?",
        score = score,
        taskCounts = taskCounts,
        scanAgeDays = scanAgeDays,
        reasons = reasons,
    }
end

function oma:getAltScores()
    local results = {}

    for characterKey, _ in pairs(self.db.characters or {}) do
        local scored = self:scoreCharacter(characterKey)
        if scored then
            table.insert(results, scored)
        end
    end

    table.sort(results, function(a, b)
        if a.score ~= b.score then
            return a.score > b.score
        end

        return (a.key or "") < (b.key or "")
    end)

    return results
end

function oma:printAltScores()
    local results = self:getAltScores()

    self:printSection("alt recommendations...")

    if #results == 0 then
        self:print("no character data available")
        return
    end

    for index, entry in ipairs(results) do
        self:print(
            string.format(
                "%d. %s (%s %s, ilvl %s) score=%d",
                index,
                entry.key,
                entry.class,
                entry.specName,
                tostring(entry.equippedItemLevel),
                entry.score
            )
        )

        if entry.reasons and entry.reasons[1] then
            self:print("   why:", entry.reasons[1])
        end
    end
end

function oma:printBestAlt()
    local results = self:getAltScores()

    self:printSection("best alt...")

    if #results == 0 then
        self:print("no character data available")
        return
    end

    local best = results[1]

    self:print(
        string.format(
            "%s (%s %s, ilvl %s) score=%d",
            best.key,
            best.class,
            best.specName,
            tostring(best.equippedItemLevel),
            best.score
        )
    )

    for _, reason in ipairs(best.reasons or {}) do
        self:print(" -", reason)
    end
end
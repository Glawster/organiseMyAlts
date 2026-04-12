local oma = organiseMyAlts

local priorityWeight = {
    critical = 4,
    high = 3,
    medium = 2,
    low = 1,
}

function oma:createTask(name, resetType)
    local key = self:getCurrentCharacterKey()
    local id = name .. "_" .. time()

    self.db.tasks[id] = {
        name = name,
        character = key,
        resetType = resetType,
        completed = false
    }

    self:print("task added:", name)
end

local priorityWeight = {
    critical = 4,
    high = 3,
    medium = 2,
    low = 1,
}

function oma:getTasksForCurrentCharacter()
    local key = self:getCurrentCharacterKey()
    local result = {}

    for _, task in pairs(self.db.tasks) do
        if task.character == key then
            table.insert(result, task)
        end
    end

    -- ✅ THIS is the missing piece
    table.sort(result, function(a, b)

        -- incomplete first
        if a.completed ~= b.completed then
            return not a.completed
        end

        -- weekly before daily
        if a.resetType ~= b.resetType then
            return a.resetType == "weekly"
        end

        -- priority
        local pa = priorityWeight[a.priority or "low"] or 1
        local pb = priorityWeight[b.priority or "low"] or 1

        if pa ~= pb then
            return pa > pb
        end

        -- fallback
        return (a.name or "") < (b.name or "")
    end)

    return result
end

function oma:printTasksForCurrentCharacter()
    local tasks = self:getTasksForCurrentCharacter()

    for _, task in ipairs(tasks) do
        local status = task.completed and "done" or "todo"
        self:print(status, task.name)
    end
end

function oma:printNextTasks()
    local tasks = self:getTasksForCurrentCharacter()

    local count = 0
    for _, task in ipairs(tasks) do
        if not task.completed then
            count = count + 1
            self:print("next:", task.name)
            if count >= 3 then break end
        end
    end
end

function oma:ensureTemplateTasks()
    local charKey = self:getCurrentCharacterKey()
    if not charKey then return end

    for _, template in ipairs(self.taskTemplates or {}) do
        local exists = false

        for _, task in pairs(self.db.tasks) do
            if task.templateKey == template.key and task.character == charKey then
                exists = true
                break
            end
        end

        if not exists then
            local id = template.key .. "_" .. charKey

            self.db.tasks[id] = {
                id = id,
                name = template.name,
                category = template.category,
                character = charKey,
                resetType = template.resetType,
                priority = template.priority,
                completed = false,
                templateKey = template.key,
                createdAt = time(),
            }

            self:print("added task:", template.name)
        end
    end
end
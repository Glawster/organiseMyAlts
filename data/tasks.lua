local oma = organiseMyAlts

local priorityWeight = {
    critical = 4,
    high = 3,
    medium = 2,
    low = 1,
}

function oma:ensureTemplateTasks()
    local charKey = self:getCurrentCharacterKey()
    if not charKey then
        return
    end

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
                completedAt = nil,
                templateKey = template.key,
                createdAt = time(),
            }

            self:print("added task:", template.name)
        end
    end
end

function oma:createTask(name, resetType)
    local key = self:getCurrentCharacterKey()
    if not key then
        self:print("unable to identify current character")
        return
    end

    local id = name:gsub("%s+", "_"):lower() .. "_" .. time()

    self.db.tasks[id] = {
        id = id,
        name = name,
        category = "custom",
        character = key,
        resetType = resetType,
        priority = resetType == "weekly" and "high" or "medium",
        completed = false,
        completedAt = nil,
        createdAt = time(),
    }

    self:print("task added:", name)
end

function oma:markTaskComplete(taskId)
    local task = self.db.tasks[taskId]
    if not task then
        self:print("task not found:", taskId)
        return
    end

    task.completed = true
    task.completedAt = time()

    self:print("task completed:", task.name)
end

function oma:markTaskIncomplete(taskId)
    local task = self.db.tasks[taskId]
    if not task then
        self:print("task not found:", taskId)
        return
    end

    task.completed = false
    task.completedAt = nil

    self:print("task reset:", task.name)
end

function oma:getTasksForCurrentCharacter()
    local key = self:getCurrentCharacterKey()
    local result = {}

    if not key then
        return result
    end

    for _, task in pairs(self.db.tasks) do
        if task.character == key then
            table.insert(result, task)
        end
    end

    table.sort(result, function(a, b)
        if a.completed ~= b.completed then
            return not a.completed
        end

        if a.resetType ~= b.resetType then
            return a.resetType == "weekly"
        end

        local pa = priorityWeight[a.priority or "low"] or 1
        local pb = priorityWeight[b.priority or "low"] or 1

        if pa ~= pb then
            return pa > pb
        end

        return (a.name or "") < (b.name or "")
    end)

    return result
end

function oma:printTasksForCurrentCharacter()
    local tasks = self:getTasksForCurrentCharacter()

    self:printSection("tasks...")

    if #tasks == 0 then
        self:print("no tasks for this character")
        return
    end

    for _, task in ipairs(tasks) do
        self:print(
            string.format(
                "[%s] %s (%s, %s) id=%s",
                task.completed and "done" or "todo",
                task.name,
                task.resetType or "unknown",
                task.priority or "low",
                task.id or "unknown"
            )
        )
    end
end

function oma:printNextTasks()
    local tasks = self:getTasksForCurrentCharacter()

    self:printSection("next steps...")

    local shown = 0

    for _, task in ipairs(tasks) do
        if not task.completed then
            shown = shown + 1
            self:print(
                string.format(
                    "%d. %s (%s)",
                    shown,
                    task.name,
                    task.priority or "low"
                )
            )

            if shown >= 3 then
                break
            end
        end
    end

    if shown == 0 then
        self:print("all tasks complete — switch alt?")
    end
end
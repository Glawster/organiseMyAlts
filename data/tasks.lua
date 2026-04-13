local oma = organiseMyAlts

local priorityWeight = {
    critical = 4,
    high = 3,
    medium = 2,
    low = 1,
}

local function createUniqueTaskId(prefix)
    local randomPart = math.random(1000, 9999)
    return string.format("%s_%d_%d", prefix, time(), randomPart)
end

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
            local id = string.format("%s_%s", template.key, charKey)

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
                locationHint = template.locationHint,
                pickupHint = template.pickupHint,
                createdAt = time(),
            }

            self:print("added task:", template.name)
        end
    end
end

function oma:createTask(name, resetType)
    local charKey = self:getCurrentCharacterKey()
    if not charKey then
        self:print("unable to identify current character")
        return
    end

    local prefix = resetType == "weekly" and "custom_weekly" or "custom_daily"
    local id = createUniqueTaskId(prefix)

    self.db.tasks[id] = {
        id = id,
        name = name,
        category = "custom",
        character = charKey,
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
    local charKey = self:getCurrentCharacterKey()
    local result = {}

    if not charKey then
        return result
    end

    for _, task in pairs(self.db.tasks) do
        if task.character == charKey then
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

function oma:getVisibleTasksForCurrentCharacter(limit, includeCompleted)
    local tasks = self:getTasksForCurrentCharacter()
    local visibleTasks = {}

    for _, task in ipairs(tasks) do
        if includeCompleted or not task.completed then
            table.insert(visibleTasks, task)

            if limit and #visibleTasks >= limit then
                break
            end
        end
    end

    return visibleTasks
end

function oma:markTaskByVisibleIndex(indexText, shouldComplete)
    if indexText == "" then
        if shouldComplete then
            self:print("usage: /oma done <number>")
        else
            self:print("usage: /oma undo <number>")
        end
        return
    end

    local index = tonumber(indexText)
    if not index then
        self:print("invalid selection:", indexText)
        return
    end

    local visibleTasks = self:getVisibleTasksForCurrentCharacter(nil, true)
    local task = visibleTasks[index]

    if not task then
        self:print("no task found for selection:", index)
        self:print("run /oma tasks to see numbered tasks")
        return
    end

    if shouldComplete then
        self:markTaskComplete(task.id)
    else
        self:markTaskIncomplete(task.id)
    end

    self:printTasksForCurrentCharacter()
end

function oma:printTasksForCurrentCharacter()
    local tasks = self:getVisibleTasksForCurrentCharacter(nil, true)

    self:printSection("tasks...")

    if #tasks == 0 then
        self:print("no tasks for this character")
        return
    end

    for index, task in ipairs(tasks) do
        self:print(
            string.format(
                "%d. [%s] %s (%s, %s)",
                index,
                task.completed and "done" or "todo",
                task.name,
                task.resetType or "unknown",
                task.priority or "low"
            )
        )

        if task.locationHint then
            self:print("   where:", task.locationHint)
        end

        if task.pickupHint then
            self:print("   how:", task.pickupHint)
        end
    end
end

function oma:printNextTasks()
    local tasks = self:getVisibleTasksForCurrentCharacter(3, false)

    self:printSection("next steps...")

    if #tasks == 0 then
        self:print("all tasks complete — switch alt?")
        return
    end

    for index, task in ipairs(tasks) do
        self:print(
            string.format(
                "%d. [%s] %s (%s, %s)",
                index,
                task.completed and "done" or "todo",
                task.name,
                task.resetType or "unknown",
                task.priority or "low"
            )
        )

        if task.locationHint then
            self:print("   where:", task.locationHint)
        end

        if task.pickupHint then
            self:print("   how:", task.pickupHint)
        end
    end
end

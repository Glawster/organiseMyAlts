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
            self:log(
                "INFO",
                string.format(
                    "event=task.create id=%s char=%s reset=%s priority=%s source=template",
                    id,
                    charKey,
                    template.resetType or "unknown",
                    template.priority or "unknown"
                )
            )
        end
    end
end

function oma:createTask(name, resetType)
    local charKey = self:getCurrentCharacterKey()
    if not charKey then
        self:print("unable to identify current character")
        self:log("ERROR", "event=task.create.failed reason=missing_character source=slash_create")
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
    self:log(
        "INFO",
        string.format(
            "event=task.create id=%s char=%s reset=%s priority=%s source=slash_create",
            id,
            charKey,
            resetType,
            self.db.tasks[id].priority or "unknown"
        )
    )
end

function oma:markTaskComplete(taskId)
    local task = self.db.tasks[taskId]
    if not task then
        self:print("task not found:", taskId)
        self:log(
            "WARN",
            string.format("event=task.lookup.failed id=%s source=mark_complete", tostring(taskId))
        )
        return
    end

    local previousCompleted = task.completed and "true" or "false"
    task.completed = true
    task.completedAt = time()

    self:print("task completed:", task.name)
    self:log(
        "INFO",
        string.format(
            "event=task.complete id=%s char=%s source=slash_done previous_completed=%s",
            task.id,
            task.character or "unknown",
            previousCompleted
        )
    )
end

function oma:markTaskIncomplete(taskId)
    local task = self.db.tasks[taskId]
    if not task then
        self:print("task not found:", taskId)
        self:log(
            "WARN",
            string.format("event=task.lookup.failed id=%s source=mark_incomplete", tostring(taskId))
        )
        return
    end

    local previousCompleted = task.completed and "true" or "false"
    task.completed = false
    task.completedAt = nil

    self:print("task reset:", task.name)
    self:log(
        "INFO",
        string.format(
            "event=task.reopen id=%s char=%s source=slash_undo previous_completed=%s",
            task.id,
            task.character or "unknown",
            previousCompleted
        )
    )
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
        self:log(
            "WARN",
            string.format(
                "event=task.command.invalid selection=empty source=%s",
                shouldComplete and "slash_done" or "slash_undo"
            )
        )
        return
    end

    local index = tonumber(indexText)
    if not index then
        self:print("invalid selection:", indexText)
        self:log(
            "WARN",
            string.format(
                "event=task.lookup.failed selection=%s source=%s reason=invalid_number",
                tostring(indexText),
                shouldComplete and "slash_done" or "slash_undo"
            )
        )
        return
    end

    local visibleTasks = self:getVisibleTasksForCurrentCharacter(nil, true)
    local task = visibleTasks[index]

    if not task then
        self:print("no task found for selection:", index)
        self:print("run /oma tasks to see numbered tasks")
        self:log(
            "WARN",
            string.format(
                "event=task.lookup.failed selection=%d available=%d source=%s",
                index,
                #visibleTasks,
                shouldComplete and "slash_done" or "slash_undo"
            )
        )
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

function oma:resetTasks(scope)
    local currentCharKey = self:getCurrentCharacterKey()
    local resetCount = 0

    if scope == "all" then
        for _, task in pairs(self.db.tasks or {}) do
            task.completed = false
            task.completedAt = nil
            resetCount = resetCount + 1
        end

        self:printSection("reset...")
        self:print("reset tasks for: all characters")
        self:print("tasks reset:", resetCount)
        self:log(
            "INFO",
            string.format("event=tasks.reset scope=all reset_count=%d source=slash_reset", resetCount)
        )
        return
    end

    if not currentCharKey then
        self:print("unable to identify current character")
        self:log("ERROR", "event=tasks.reset.failed scope=current reason=missing_character source=slash_reset")
        return
    end

    for _, task in pairs(self.db.tasks or {}) do
        if task.character == currentCharKey then
            task.completed = false
            task.completedAt = nil
            resetCount = resetCount + 1
        end
    end

    self:printSection("reset...")
    self:print("reset tasks for:", currentCharKey)
    self:print("tasks reset:", resetCount)
    self:log(
        "INFO",
        string.format(
            "event=tasks.reset scope=character char=%s reset_count=%d source=slash_reset",
            currentCharKey,
            resetCount
        )
    )
end

function oma:resetTasksForCurrentCharacter()
    local charKey = self:getCurrentCharacterKey()
    if not charKey then
        self:print("unable to identify current character")
        return
    end

    local resetCount = 0

    for _, task in pairs(self.db.tasks or {}) do
        if task.character == charKey then
            task.completed = false
            task.completedAt = nil
            resetCount = resetCount + 1
        end
    end

    self:printSection("reset...")
    self:print("reset tasks for:", charKey)
    self:print("tasks reset:", resetCount)
end

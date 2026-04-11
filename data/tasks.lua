local oma = organiseMyAlts

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

function oma:getTasksForCurrentCharacter()
    local key = self:getCurrentCharacterKey()
    local result = {}

    for _, task in pairs(self.db.tasks) do
        if task.character == key then
            table.insert(result, task)
        end
    end

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

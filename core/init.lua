function oma:handleSlash(msg)
    local command, rest = msg:match("^(%S+)%s*(.-)$")
    command = command and string.lower(command) or ""

    if command == "" or command == "help" then
        self:print("commands: /oma chars | char | tasks | next | scan | done <id> | undo <id> | adddaily <name> | addweekly <name>")

    elseif command == "chars" then
        self:printCharacters()

    elseif command == "char" then
        self:printCurrentCharacterSummary()

    elseif command == "tasks" then
        self:printTasksForCurrentCharacter()

    elseif command == "next" then
        self:printNextTasks()

    elseif command == "scan" then
        self:scanCurrentCharacter()
        self:printCurrentCharacterSummary()

    elseif command == "done" then
        if rest == "" then
            self:print("usage: /oma done <taskId>")
        else
            self:markTaskComplete(rest)
        end

    elseif command == "undo" then
        if rest == "" then
            self:print("usage: /oma undo <taskId>")
        else
            self:markTaskIncomplete(rest)
        end

    elseif command == "adddaily" then
        if rest == "" then
            self:print("usage: /oma adddaily <name>")
        else
            self:createTask(rest, "daily")
        end

    elseif command == "addweekly" then
        if rest == "" then
            self:print("usage: /oma addweekly <name>")
        else
            self:createTask(rest, "weekly")
        end

    else
        self:print("commands: /oma chars | char | tasks | next | scan | done <id> | undo <id> | adddaily <name> | addweekly <name>")
    end
end
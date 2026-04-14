local oma = organiseMyAlts

-- 🔹 Initialise reset tracking
function oma:initialiseResets()
    self.db.resets.daily = self.db.resets.daily or date("%Y-%m-%d")
    self.db.resets.weekly = self.db.resets.weekly or date("%Y-%U")

    self:log(
        "DEBUG",
        string.format(
            "event=resets.initialised daily=%s weekly=%s",
            self.db.resets.daily,
            self.db.resets.weekly
        )
    )
end

-- 🔹 Refresh tasks based on reset changes
function oma:refreshTaskResets()
    local currentDaily = date("%Y-%m-%d")
    local currentWeekly = date("%Y-%U")

    -- 🗓 Daily reset
    if currentDaily ~= self.db.resets.daily then
        self:printSection("daily reset...")
        local resetCount = 0

        for _, task in pairs(self.db.tasks) do
            if task.resetType == "daily" then
                if task.completed then
                    resetCount = resetCount + 1
                end
                task.completed = false
                task.completedAt = nil
            end
        end

        local previousDaily = self.db.resets.daily
        self.db.resets.daily = currentDaily
        self:print("daily tasks reset")
        self:log(
            "INFO",
            string.format(
                "event=tasks.reset period=daily previous=%s current=%s reset_count=%d source=system_rollover",
                previousDaily,
                currentDaily,
                resetCount
            )
        )
    end

    -- 📅 Weekly reset
    if currentWeekly ~= self.db.resets.weekly then
        self:printSection("weekly reset...")
        local resetCount = 0

        for _, task in pairs(self.db.tasks) do
            if task.resetType == "weekly" then
                if task.completed then
                    resetCount = resetCount + 1
                end
                task.completed = false
                task.completedAt = nil
            end
        end

        local previousWeekly = self.db.resets.weekly
        self.db.resets.weekly = currentWeekly
        self:print("weekly tasks reset")
        self:log(
            "INFO",
            string.format(
                "event=tasks.reset period=weekly previous=%s current=%s reset_count=%d source=system_rollover",
                previousWeekly,
                currentWeekly,
                resetCount
            )
        )
    end
end

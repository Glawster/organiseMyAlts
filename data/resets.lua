local oma = organiseMyAlts

-- 🔹 Initialise reset tracking
function oma:initialiseResets()
    self.db.resets.daily = self.db.resets.daily or date("%Y-%m-%d")
    self.db.resets.weekly = self.db.resets.weekly or date("%Y-%U")
end

-- 🔹 Refresh tasks based on reset changes
function oma:refreshTaskResets()
    local currentDaily = date("%Y-%m-%d")
    local currentWeekly = date("%Y-%U")

    -- 🗓 Daily reset
    if currentDaily ~= self.db.resets.daily then
        self:printSection("daily reset...")

        for _, task in pairs(self.db.tasks) do
            if task.resetType == "daily" then
                task.completed = false
                task.completedAt = nil
            end
        end

        self.db.resets.daily = currentDaily
        self:print("daily tasks reset")
    end

    -- 📅 Weekly reset
    if currentWeekly ~= self.db.resets.weekly then
        self:printSection("weekly reset...")

        for _, task in pairs(self.db.tasks) do
            if task.resetType == "weekly" then
                task.completed = false
                task.completedAt = nil
            end
        end

        self.db.resets.weekly = currentWeekly
        self:print("weekly tasks reset")
    end
end
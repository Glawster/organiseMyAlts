local oma = organiseMyAlts

function oma:initialiseResets()
    self.db.resets.daily = self.db.resets.daily or date("%Y-%m-%d")
    self.db.resets.weekly = self.db.resets.weekly or date("%Y-%U")
end

function oma:refreshTaskResets()
    local newDaily = date("%Y-%m-%d")
    local newWeekly = date("%Y-%U")

    if newDaily ~= self.db.resets.daily then
        for _, task in pairs(self.db.tasks) do
            if task.resetType == "daily" then
                task.completed = false
                task.completedAt = nil
            end
        end
        self.db.resets.daily = newDaily
    end

    if newWeekly ~= self.db.resets.weekly then
        for _, task in pairs(self.db.tasks) do
            if task.resetType == "weekly" then
                task.completed = false
                task.completedAt = nil
            end
        end
        self.db.resets.weekly = newWeekly
    end
end
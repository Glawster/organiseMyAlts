local oma = organiseMyAlts

oma.taskTemplates = {

    -- Weekly priorities
    {
        key = "prey_weekly",
        name = "Complete Prey Weekly",
        resetType = "weekly",
        category = "prey",
        priority = "critical",
    },

    {
        key = "delves_weekly",
        name = "Complete Delves (Weekly)",
        resetType = "weekly",
        category = "delves",
        priority = "high",
    },

    -- Daily loop
    {
        key = "delve_daily",
        name = "Run 1 Delve",
        resetType = "daily",
        category = "delves",
        priority = "high",
    },

    {
        key = "crafting_daily",
        name = "Use Crafting Cooldowns",
        resetType = "daily",
        category = "crafting",
        priority = "high",
    },
}
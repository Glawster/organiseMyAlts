local oma = organiseMyAlts

oma.taskTemplates = {

    -- Weekly priorities
    {
        key = "prey_weekly",
        name = "Complete Prey Weekly",
        resetType = "weekly",
        category = "prey",
        priority = "critical",

        -- 👇 NEW
        locationHint = "Silvermoon City -> Astalor's Sanctum",
        pickupHint = "Speak to Magister Astalor Bloodsworn to pick up a Prey target.",
    },

    {
        key = "delves_weekly",
        name = "Complete Delves (Weekly)",
        resetType = "weekly",
        category = "delves",
        priority = "high",

        -- 👇 NEW
        locationHint = "Relevant delve entrance",
        pickupHint = "Pick up the Delver's Call quest from the quest giver or object at the delve entrance.",
    },

    -- Daily loop
    {
        key = "delve_daily",
        name = "Run 1 Delve",
        resetType = "daily",
        category = "delves",
        priority = "high",

        -- 👇 NEW
        locationHint = "Any available delve entrance",
        pickupHint = "If available, pick up the Delver's Call quest at the delve entrance before starting.",
    },

    {
        key = "crafting_daily",
        name = "Use Crafting Cooldowns",
        resetType = "daily",
        category = "crafting",
        priority = "high",

        -- 👇 NEW
        locationHint = "Profession area or crafting hub",
        pickupHint = "No pickup required. Check your profession cooldowns on this character.",
    },
}
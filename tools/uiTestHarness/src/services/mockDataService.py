from models.character import Character


class MockDataService:
    def getCharacters(self):
        return [
            Character("Menion", 70, "Hunter"),
            Character("AltTwo", 70, "Paladin"),
            Character("Crafter", 70, "Mage"),
        ]

    def getWeeklyTasks(self, character):
        return [
            f"Delve ({character.name})",
            "World Boss",
            "Profession Cooldown",
        ]

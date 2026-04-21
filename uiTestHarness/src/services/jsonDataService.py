import json
from pathlib import Path


class JsonDataService:
    def __init__(self, path):
        self.path = Path(path)
        self._data = None

    def load(self):
        with self.path.open(encoding="utf-8") as fileHandle:
            self._data = json.load(fileHandle)

    def getCharacters(self):
        if self._data is None:
            raise RuntimeError("json data has not been loaded")

        return self._data.get("characters", [])

    def getWeeklyTasks(self, character):
        weekly = character.get("weekly", {})
        tasks = []

        if not weekly.get("delve", False):
            tasks.append("Delve")

        if not weekly.get("worldBoss", False):
            tasks.append("World Boss")

        return tasks

    def getCharacterOverviewRows(self):
        characters = self.getCharacters()
        rows = []

        for char in characters:
            ilvl = char.get("ilvl", 0)
            rows.append({
                "name": char.get("name", ""),
                "class": char.get("class", "?"),
                "spec": char.get("spec", "?"),
                "level": char.get("level", 0),
                "ilvl": str(ilvl) if ilvl else "?",
                "scannedSpecs": char.get("scannedSpecs", []),
                "lastScan": char.get("lastScan", "---"),
            })

        return rows

from collections import Counter, defaultdict
from copy import deepcopy

from src.models.keybindFinding import (
    ActualBinding,
    ConsensusEntry,
    KeyFinding,
    PlaystyleProfile,
    SpellClassification,
)


ROLE_ORDER = [
    "assist",
    "rotation",
    "self_heal",
    "offensive",
    "defensive",
    "interrupt",
    "movement",
    "utility",
    "system",
    "neutral",
]

DEFAULT_KEY_ROLES = {
    "1": "assist",
    "2": "self_heal",
    "3": "rotation",
    "4": "rotation",
    "5": "rotation",
    "6": "rotation",
    "Q": "offensive",
    "E": "offensive",
    "R": "offensive",
    "T": "offensive",
    "Y": "offensive",
    "U": "offensive",
    "F1": "rotation",
    "F2": "rotation",
    "F3": "interrupt",
    "F5": "defensive",
    "F6": "defensive",
    "F7": "defensive",
    "F8": "movement",
    "`": "utility",
    "H": "system",
    "J": "system",
    "K": "system",
    "L": "system",
}

STRAFE_MODE_PROFILE = PlaystyleProfile(
    name="Strafe Mode",
    reachableKeys=("1", "2", "3", "4", "F1", "F2"),
    rolePreferences={
        "assist": ("1",),
        "self_heal": ("2",),
        "rotation": ("3", "4", "F1", "F2"),
        "interrupt": ("F3",),
        "defensive": ("F5", "F6", "F7"),
        "movement": ("F8",),
        "utility": ("`",),
    },
    reservedKeys=("H", "J", "K", "L"),
)

DEFAULT_BINDINGS = [
    ActualBinding("Menion", "HUNTER", "Marksmanship", "1", "Assist", None, "assist"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "2", "Steady Shot", 56641, "rotation"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "3", "Arcane Shot", 185358, "rotation"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "4", "Aimed Shot", 19434, "rotation"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "5", "Rapid Fire", 257044, "rotation"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "6", "Kill Shot", 53351, "rotation"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "Q", "Trueshot", 288613, "offensive"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "E", "Explosive Shot", 212431, "offensive"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "R", "Volley", 260243, "offensive"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "T", "Salvo", 400456, "offensive"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "Y", "Wailing Arrow", 392060, "offensive"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "U", "Barrage", 120360, "offensive"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "F3", "Counter Shot", 147362, "interrupt"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "F5", "Exhilaration", 109304, "defensive"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "F6", "Fortitude of the Bear", 388035, "defensive"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "F7", "Aspect of the Turtle", 186265, "defensive"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "F8", "Aspect of the Cheetah", 186257, "movement"),
    ActualBinding("Menion", "HUNTER", "Marksmanship", "`", "Hunter's Mark", 257284, "utility"),
    ActualBinding("Crafter", "MAGE", "Arcane", "1", "Assist", None, "assist"),
    ActualBinding("Crafter", "MAGE", "Arcane", "2", "Arcane Blast", 30451, "rotation"),
    ActualBinding("Crafter", "MAGE", "Arcane", "3", "Arcane Missiles", 5143, "rotation"),
    ActualBinding("Crafter", "MAGE", "Arcane", "4", "Arcane Barrage", 44425, "rotation"),
    ActualBinding("Crafter", "MAGE", "Arcane", "5", "Nether Tempest", 114923, "rotation"),
    ActualBinding("Crafter", "MAGE", "Arcane", "6", "Arcane Orb", 153626, "rotation"),
    ActualBinding("Crafter", "MAGE", "Arcane", "Q", "Touch of the Magi", 321507, "offensive"),
    ActualBinding("Crafter", "MAGE", "Arcane", "E", "Radiant Spark", 307443, "offensive"),
    ActualBinding("Crafter", "MAGE", "Arcane", "R", "Arcane Surge", 365350, "offensive"),
    ActualBinding("Crafter", "MAGE", "Arcane", "T", "Presence of Mind", 205025, "offensive"),
    ActualBinding("Crafter", "MAGE", "Arcane", "Y", "Shifting Power", 382440, "offensive"),
    ActualBinding("Crafter", "MAGE", "Arcane", "U", "Time Warp", 80353, "offensive"),
    ActualBinding("Crafter", "MAGE", "Arcane", "F3", "Counterspell", 2139, "interrupt"),
    ActualBinding("Crafter", "MAGE", "Arcane", "F5", "Prismatic Barrier", 235450, "defensive"),
    ActualBinding("Crafter", "MAGE", "Arcane", "F6", "Mirror Image", 55342, "defensive"),
    ActualBinding("Crafter", "MAGE", "Arcane", "F7", "Ice Block", 45438, "defensive"),
    ActualBinding("Crafter", "MAGE", "Arcane", "F8", "Blink", 1953, "movement"),
    ActualBinding("Crafter", "MAGE", "Arcane", "`", "Spellsteal", 30449, "utility"),
    ActualBinding("Thane", "DEATHKNIGHT", "Blood", "1", "Assist", None, "assist"),
    ActualBinding("Thane", "DEATHKNIGHT", "Blood", "2", "Death Strike", 49998, "self_heal"),
    ActualBinding("Thane", "DEATHKNIGHT", "Frost", "2", "Death Strike", 49998, "self_heal"),
    ActualBinding("Thane", "DEATHKNIGHT", "Unholy", "2", "Death Strike", 49998, "self_heal"),
]


class KeybindFindingsService:
    def __init__(self, preferredRoles=None, bindings=None, playstyleProfile=None):
        self.preferredRoles = dict(preferredRoles or DEFAULT_KEY_ROLES)
        self.bindings = list(bindings or DEFAULT_BINDINGS)
        self.playstyleProfile = playstyleProfile or STRAFE_MODE_PROFILE
        self.classifications = self._buildClassifications()

    def getPreferredRoles(self):
        return self.preferredRoles.copy()

    def getRoleOrder(self):
        return list(ROLE_ORDER)

    def getCharacters(self):
        seen = set()
        characters = []
        for binding in self.bindings:
            key = (binding.characterName, binding.specName)
            if key in seen:
                continue
            seen.add(key)
            existing = next((item for item in characters if item["name"] == binding.characterName), None)
            if existing is None:
                characters.append({
                    "name": binding.characterName,
                    "class": binding.className,
                    "spec": binding.specName,
                    "scannedSpecs": [binding.specName],
                })
            elif binding.specName not in existing["scannedSpecs"]:
                existing["scannedSpecs"].append(binding.specName)
        return characters

    def getSpellLayout(self, characterName, specName):
        return {
            binding.key: binding.spellName
            for binding in self.bindings
            if binding.characterName == characterName and binding.specName == specName
        }

    def setSpellName(self, characterName, specName, key, spellName):
        retained = [
            binding
            for binding in self.bindings
            if not (
                binding.characterName == characterName
                and binding.specName == specName
                and binding.key == key
            )
        ]
        if spellName:
            retained.append(ActualBinding(characterName, "UNKNOWN", specName, key, spellName))
        self.bindings = retained

    def getFindings(self, characterName, specName, allKeys):
        bindingsByKey = {
            binding.key: binding
            for binding in self.bindings
            if binding.characterName == characterName and binding.specName == specName
        }
        spellConsensus = self.buildSpellConsensus()
        findings = {}

        for key in allKeys:
            role = self.preferredRoles.get(key, "neutral")
            binding = bindingsByKey.get(key)
            if binding is None:
                findings[key] = KeyFinding(key=key, role=role)
                continue

            classification = self._classify(binding)
            consensus = spellConsensus.get(binding.spellName)
            status = self._getStatus(key, role, classification.category)
            findings[key] = KeyFinding(
                key=key,
                role=role,
                spellName=binding.spellName,
                spellId=binding.spellId,
                spellCategory=classification.category,
                status=status,
                classificationSource=classification.source,
                consensusKey=consensus.consensusKey if consensus else None,
                consensusConfidence=consensus.confidence if consensus else 0.0,
            )

        return findings

    def buildSpellConsensus(self):
        votes = defaultdict(Counter)
        for binding in self.bindings:
            if binding.spellName:
                votes[binding.spellName][binding.key] += 1
        return self._buildConsensusEntries(votes)

    def buildCategoryConsensus(self):
        votes = defaultdict(Counter)
        for binding in self.bindings:
            category = self._classify(binding).category
            if category:
                votes[category][binding.key] += 1
        return self._buildConsensusEntries(votes)

    def _buildClassifications(self):
        classifications = {}
        for binding in self.bindings:
            if binding.spellId is not None and binding.category:
                classifications[binding.spellId] = SpellClassification(binding.category, "fixture")
        return classifications

    def _classify(self, binding):
        if binding.spellId in self.classifications:
            return self.classifications[binding.spellId]
        if binding.category:
            return SpellClassification(binding.category, "binding")
        return SpellClassification("unknown", "unknown", 0.0)

    def _getStatus(self, key, role, category):
        if role == "system":
            return "reserved_conflict" if category and category != "system" else "system"
        if not category or category == "unknown":
            return "unknown"
        if role == category:
            return "match"
        if role == "rotation" and category in {"assist", "rotation"}:
            return "match"
        return "mismatch"

    def _buildConsensusEntries(self, votesBySubject):
        entries = {}
        for subject, keyVotes in votesBySubject.items():
            total = sum(keyVotes.values())
            consensusKey, winningVotes = self._getWinningKey(keyVotes)
            entries[subject] = ConsensusEntry(
                subject=subject,
                keyVotes=dict(keyVotes),
                consensusKey=consensusKey,
                confidence=winningVotes / total if total else 0.0,
                totalVotes=total,
            )
        return entries

    def _getWinningKey(self, keyVotes):
        if not keyVotes:
            return None, 0
        rankedKeys = {
            key: index
            for index, key in enumerate(self.playstyleProfile.reachableKeys)
        }
        return max(
            keyVotes.items(),
            key=lambda item: (item[1], -rankedKeys.get(item[0], 999), item[0]),
        )

    def cloneBindings(self):
        return deepcopy(self.bindings)

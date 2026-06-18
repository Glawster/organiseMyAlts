from dataclasses import dataclass, field


@dataclass(frozen=True)
class ActualBinding:
    characterName: str
    className: str
    specName: str
    key: str
    spellName: str
    spellId: int | None = None
    category: str | None = None


@dataclass(frozen=True)
class SpellClassification:
    category: str
    source: str = "manual"
    confidence: float = 1.0


@dataclass(frozen=True)
class KeyFinding:
    key: str
    role: str
    spellName: str = ""
    spellId: int | None = None
    spellCategory: str | None = None
    status: str = "empty"
    classificationSource: str = "none"
    consensusKey: str | None = None
    consensusConfidence: float = 0.0


@dataclass(frozen=True)
class ConsensusEntry:
    subject: str
    keyVotes: dict[str, int] = field(default_factory=dict)
    consensusKey: str | None = None
    confidence: float = 0.0
    totalVotes: int = 0


@dataclass(frozen=True)
class PlaystyleProfile:
    name: str
    reachableKeys: tuple[str, ...]
    rolePreferences: dict[str, tuple[str, ...]]
    reservedKeys: tuple[str, ...] = ()

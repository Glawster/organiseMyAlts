from src.services.keybindFindingsService import KeybindFindingsService


def testSpellConsensusLearnsDeathStrikeOnTwo():
    service = KeybindFindingsService()

    consensus = service.buildSpellConsensus()["Death Strike"]

    assert consensus.consensusKey == "2"
    assert consensus.confidence == 1.0
    assert consensus.totalVotes == 3


def testCategoryConsensusLearnsSelfHealOnTwo():
    service = KeybindFindingsService()

    consensus = service.buildCategoryConsensus()["self_heal"]

    assert consensus.consensusKey == "2"
    assert consensus.confidence == 1.0


def testFindingsCompareActualBindingAgainstPreferredRole():
    service = KeybindFindingsService()

    findings = service.getFindings("Thane", "Blood", ["1", "2", "3"])

    assert findings["1"].role == "assist"
    assert findings["1"].status == "match"
    assert findings["2"].role == "self_heal"
    assert findings["2"].spellName == "Death Strike"
    assert findings["2"].status == "match"
    assert findings["2"].consensusKey == "2"
    assert findings["3"].status == "empty"


def testFindingsMarkRoleMismatch():
    service = KeybindFindingsService(preferredRoles={"2": "defensive"})

    findings = service.getFindings("Thane", "Blood", ["2"])

    assert findings["2"].spellName == "Death Strike"
    assert findings["2"].spellCategory == "self_heal"
    assert findings["2"].status == "mismatch"

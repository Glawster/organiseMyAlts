from src.mainWindow import MainWindow
from src.widgets.characterOverviewPanel import CLASS_SPECS, COLUMNS, CharacterOverviewPanel


# ---------------------------------------------------------------------------
# Column structure
# ---------------------------------------------------------------------------

def testCharacterOverviewPanelHasCorrectColumns(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    assert panel.columnCount() == len(COLUMNS)
    for col, label in enumerate(COLUMNS):
        assert panel.horizontalHeaderItem(col).text() == label


# ---------------------------------------------------------------------------
# Loading rows
# ---------------------------------------------------------------------------

def testCharacterOverviewPanelShowsAllCharacters(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    rows = [
        {"name": "Alpha", "class": "WARRIOR", "spec": "Arms", "level": 80, "ilvl": "635",
         "scannedSpecs": ["Arms", "Fury"], "lastScan": "04-18 08:51"},
        {"name": "Beta",  "class": "PRIEST",  "spec": "Holy",  "level": 75, "ilvl": "610",
         "scannedSpecs": [], "lastScan": "---"},
    ]
    panel.loadRows(rows)

    assert panel.rowCount() == 2


def testCharacterOverviewPanelCharacterNameColumn(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Menion", "class": "HUNTER", "spec": "Marksmanship", "level": 70,
         "ilvl": "625", "scannedSpecs": ["Marksmanship"], "lastScan": "04-17 21:10"},
    ])

    assert panel.item(0, 0).text() == "Menion"


def testCharacterOverviewPanelClassColumn(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Menion", "class": "HUNTER", "spec": "Marksmanship", "level": 70,
         "ilvl": "625", "scannedSpecs": ["Marksmanship"], "lastScan": "04-17 21:10"},
    ])

    assert panel.item(0, 1).text() == "HUNTER"


def testCharacterOverviewPanelSpecColumn(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Menion", "class": "HUNTER", "spec": "Marksmanship", "level": 70,
         "ilvl": "625", "scannedSpecs": ["Marksmanship"], "lastScan": "04-17 21:10"},
    ])

    assert panel.item(0, 2).text() == "Marksmanship"


def testCharacterOverviewPanelLevelColumn(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Menion", "class": "HUNTER", "spec": "Marksmanship", "level": 70,
         "ilvl": "625", "scannedSpecs": ["Marksmanship"], "lastScan": "04-17 21:10"},
    ])

    assert panel.item(0, 3).text() == "70"


def testCharacterOverviewPanelIlvlColumn(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Menion", "class": "HUNTER", "spec": "Marksmanship", "level": 70,
         "ilvl": "625", "scannedSpecs": ["Marksmanship"], "lastScan": "04-17 21:10"},
    ])

    assert panel.item(0, 4).text() == "625"


def testCharacterOverviewPanelKbSpecsPartiallyScanned(qtbot):
    """Hunter with only Marksmanship scanned shows +Mar alongside -Bea and -Sur."""
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Menion", "class": "HUNTER", "spec": "Marksmanship", "level": 70,
         "ilvl": "625", "scannedSpecs": ["Marksmanship"], "lastScan": "04-17 21:10"},
    ])

    assert panel.item(0, 5).text() == "-Bea +Mar -Sur"


def testCharacterOverviewPanelKbSpecsNoneScanned(qtbot):
    """Mage with no specs scanned shows all specs prefixed with '-'."""
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Crafter", "class": "MAGE", "spec": "Arcane", "level": 70,
         "ilvl": "598", "scannedSpecs": [], "lastScan": "04-16 23:03"},
    ])

    assert panel.item(0, 5).text() == "-Arc -Fir -Fro"


def testCharacterOverviewPanelKbSpecsAllScanned(qtbot):
    """Paladin with all specs scanned shows all specs prefixed with '+'."""
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Tanker", "class": "PALADIN", "spec": "Protection", "level": 80,
         "ilvl": "640", "scannedSpecs": ["Holy", "Protection", "Retribution"],
         "lastScan": "04-18 10:00"},
    ])

    assert panel.item(0, 5).text() == "+Hol +Pro +Ret"


def testCharacterOverviewPanelKbSpecsUnknownClass(qtbot):
    """A row with an unrecognised class shows '[?]' in the KB Specs column."""
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Ghost", "class": "UNKNOWN", "spec": "?", "level": 1,
         "ilvl": "?", "scannedSpecs": [], "lastScan": "---"},
    ])

    assert panel.item(0, 5).text() == "[?]"


def testCharacterOverviewPanelLastScanColumn(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Menion", "class": "HUNTER", "spec": "Marksmanship", "level": 70,
         "ilvl": "625", "scannedSpecs": ["Marksmanship"], "lastScan": "04-17 21:10"},
    ])

    assert panel.item(0, 6).text() == "04-17 21:10"


def testCharacterOverviewPanelEmptyLastScanShowsDash(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "NewChar", "class": "ROGUE", "spec": "?", "level": 60,
         "ilvl": "?", "scannedSpecs": []},
    ])

    assert panel.item(0, 6).text() == "---"


def testCharacterOverviewPanelClearsOnReload(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([{"name": "A", "class": "WARRIOR", "spec": "Arms", "level": 80,
                     "ilvl": "600", "scannedSpecs": ["Arms"], "lastScan": "04-18"}])
    panel.loadRows([])

    assert panel.rowCount() == 0


def testCharacterOverviewPanelClassSpecsTableCoversAllKnownClasses(qtbot):
    """CLASS_SPECS must contain at least 13 WoW retail classes."""
    assert len(CLASS_SPECS) >= 13


# ---------------------------------------------------------------------------
# Integration via MainWindow
# ---------------------------------------------------------------------------

def testMainWindowContainsCharacterOverviewPanel(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    assert hasattr(window, "characterOverviewPanel")


def testCharacterOverviewPanelLoadedFromFixture(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    panel = window.characterOverviewPanel
    assert panel.rowCount() == 2


def testCharacterOverviewPanelFixtureFirstRowName(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    panel = window.characterOverviewPanel
    assert panel.item(0, 0).text() == "Menion"


def testCharacterOverviewPanelFixtureSecondRowName(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    panel = window.characterOverviewPanel
    assert panel.item(1, 0).text() == "Crafter"


def testCharacterOverviewPanelFixtureMenionKbSpecs(qtbot):
    """Menion (HUNTER, only Marksmanship scanned) shows correct spec badges."""
    window = MainWindow()
    qtbot.addWidget(window)

    panel = window.characterOverviewPanel
    assert panel.item(0, 5).text() == "-Bea +Mar -Sur"


def testCharacterOverviewPanelFixtureCrafterKbSpecs(qtbot):
    """Crafter (MAGE, no specs scanned) shows all specs as missing."""
    window = MainWindow()
    qtbot.addWidget(window)

    panel = window.characterOverviewPanel
    assert panel.item(1, 5).text() == "-Arc -Fir -Fro"

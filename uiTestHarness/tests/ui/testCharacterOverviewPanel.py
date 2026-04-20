from src.mainWindow import MainWindow
from src.widgets.characterOverviewPanel import COLUMNS, CharacterOverviewPanel


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
        {"name": "Alpha", "class": "WARRIOR", "spec": "Arms", "level": 80, "ilvl": "635", "keybindScanned": True, "lastScan": "04-18 08:51"},
        {"name": "Beta",  "class": "PRIEST",  "spec": "Holy",  "level": 75, "ilvl": "610", "keybindScanned": False, "lastScan": "---"},
    ]
    panel.loadRows(rows)

    assert panel.rowCount() == 2


def testCharacterOverviewPanelCharacterNameColumn(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Menion", "class": "HUNTER", "spec": "Marksmanship", "level": 70, "ilvl": "625", "keybindScanned": True, "lastScan": "04-17 21:10"},
    ])

    assert panel.item(0, 0).text() == "Menion"


def testCharacterOverviewPanelClassColumn(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Menion", "class": "HUNTER", "spec": "Marksmanship", "level": 70, "ilvl": "625", "keybindScanned": True, "lastScan": "04-17 21:10"},
    ])

    assert panel.item(0, 1).text() == "HUNTER"


def testCharacterOverviewPanelSpecColumn(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Menion", "class": "HUNTER", "spec": "Marksmanship", "level": 70, "ilvl": "625", "keybindScanned": True, "lastScan": "04-17 21:10"},
    ])

    assert panel.item(0, 2).text() == "Marksmanship"


def testCharacterOverviewPanelLevelColumn(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Menion", "class": "HUNTER", "spec": "Marksmanship", "level": 70, "ilvl": "625", "keybindScanned": True, "lastScan": "04-17 21:10"},
    ])

    assert panel.item(0, 3).text() == "70"


def testCharacterOverviewPanelIlvlColumn(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Menion", "class": "HUNTER", "spec": "Marksmanship", "level": 70, "ilvl": "625", "keybindScanned": True, "lastScan": "04-17 21:10"},
    ])

    assert panel.item(0, 4).text() == "625"


def testCharacterOverviewPanelKeybindScannedYes(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Menion", "class": "HUNTER", "spec": "Marksmanship", "level": 70, "ilvl": "625", "keybindScanned": True, "lastScan": "04-17 21:10"},
    ])

    assert panel.item(0, 5).text() == "YES"


def testCharacterOverviewPanelKeybindScannedNo(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Crafter", "class": "MAGE", "spec": "Arcane", "level": 70, "ilvl": "598", "keybindScanned": False, "lastScan": "04-16 23:03"},
    ])

    assert panel.item(0, 5).text() == "NO"


def testCharacterOverviewPanelLastScanColumn(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "Menion", "class": "HUNTER", "spec": "Marksmanship", "level": 70, "ilvl": "625", "keybindScanned": True, "lastScan": "04-17 21:10"},
    ])

    assert panel.item(0, 6).text() == "04-17 21:10"


def testCharacterOverviewPanelEmptyLastScanShowsDash(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([
        {"name": "NewChar", "class": "ROGUE", "spec": "?", "level": 60, "ilvl": "?", "keybindScanned": False},
    ])

    assert panel.item(0, 6).text() == "---"


def testCharacterOverviewPanelClearsOnReload(qtbot):
    panel = CharacterOverviewPanel()
    qtbot.addWidget(panel)

    panel.loadRows([{"name": "A", "class": "WARRIOR", "spec": "Arms", "level": 80, "ilvl": "600", "keybindScanned": True, "lastScan": "04-18"}])
    panel.loadRows([])

    assert panel.rowCount() == 0


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


def testCharacterOverviewPanelFixtureMenionKeybindScanned(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    panel = window.characterOverviewPanel
    # Menion has keybindScanned = true in fixture
    assert panel.item(0, 5).text() == "YES"


def testCharacterOverviewPanelFixtureCrafterKeybindNotScanned(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    panel = window.characterOverviewPanel
    # Crafter has keybindScanned = false in fixture
    assert panel.item(1, 5).text() == "NO"

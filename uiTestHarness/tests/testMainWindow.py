from src.mainWindow import MainWindow


def testMainWindowLoads(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    window.show()

    assert window.windowTitle() == "OrganiseMyAlts UI Test Harness"


def testCharacterListLoadsFixtureData(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.characterList.count() == 2
    assert window.characterList.item(0).text() == "Menion"
    assert window.characterList.item(1).text() == "Crafter"



def testMainWindowHasShowFindingsButton(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.showFindingsButton.text() == "Show Findings"


def testShowFindingsButtonOpensFindingsWindow(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    window.showFindingsButton.click()

    assert window.findingsWindow is not None
    assert window.findingsWindow.isVisible()
    assert window.findingsWindow.windowTitle() == "OrganiseMyAlts Findings"

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


def testMainWindowHasExitButton(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.exitButton.text() == "Exit"


def testShowFindingsHidesMainWindow(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    window.showFindingsButton.click()

    assert not window.isVisible()
    assert window.findingsWindow is not None
    assert window.findingsWindow.isVisible()


def testClosingFindingsRestoresMainWindow(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    window.showFindingsButton.click()
    window.findingsWindow.close()

    assert window.isVisible()
    assert not window.findingsWindow.isVisible()


def testMainWindowStartsWideEnough(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.minimumWidth() >= 1480
    assert window.minimumHeight() >= 900

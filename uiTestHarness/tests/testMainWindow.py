from src.mainWindow import MainWindow

def testMainWindowLoads(qtbot):

    window = MainWindow()
    qtbot.addWidget(window)

    window.show()

    assert window.windowTitle() == "OrganiseMyAlts UI Test Harness"
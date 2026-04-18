def testMainWindowLoads(qtbot):
    from src.mainWindow import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)

    window.show()

    assert window.windowTitle() == "OrganiseMyAlts UI Test Harness"

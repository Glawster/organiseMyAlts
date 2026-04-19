def testMainWindowLoads(qtbot):
    from uiTestHarness.src.mainWindow import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)

    window.show()

    assert window.windowTitle() == "OrganiseMyAlts UI Test Harness"
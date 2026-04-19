def testSelectingCharacterUpdatesTasks(qtbot):
    from uiTestHarness.src.mainWindow import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)

    window.show()

    window.characterList.setCurrentRow(0)

    qtbot.waitUntil(
        lambda: "Menion" in window.weeklyPanel.tasksLabel.text()
    )

    assert "Delve (Menion)" in window.weeklyPanel.tasksLabel.text()
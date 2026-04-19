def testSelectingCharacterUpdatesTasks(qtbot):
    from src.mainWindow import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)

    window.show()

    window.characterList.setCurrentRow(0)

    qtbot.waitUntil(
        lambda: "Delve" in window.weeklyPanel.tasksLabel.text()
    )

    assert "Delve" in window.weeklyPanel.tasksLabel.text()
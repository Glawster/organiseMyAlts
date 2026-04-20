from src.mainWindow import MainWindow


def testSelectingCharacterUpdatesTasks(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    window.show()
    window.characterList.setCurrentRow(0)

    qtbot.waitUntil(lambda: "Delve" in window.weeklyPanel.tasksLabel.text())

    assert "Delve" in window.weeklyPanel.tasksLabel.text()
    assert "World Boss" not in window.weeklyPanel.tasksLabel.text()


def testSelectingSecondCharacterShowsWorldBoss(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    window.show()
    window.characterList.setCurrentRow(1)

    qtbot.waitUntil(lambda: "World Boss" in window.weeklyPanel.tasksLabel.text())

    assert "World Boss" in window.weeklyPanel.tasksLabel.text()
    assert "Delve" not in window.weeklyPanel.tasksLabel.text()

from src.widgets.findingsWindow import FindingsWindow


def testFindingsWindowContainsKeyboardDiagram(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    assert window.keyboardDiagram.objectName() == "keyboardDiagram"


def testKeyboardDiagramShowsPreferredRotationKeys(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    for keyName in ["2", "3", "4", "5", "6"]:
        assert keyName in window.keyboardDiagram.keyCaps
        assert window.keyboardDiagram.keyCaps[keyName].roleLabel.text() == "Rotation"


def testKeyboardDiagramShowsInterruptDefensiveAndMovementKeys(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    assert window.keyboardDiagram.keyCaps["F3"].roleLabel.text() == "Interrupt"
    assert window.keyboardDiagram.keyCaps["F5"].roleLabel.text() == "Defensive"
    assert window.keyboardDiagram.keyCaps["F8"].roleLabel.text() == "Movement"


def testKeyboardDiagramShowsFullRowsIncludingEmptyKeys(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    for keyName in ["F1", "F12", "`", "=", "Q", "P", "A", "L", "\\", "Z", "/", "SPACE"]:
        assert keyName in window.keyboardDiagram.keyCaps

    assert window.keyboardDiagram.keyCaps["1"].roleLabel.text() == ""
    assert window.keyboardDiagram.keyCaps["SPACE"].roleLabel.text() == ""


def testKeyboardDiagramMarksWowOperationKeysAsSystem(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    for keyName in ["H", "J", "K", "L"]:
        assert window.keyboardDiagram.keyCaps[keyName].roleLabel.text() == "System"


def testKeyboardDiagramCanReassignKeyRole(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    assert window.keyboardDiagram.getKeyRole("`") == "utility"

    window.keyboardDiagram.setKeyRole("`", "rotation")

    assert window.keyboardDiagram.getKeyRole("`") == "rotation"
    assert window.keyboardDiagram.keyCaps["`"].roleLabel.text() == "Rotation"


def testKeyboardDiagramCanResetToDefaults(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    window.keyboardDiagram.setKeyRole("`", "rotation")
    window.keyboardDiagram.resetToDefaults()

    assert window.keyboardDiagram.getKeyRole("`") == "utility"
    assert window.keyboardDiagram.keyCaps["`"].roleLabel.text() == "Utility"


def testFindingsWindowCallsCloseCallback(qtbot):
    called = {"value": False}

    def onClose():
        called["value"] = True

    window = FindingsWindow(onCloseCallback=onClose)
    qtbot.addWidget(window)
    window.show()
    window.close()

    assert called["value"] is True


def testKeyboardDiagramUsesTrueSpacersForAlignment(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    assert "\\" in window.keyboardDiagram.keyCaps

    functionSpacer = window.keyboardDiagram.grid.itemAtPosition(0, 0).widget()
    qRowSpacer = window.keyboardDiagram.grid.itemAtPosition(2, 0).widget()
    aRowSpacer = window.keyboardDiagram.grid.itemAtPosition(3, 0).widget()

    assert functionSpacer.objectName() == "spacer_0_0"
    assert qRowSpacer.objectName() == "spacer_2_0"
    assert aRowSpacer.objectName() == "spacer_3_0"

    assert window.keyboardDiagram.grid.itemAtPosition(4, 0).widget() is window.keyboardDiagram.keyCaps["\\"]
    assert window.keyboardDiagram.grid.itemAtPosition(0, 1).widget() is window.keyboardDiagram.keyCaps["F1"]
    assert window.keyboardDiagram.grid.itemAtPosition(1, 1).widget() is window.keyboardDiagram.keyCaps["1"]
    assert window.keyboardDiagram.grid.itemAtPosition(2, 1).widget() is window.keyboardDiagram.keyCaps["Q"]
    assert window.keyboardDiagram.grid.itemAtPosition(3, 1).widget() is window.keyboardDiagram.keyCaps["A"]
    assert window.keyboardDiagram.grid.itemAtPosition(4, 1).widget() is window.keyboardDiagram.keyCaps["Z"]


def testFindingsWindowStartsWideEnough(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    assert window.minimumWidth() >= 1360
    assert window.minimumHeight() >= 760


def testSpacebarSpansFiveKeyboardColumns(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    spaceItem = window.keyboardDiagram.grid.itemAtPosition(5, 2)

    assert spaceItem.widget() is window.keyboardDiagram.keyCaps["SPACE"]
    assert spaceItem.columnSpan() == 5

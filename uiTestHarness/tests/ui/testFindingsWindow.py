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

    for keyName in ["F1", "F12", "`", "=", "Q", "P", "A", "L", "Z", "/", "SPACE"]:
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

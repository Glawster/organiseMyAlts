from PySide6.QtCore import Qt

from src.widgets.findingsWindow import FindingsWindow, formatSpellDisplay


def testFindingsWindowContainsKeyboardDiagram(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    assert window.keyboardDiagram.objectName() == "keyboardDiagram"


def testFindingsWindowContainsDropdownPanel(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    assert window.characterDropdown.count() >= 2
    assert window.specDropdown.count() >= 1
    assert window.spellNameEdit.objectName() == "spellNameEdit"


def testKeyboardDiagramShowsStrafeModeCoreKeys(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    assert window.keyboardDiagram.getKeyRole("1") == "assist"
    assert window.keyboardDiagram.getKeyRole("2") == "self_heal"

    for keyName in ["3", "4", "5", "6", "F1", "F2"]:
        assert keyName in window.keyboardDiagram.keyCaps
        assert window.keyboardDiagram.getKeyRole(keyName) == "rotation"


def testKeyboardDiagramShowsInterruptDefensiveAndMovementKeys(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    assert window.keyboardDiagram.getKeyRole("F3") == "interrupt"
    assert window.keyboardDiagram.getKeyRole("F5") == "defensive"
    assert window.keyboardDiagram.getKeyRole("F8") == "movement"


def testKeyboardDiagramShowsFullRowsIncludingEmptyKeys(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    for keyName in ["F1", "F12", "`", "=", "Q", "P", "A", "L", "\\", "Z", "/", "SPACE"]:
        assert keyName in window.keyboardDiagram.keyCaps

    assert window.keyboardDiagram.getKeyRole("SPACE") == "neutral"


def testKeyboardDiagramMarksWowOperationKeysAsSystem(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    for keyName in ["H", "J", "K", "L"]:
        assert window.keyboardDiagram.getKeyRole(keyName) == "system"


def testFindingsWindowLoadsSpellNamesFromDropdownSelection(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    assert window.characterDropdown.currentText() == "Menion"
    assert window.specDropdown.currentText() == "Marksmanship"
    assert window.keyboardDiagram.keyCaps["2"].fullSpellName == "Steady Shot"
    assert window.keyboardDiagram.keyCaps["F3"].fullSpellName == "Counter Shot"

    window.characterDropdown.setCurrentText("Crafter")

    assert window.specDropdown.currentText() == "Arcane"
    assert window.keyboardDiagram.keyCaps["2"].fullSpellName == "Arcane Blast"
    assert window.keyboardDiagram.keyCaps["F3"].fullSpellName == "Counterspell"


def testKeyboardDiagramCanReassignKeyRole(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    assert window.keyboardDiagram.getKeyRole("`") == "utility"

    window.keyboardDiagram.setKeyRole("`", "rotation")

    assert window.keyboardDiagram.getKeyRole("`") == "rotation"
    assert window.keyboardDiagram.getKeyRole("`") == "rotation"


def testKeyboardDiagramCanResetToDefaults(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    window.keyboardDiagram.setKeyRole("`", "rotation")
    window.keyboardDiagram.resetToDefaults()

    assert window.keyboardDiagram.getKeyRole("`") == "utility"
    assert window.keyboardDiagram.getKeyRole("`") == "utility"


def testFindingsWindowCanTypeSpellNameForSelectedKey(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    window.keyboardDiagram.setSelectedKey("Q")
    window.spellNameEdit.setText("Rapid Fire")
    window.saveSpellButton.click()

    assert window.selectedKeyValue.text() == "Q"
    assert window.keyboardDiagram.keyCaps["Q"].fullSpellName == "Rapid Fire"


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

    assert window.minimumWidth() >= 1500
    assert window.minimumHeight() >= 860


def testSpacebarSpansFiveKeyboardColumns(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    spaceItem = window.keyboardDiagram.grid.itemAtPosition(5, 2)

    assert spaceItem.widget() is window.keyboardDiagram.keyCaps["SPACE"]
    itemIndex = window.keyboardDiagram.grid.indexOf(window.keyboardDiagram.keyCaps["SPACE"])
    row, column, rowSpan, columnSpan = window.keyboardDiagram.grid.getItemPosition(itemIndex)
    assert (row, column, rowSpan, columnSpan) == (5, 2, 1, 5)


def testSpellDisplayFormattingWrapsLongNames():
    displayText = formatSpellDisplay("Fortitude of the Bear")

    assert "\n" in displayText or "…" in displayText
    assert len(displayText.splitlines()) <= 2


def testDoubleClickStartsInlineEditAndSavesSpellName(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)
    window.show()

    keyCap = window.keyboardDiagram.keyCaps["Q"]
    qtbot.mouseDClick(keyCap, Qt.MouseButton.LeftButton)

    assert keyCap.spellEdit.isVisible() is True

    keyCap.spellEdit.setText("A Very Long Offensive Cooldown")
    qtbot.keyClick(keyCap.spellEdit, Qt.Key.Key_Return)

    assert keyCap.spellEdit.isVisible() is False
    assert keyCap.fullSpellName == "A Very Long Offensive Cooldown"
    assert window.spellNameEdit.text() == "A Very Long Offensive Cooldown"
    assert len(keyCap.spellLabel.text().splitlines()) <= 2


def testSelectedKeyCanStartInlineEditWithEnter(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)
    window.show()

    keyCap = window.keyboardDiagram.keyCaps["2"]
    window.keyboardDiagram.setSelectedKey("2")
    keyCap.setFocus()
    qtbot.keyClick(keyCap, Qt.Key.Key_Return)

    assert keyCap.spellEdit.isVisible() is True


def testEscapeCancelsInlineEdit(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    keyCap = window.keyboardDiagram.keyCaps["E"]
    originalName = keyCap.fullSpellName
    keyCap.startInlineEdit()
    keyCap.spellEdit.setText("Changed Name")
    qtbot.keyClick(keyCap.spellEdit, Qt.Key.Key_Escape)

    assert keyCap.spellEdit.isVisible() is False
    assert keyCap.fullSpellName == originalName


def testKeyCapsDoNotShowRoleText(qtbot):
    window = FindingsWindow()
    qtbot.addWidget(window)

    keyCap = window.keyboardDiagram.keyCaps["Q"]

    assert keyCap.findChild(object, "roleLabel") is None


def testSpellDisplayFormattingKeepsTwoLinesClean():
    displayText = formatSpellDisplay("Aspect of the Cheetah")

    assert len(displayText.splitlines()) <= 2
    assert displayText == "Aspect\nCheetah"

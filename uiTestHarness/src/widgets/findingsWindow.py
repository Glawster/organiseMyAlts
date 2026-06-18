from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtGui import QCloseEvent, QKeyEvent, QMouseEvent
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.services.keybindFindingsService import (
    DEFAULT_KEY_ROLES,
    KeybindFindingsService,
    ROLE_ORDER,
)


SPACER = None
KEY_UNIT_WIDTH = 72
KEY_HEIGHT = 80

KEY_ROWS = [
    [(SPACER, 1), ("F1", 1), ("F2", 1), ("F3", 1), ("F4", 1), ("F5", 1), ("F6", 1), ("F7", 1), ("F8", 1), ("F9", 1), ("F10", 1), ("F11", 1), ("F12", 1)],
    [("`", 1), ("1", 1), ("2", 1), ("3", 1), ("4", 1), ("5", 1), ("6", 1), ("7", 1), ("8", 1), ("9", 1), ("0", 1), ("-", 1), ("=", 1)],
    [(SPACER, 1), ("Q", 1), ("W", 1), ("E", 1), ("R", 1), ("T", 1), ("Y", 1), ("U", 1), ("I", 1), ("O", 1), ("P", 1), ("[", 1), ("]", 1)],
    [(SPACER, 1), ("A", 1), ("S", 1), ("D", 1), ("F", 1), ("G", 1), ("H", 1), ("J", 1), ("K", 1), ("L", 1), (";", 1), ("'", 1)],
    [("\\", 1), ("Z", 1), ("X", 1), ("C", 1), ("V", 1), ("B", 1), ("N", 1), ("M", 1), (",", 1), (".", 1), ("/", 1)],
    [("CTRL", 1), ("ALT", 1), ("SPACE", 5), ("ALT_R", 1), ("CTRL_R", 1)],
]

ROLE_STYLES = {
    "assist": "background-color: #574b90; color: white; border: 1px solid #40376c;",
    "rotation": "background-color: #1f4f99; color: white; border: 1px solid #24466f;",
    "self_heal": "background-color: #0d6f6f; color: white; border: 1px solid #095151;",
    "offensive": "background-color: #8a4b08; color: white; border: 1px solid #6c3a06;",
    "defensive": "background-color: #1f6a33; color: white; border: 1px solid #184f27;",
    "interrupt": "background-color: #7a1c1c; color: white; border: 1px solid #5d1515;",
    "movement": "background-color: #5a2b88; color: white; border: 1px solid #45206a;",
    "utility": "background-color: #7a650d; color: white; border: 1px solid #5b4b09;",
    "system": "background-color: #5d5d5d; color: white; border: 1px solid #484848;",
    "neutral": "background-color: #efefef; color: #333333; border: 1px solid #bbbbbb;",
}

DISPLAY_LABELS = {
    "SPACE": "Space",
    "ALT_R": "Alt",
    "CTRL_R": "Ctrl",
    "\\": "\\",
}


def formatSpellDisplay(spellName, maxCharsPerLine=12, maxLines=2):
    spellName = spellName.strip()
    if not spellName:
        return ""

    replacements = {
        "Counterspell": "Counter\nspell",
        "Counter Shot": "Counter\nShot",
        "Explosive Shot": "Explosive\nShot",
        "Rapid Fire": "Rapid\nFire",
        "Steady Shot": "Steady\nShot",
        "Arcane Blast": "Arcane\nBlast",
        "Arcane Missiles": "Arcane\nMissiles",
        "Arcane Barrage": "Arcane\nBarrage",
        "Arcane Surge": "Arcane\nSurge",
        "Arcane Orb": "Arcane\nOrb",
        "Aspect of the Turtle": "Aspect\nTurtle",
        "Aspect of the Cheetah": "Aspect\nCheetah",
        "Hunter's Mark": "Hunter's\nMark",
        "Touch of the Magi": "Touch of\nMagi",
        "Presence of Mind": "Pres. of\nMind",
        "Fortitude of the Bear": "Fort. of\nBear",
        "Mirror Image": "Mirror\nImage",
        "Wailing Arrow": "Wailing\nArrow",
    }
    if spellName in replacements:
        return replacements[spellName]

    words = spellName.split()
    if len(words) == 1:
        word = words[0]
        if len(word) <= maxCharsPerLine:
            return word
        splitAt = min(maxCharsPerLine, max(4, len(word) // 2))
        line1 = word[:splitAt]
        line2 = word[splitAt: splitAt + maxCharsPerLine - 1]
        if len(word) > splitAt + len(line2):
            line2 = f"{line2.rstrip('.')}…"
        return f"{line1}\n{line2}"

    lines = []
    currentLine = []

    for word in words:
        candidate = " ".join(currentLine + [word]).strip()
        if len(candidate) <= maxCharsPerLine:
            currentLine.append(word)
            continue

        if currentLine:
            lines.append(" ".join(currentLine))
            currentLine = [word]
        else:
            lines.append(word[:maxCharsPerLine])
            currentLine = [word[maxCharsPerLine:]] if len(word) > maxCharsPerLine else []

        if len(lines) == maxLines:
            break

    if len(lines) < maxLines and currentLine:
        lines.append(" ".join(part for part in currentLine if part))

    lines = [line for line in lines[:maxLines] if line]
    if not lines:
        return spellName[:maxCharsPerLine]

    reconstructed = " ".join(lines).replace("\n", " ").strip()
    if reconstructed != spellName:
        finalLine = lines[-1]
        if len(finalLine) >= maxCharsPerLine:
            finalLine = finalLine[: maxCharsPerLine - 1].rstrip()
        lines[-1] = f"{finalLine.rstrip('.')}…"

    return "\n".join(lines[:maxLines])


class KeyCap(QFrame):
    def __init__(self, keyText, role, roleChangedCallback, keySelectedCallback, spellNameEditedCallback):
        super().__init__()
        self.keyText = keyText
        self.role = role
        self.roleChangedCallback = roleChangedCallback
        self.keySelectedCallback = keySelectedCallback
        self.spellNameEditedCallback = spellNameEditedCallback
        self.isSelected = False
        self.fullSpellName = ""
        self.finding = None

        safeName = (
            keyText.replace("`", "backtick")
            .replace("'", "apostrophe")
            .replace(";", "semicolon")
            .replace(",", "comma")
            .replace(".", "period")
            .replace("/", "slash")
            .replace("[", "lbracket")
            .replace("]", "rbracket")
            .replace("=", "equals")
            .replace("-", "dash")
            .replace("\\", "backslash")
        )
        self.setObjectName(f"keyCap_{safeName}")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._showContextMenu)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        layout = QVBoxLayout()
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(1)

        self.keyLabel = QLabel(DISPLAY_LABELS.get(keyText, keyText))
        self.keyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.keyLabel.setObjectName("keyLabel")
        self.keyLabel.setStyleSheet("font-size: 11px; font-weight: 700;")

        self.spellLabel = QLabel()
        self.spellLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spellLabel.setWordWrap(True)
        self.spellLabel.setObjectName("spellLabel")
        self.spellLabel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.spellLabel.setStyleSheet("font-size: 10px; font-weight: 600; padding-top: 2px;")

        self.spellEdit = QLineEdit()
        self.spellEdit.setObjectName("spellEdit")
        self.spellEdit.setPlaceholderText("Spell")
        self.spellEdit.hide()
        self.spellEdit.returnPressed.connect(self._commitInlineEdit)
        self.spellEdit.editingFinished.connect(self._commitInlineEditIfVisible)
        self.spellEdit.installEventFilter(self)

        layout.addWidget(self.keyLabel)
        layout.addWidget(self.spellLabel, 1)
        layout.addWidget(self.spellEdit)
        self.setLayout(layout)

        self.setMinimumSize(KEY_UNIT_WIDTH, KEY_HEIGHT)
        self.setRole(role)
        self.setSpellName("")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.keySelectedCallback(self.keyText)
            self.setFocus(Qt.FocusReason.MouseFocusReason)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.keySelectedCallback(self.keyText)
            self.startInlineEdit()
        super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_F2) and not self.spellEdit.isVisible():
            self.startInlineEdit()
            event.accept()
            return
        if event.key() == Qt.Key.Key_Escape and self.spellEdit.isVisible():
            self.cancelInlineEdit()
            event.accept()
            return
        super().keyPressEvent(event)

    def eventFilter(self, watched, event):
        if watched is self.spellEdit and event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self._commitInlineEdit()
                return True
            if event.key() == Qt.Key.Key_Escape:
                self.cancelInlineEdit()
                return True
        return super().eventFilter(watched, event)

    def setRole(self, role):
        self.role = role
        self._refreshStyle()

    def setSpellName(self, spellName):
        self.fullSpellName = spellName
        self.spellLabel.setText(formatSpellDisplay(spellName))
        self.spellLabel.setToolTip(spellName)
        self.spellEdit.setText(spellName)

    def setFinding(self, finding):
        self.finding = finding
        self.setRole(finding.role)
        self.setSpellName(finding.spellName)
        tooltipParts = [
            f"Key: {finding.key}",
            f"Role: {finding.role}",
            f"Status: {finding.status}",
        ]
        if finding.spellName:
            tooltipParts.append(f"Spell: {finding.spellName}")
        if finding.spellCategory:
            tooltipParts.append(f"Spell category: {finding.spellCategory}")
            tooltipParts.append(f"Classification: {finding.classificationSource}")
        if finding.consensusKey:
            tooltipParts.append(
                f"Consensus key: {finding.consensusKey} ({finding.consensusConfidence:.0%})"
            )
        self.setToolTip("\n".join(tooltipParts))

    def setSelected(self, isSelected):
        self.isSelected = isSelected
        self._refreshStyle()

    def startInlineEdit(self):
        self.spellEdit.setText(self.fullSpellName)
        self.spellLabel.hide()
        self.spellEdit.show()
        self.spellEdit.setFocus(Qt.FocusReason.MouseFocusReason)
        self.spellEdit.selectAll()

    def cancelInlineEdit(self):
        self.spellEdit.setText(self.fullSpellName)
        self.spellEdit.hide()
        self.spellLabel.show()
        self.setFocus(Qt.FocusReason.OtherFocusReason)

    def _commitInlineEditIfVisible(self):
        if self.spellEdit.isVisible():
            self._commitInlineEdit()

    def _commitInlineEdit(self):
        if not self.spellEdit.isVisible():
            return
        spellName = self.spellEdit.text().strip()
        self.spellEdit.hide()
        self.spellLabel.show()
        self.spellNameEditedCallback(self.keyText, spellName)
        self.setFocus(Qt.FocusReason.OtherFocusReason)

    def _refreshStyle(self):
        statusBorders = {
            "match": "2px solid #2e7d32",
            "mismatch": "2px solid #c62828",
            "unknown": "2px solid #f9a825",
            "reserved_conflict": "2px solid #c62828",
        }
        outline = "2px solid #1a73e8" if self.isSelected else statusBorders.get(
            self.finding.status if self.finding else "",
            "1px solid transparent",
        )
        self.setStyleSheet(
            "border-radius: 4px; padding: 4px;"
            + ROLE_STYLES.get(self.role, ROLE_STYLES["neutral"])
            + f"outline: {outline};"
        )

    def _showContextMenu(self, position: QPoint):
        menu = QMenu(self)
        assignMenu = menu.addMenu("Assign Role")

        for role in ROLE_ORDER:
            action = assignMenu.addAction(role.title())
            action.setCheckable(True)
            action.setChecked(self.role == role)
            action.triggered.connect(
                lambda checked=False, selectedRole=role: self.roleChangedCallback(self.keyText, selectedRole)
            )

        menu.addSeparator()

        editAction = menu.addAction("Edit Spell Name")
        editAction.triggered.connect(self.startInlineEdit)

        clearSpellAction = menu.addAction("Clear Spell Name")
        clearSpellAction.triggered.connect(lambda: self.spellNameEditedCallback(self.keyText, ""))

        menu.addSeparator()

        clearAction = menu.addAction("Clear Role")
        clearAction.triggered.connect(lambda: self.roleChangedCallback(self.keyText, "neutral"))

        resetAction = menu.addAction("Reset Key To Default")
        resetAction.triggered.connect(
            lambda: self.roleChangedCallback(self.keyText, DEFAULT_KEY_ROLES.get(self.keyText, "neutral"))
        )

        menu.exec(self.mapToGlobal(position))


class KeyboardDiagram(QWidget):
    def __init__(self, preferredRoles=None):
        super().__init__()
        self.setObjectName("keyboardDiagram")
        self.defaultKeyRoles = dict(preferredRoles or DEFAULT_KEY_ROLES)
        self.keyRoles = self.defaultKeyRoles.copy()
        self.keyCaps = {}
        self.spacerWidgets = []
        self.selectedKey = None
        self._selectedKeyChangedCallback = None
        self._spellNameEditedCallback = None

        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel("Target key layout")
        title.setObjectName("keyboardDiagramTitle")

        subtitle = QLabel(
            "Right-click any key to change its role colour. Double-click a key, or press Enter/F2 on the selected key, to edit the spell name in place."
        )
        subtitle.setWordWrap(True)
        subtitle.setObjectName("keyboardDiagramSubtitle")

        gridHost = QWidget()
        self.grid = QGridLayout()
        self.grid.setHorizontalSpacing(8)
        self.grid.setVerticalSpacing(8)
        gridHost.setLayout(self.grid)

        for rowIndex, row in enumerate(KEY_ROWS):
            columnIndex = 0
            for keyText, span in row:
                if keyText is SPACER:
                    spacer = QWidget()
                    spacer.setObjectName(f"spacer_{rowIndex}_{columnIndex}")
                    spacer.setFixedSize(KEY_UNIT_WIDTH * span, KEY_HEIGHT)
                    spacer.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
                    self.spacerWidgets.append(spacer)
                    self.grid.addWidget(spacer, rowIndex, columnIndex, 1, span)
                    columnIndex += span
                    continue

                role = self.keyRoles.get(keyText, "neutral")
                keyCap = KeyCap(keyText, role, self.setKeyRole, self.setSelectedKey, self._onSpellNameEdited)
                self.keyCaps[keyText] = keyCap
                self.grid.addWidget(keyCap, rowIndex, columnIndex, 1, span)
                columnIndex += span

        legend = QWidget()
        legendLayout = QHBoxLayout()
        legendLayout.setContentsMargins(0, 0, 0, 0)
        legendLayout.setSpacing(8)
        legend.setLayout(legendLayout)

        legendTitle = QLabel("Legend")
        legendLayout.addWidget(legendTitle)
        for labelText in ROLE_ORDER:
            chip = QLabel(labelText.title())
            chip.setStyleSheet(
                "padding: 4px 8px; border-radius: 10px;" + ROLE_STYLES[labelText]
            )
            legendLayout.addWidget(chip)
        legendLayout.addStretch()

        hint = QLabel(
            "Reserved WoW operation keys such as H, J, K, and L start as System. Empty keys stay visible so we can spot wasted space later."
        )
        hint.setWordWrap(True)
        hint.setObjectName("keyboardDiagramHint")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(gridHost)
        layout.addWidget(legend)
        layout.addWidget(hint)
        layout.addStretch()
        self.setLayout(layout)

    def setSelectedKeyChangedCallback(self, callback):
        self._selectedKeyChangedCallback = callback

    def setSpellNameEditedCallback(self, callback):
        self._spellNameEditedCallback = callback

    def getKeyRole(self, keyText):
        return self.keyRoles.get(keyText, "neutral")

    def setKeyRole(self, keyText, role):
        self.keyRoles[keyText] = role
        if keyText in self.keyCaps:
            self.keyCaps[keyText].setRole(role)

    def setSelectedKey(self, keyText):
        self.selectedKey = keyText
        for currentKey, keyCap in self.keyCaps.items():
            keyCap.setSelected(currentKey == keyText)
        if self._selectedKeyChangedCallback is not None:
            self._selectedKeyChangedCallback(keyText)

    def setSpellName(self, keyText, spellName):
        if keyText in self.keyCaps:
            self.keyCaps[keyText].setSpellName(spellName)

    def setFindings(self, findings):
        for keyText, keyCap in self.keyCaps.items():
            finding = findings.get(keyText)
            if finding is None:
                continue
            self.keyRoles[keyText] = finding.role
            keyCap.setFinding(finding)

    def startInlineEditForKey(self, keyText):
        if keyText in self.keyCaps:
            self.setSelectedKey(keyText)
            self.keyCaps[keyText].startInlineEdit()

    def _onSpellNameEdited(self, keyText, spellName):
        self.setSpellName(keyText, spellName)
        if self._spellNameEditedCallback is not None:
            self._spellNameEditedCallback(keyText, spellName)

    def resetToDefaults(self):
        self.keyRoles = self.defaultKeyRoles.copy()
        for keyText, keyCap in self.keyCaps.items():
            keyCap.setRole(self.keyRoles.get(keyText, "neutral"))


class FindingsWindow(QWidget):
    def __init__(self, characters=None, onCloseCallback=None, findingsService=None):
        super().__init__()
        self.onCloseCallback = onCloseCallback
        self.findingsService = findingsService or KeybindFindingsService()
        self.characters = characters or self.findingsService.getCharacters()
        self.specOptionsByCharacter = self._buildSpecOptions()
        self.selectedKey = None

        self.setObjectName("findingsWindow")
        self.setWindowTitle("OrganiseMyAlts Findings")
        self.resize(1500, 860)
        self.setMinimumSize(1500, 860)

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        title = QLabel("Keybind findings")
        title.setObjectName("findingsTitle")

        summary = QLabel("Consensus mode: review actual bindings against the learned Strafe Mode key-role model.")
        summary.setWordWrap(True)
        summary.setObjectName("findingsSummary")

        self.controlPanel = self._buildControlPanel()
        self.keyboardDiagram = KeyboardDiagram(self.findingsService.getPreferredRoles())
        self.keyboardDiagram.setSelectedKeyChangedCallback(self._onSelectedKeyChanged)
        self.keyboardDiagram.setSpellNameEditedCallback(self._onInlineSpellEdited)

        layout.addWidget(title)
        layout.addWidget(summary)
        layout.addWidget(self.controlPanel)
        layout.addWidget(self.keyboardDiagram)
        self.setLayout(layout)

        self._populateCharacterDropdown()
        self.keyboardDiagram.setSelectedKey("2")
        self._refreshSpellLayout()

    def _buildDefaultCharacters(self):
        return self.findingsService.getCharacters()

    def _buildSpecOptions(self):
        specOptions = {}
        for character in self.characters:
            characterName = character.get("name", "")
            scannedSpecs = list(character.get("scannedSpecs", []))
            currentSpec = character.get("spec", "")
            if currentSpec and currentSpec not in scannedSpecs:
                scannedSpecs.insert(0, currentSpec)
            if not scannedSpecs and currentSpec:
                scannedSpecs = [currentSpec]
            specOptions[characterName] = scannedSpecs or ["Unknown"]
        return specOptions

    def _buildControlPanel(self):
        panel = QWidget()
        panel.setObjectName("findingsControlPanel")
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        characterLabel = QLabel("Character")
        self.characterDropdown = QComboBox()
        self.characterDropdown.setObjectName("characterDropdown")

        specLabel = QLabel("Spec")
        self.specDropdown = QComboBox()
        self.specDropdown.setObjectName("specDropdown")

        selectedKeyTitle = QLabel("Selected Key")
        self.selectedKeyValue = QLabel("-")
        self.selectedKeyValue.setObjectName("selectedKeyValue")

        spellLabel = QLabel("Spell Name")
        self.spellNameEdit = QLineEdit()
        self.spellNameEdit.setObjectName("spellNameEdit")
        self.spellNameEdit.setPlaceholderText("Type a spell name for the selected key")

        self.editOnKeyButton = QPushButton("Edit On Key")
        self.editOnKeyButton.setObjectName("editOnKeyButton")
        self.saveSpellButton = QPushButton("Save Spell")
        self.saveSpellButton.setObjectName("saveSpellButton")
        self.clearSpellButton = QPushButton("Clear Spell")
        self.clearSpellButton.setObjectName("clearSpellButton")

        self.characterDropdown.currentTextChanged.connect(self._onCharacterChanged)
        self.specDropdown.currentTextChanged.connect(self._refreshSpellLayout)
        self.editOnKeyButton.clicked.connect(self._startInlineEditForSelectedKey)
        self.saveSpellButton.clicked.connect(self._saveSpellName)
        self.clearSpellButton.clicked.connect(self._clearSpellName)
        self.spellNameEdit.returnPressed.connect(self._saveSpellName)

        for widget in [
            characterLabel,
            self.characterDropdown,
            specLabel,
            self.specDropdown,
            selectedKeyTitle,
            self.selectedKeyValue,
            spellLabel,
            self.spellNameEdit,
            self.editOnKeyButton,
            self.saveSpellButton,
            self.clearSpellButton,
        ]:
            layout.addWidget(widget)

        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def _populateCharacterDropdown(self):
        self.characterDropdown.blockSignals(True)
        self.characterDropdown.clear()
        for character in self.characters:
            self.characterDropdown.addItem(character.get("name", ""))
        self.characterDropdown.blockSignals(False)
        if self.characterDropdown.count() > 0:
            self.characterDropdown.setCurrentIndex(0)
            self._onCharacterChanged(self.characterDropdown.currentText())

    def _onCharacterChanged(self, characterName):
        specOptions = self.specOptionsByCharacter.get(characterName, ["Unknown"])
        self.specDropdown.blockSignals(True)
        self.specDropdown.clear()
        self.specDropdown.addItems(specOptions)
        self.specDropdown.blockSignals(False)
        if self.specDropdown.count() > 0:
            self.specDropdown.setCurrentIndex(0)
        self._refreshSpellLayout()

    def _getCurrentCharacterName(self):
        return self.characterDropdown.currentText()

    def _getCurrentSpecName(self):
        return self.specDropdown.currentText()

    def _getSpellLayout(self, characterName, specName, createMissing=False):
        return self.findingsService.getSpellLayout(characterName, specName)

    def _refreshSpellLayout(self):
        characterName = self._getCurrentCharacterName()
        specName = self._getCurrentSpecName()
        findings = self.findingsService.getFindings(
            characterName,
            specName,
            self.keyboardDiagram.keyCaps.keys(),
        )
        self.keyboardDiagram.setFindings(findings)

        self._updateSpellEditFromSelection()

    def _onSelectedKeyChanged(self, keyText):
        self.selectedKey = keyText
        self.selectedKeyValue.setText(keyText)
        self._updateSpellEditFromSelection()

    def _onInlineSpellEdited(self, keyText, spellName):
        if keyText != self.selectedKey:
            self.keyboardDiagram.setSelectedKey(keyText)
        self._saveSpellNameForKey(keyText, spellName)
        self._updateSpellEditFromSelection()

    def _updateSpellEditFromSelection(self):
        if not self.selectedKey:
            self.spellNameEdit.setText("")
            return

        spellLayout = self._getSpellLayout(self._getCurrentCharacterName(), self._getCurrentSpecName())
        self.spellNameEdit.setText(spellLayout.get(self.selectedKey, ""))

    def _startInlineEditForSelectedKey(self):
        if self.selectedKey:
            self.keyboardDiagram.startInlineEditForKey(self.selectedKey)

    def _saveSpellName(self):
        if not self.selectedKey:
            return
        self._saveSpellNameForKey(self.selectedKey, self.spellNameEdit.text().strip())

    def _saveSpellNameForKey(self, keyText, spellName):
        characterName = self._getCurrentCharacterName()
        specName = self._getCurrentSpecName()
        self.findingsService.setSpellName(characterName, specName, keyText, spellName)
        self._refreshSpellLayout()

    def _clearSpellName(self):
        self.spellNameEdit.clear()
        self._saveSpellName()

    def closeEvent(self, event: QCloseEvent):
        if self.onCloseCallback is not None:
            self.onCloseCallback()
        super().closeEvent(event)

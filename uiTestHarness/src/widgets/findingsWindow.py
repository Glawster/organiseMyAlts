from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMenu,
    QVBoxLayout,
    QWidget,
)


KEY_ROWS = [
    ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"],
    ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
    ["CTRL", "ALT", "SPACE", "ALT_R", "CTRL_R"],
]

ROLE_ORDER = [
    "rotation",
    "offensive",
    "defensive",
    "interrupt",
    "movement",
    "utility",
    "system",
    "neutral",
]

DEFAULT_KEY_ROLES = {
    "2": "rotation",
    "3": "rotation",
    "4": "rotation",
    "5": "rotation",
    "6": "rotation",
    "Q": "offensive",
    "E": "offensive",
    "R": "offensive",
    "T": "offensive",
    "Y": "offensive",
    "U": "offensive",
    "F3": "interrupt",
    "F5": "defensive",
    "F6": "defensive",
    "F7": "defensive",
    "F8": "movement",
    "`": "utility",
    "H": "system",
    "J": "system",
    "K": "system",
    "L": "system",
}

ROLE_STYLES = {
    "rotation": "background-color: #1f4f99; color: white; border: 1px solid #24466f;",
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
}

ROLE_LABELS = {
    "rotation": "Rotation",
    "offensive": "Offensive",
    "defensive": "Defensive",
    "interrupt": "Interrupt",
    "movement": "Movement",
    "utility": "Utility",
    "system": "System",
    "neutral": "",
}


class KeyCap(QFrame):
    def __init__(self, keyText, role, roleChangedCallback):
        super().__init__()
        self.keyText = keyText
        self.role = role
        self.roleChangedCallback = roleChangedCallback

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
        )
        self.setObjectName(f"keyCap_{safeName}")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._showContextMenu)

        layout = QVBoxLayout()
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(1)

        self.keyLabel = QLabel(DISPLAY_LABELS.get(keyText, keyText))
        self.keyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.keyLabel.setObjectName("keyLabel")

        self.roleLabel = QLabel()
        self.roleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.roleLabel.setObjectName("roleLabel")

        layout.addWidget(self.keyLabel)
        layout.addWidget(self.roleLabel)
        self.setLayout(layout)

        if keyText == "SPACE":
            self.setMinimumSize(160, 52)
        else:
            self.setMinimumSize(64, 52)

        self.setRole(role)

    def setRole(self, role):
        self.role = role
        self.roleLabel.setText(ROLE_LABELS.get(role, role.title()))
        self.setStyleSheet(
            "border-radius: 4px; padding: 4px;"
            + ROLE_STYLES.get(role, ROLE_STYLES["neutral"])
        )

    def _showContextMenu(self, position: QPoint):
        menu = QMenu(self)
        assignMenu = menu.addMenu("Assign Role")

        for role in ROLE_ORDER:
            action = assignMenu.addAction(role.title())
            action.setCheckable(True)
            action.setChecked(self.role == role)
            action.triggered.connect(lambda checked=False, selectedRole=role: self.roleChangedCallback(self.keyText, selectedRole))

        menu.addSeparator()

        clearAction = menu.addAction("Clear Role")
        clearAction.triggered.connect(lambda: self.roleChangedCallback(self.keyText, "neutral"))

        resetAction = menu.addAction("Reset Key To Default")
        resetAction.triggered.connect(lambda: self.roleChangedCallback(self.keyText, DEFAULT_KEY_ROLES.get(self.keyText, "neutral")))

        menu.exec(self.mapToGlobal(position))


class KeyboardDiagram(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("keyboardDiagram")
        self.keyRoles = DEFAULT_KEY_ROLES.copy()
        self.keyCaps = {}

        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel("Target key layout")
        title.setObjectName("keyboardDiagramTitle")

        subtitle = QLabel(
            "Right-click any key to change its role. Phase 1 shows the preferred layout first, including empty and reserved keys."
        )
        subtitle.setWordWrap(True)
        subtitle.setObjectName("keyboardDiagramSubtitle")

        gridHost = QWidget()
        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(8)
        gridHost.setLayout(grid)

        for rowIndex, row in enumerate(KEY_ROWS):
            for colIndex, keyText in enumerate(row):
                role = self.keyRoles.get(keyText, "neutral")
                keyCap = KeyCap(keyText, role, self.setKeyRole)
                self.keyCaps[keyText] = keyCap

                if keyText == "SPACE":
                    grid.addWidget(keyCap, rowIndex, colIndex, 1, 2)
                else:
                    grid.addWidget(keyCap, rowIndex, colIndex)

        legend = QWidget()
        legendLayout = QHBoxLayout()
        legendLayout.setContentsMargins(0, 0, 0, 0)
        legendLayout.setSpacing(8)
        legend.setLayout(legendLayout)

        for labelText in ROLE_ORDER:
            chip = QLabel(labelText.title())
            chip.setStyleSheet(
                "padding: 4px 8px; border-radius: 10px;"
                + ROLE_STYLES[labelText]
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

    def getKeyRole(self, keyText):
        return self.keyRoles.get(keyText, "neutral")

    def setKeyRole(self, keyText, role):
        self.keyRoles[keyText] = role
        if keyText in self.keyCaps:
            self.keyCaps[keyText].setRole(role)

    def resetToDefaults(self):
        self.keyRoles = DEFAULT_KEY_ROLES.copy()
        for keyText, keyCap in self.keyCaps.items():
            keyCap.setRole(self.keyRoles.get(keyText, "neutral"))


class FindingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("findingsWindow")
        self.setWindowTitle("OrganiseMyAlts Findings")
        self.resize(1080, 520)

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        title = QLabel("Keybind findings")
        title.setObjectName("findingsTitle")

        summary = QLabel(
            "Phase 1 baseline: show the full preferred keyboard map, allow role edits, then add scan overlays, per-spec scores, and recommendations."
        )
        summary.setWordWrap(True)
        summary.setObjectName("findingsSummary")

        self.keyboardDiagram = KeyboardDiagram()

        layout.addWidget(title)
        layout.addWidget(summary)
        layout.addWidget(self.keyboardDiagram)
        self.setLayout(layout)

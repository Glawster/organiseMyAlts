from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMenu,
    QVBoxLayout,
    QWidget,
)


SPACER = None
KEY_UNIT_WIDTH = 64
KEY_HEIGHT = 52

KEY_ROWS = [
    [(SPACER, 1), ("F1", 1), ("F2", 1), ("F3", 1), ("F4", 1), ("F5", 1), ("F6", 1), ("F7", 1), ("F8", 1), ("F9", 1), ("F10", 1), ("F11", 1), ("F12", 1)],
    [("`", 1), ("1", 1), ("2", 1), ("3", 1), ("4", 1), ("5", 1), ("6", 1), ("7", 1), ("8", 1), ("9", 1), ("0", 1), ("-", 1), ("=", 1)],
    [(SPACER, 1), ("Q", 1), ("W", 1), ("E", 1), ("R", 1), ("T", 1), ("Y", 1), ("U", 1), ("I", 1), ("O", 1), ("P", 1), ("[", 1), ("]", 1)],
    [(SPACER, 1), ("A", 1), ("S", 1), ("D", 1), ("F", 1), ("G", 1), ("H", 1), ("J", 1), ("K", 1), ("L", 1), (";", 1), ("'", 1)],
    [("\\", 1), ("Z", 1), ("X", 1), ("C", 1), ("V", 1), ("B", 1), ("N", 1), ("M", 1), (",", 1), (".", 1), ("/", 1)],
    [("CTRL", 1), ("ALT", 1), ("SPACE", 5), ("ALT_R", 1), ("CTRL_R", 1)],
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
    "\\": "\\",
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
            .replace("\\", "backslash")
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

        self.setMinimumSize(KEY_UNIT_WIDTH, KEY_HEIGHT)
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
            action.triggered.connect(
                lambda checked=False, selectedRole=role: self.roleChangedCallback(self.keyText, selectedRole)
            )

        menu.addSeparator()

        clearAction = menu.addAction("Clear Role")
        clearAction.triggered.connect(lambda: self.roleChangedCallback(self.keyText, "neutral"))

        resetAction = menu.addAction("Reset Key To Default")
        resetAction.triggered.connect(
            lambda: self.roleChangedCallback(self.keyText, DEFAULT_KEY_ROLES.get(self.keyText, "neutral"))
        )

        menu.exec(self.mapToGlobal(position))


class KeyboardDiagram(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("keyboardDiagram")
        self.keyRoles = DEFAULT_KEY_ROLES.copy()
        self.keyCaps = {}
        self.spacerWidgets = []

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
                keyCap = KeyCap(keyText, role, self.setKeyRole)
                self.keyCaps[keyText] = keyCap
                self.grid.addWidget(keyCap, rowIndex, columnIndex, 1, span)
                columnIndex += span

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
    def __init__(self, onCloseCallback=None):
        super().__init__()
        self.onCloseCallback = onCloseCallback
        self.setObjectName("findingsWindow")
        self.setWindowTitle("OrganiseMyAlts Findings")
        self.resize(1360, 760)
        self.setMinimumSize(1360, 760)

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

    def closeEvent(self, event: QCloseEvent):
        if self.onCloseCallback is not None:
            self.onCloseCallback()
        super().closeEvent(event)

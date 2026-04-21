from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QWidget

# Mirrors CLASS_SPECS in core/ui.lua.
CLASS_SPECS = {
    "DEATHKNIGHT": ["Blood", "Frost", "Unholy"],
    "DEMONHUNTER": ["Havoc", "Vengeance"],
    "DRUID":       ["Balance", "Feral", "Guardian", "Restoration"],
    "EVOKER":      ["Augmentation", "Devastation", "Preservation"],
    "HUNTER":      ["Beast Mastery", "Marksmanship", "Survival"],
    "MAGE":        ["Arcane", "Fire", "Frost"],
    "MONK":        ["Brewmaster", "Mistweaver", "Windwalker"],
    "PALADIN":     ["Holy", "Protection", "Retribution"],
    "PRIEST":      ["Discipline", "Holy", "Shadow"],
    "ROGUE":       ["Assassination", "Outlaw", "Subtlety"],
    "SHAMAN":      ["Elemental", "Enhancement", "Restoration"],
    "WARLOCK":     ["Affliction", "Demonology", "Destruction"],
    "WARRIOR":     ["Arms", "Fury", "Protection"],
}

COLUMNS = ["Character", "Class", "Spec", "Level", "iLvl", "KB Specs", "Last Scan"]


class SpecBadgesWidget(QWidget):
    """Renders per-spec coloured badge cells inside the KB Specs table column.

    Each spec gets its own QLabel: green background if scanned, red if not.
    """

    SCANNED_COLOR   = "#0d5e0d"
    UNSCANNED_COLOR = "#5e0d0d"

    def __init__(self, specs):
        """
        Args:
            specs: list of (abbrev: str, scanned: bool) pairs.
        """
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(3, 1, 3, 1)
        layout.setSpacing(3)
        self._labels = []
        for abbrev, scanned in specs:
            color = self.SCANNED_COLOR if scanned else self.UNSCANNED_COLOR
            label = QLabel(abbrev)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFixedHeight(18)
            label.setMinimumWidth(28)
            label.setStyleSheet(
                f"background-color: {color}; color: white; "
                "border-radius: 2px; padding: 0px 3px; font-size: 10px;"
            )
            layout.addWidget(label)
            self._labels.append((abbrev, scanned, label))
        layout.addStretch()
        self.setLayout(layout)

    @property
    def labels(self):
        """Return list of (abbrev, scanned, QLabel) triples for test assertions."""
        return self._labels


class CharacterOverviewPanel(QTableWidget):
    """Column-table view of all tracked characters, mirroring core/ui.lua."""

    def __init__(self):
        super().__init__(0, len(COLUMNS))
        self.setObjectName("characterOverviewPanel")
        self.setHorizontalHeaderLabels(COLUMNS)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setDefaultSectionSize(26)

    def loadRows(self, rows):
        """Populate the table from a list of row dicts produced by JsonDataService."""
        self.setRowCount(0)

        for row in rows:
            rowIndex = self.rowCount()
            self.insertRow(rowIndex)

            class_name = row.get("class", "")
            all_specs = CLASS_SPECS.get(class_name, [])
            scanned_set = set(row.get("scannedSpecs", []))

            if all_specs:
                specs = [(spec[:3], spec in scanned_set) for spec in all_specs]
            else:
                specs = [("?", False)]

            text_cells = [
                (0, row.get("name", "")),
                (1, row.get("class", "?")),
                (2, row.get("spec", "?")),
                (3, str(row.get("level", 0))),
                (4, str(row.get("ilvl", "?"))),
                (6, row.get("lastScan", "---")),
            ]

            for col, text in text_cells:
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                self.setItem(rowIndex, col, item)

            self.setCellWidget(rowIndex, 5, SpecBadgesWidget(specs))

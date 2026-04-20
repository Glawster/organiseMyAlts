from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

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

_GREEN  = QColor(0x00, 0xFF, 0x00)
_RED    = QColor(0xFF, 0x44, 0x44)
_YELLOW = QColor(0xFF, 0xFF, 0x00)


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
                parts = []
                for spec in all_specs:
                    prefix = "+" if spec in scanned_set else "-"
                    parts.append(prefix + spec[:3])
                kb_text = " ".join(parts)

                scanned_count = sum(1 for s in all_specs if s in scanned_set)
                if scanned_count == len(all_specs):
                    kb_color = _GREEN
                elif scanned_count == 0:
                    kb_color = _RED
                else:
                    kb_color = _YELLOW
            else:
                kb_text = "[?]"
                kb_color = None

            cells = [
                row.get("name", ""),
                row.get("class", "?"),
                row.get("spec", "?"),
                str(row.get("level", 0)),
                str(row.get("ilvl", "?")),
                kb_text,
                row.get("lastScan", "---"),
            ]

            for col, text in enumerate(cells):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                if col == 5 and kb_color is not None:
                    item.setForeground(QBrush(kb_color))
                self.setItem(rowIndex, col, item)

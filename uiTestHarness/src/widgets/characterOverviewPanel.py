from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

COLUMNS = ["Character", "Class", "Spec", "Level", "iLvl", "KB Scan", "Last Scan"]


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

            kbText = "YES" if row.get("keybindScanned") else "NO"

            cells = [
                row.get("name", ""),
                row.get("class", "?"),
                row.get("spec", "?"),
                str(row.get("level", 0)),
                str(row.get("ilvl", "?")),
                kbText,
                row.get("lastScan", "---"),
            ]

            for col, text in enumerate(cells):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                self.setItem(rowIndex, col, item)

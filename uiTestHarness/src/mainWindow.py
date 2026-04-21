from pathlib import Path

from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.services.jsonDataService import JsonDataService
from src.widgets.characterList import CharacterList
from src.widgets.characterOverviewPanel import CharacterOverviewPanel
from src.widgets.findingsWindow import FindingsWindow
from src.widgets.weeklyPanel import WeeklyPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OrganiseMyAlts UI Test Harness")
        self.findingsWindow = None

        baseDir = Path(__file__).resolve().parents[1]
        fixturePath = baseDir / "tests" / "fixtures" / "sampleRoster.json"

        self.dataService = JsonDataService(fixturePath)
        self.dataService.load()

        self._buildUi()
        self._loadData()
        self._connectSignals()

    def _buildUi(self):
        central = QWidget()
        outerLayout = QVBoxLayout()

        topRow = QWidget()
        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(0, 0, 0, 0)

        self.characterList = CharacterList()
        self.weeklyPanel = WeeklyPanel()

        topLayout.addWidget(self.characterList)
        topLayout.addWidget(self.weeklyPanel)
        topRow.setLayout(topLayout)

        self.characterOverviewPanel = CharacterOverviewPanel()

        buttonRow = QWidget()
        buttonLayout = QHBoxLayout()
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.showFindingsButton = QPushButton("Show Findings")
        self.showFindingsButton.setObjectName("showFindingsButton")
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.showFindingsButton)
        buttonRow.setLayout(buttonLayout)

        outerLayout.addWidget(topRow)
        outerLayout.addWidget(self.characterOverviewPanel)
        outerLayout.addWidget(buttonRow)

        central.setLayout(outerLayout)
        self.setCentralWidget(central)

    def _loadData(self):
        self.characters = self.dataService.getCharacters()
        self.characterList.loadCharacters(self.characters)
        overviewRows = self.dataService.getCharacterOverviewRows()
        self.characterOverviewPanel.loadRows(overviewRows)

    def _connectSignals(self):
        self.characterList.currentRowChanged.connect(self._onCharacterSelected)
        self.showFindingsButton.clicked.connect(self._showFindings)

    def _onCharacterSelected(self, index):
        if index < 0:
            return

        character = self.characters[index]
        tasks = self.dataService.getWeeklyTasks(character)
        self.weeklyPanel.updateTasks(tasks)

    def _showFindings(self):
        if self.findingsWindow is None:
            self.findingsWindow = FindingsWindow()

        self.findingsWindow.show()
        self.findingsWindow.raise_()
        self.findingsWindow.activateWindow()

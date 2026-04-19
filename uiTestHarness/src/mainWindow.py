from pathlib import Path

from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

from src.services.jsonDataService import JsonDataService
from src.widgets.characterList import CharacterList
from src.widgets.characterOverviewPanel import CharacterOverviewPanel
from src.widgets.weeklyPanel import WeeklyPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OrganiseMyAlts UI Test Harness")

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

        outerLayout.addWidget(topRow)
        outerLayout.addWidget(self.characterOverviewPanel)

        central.setLayout(outerLayout)
        self.setCentralWidget(central)

    def _loadData(self):
        self.characters = self.dataService.getCharacters()
        self.characterList.loadCharacters(self.characters)
        overviewRows = self.dataService.getCharacterOverviewRows()
        self.characterOverviewPanel.loadRows(overviewRows)

    def _connectSignals(self):
        self.characterList.currentRowChanged.connect(self._onCharacterSelected)

    def _onCharacterSelected(self, index):
        if index < 0:
            return

        character = self.characters[index]
        tasks = self.dataService.getWeeklyTasks(character)
        self.weeklyPanel.updateTasks(tasks)

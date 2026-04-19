from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from src.widgets.characterList import CharacterList
from src.widgets.weeklyPanel import WeeklyPanel
from src.services.jsonDataService import JsonDataService

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
        layout = QHBoxLayout()

        self.characterList = CharacterList()
        self.weeklyPanel = WeeklyPanel()

        layout.addWidget(self.characterList)
        layout.addWidget(self.weeklyPanel)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def _loadData(self):
        self.characters = self.dataService.getCharacters()
        self.characterList.loadCharacters(self.characters)

    def _connectSignals(self):
        self.characterList.currentRowChanged.connect(self._onCharacterSelected)

    def _onCharacterSelected(self, index):
        if index < 0:
            return

        character = self.characters[index]
        tasks = self.dataService.getWeeklyTasks(character)
        self.weeklyPanel.updateTasks(tasks)

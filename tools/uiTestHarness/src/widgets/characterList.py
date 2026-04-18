from PySide6.QtWidgets import QListWidget


class CharacterList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("characterList")

    def loadCharacters(self, characters):
        self.clear()
        for char in characters:
            self.addItem(char.name)

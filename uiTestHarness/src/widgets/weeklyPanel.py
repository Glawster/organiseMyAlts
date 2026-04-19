from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class WeeklyPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("weeklyPanel")

        self.layout = QVBoxLayout()

        self.title = QLabel("Weekly Tasks")
        self.tasksLabel = QLabel("Select a character")

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.tasksLabel)

        self.setLayout(self.layout)

    def updateTasks(self, tasks):
        self.tasksLabel.setText("\n".join(tasks))

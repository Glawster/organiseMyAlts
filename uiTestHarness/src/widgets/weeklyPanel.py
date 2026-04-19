from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class WeeklyPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("weeklyPanel")

        layout = QVBoxLayout()

        self.title = QLabel("Weekly Tasks")
        self.tasksLabel = QLabel("Select a character")

        layout.addWidget(self.title)
        layout.addWidget(self.tasksLabel)

        self.setLayout(layout)

    def updateTasks(self, tasks):
        if tasks:
            self.tasksLabel.setText("\n".join(tasks))
        else:
            self.tasksLabel.setText("No weekly tasks remaining")
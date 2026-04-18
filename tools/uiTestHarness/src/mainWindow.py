from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OrganiseMyAlts UI Test Harness")

        self._buildUi()

    def _buildUi(self):
        central = QWidget()
        layout = QVBoxLayout()

        self.label = QLabel("UI Harness Running")
        self.label.setObjectName("statusLabel")

        layout.addWidget(self.label)
        central.setLayout(layout)

        self.setCentralWidget(central)

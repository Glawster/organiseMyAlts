from PySide6.QtWidgets import QApplication
from src.mainWindow import MainWindow

import sys

def run():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    return app.exec()

if __name__ == "__main__":
    sys.exit(run())

# main.py
import sys
from PySide6.QtWidgets import QApplication
from ui.login_window import LoginWindow

app = QApplication(sys.argv)

# Подключение стилей (опционально)
with open("ui/styles.css", "r") as f:
    app.setStyleSheet(f.read())

window = LoginWindow()
window.show()
sys.exit(app.exec())
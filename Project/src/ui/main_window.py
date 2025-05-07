# ui/main_window.py
from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Бизнес-анализ: Таблица")
		self.setGeometry(100, 100, 800, 600)

		self.setup_ui()

	def setup_ui(self):
		self.table = QTableWidget()
		self.table.setRowCount(10)
		self.table.setColumnCount(5)

		layout = QVBoxLayout()
		layout.addWidget(self.table)

		container = QWidget()
		container.setLayout(layout)
		self.setCentralWidget(container)
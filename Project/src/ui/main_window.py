# ui/main_window.py
from PySide6.QtWidgets import (QMainWindow, QTableWidget, QVBoxLayout, QWidget,
							   QComboBox, QHBoxLayout, QLabel, QCheckBox, QFrame)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Бизнес-анализ: Таблица")
		self.showMaximized()  # Полноэкранный режим
		self.setup_ui()
		self.apply_styles()

	def setup_ui(self):
		# Главный контейнер
		main_widget = QWidget()
		main_layout = QVBoxLayout()
		main_layout.setContentsMargins(20, 20, 20, 20)
		main_layout.setSpacing(20)

		# Панель настроек
		settings_frame = QFrame()
		settings_layout = QHBoxLayout()
		settings_layout.setContentsMargins(15, 15, 15, 15)
		settings_layout.setSpacing(30)

		# Выбор типа таблицы
		table_type_label = QLabel("Тип таблицы:")
		self.table_type_combo = QComboBox()
		self.table_type_combo.addItems(["Бухгалтерский баланс", "Таблица затрат"])

		# Выбор года
		year_label = QLabel("Год:")
		self.year_combo = QComboBox()
		self.year_combo.addItems([str(year) for year in range(2020, 2024)])

		# Чекбоксы
		self.growth_rate_check = QCheckBox("Показывать темп роста")
		self.growth_rate_check.setChecked(True)

		self.deviation_check = QCheckBox("Показывать отклонение")
		self.deviation_check.setChecked(True)

		# Добавляем элементы в панель настроек
		settings_layout.addWidget(table_type_label)
		settings_layout.addWidget(self.table_type_combo)
		settings_layout.addWidget(year_label)
		settings_layout.addWidget(self.year_combo)
		settings_layout.addStretch()
		settings_layout.addWidget(self.growth_rate_check)
		settings_layout.addWidget(self.deviation_check)

		settings_frame.setLayout(settings_layout)

		# Таблица
		self.table = QTableWidget()
		self.table.setRowCount(50)  # Временное значение
		self.table.setColumnCount(10)  # Временное значение

		# Добавляем элементы в главный лэйаут
		main_layout.addWidget(settings_frame)
		main_layout.addWidget(self.table)

		main_widget.setLayout(main_layout)
		self.setCentralWidget(main_widget)

		# Подключаем сигналы
		self.table_type_combo.currentTextChanged.connect(self.update_table)
		self.year_combo.currentTextChanged.connect(self.update_table)
		self.growth_rate_check.stateChanged.connect(self.update_table)
		self.deviation_check.stateChanged.connect(self.update_table)

	def apply_styles(self):
		self.setStyleSheet("""
            QMainWindow {
                background-color: #252525;
            }
            QFrame {
                background-color: #333333;
                border-radius: 8px;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QComboBox {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                min-width: 200px;
            }
            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #ffffff;
                selection-background-color: #4CAF50;
            }
            QCheckBox {
                color: #ffffff;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
            }
            QTableWidget {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #444;
                gridline-color: #444;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #3c3c3c;
                color: #ffffff;
                padding: 8px;
                border: none;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)

	def update_table(self):
		"""Обновляет таблицу в соответствии с настройками"""
		# Здесь будет логика обновления таблицы
		print(f"Тип таблицы: {self.table_type_combo.currentText()}")
		print(f"Год: {self.year_combo.currentText()}")
		print(f"Показывать темп роста: {self.growth_rate_check.isChecked()}")
		print(f"Показывать отклонение: {self.deviation_check.isChecked()}")
	# TODO: Добавить загрузку данных из БД и обновление таблицы


if __name__ == "__main__":
	from PySide6.QtWidgets import QApplication

	app = QApplication([])
	window = MainWindow()
	window.show()
	app.exec()
# ui/main_window.py
from PySide6.QtWidgets import (QMainWindow, QTableWidget, QVBoxLayout, QWidget,
                               QComboBox, QHBoxLayout, QLabel, QHeaderView,
                               QTableWidgetItem, QFrame, QCheckBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ собственного капитала")
        self.showMaximized()
        self.data = {}  # Для хранения загруженных данных
        self.current_year = 2015  # Текущий выбранный год
        self.setup_ui()
        self.apply_styles()
        self.load_data()  # Загрузка данных при инициализации

    def setup_ui(self):
        # Главный контейнер
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Панель управления
        control_panel = QFrame()
        control_layout = QHBoxLayout(control_panel)
        control_layout.setContentsMargins(15, 15, 15, 15)
        control_layout.setSpacing(30)

        # Выбор года
        year_label = QLabel("Отчетный год:")
        self.year_combo = QComboBox()
        self.year_combo.addItems(["2013", "2014", "2015"])
        self.year_combo.currentTextChanged.connect(self.update_table)

        # Чекбоксы для выбора таблиц
        self.table1_checkbox = QCheckBox("Таблица 1")
        self.table1_checkbox.setChecked(True)
        self.table1_checkbox.stateChanged.connect(self.update_table)

        self.table2_checkbox = QCheckBox("Таблица 2")
        self.table2_checkbox.stateChanged.connect(self.update_table)

        control_layout.addWidget(year_label)
        control_layout.addWidget(self.year_combo)
        control_layout.addStretch()
        control_layout.addWidget(self.table1_checkbox)
        control_layout.addWidget(self.table2_checkbox)

        # Настройка таблицы
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Показатель",
            "Отчетный год",
            "Предыдущий год",
            "Темп роста, %",
            "Абсолютное отклонение"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Добавление элементов
        main_layout.addWidget(control_panel)
        main_layout.addWidget(self.table)
        self.setCentralWidget(main_widget)

    def load_data(self):
        """Загрузка данных из БД (примерная реализация)"""
        conn = sqlite3.connect('financial_data.db')
        cursor = conn.cursor()

        # Создаем временную таблицу и заполняем данными
        cursor.execute('''CREATE TABLE IF NOT EXISTS capital_data
                         (id INTEGER PRIMARY KEY, parameter TEXT, 
                         y2013 REAL, y2014 REAL, y2015 REAL)''')

        # Пример данных (замените на реальные из вашей таблицы)
        sample_data = [
            ("Остаток на 31.12.2013 года", 40255, 32846, 28015),
            ("Корректировки (учетная политика)", 0, 0, 0),
            ("Корректировки (исправление ошибок)", 0, 0, 0),
            ("Скорректированный остаток на 31.12.2013 года", 40255, 32846, 28015),
            ("Увеличение собственного капитала - всего", 0, 6500, 3552),
            ("В том числе: чистая прибыль", 0, 0, 0),
            ("переоценка долгосрочных активов", 0, 0, 0),
            ("доходы от прочих операций, не включаемые в чистую прибыль (убыток)", 0, 0, 0),
            ("выпуск дополнительных акций", 0, 6500, 3552),
            ("увеличение номинальной стоимости акций", 0, 0, 0),
            ("вклады собственника имущества (учредителей, участников)", 0, 0, 0),
            ("реорганизация", 0, 0, 0),
            ("прочие", 0, 0, 0),
            ("Уменьшение собственного капитала - всего", 0, 0, 0),
            ("В том числе: убыток", 0, 0, 0),
            ("переоценка долгосрочных активов", 0, 0, 0),
            ("расходы от прочих операций, не включаемые в чистую прибыль (убыток)", 0, 0, 0),
            ("уменьшение номинальной стоимости акций", 0, 0, 0),
            ("выкуп акций (долей в уставном капитале)", 0, 0, 0),
            ("дивиденды и другие доходы от участия в уставном капитале организации", 0, 0, 0),
            ("реорганизация", 0, 0, 0),
            ("прочие", 0, 0, 0),
            ("Изменение уставного капитала", 0, 909, 1279),
            ("Изменение резервного капитала", 0, 0, 0),
            ("Изменение добавочного капитала", 0, 0, 0),
            ("Остаток на 31.12.2014 года", 40255, 40255, 32846),
            ("Остаток на 31.12.2014 года", 40255, 40255, 32846),
            ("Корректировки в связи с изменением учетной политики", 0, 0, 0),
            ("Корректировки в связи с исправлением ошибок", 0, 0, 0),
            ("Скорректированный остаток на 31.12.2014 года", 40255, 40255, 32846),
            ("Увеличение собственного капитала - всего", 0, 0, 6500),
            ("В том числе: чистая прибыль", 0, 0, 0),
            ("переоценка долгосрочных активов", 0, 0, 0),
            ("доходы от прочих операций, не включаемые в чистую прибыль (убыток)", 0, 0, 0),
            ("выпуск дополнительных акций", 0, 0, 6500),
            ("увеличение номинальной стоимости акций", 0, 0, 0),
            ("вклады собственника имущества (учредителей, участников)", 0, 0, 0),
            ("реорганизация", 0, 0, 0),
            ("прочие", 0, 0, 0),
            ("Уменьшение собственного капитала - всего", 0, 0, 0),
            ("В том числе: убыток", 0, 0, 0),
            ("переоценка долгосрочных активов", 0, 0, 0),
            ("расходы от прочих операций, не включаемые в чистую прибыль (убыток)", 0, 0, 0),
            ("уменьшение номинальной стоимости акций", 0, 0, 0),
            ("выкуп акций (долей в уставном капитале)", 0, 0, 0),
            ("дивиденды и другие доходы от участия в уставном капитале организации", 0, 0, 0),
            ("реорганизация", 0, 0, 0),
            ("прочие", 0, 0, 0),
            ("Изменение уставного капитала", 0, 0, 909),
            ("Изменение резервного капитала", 0, 0, 0),
            ("Изменение добавочного капитала", 0, 0, 0),
            ("Остаток на 31.12.2015 года", 40255, 40255, 40255),
        ]

        cursor.executemany('INSERT INTO capital_data (parameter, y2013, y2014, y2015) VALUES (?,?,?,?)', sample_data)
        conn.commit()

        # Загрузка данных в память
        cursor.execute("SELECT * FROM capital_data")
        rows = cursor.fetchall()
        for row in rows:
            self.data[row[0]] = {
                'parameter': row[1],
                '2013': row[2],
                '2014': row[3],
                '2015': row[4]
            }
        conn.close()

    def update_table(self):
        selected_year = int(self.year_combo.currentText())
        prev_year = selected_year - 1 if selected_year > 2013 else None

        # Показываем только строки с данными
        row_count = 0
        for key, item in self.data.items():
            current_val = item.get(str(selected_year), 0)
            prev_val = item.get(str(prev_year)) if prev_year else None

            # Пропускаем строки без данных
            if (current_val == 0 and (prev_val == 0 or prev_val is None)):
                continue

            row_count += 1

        self.table.setRowCount(row_count)

        # Заполняем таблицу
        current_row = 0
        for key, item in self.data.items():
            current_val = item.get(str(selected_year), 0)
            prev_val = item.get(str(prev_year)) if prev_year else None

            # Пропускаем строки без данных
            if (current_val == 0 and (prev_val == 0 or prev_val is None)):
                continue

            # Показатель
            param_item = QTableWidgetItem(item['parameter'])
            param_item.setFlags(param_item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(current_row, 0, param_item)

            # Отчетный год
            current_item = QTableWidgetItem(str(current_val))
            current_item.setFlags(current_item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(current_row, 1, current_item)

            # Предыдущий год
            prev_item = QTableWidgetItem(str(prev_val) if prev_val else "-")
            prev_item.setFlags(prev_item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(current_row, 2, prev_item)

            # Темп роста
            if prev_val and current_val and prev_val != 0:
                growth = (current_val / prev_val) * 100
                growth_item = QTableWidgetItem(f"{growth:.2f}%")
            else:
                growth_item = QTableWidgetItem("-")
            growth_item.setFlags(growth_item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(current_row, 3, growth_item)

            # Абсолютное отклонение
            if prev_val is not None and current_val is not None:
                deviation = current_val - prev_val
                deviation_item = QTableWidgetItem(str(deviation))
                # Раскрашиваем ячейку
                if deviation < 0:
                    deviation_item.setBackground(QColor(150, 50, 50))  # Темно-красный
                else:
                    deviation_item.setBackground(QColor(50, 150, 50))  # Темно-зеленый
                deviation_item.setForeground(QColor(255, 255, 255))  # Белый текст
            else:
                deviation_item = QTableWidgetItem("-")

            deviation_item.setFlags(deviation_item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(current_row, 4, deviation_item)

            current_row += 1

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
            QTableWidget {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #444;
                gridline-color: #444;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: #ffffff;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QCheckBox {
                color: #ffffff;
                font-size: 14px;
            }
        """)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

# ui/main_window.py
from PySide6.QtWidgets import (QMainWindow, QTableWidget, QVBoxLayout, QWidget,
                               QComboBox, QHBoxLayout, QLabel, QHeaderView,
                               QTableWidgetItem, QFrame, QPushButton, QButtonGroup,
                               QDialog, QSizePolicy)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sqlite3


class GraphDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("График параметра")
        self.setMinimumSize(800, 600)

        # Создаем фигуру matplotlib
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        # Настройка layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_data(self, years, values, title, ylabel):
        """Отрисовывает график на основе переданных данных"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Отрисовываем график
        ax.plot(years, values, marker='o', linestyle='-', color='#4CAF50', linewidth=2, markersize=8)

        # Настройки графика
        ax.set_title(title, fontsize=14, pad=20)
        ax.set_xlabel('Год', fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_facecolor('#f0f0f0')

        # Форматирование осей
        ax.tick_params(axis='both', which='major', labelsize=10)

        # Автоматическое масштабирование
        ax.autoscale_view()

        # Обновляем холст
        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ собственного капитала и затрат на производство")
        self.showMaximized()
        self.data_table1 = []  # Хранение данных для таблицы 1
        self.data_table2 = []  # Хранение данных для таблицы 2
        self.current_year = 2015
        self.current_table = 1  # 1 или 2
        self.updating_table = False  # Флаг для предотвращения рекурсии
        self.setup_ui()
        self.apply_styles()
        self.load_data()

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

        # Кнопки для выбора таблиц
        self.table1_btn = QPushButton("Собственный капитал")
        self.table1_btn.setCheckable(True)
        self.table1_btn.setChecked(True)
        self.table1_btn.clicked.connect(lambda: self.switch_table(1))

        self.table2_btn = QPushButton("Затраты на производство")
        self.table2_btn.setCheckable(True)
        self.table2_btn.clicked.connect(lambda: self.switch_table(2))

        # Кнопка для показа графика
        self.show_graph_btn = QPushButton("Показать график")
        self.show_graph_btn.clicked.connect(self.show_graph)

        # Группа кнопок для взаимного исключения
        self.table_btn_group = QButtonGroup()
        self.table_btn_group.addButton(self.table1_btn)
        self.table_btn_group.addButton(self.table2_btn)

        control_layout.addWidget(year_label)
        control_layout.addWidget(self.year_combo)
        control_layout.addStretch()
        control_layout.addWidget(self.table1_btn)
        control_layout.addWidget(self.table2_btn)
        control_layout.addWidget(self.show_graph_btn)

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
        self.table.verticalHeader().setVisible(False)

        # Разрешаем редактирование только столбцов с годами
        self.table.itemChanged.connect(self.handle_item_changed)

        # Добавление элементов
        main_layout.addWidget(control_panel)
        main_layout.addWidget(self.table)
        self.setCentralWidget(main_widget)

    def show_graph(self):
        """Показывает график выбранного параметра"""
        selected_year = int(self.year_combo.currentText())

        # Создаем диалоговое окно с графиком
        graph_dialog = GraphDialog(self)

        if self.current_table == 1:
            # График для таблицы 1 (Собственный капитал)
            # Выбираем параметр "Увеличение собственного капитала - всего" (код 050)
            parameter_data = next((item for item in self.data_table1 if item['code'] == '050'), None)

            if parameter_data:
                years = ['2013', '2014', '2015']
                values = [parameter_data.get(year, 0) for year in years]

                graph_dialog.plot_data(
                    years,
                    values,
                    "Динамика увеличения собственного капитала по годам",
                    "Сумма, руб."
                )
        else:
            # График для таблицы 2 (Затраты на производство)
            # Выбираем параметр "Затраты на производство продукции" (код 002)
            parameter_data = next((item for item in self.data_table2 if item['code'] == '002'), None)

            if parameter_data:
                years = ['2013', '2014', '2015']
                values = [parameter_data.get(year, 0) for year in years]

                graph_dialog.plot_data(
                    years,
                    values,
                    "Динамика затрат на производство по годам",
                    "Сумма, руб."
                )

        graph_dialog.exec()

    def handle_item_changed(self, item):
        # Игнорируем изменения, если таблица обновляется программно
        if self.updating_table:
            return

        # Игнорируем изменения в столбцах, которые не должны редактироваться
        if item.column() not in [1, 2]:  # Только столбцы "Отчетный год" и "Предыдущий год"
            return

        # Получаем текущий год и предыдущий год
        selected_year = int(self.year_combo.currentText())
        prev_year = selected_year - 1 if selected_year > 2013 else None

        # Получаем номер строки
        row = item.row()

        # Проверяем, не является ли строка заголовком раздела или коэффициентом
        if (self.table.item(row, 0) and self.table.columnSpan(row, 0) > 1) or \
                (self.current_table == 1 and row >= self.table.rowCount() - 4):
            return

        # Определяем, какое значение изменилось
        try:
            new_value = float(item.text().replace(",", "")) if item.text() != "-" else None

            # Обновляем данные в соответствующей таблице
            data_item = self.get_data_item(row)
            if data_item:
                if item.column() == 1:  # Изменился отчетный год
                    data_item[str(selected_year)] = new_value if new_value is not None else 0
                elif item.column() == 2 and prev_year:  # Изменился предыдущий год
                    data_item[str(prev_year)] = new_value if new_value is not None else 0
        except ValueError:
            # Если введено некорректное значение, восстанавливаем предыдущее
            self.updating_table = True
            if item.column() == 1:
                data_item = self.get_data_item(row)
                if data_item:
                    current_val = data_item.get(str(selected_year), 0)
                    item.setText(f"{current_val:,}" if current_val is not None else "-")
            elif item.column() == 2:
                data_item = self.get_data_item(row)
                if data_item and prev_year:
                    prev_val = data_item.get(str(prev_year), 0)
                    item.setText(f"{prev_val:,}" if prev_val is not None else "-")
            self.updating_table = False
            return

        # Пересчитываем темп роста и абсолютное отклонение для этой строки
        self.update_row_calculations(row, selected_year, prev_year)

        # Если это таблица 1, пересчитываем коэффициенты
        if self.current_table == 1:
            self.update_coefficients(selected_year)

    def get_data_item(self, table_row):
        """Возвращает элемент данных, соответствующий строке в таблице"""
        current_data = self.data_table1 if self.current_table == 1 else self.data_table2
        data_row = table_row
        current_section = None

        # Корректируем индекс с учетом разделов
        for i, item in enumerate(current_data):
            if 'section' in item and item['section'] != current_section:
                current_section = item['section']
                data_row -= 1

            if data_row == i:
                return item

        return None

    def update_row_calculations(self, row, selected_year, prev_year):
        """Пересчитывает темп роста и абсолютное отклонение для указанной строки"""
        # Получаем соответствующий элемент данных
        data_item = self.get_data_item(row)
        if not data_item:
            return

        # Получаем значения
        current_val = data_item.get(str(selected_year), 0)
        prev_val = data_item.get(str(prev_year), 0) if prev_year else None

        # Преобразуем нули в None для отображения "-"
        current_val = current_val if current_val != 0 else None
        prev_val = prev_val if prev_val and prev_val != 0 else None

        # Устанавливаем флаг обновления таблицы
        self.updating_table = True

        # Обновляем темп роста
        if current_val and prev_val:
            growth = (current_val / prev_val) * 100 if prev_val != 0 else 0
            growth_text = f"{growth:.2f}%" if prev_val != 0 else "-"
        else:
            growth_text = "-"

        growth_item = QTableWidgetItem(growth_text)
        growth_item.setFlags(growth_item.flags() ^ Qt.ItemIsEditable)
        self.table.setItem(row, 3, growth_item)

        # Обновляем абсолютное отклонение
        if current_val is not None and prev_val is not None:
            deviation = current_val - prev_val
            deviation_text = f"{deviation:,}"
            deviation_item = QTableWidgetItem(deviation_text)
            # Раскраска
            if deviation < 0:
                deviation_item.setBackground(QColor(150, 50, 50))
            else:
                deviation_item.setBackground(QColor(50, 150, 50))
            deviation_item.setForeground(QColor(255, 255, 255))
        else:
            deviation_item = QTableWidgetItem("-")

        deviation_item.setFlags(deviation_item.flags() ^ Qt.ItemIsEditable)
        self.table.setItem(row, 4, deviation_item)

        # Снимаем флаг обновления таблицы
        self.updating_table = False

    def switch_table(self, table_num):
        self.current_table = table_num
        self.update_table()

    def load_data(self):
        """Загрузка данных из БД для обеих таблиц"""
        conn = sqlite3.connect('financial_data.db')
        cursor = conn.cursor()

        # Создаем таблицы, если их нет
        cursor.execute('''CREATE TABLE IF NOT EXISTS capital_data
                         (id INTEGER PRIMARY KEY, code TEXT, parameter TEXT, 
                         y2013 REAL, y2014 REAL, y2015 REAL, section TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS production_costs
                         (id INTEGER PRIMARY KEY, code TEXT, parameter TEXT, 
                         y2013 REAL, y2014 REAL, y2015 REAL, section TEXT)''')

        # Данные для таблицы 1 (Собственный капитал)
        table1_data = [
            ("010", "Остаток на 31.12.2013 года", 40255, 32846, 28015, "Основные данные"),
            ("020", "Корректировки (учетная политика)", 0, 0, 0, "Основные данные"),
            ("030", "Корректировки (исправление ошибок)", 0, 0, 0, "Основные данные"),
            ("040", "Скорректированный остаток на 31.12.2013 года", 40255, 32846, 28015, "Основные данные"),
            ("050", "Увеличение собственного капитала - всего", 0, 6500, 3552, "Основные данные"),
            ("051", "    В том числе: чистая прибыль", 0, 0, 0, "Основные данные"),
            ("052", "    переоценка долгосрочных активов", 0, 0, 0, "Основные данные"),
            ("053", "    доходы от прочих операций...", 0, 0, 0, "Основные данные"),
            ("054", "    выпуск дополнительных акций", 0, 6500, 3552, "Основные данные"),
            ("070", "Изменение уставного капитала", 0, 909, 1279, "Основные данные"),
            ("100", "Остаток на 31.12.2014 года", 40255, 40255, 32846, "Основные данные"),
            ("150", "Увеличение собственного капитала - всего", 0, 0, 6500, "Основные данные"),
            ("154", "    выпуск дополнительных акций", 0, 0, 6500, "Основные данные"),
            ("170", "Изменение уставного капитала", 0, 0, 909, "Основные данные"),
            ("200", "Остаток на 31.12.2015 года", 40255, 40255, 40255, "Основные данные"),
        ]

        # Данные для таблицы 2 (Затраты на производство)
        table2_data = [
            # Раздел I
            ("001",
             "Объем производства продукции (работ, услуг) в отпускных ценах за вычетом налогов и сборов, исчисляемых из выручки",
             552219, 444964, 420396, "Раздел I"),
            ("002", "Затраты на производство продукции (работ, услуг)", 390660, 329104, 275832, "Раздел I"),
            ("003", "материальные затраты", 219913, 170476, 182752, "Раздел I"),
            ("004", "сырье, материалы, покупные комплектующие изделия и полуфабрикаты", 179129, 136870, 143680,
             "Раздел I"),
            ("005", "из них импортные", 141298, 111927, 117322, "Раздел I"),
            ("006", "топливо", 18184, 12099, 20655, "Раздел I"),
            ("007", "из него импортное", 16672, 10684, 19904, "Раздел I"),
            ("008", "электрическая энергия", 19284, 18258, 15607, "Раздел I"),
            ("009", "тепловая энергия", 1604, 1225, 1355, "Раздел I"),
            ("010", "затраты на оплату труда", 90033, 82560, 58000, "Раздел I"),
            ("011", "отчисления на социальные нужды", 28129, 25347, 18512, "Раздел I"),
            ("012",
             "амортизация основных средств и нематериальных активов, используемых в предпринимательской деятельности",
             34224, 34398, 1577, "Раздел I"),
            ("013", "амортизация основных средств", 33537, 33757, 1134, "Раздел I"),
            ("014", "амортизация нематериальных активов", 687, 641, 443, "Раздел I"),
            ("015", "прочие затраты", 18361, 16323, 14991, "Раздел I"),
            ("016", "расходы на рекламу - всего", 114, 10, 90, "Раздел I"),
            ("017", "из них на: наружную", 0, 0, 0, "Раздел I"),
            ("018", "телевизионную", 0, 0, 0, "Раздел I"),
            ("019", "интернет-рекламу", 0, 0, 0, "Раздел I"),
            ("203", "Плата за природные ресурсы (из строки 003)", 291, 229, 226, "Раздел I"),
            ("215", "Отдельные статьи затрат (из строки 015)", 13921, 12598, 10447, "Раздел I"),

            # Раздел II
            ("020",
             "Объем производства продукции (работ, услуг) в отпускных ценах за вычетом налогов и сборов, исчисляемых из выручки",
             454453, 389711, 342288, "Раздел II"),
            ("021", "Затраты на производство продукции (работ, услуг)", 313933, 287262, 219072, "Раздел II"),
            ("022", "материальные затраты", 176457, 148361, 145344, "Раздел II"),
            ("023", "сырье и материалы", 65941, 46936, 53868, "Раздел II"),
            ("024", "покупные комплектующие изделия и полуфабрикаты", 77469, 71642, 59932, "Раздел II"),
            ("025", "работы (услуги) производственного характера, выполненные другими организациями", 921, 1527, 981,
             "Раздел II"),
            ("026", "перевозка грузов", 0, 0, 0, "Раздел II"),
            ("027", "текущий и капитальный ремонт зданий и сооружений", 460, 725, 235, "Раздел II"),
            ("028", "техническое обслуживание и ремонт офисных машин и вычислительной техники", 58, 78, 39,
             "Раздел II"),
            ("029", "техническое обслуживание и ремонт автомобилей и мотоциклов", 403, 724, 707, "Раздел II"),
            ("030", "топливо", 14854, 10741, 16692, "Раздел II"),
            ("031", "электрическая энергия", 15747, 16196, 12595, "Раздел II"),
            ("032", "тепловая энергия", 1295, 1138, 1099, "Раздел II"),
            ("033", "прочие материальные затраты", 230, 181, 177, "Раздел II"),
            ("034", "плата за природные ресурсы", 230, 181, 177, "Раздел II"),
            ("035", "налог на добавленную стоимость, включенный в затраты", 0, 0, 0, "Раздел II"),
            ("036", "затраты на оплату труда", 72225, 71987, 45944, "Раздел II"),
            ("037", "из них расходы на форменную и фирменную одежду, обмундирование", 0, 0, 0, "Раздел II"),
            ("038", "отчисления на социальные нужды", 22536, 22059, 14629, "Раздел II"),
            ("039",
             "амортизация основных средств и нематериальных активов, используемых в предпринимательской деятельности",
             27868, 30571, 1266, "Раздел II"),
            ("040", "прочие затраты", 14847, 14284, 11889, "Раздел II"),
            ("041", "арендная плата", 104, 114, 172, "Раздел II"),
            ("042", "вознаграждения за рационализаторские предложения и выплата авторских гонораров", 0, 0, 0,
             "Раздел II"),
            ("043", "суточные и подъемные", 1209, 148, 512, "Раздел II"),
            ("044",
             "начисленные налоги, сборы (пошлины), платежи, включаемые в затраты на производство продукции (работ, услуг)",
             1704, 1977, 1870, "Раздел II"),
            ("045", "представительские расходы", 10, 11, 10, "Раздел II"),
            ("046", "услуги других организаций", 11284, 11043, 8207, "Раздел II"),
            ("047", "гостиниц и прочих мест временного проживания", 263, 135, 45, "Раздел II"),
            ("048", "пассажирского транспорта", 104, 151, 71, "Раздел II"),
            ("049", "связи", 261, 297, 287, "Раздел II"),
            ("050", "по созданию и обновлению web-сайтов", 0, 0, 0, "Раздел II"),
            ("051", "по научным разработкам", 0, 0, 0, "Раздел II"),
            ("052", "по охране имущества", 143, 186, 53, "Раздел II"),
            ("053", "банков и небанковских кредитно-финансовых организаций", 1406, 1174, 593, "Раздел II"),
            ("054", "консультационные, аудиторские", 107, 320, 785, "Раздел II"),
            ("055", "по уборке территории, сбору и вывозу отходов", 390, 407, 381, "Раздел II"),
            ("056", "образования", 107, 34, 39, "Раздел II"),
            ("057", "здравоохранения", 64, 117, 100, "Раздел II"),
            ("058", "другие затраты", 536, 991, 1118, "Раздел II"),
            ("059",
             "Прирост (+) или уменьшение (–) остатка незавершенного производства, полуфабрикатов и приспособлений собственной выработки, не включаемых в стоимость продукции",
             -6219, -6416, 3787, "Раздел II"),
            ("060", "Внутризаводской оборот, включаемый в затраты на производство продукции (работ, услуг)", 0, 0, 0,
             "Раздел II"),
            ("061", "Внутризаводской оборот, включаемый в объем продукции (работ, услуг)", 0, 0, 0, "Раздел II"),
            ("062", "Командировочные расходы", 1425, 1604, 1154, "Раздел II"),
            ("063", "семена и посадочный материал", 0, 0, 0, "Раздел II"),
            ("064", "из них покупные", 0, 0, 0, "Раздел II"),
            ("065", "корма", 0, 0, 0, "Раздел II"),
            ("066", "из них покупные", 0, 0, 0, "Раздел II"),
            ("067", "минеральные удобрения", 0, 0, 0, "Раздел II"),
            ("068", "средства защиты растений и животных", 0, 0, 0, "Раздел II"),
            ("069", "подстилка, яйцо для инкубации, навоз", 0, 0, 0, "Раздел II"),

            # Раздел IV
            ("110", "Продукты и услуги сельского хозяйства и охоты", 0, 0, 0, "Раздел IV"),
            ("111", "Продукты и услуги лесного хозяйства", 5, 5, 6, "Раздел IV"),
            ("112", "Продукты и услуги рыболовства и рыбоводства", 0, 0, 0, "Раздел IV"),
            ("113", "Уголь", 0, 0, 0, "Раздел IV"),
            ("114", "Торф", 0, 0, 0, "Раздел IV"),
            ("115", "Сырая нефть и природный газ", 14218, 0, 0, "Раздел IV"),
            ("116", "Металлические руды и прочие продукты горнодобывающей промышленности", 263, 263, 270, "Раздел IV"),
            ("117", "Пищевые продукты, включая напитки, табачные изделия", 130, 130, 250, "Раздел IV"),
            ("118", "Продукты и услуги текстильного производства, одежда, меха и меховые изделия", 880, 1062, 986,
             "Раздел IV"),
            ("119", "Кожа, изделия из кожи, обувь", 0, 0, 0, "Раздел IV"),
            ("120",
             "Продукты обработки древесины, изделия из дерева и пробки, кроме мебели, изделия из соломки и материалов для плетения",
             47, 47, 202, "Раздел IV"),
            ("121",
             "Целлюлоза, древесная масса, бумага, картон и изделия из них. Издательская и полиграфическая продукция",
             13981, 2820, 4188, "Раздел IV"),
            ("122", "Кокс, ядерные материалы", 0, 0, 0, "Раздел IV"),
            ("123", "Нефтепродукты", 1774, 24, 28, "Раздел IV"),
            ("124", "Химическая продукция", 16291, 1417, 2755, "Раздел IV"),
            ("125", "Резиновые и пластмассовые изделия", 50, 27, 112, "Раздел IV"),
            ("126", "Прочие неметаллические минеральные продукты", 39973, 4915, 3817, "Раздел IV"),
            ("127", "Продукты и услуги металлургического производства и готовые металлические изделия", 38425, 19009,
             13939, "Раздел IV"),
            ("128", "Машины и оборудование", 4168, 3448, 1944, "Раздел IV"),
            ("129", "Электрическое оборудование, электронное и оптическое оборудование", 528, 1824, 254, "Раздел IV"),
            ("130", "Транспортные средства и оборудование", 204, 438, 527, "Раздел IV"),
            ("131", "Мебель и прочая промышленная продукция, не включенная в другие строки. Обработка вторичного сырья",
             0, 0, 0, "Раздел IV"),
            ("132", "Электрическая энергия, газообразное топливо, пар и горячая вода", 13694, 0, 0, "Раздел IV"),
            ("133", "Услуги по сбору, очистке и распределению воды", 0, 0, 0, "Раздел IV"),
            ("134", "Всего (сумма строк с 110 по 133)", 144186, 35429, 29278, "Раздел IV"),
        ]

        # Очищаем таблицы перед вставкой новых данных
        cursor.execute("DELETE FROM capital_data")
        cursor.execute("DELETE FROM production_costs")

        # Вставляем данные для таблицы 1
        for row in table1_data:
            cursor.execute(
                'INSERT INTO capital_data (code, parameter, y2013, y2014, y2015, section) VALUES (?,?,?,?,?,?)', row)

        # Вставляем данные для таблицы 2
        for row in table2_data:
            cursor.execute(
                'INSERT INTO production_costs (code, parameter, y2013, y2014, y2015, section) VALUES (?,?,?,?,?,?)',
                row)

        conn.commit()

        # Загрузка данных таблицы 1 с сохранением порядка
        cursor.execute("SELECT code, parameter, y2013, y2014, y2015, section FROM capital_data ORDER BY id")
        self.data_table1 = [{
            'code': row[0],
            'parameter': row[1],
            '2013': row[2],
            '2014': row[3],
            '2015': row[4],
            'section': row[5]
        } for row in cursor.fetchall()]

        # Загрузка данных таблицы 2 с сохранением порядка
        cursor.execute("SELECT code, parameter, y2013, y2014, y2015, section FROM production_costs ORDER BY id")
        self.data_table2 = [{
            'code': row[0],
            'parameter': row[1],
            '2013': row[2],
            '2014': row[3],
            '2015': row[4],
            'section': row[5]
        } for row in cursor.fetchall()]

        conn.close()

    def update_table(self):
        selected_year = int(self.year_combo.currentText())
        prev_year = selected_year - 1 if selected_year > 2013 else None

        # Очищаем таблицу перед заполнением
        self.table.clearContents()

        # Выбираем нужный набор данных в зависимости от текущей таблицы
        current_data = self.data_table1 if self.current_table == 1 else self.data_table2

        # Сначала подсчитаем общее количество строк с учетом разделов
        total_rows = len(current_data)
        current_section = None
        sections_count = 0

        # Подсчитываем количество разделов
        for item in current_data:
            if 'section' in item and item['section'] != current_section:
                current_section = item['section']
                sections_count += 1

        total_rows += sections_count  # Добавляем строки для разделов

        # Добавляем строки для коэффициентов (только для таблицы 1)
        if self.current_table == 1:
            total_rows += 4  # 1 пустая строка + 3 строки коэффициентов

        self.table.setRowCount(total_rows)

        current_section = None
        row_idx = 0

        # Устанавливаем флаг обновления таблицы
        self.updating_table = True

        for item in current_data:
            # Проверяем, нужно ли добавить разделитель раздела
            if 'section' in item and item['section'] != current_section:
                current_section = item['section']
                # Добавляем строку с названием раздела
                section_item = QTableWidgetItem(current_section)
                section_item.setFlags(section_item.flags() ^ Qt.ItemIsEditable)
                font = QFont()
                font.setBold(True)
                section_item.setFont(font)
                section_item.setBackground(QColor(70, 70, 70))
                self.table.setItem(row_idx, 0, section_item)
                # Объединяем ячейки для названия раздела
                self.table.setSpan(row_idx, 0, 1, 5)
                row_idx += 1

            # Заполняем строку данными
            # Показатель
            param_item = QTableWidgetItem(item['parameter'])
            param_item.setFlags(param_item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row_idx, 0, param_item)

            # Отчетный год
            current_val = item.get(str(selected_year), 0)
            current_item = QTableWidgetItem(f"{current_val:,}" if current_val != 0 else "-")
            current_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 1, current_item)

            # Предыдущий год
            if prev_year:
                prev_val = item.get(str(prev_year), 0)
                prev_item = QTableWidgetItem(f"{prev_val:,}" if prev_val != 0 else "-")
            else:
                prev_item = QTableWidgetItem("-")
            prev_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 2, prev_item)

            # Темп роста
            if prev_year and current_val and prev_val and prev_val != 0:
                growth = (current_val / prev_val) * 100
                growth_item = QTableWidgetItem(f"{growth:.2f}%")
            else:
                growth_item = QTableWidgetItem("-")
            growth_item.setFlags(growth_item.flags() ^ Qt.ItemIsEditable)
            growth_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 3, growth_item)

            # Абсолютное отклонение
            if prev_year and current_val is not None and prev_val is not None:
                deviation = current_val - prev_val
                deviation_item = QTableWidgetItem(f"{deviation:,}")
                # Раскраска
                if deviation < 0:
                    deviation_item.setBackground(QColor(150, 50, 50))
                else:
                    deviation_item.setBackground(QColor(50, 150, 50))
                deviation_item.setForeground(QColor(255, 255, 255))
            else:
                deviation_item = QTableWidgetItem("-")
            deviation_item.setFlags(deviation_item.flags() ^ Qt.ItemIsEditable)
            deviation_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row_idx, 4, deviation_item)

            row_idx += 1

        # Добавляем коэффициенты только для таблицы 1
        if self.current_table == 1:
            # Пустая строка для разделения
            empty_item = QTableWidgetItem("")
            empty_item.setFlags(empty_item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row_idx, 0, empty_item)
            row_idx += 1

            # Рассчитываем коэффициенты
            k1, k2, liquidity = self.calculate_coefficients(selected_year)

            # Создаем список коэффициентов для удобного добавления
            coefficients = [
                ("K1 (Обязательства / Активы)", k1),
                ("K2 (Непросроченные обязательства / Общие обязательства)", k2),
                ("Ликвидность (Ден.средства + Фин.вложения / Краткосрочные обязательства)", liquidity)
            ]

            font = QFont()
            font.setBold(True)

            # Добавляем коэффициенты
            for name, value in coefficients:
                # Название коэффициента
                name_item = QTableWidgetItem(name)
                name_item.setFlags(name_item.flags() ^ Qt.ItemIsEditable)
                name_item.setFont(font)
                name_item.setBackground(QColor(70, 70, 70))
                self.table.setItem(row_idx, 0, name_item)

                # Значение коэффициента
                value_item = QTableWidgetItem(f"{value:.4f}")
                value_item.setFlags(value_item.flags() ^ Qt.ItemIsEditable)
                value_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row_idx, 1, value_item)
                row_idx += 1

        # Снимаем флаг обновления таблицы
        self.updating_table = False

    def calculate_coefficients(self, year):
        """Рассчитывает коэффициенты K1, K2 и ликвидности для указанного года"""
        year_str = str(year)

        # Находим нужные значения в данных таблицы 1
        # Активы - берем остаток на конец года (строка с кодом 200)
        assets = 0
        for item in self.data_table1:
            if item['code'] == '200':  # Остаток на конец года
                assets = item.get(year_str, 0)
                break

        # Обязательства - берем сумму всех корректировок и изменений
        # Для простоты будем считать их как разницу между увеличением капитала и остатком
        # В реальном приложении нужно использовать точные формулы
        total_liabilities = 0
        for item in self.data_table1:
            if item['code'] in ['050', '070', '150', '170']:  # Строки с изменениями капитала
                total_liabilities += abs(item.get(year_str, 0))

        # Краткосрочные обязательства - часть от общих обязательств (30%)
        short_term_liabilities = total_liabilities * 0.3

        # Денежные средства - берем 10% от активов (в реальном приложении нужно брать из данных)
        cash = assets * 0.1

        # Финансовые вложения - берем 5% от активов
        financial_investments = assets * 0.05

        # Непросроченные обязательства - 80% от общих обязательств
        non_overdue_liabilities = total_liabilities * 0.8

        # Рассчитываем коэффициенты
        try:
            # K1 = Обязательства / Активы
            k1 = total_liabilities / assets if assets != 0 else 0

            # K2 = Непросроченные обязательства / Общие обязательства
            k2 = non_overdue_liabilities / total_liabilities if total_liabilities != 0 else 0

            # Ликвидность = (Денежные средства + Фин.вложения) / Краткосрочные обязательства
            liquidity = (cash + financial_investments) / short_term_liabilities if short_term_liabilities != 0 else 0
        except ZeroDivisionError:
            k1, k2, liquidity = 0, 0, 0

        return k1, k2, liquidity

    def update_coefficients(self, selected_year):
        """Обновляет только строки с коэффициентами"""
        if not self.current_table == 1:
            return

        # Рассчитываем коэффициенты
        k1, k2, liquidity = self.calculate_coefficients(selected_year)
        coefficients = [k1, k2, liquidity]

        # Устанавливаем флаг обновления таблицы
        self.updating_table = True

        # Находим строки с коэффициентами (последние 3 строки)
        start_row = self.table.rowCount() - 3

        for i in range(3):
            row = start_row + i
            if row >= 0 and self.table.item(row, 1) is not None:
                self.table.item(row, 1).setText(f"{coefficients[i]:.4f}")

        # Снимаем флаг обновления таблицы
        self.updating_table = False

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
            QPushButton {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                min-width: 150px;
            }
            QPushButton:checked {
                background-color: #4CAF50;
                font-weight: bold;
            }
        """)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
							   QLabel, QLineEdit, QPushButton, QMessageBox, QDialog)
from PySide6.QtCore import Qt
import os
from src.database.database import add_user, check_user
from src.ui.main_window import MainWindow


class RegisterWindow(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle("Регистрация")
		self.setWindowState(Qt.WindowMaximized)  # Полноэкранный режим
		self.setup_ui()
		self.apply_styles()

	def setup_ui(self):
		# Главный контейнер для центрирования
		main_widget = QWidget()
		main_layout = QVBoxLayout(main_widget)
		main_layout.setAlignment(Qt.AlignCenter)

		# Контейнер формы с фиксированной шириной
		form_widget = QWidget()
		form_widget.setFixedWidth(400)  # Фиксированная ширина формы
		form_layout = QVBoxLayout(form_widget)
		form_layout.setSpacing(20)
		form_layout.setContentsMargins(0, 0, 0, 0)

		# Элементы формы
		title = QLabel("Создание аккаунта")
		title.setAlignment(Qt.AlignCenter)

		self.username_input = QLineEdit()
		self.username_input.setPlaceholderText("Придумайте логин")
		self.username_input.setMinimumHeight(45)

		self.password_input = QLineEdit()
		self.password_input.setPlaceholderText("Придумайте пароль")
		self.password_input.setEchoMode(QLineEdit.Password)
		self.password_input.setMinimumHeight(45)

		self.confirm_password_input = QLineEdit()
		self.confirm_password_input.setPlaceholderText("Повторите пароль")
		self.confirm_password_input.setEchoMode(QLineEdit.Password)
		self.confirm_password_input.setMinimumHeight(45)

		self.register_button = QPushButton("Создать аккаунт")
		self.register_button.setMinimumHeight(45)

		# Добавление элементов
		form_layout.addWidget(title)
		form_layout.addWidget(self.username_input)
		form_layout.addWidget(self.password_input)
		form_layout.addWidget(self.confirm_password_input)
		form_layout.addWidget(self.register_button)

		# Центрирование формы
		main_layout.addWidget(form_widget)

		# Установка главного виджета
		self.setLayout(QVBoxLayout())
		self.layout().addWidget(main_widget)
		self.layout().setContentsMargins(0, 0, 0, 0)

		# Подключение сигналов
		self.register_button.clicked.connect(self.on_register)

	def apply_styles(self):
		self.setStyleSheet("""
            QDialog {
                background-color: #252525;
            }
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #4CAF50;
                margin-bottom: 10px;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 16px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

	def on_register(self):
		username = self.username_input.text()
		password = self.password_input.text()
		confirm_password = self.confirm_password_input.text()

		if not username or not password or not confirm_password:
			QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
			return

		if len(username) < 4:
			QMessageBox.warning(self, "Ошибка", "Логин должен содержать минимум 4 символа")
			return

		if len(password) < 6:
			QMessageBox.warning(self, "Ошибка", "Пароль должен содержать минимум 6 символов")
			return

		if password != confirm_password:
			QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
			return

		if add_user(username, password):
			QMessageBox.information(self, "Успех", "Аккаунт успешно создан!")
			self.close()
		else:
			QMessageBox.warning(self, "Ошибка", "Пользователь с таким логином уже существует")


class LoginWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Авторизация")
		self.setWindowState(Qt.WindowMaximized)  # Полноэкранный режим
		self.setup_ui()
		self.apply_styles()

	def setup_ui(self):
		# Главный контейнер для центрирования
		main_widget = QWidget()
		main_layout = QVBoxLayout(main_widget)
		main_layout.setAlignment(Qt.AlignCenter)

		# Контейнер формы с фиксированной шириной
		form_widget = QWidget()
		form_widget.setFixedWidth(450)  # Фиксированная ширина формы
		form_layout = QVBoxLayout(form_widget)
		form_layout.setSpacing(25)
		form_layout.setContentsMargins(0, 0, 0, 0)

		# Элементы формы
		title = QLabel("Добро пожаловать")
		title.setAlignment(Qt.AlignCenter)

		self.username_input = QLineEdit()
		self.username_input.setPlaceholderText("Введите ваш логин")
		self.username_input.setMinimumHeight(45)

		self.password_input = QLineEdit()
		self.password_input.setPlaceholderText("Введите ваш пароль")
		self.password_input.setEchoMode(QLineEdit.Password)
		self.password_input.setMinimumHeight(45)

		self.login_button = QPushButton("Войти в систему")
		self.login_button.setMinimumHeight(45)
		self.login_button.setObjectName("login_button")

		self.register_button = QPushButton("Создать новый аккаунт")
		self.register_button.setMinimumHeight(45)
		self.register_button.setObjectName("register_button")

		# Добавление элементов
		form_layout.addWidget(title)
		form_layout.addWidget(self.username_input)
		form_layout.addWidget(self.password_input)
		form_layout.addWidget(self.login_button)
		form_layout.addWidget(self.register_button)

		# Центрирование формы
		main_layout.addWidget(form_widget)

		# Установка центрального виджета
		self.setCentralWidget(main_widget)

		# Подключение сигналов
		self.login_button.clicked.connect(self.on_login)
		self.register_button.clicked.connect(self.show_register_window)

	def apply_styles(self):
		self.setStyleSheet("""
            QMainWindow {
                background-color: #252525;
            }
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #4CAF50;
                margin-bottom: 20px;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 16px;
            }
            QPushButton {
                min-width: 100%;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            #login_button {
                background-color: #4CAF50;
                color: white;
                border: none;
            }
            #login_button:hover {
                background-color: #45a049;
            }
            #register_button {
                background-color: transparent;
                color: #4CAF50;
                border: 2px solid #4CAF50;
            }
            #register_button:hover {
                background-color: rgba(76, 175, 80, 0.1);
            }
        """)

	def on_login(self):
		username = self.username_input.text()
		password = self.password_input.text()

		if not username or not password:
			QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля")
			return

		if check_user(username, password):
			self.open_main_window()
		else:
			QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

	def show_register_window(self):
		self.register_window = RegisterWindow(self)
		self.register_window.exec_()

	def open_main_window(self):
		self.main_window = MainWindow()
		self.main_window.show()
		self.close()


if __name__ == "__main__":
	app = QApplication([])
	app.setStyle("Fusion")

	window = LoginWindow()
	window.show()
	app.exec()
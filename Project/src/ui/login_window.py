# login_window.py
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
		self.setFixedSize(600, 500)
		self.setup_ui()
		self.apply_styles()

	def setup_ui(self):
		layout = QVBoxLayout()
		layout.setContentsMargins(40, 40, 40, 40)
		layout.setSpacing(20)

		title = QLabel("Создание аккаунта")
		title.setAlignment(Qt.AlignCenter)

		self.username_input = QLineEdit()
		self.username_input.setPlaceholderText("Придумайте логин")

		self.password_input = QLineEdit()
		self.password_input.setPlaceholderText("Придумайте пароль")
		self.password_input.setEchoMode(QLineEdit.Password)

		self.confirm_password_input = QLineEdit()
		self.confirm_password_input.setPlaceholderText("Повторите пароль")
		self.confirm_password_input.setEchoMode(QLineEdit.Password)

		self.register_button = QPushButton("Создать аккаунт")

		layout.addWidget(title)
		layout.addWidget(self.username_input)
		layout.addWidget(self.password_input)
		layout.addWidget(self.confirm_password_input)
		layout.addWidget(self.register_button)

		self.setLayout(layout)
		self.register_button.clicked.connect(self.on_register)

	def apply_styles(self):
		self.setStyleSheet("""
            QDialog {
                background-color: #252525;
                color: #ffffff;
                font-family: 'Segoe UI';
            }
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #4CAF50;
                margin-bottom: 20px;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                min-width: 300px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 20px;
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
		self.setFixedSize(600, 500)
		self.setup_ui()
		self.apply_styles()

	def setup_ui(self):
		central_widget = QWidget()
		self.setCentralWidget(central_widget)

		layout = QVBoxLayout()
		layout.setContentsMargins(60, 60, 60, 60)
		layout.setSpacing(30)

		title = QLabel("Добро пожаловать")
		title.setAlignment(Qt.AlignCenter)

		self.username_input = QLineEdit()
		self.username_input.setPlaceholderText("Введите ваш логин")

		self.password_input = QLineEdit()
		self.password_input.setPlaceholderText("Введите ваш пароль")
		self.password_input.setEchoMode(QLineEdit.Password)

		self.login_button = QPushButton("Войти в систему")
		self.register_button = QPushButton("Создать новый аккаунт")

		layout.addWidget(title)
		layout.addWidget(self.username_input)
		layout.addWidget(self.password_input)
		layout.addWidget(self.login_button)
		layout.addWidget(self.register_button)

		central_widget.setLayout(layout)

		self.login_button.clicked.connect(self.on_login)
		self.register_button.clicked.connect(self.show_register_window)

	def apply_styles(self):
		self.setStyleSheet("""
            QMainWindow {
                background-color: #252525;
                color: #ffffff;
                font-family: 'Segoe UI';
            }
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #4CAF50;
                margin-bottom: 30px;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 14px;
                font-size: 16px;
                min-width: 350px;
            }
            QPushButton {
                min-width: 350px;
                padding: 16px;
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
		# Назначаем objectName для кнопок
		self.login_button.setObjectName("login_button")
		self.register_button.setObjectName("register_button")

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
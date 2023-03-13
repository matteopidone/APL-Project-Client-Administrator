from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PySide6.QtGui import QFont
import requests
import os

class LoginWindow(QWidget):

	def __init__(self):
		# Costruttore classe padre e inizializzazione attributi
		super().__init__()

		# Definisco lo stile
		self.setWindowTitle("Administrator Login")
		self.resize(400, 200)
		self.setFont(QFont("Arial", 20))

		# Input email
		email_label = QLabel("Email:")
		self.email_input = QLineEdit()

		# Input password
		password_label = QLabel("Password:")
		self.password_input = QLineEdit()
		self.password_input.setEchoMode(QLineEdit.Password)

		# Bottone login
		login_button = QPushButton("Login")
		login_button.clicked.connect(self.login)

		# Inserimento dei widgets
		layout = QVBoxLayout()
		layout.addWidget(email_label)
		layout.addWidget(self.email_input)
		layout.addWidget(password_label)
		layout.addWidget(self.password_input)
		layout.addWidget(login_button)

		self.setLayout(layout)

	def login(self):
		url_login = os.environ.get('URL_LOGIN')
		email = self.email_input.text()
		password = self.password_input.text()

		obj = {'email': email, 'password': password}
		response = requests.post(url=url_login, json=obj)

		if response.status_code == 200:
			print("Login successful!")
		else:
			print("Login failed.")

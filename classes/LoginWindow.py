from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PySide6.QtGui import QFont, QColor
import requests
import os

class LoginWindow(QWidget):

	def __init__(self, dispatcher):
		# Costruttore classe padre e inizializzazione attributi
		super().__init__()

		# Inizializzo il riferimento al Dispatcher
		self.dispatcher = dispatcher

		# Definisco lo stile
		self.setWindowTitle("Administrator Login")
		self.resize(400, 200)
		self.setFont(QFont("Arial", 20))

		self.create_interface()

	# Funzione per la generazione dell'interfaccia grafica
	def create_interface(self):
		# Input email
		email_label = QLabel("Email:")
		self.email_input = QLineEdit()

		# Input password
		password_label = QLabel("Password:")
		self.password_input = QLineEdit()
		self.password_input.setEchoMode(QLineEdit.Password)

		# Messaggio errore nascosto
		self.error_label = QLabel("Credenziali errate")
		self.error_label.hide()
		self.error_label.setAlignment(Qt.AlignCenter)
		self.error_label.setFont(QFont("Arial", 20))
		self.error_label.setStyleSheet("color: red")

		# Bottone login
		login_button = QPushButton("Login")
		login_button.clicked.connect(self.login)

		# Inserimento dei widgets
		layout = QVBoxLayout()
		layout.addWidget(email_label)
		layout.addWidget(self.email_input)
		layout.addWidget(password_label)
		layout.addWidget(self.password_input)
		layout.addWidget(self.error_label)
		layout.addWidget(login_button)

		self.setLayout(layout)

	# Funzione per la gestione del login
	def login(self):
		url_login = os.environ.get('URL_LOGIN')
		email = self.email_input.text()
		password = self.password_input.text()

		obj = {'email': email, 'password': password}
		response = requests.post(url=url_login, json=obj)

		if response.status_code == 200:
			self.close()
			self.dispatcher.get_window('HomeWindow').show()
		else:
			self.error_label.show()
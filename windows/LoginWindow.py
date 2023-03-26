from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PySide6.QtGui import QFont
import requests
import os

from classes.EnumState import UserState

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

	# Override funzione show per creare prima l'interfaccia
	def show(self):
		self.create_interface()
		super().show()

	# Funzione per la generazione dell'interfaccia grafica
	def create_interface(self):
		# Input email
		email_label = QLabel("Email:")
		self.email_input = QLineEdit()

		# Input password
		password_label = QLabel("Password:")
		self.password_input = QLineEdit()
		self.password_input.setEchoMode(QLineEdit.Password)

		# Messaggio errore login
		self.error_login_label = QLabel("Credenziali errate")
		self.error_login_label.hide()
		self.error_login_label.setAlignment(Qt.AlignCenter)
		self.error_login_label.setFont(QFont("Arial", 20))
		self.error_login_label.setStyleSheet("color: red")

		# Messaggio errore server
		self.error_server_label = QLabel("Server non disponibile")
		self.error_server_label.hide()
		self.error_server_label.setAlignment(Qt.AlignCenter)
		self.error_server_label.setFont(QFont("Arial", 20))
		self.error_server_label.setStyleSheet("color: red")

		# Bottone login
		login_button = QPushButton("Login")
		login_button.clicked.connect(self.login)

		# Inserimento dei widgets
		layout = QVBoxLayout()
		layout.addWidget(email_label)
		layout.addWidget(self.email_input)
		layout.addWidget(password_label)
		layout.addWidget(self.password_input)
		layout.addWidget(self.error_login_label)
		layout.addWidget(self.error_server_label)
		layout.addWidget(login_button)

		self.setLayout(layout)

	# Funzione per la gestione del login
	def login(self):
		self.error_login_label.hide()
		self.error_server_label.hide()

		# Creo un timer per nascondere il messaggio di errore
		timer = QTimer(self)
		timer.setSingleShot(True)

		url_login = os.environ.get('URL_LOGIN')
		email = self.email_input.text()
		password = self.password_input.text()
		role = str(UserState.Admin.value)

		obj = {'email': email, 'password': password, 'role': role}

		try:
			response = requests.post(url=url_login, json=obj)

			if response.status_code == 200:
				admin = self.dispatcher.get_class('Admin')
				data = response.json()
				admin.set_token(data['token'])
				admin.set_email(data['email'])

				self.close()
				self.dispatcher.get_class('HomeWindow').show()
			else:
				self.error_login_label.show()
				timer.timeout.connect(self.error_login_label.hide)
				timer.start(3000)

		except requests.exceptions.RequestException:
			# Gestione dell'eccezione
			print("Impossibile connettersi al server.")
			self.error_server_label.show()
			timer.timeout.connect(self.error_server_label.hide)
			timer.start(3000)

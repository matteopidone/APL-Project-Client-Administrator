from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PySide6.QtGui import QFont
import requests
import os

from classes.EnumState import UserState

class NewEmployeeWindow(QWidget):

	def __init__(self, dispatcher):
		# Costruttore classe padre e inizializzazione attributi
		super().__init__()

		# Inizializzo il riferimento al Dispatcher
		self.dispatcher = dispatcher
		self.interface_created = False

		# Definisco lo stile
		self.setWindowTitle("Nuovo Dipendente")
		self.resize(500, 400)
		self.setFont(QFont("Arial", 20))

	# Override funzione show per creare prima l'interfaccia
	def show(self):
		if not self.interface_created:
			self.create_interface()
			self.interface_created = True
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

		# Input nome
		name_label = QLabel("Nome:")
		self.name_input = QLineEdit()

		# Input cognome
		surname_label = QLabel("Cognome:")
		self.surname_input = QLineEdit()

		# Input descrizione
		description_label = QLabel("Descrizione:")
		self.description_input = QLineEdit()

		# Messaggio errore inserimento
		self.error_add_label = QLabel("Errore inserimento")
		self.error_add_label.hide()
		self.error_add_label.setAlignment(Qt.AlignCenter)
		self.error_add_label.setFont(QFont("Arial", 20))
		self.error_add_label.setStyleSheet("color: red")

		# Messaggio inserimento con successo
		self.success_add_label = QLabel("Dipendente inserito")
		self.success_add_label.hide()
		self.success_add_label.setAlignment(Qt.AlignCenter)
		self.success_add_label.setFont(QFont("Arial", 20))
		self.success_add_label.setStyleSheet("color: green")

		# Bottone aggiungi
		add_button = QPushButton("Aggiungi Dipendente")
		add_button.clicked.connect(self.addEmployee)

		# Inserimento dei widgets
		layout = QVBoxLayout()
		layout.addWidget(email_label)
		layout.addWidget(self.email_input)
		layout.addWidget(password_label)
		layout.addWidget(self.password_input)
		layout.addWidget(name_label)
		layout.addWidget(self.name_input)
		layout.addWidget(surname_label)
		layout.addWidget(self.surname_input)
		layout.addWidget(description_label)
		layout.addWidget(self.description_input)
		layout.addWidget(self.error_add_label)
		layout.addWidget(self.success_add_label)
		layout.addWidget(add_button)

		self.setLayout(layout)

	# Funzione per l'inserimento di un nuovo dipendente
	def addEmployee(self):
		self.error_add_label.hide()
		self.success_add_label.hide()

		# Creo un timer per nascondere il messaggio di successo/errore
		timer = QTimer(self)
		timer.setSingleShot(True)

		admin = self.dispatcher.get_class("Admin")

		# Recupero i valori di input
		email = self.email_input.text()
		password = self.password_input.text()
		name = self.name_input.text()
		surname = self.surname_input.text()
		description = self.description_input.text()

		if not email or not password or not name or not surname:
			self.error_add_label.show()
			timer.timeout.connect(self.error_add_label.hide)
			timer.start(3000)
			return

		# Preparo la request
		headers = {'Authorization': 'Bearer ' + admin.get_token()}
		url = os.environ.get('URL_INSERT_USER')
		json = {'email': email, 'password': password, 'name': name, 'surname': surname, 'description': description, 'role': UserState.Employee.value}

		try:
			response = requests.post(url=url, json=json, headers=headers)

			if response.status_code == 200:
				self.error_add_label.hide()
				self.success_add_label.show()
				timer.timeout.connect(self.success_add_label.hide)
				timer.start(3000)

				# Svuoto i valori di input
				self.email_input.clear()
				self.password_input.clear()
				self.name_input.clear()
				self.surname_input.clear()
				self.description_input.clear()

				# Aggiungo il dipendente all'elenco
				admin.add_employee({'email': email, 'name': name, 'surname': surname, 'description': description})
			else:
				self.error_add_label.show()
				self.success_add_label.hide()
				timer.timeout.connect(self.error_add_label.hide)
				timer.start(3000)

		except requests.exceptions.RequestException:
			# Gestione dell'eccezione
			print("Impossibile connettersi al server.")
			self.error_add_label.show()
			self.success_add_label.hide()
			timer.timeout.connect(self.error_add_label.hide)
			timer.start(3000)

from PySide6.QtWidgets import QWidget
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

		# Definisco lo stile
		self.setWindowTitle("Nuovo Dipendente")
		#self.resize(400, 200)
		self.setFont(QFont("Arial", 20))

	# Override funzione show per creare prima l'interfaccia
	def show(self):
		self.create_interface()
		super().show()

	# Funzione per la generazione dell'interfaccia grafica
	def create_interface(self):
		pass

	# Funzione per l'inserimento di un nuovo dipendente
	def addEmployee(self, email, password, name, surname):
		admin = self.dispatcher.get_class("Admin")

		headers = {'Authorization': 'Bearer ' + admin.get_token()}
		url = os.environ.get('URL_INSERT_USER')
		json = {'email': email, 'password': password, 'name': name, 'surname': surname, 'role': UserState.Employee.value}

		try:
			response = requests.post(url=url, json=json, headers=headers)

			return response.status_code == 200

		except requests.exceptions.RequestException:
			# Gestione dell'eccezione
			print("Impossibile connettersi al server.")
			return False

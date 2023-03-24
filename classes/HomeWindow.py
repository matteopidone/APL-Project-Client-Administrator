from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView
from PySide6.QtGui import QFont, QColor
import requests
import os

from functools import partial
from classes.HolidayState import HolidayState

class HomeWindow(QWidget):

	def __init__(self, dispatcher):
		# Costruttore classe padre e inizializzazione attributi
		super().__init__()

		# Inizializzo il riferimento al Dispatcher
		self.dispatcher = dispatcher

		# Definisco lo stile
		self.setWindowTitle("Home")
		self.resize(1600, 800)
		self.setFont(QFont("Arial", 20))

	# Override funzione show per creare prima l'interfaccia
	def show(self):
		self.create_interface()
		super().show()

	# Funzione per la generazione dell'interfaccia grafica
	def create_interface(self):
		# Creo il layout per i bottoni sulla sinistra
		left_layout = QVBoxLayout()
		self.create_left_layout(left_layout)

		# Creo il layout per la tabella sulla destra
		right_layout = QGridLayout()
		self.create_right_layout(right_layout)

		# Creo un layout principale per contenere i due layout precedenti
		main_layout = QHBoxLayout()
		main_layout.addLayout(left_layout)
		main_layout.addLayout(right_layout)

		# Imposto il layout della finestra
		self.setLayout(main_layout)

	# Funzione per la creazione del layout di sinistra
	def create_left_layout(self, left_layout):
		# Creo i bottoni
		button1 = QPushButton("Elenco dipendenti")
		button2 = QPushButton("Aggiungi dipendente")
		button3 = QPushButton("Esci")

		font = QFont("Arial", 16)
		button1.setFont(font)
		button1.setFixedSize(250, 50)
		button2.setFont(font)
		button2.setFixedSize(250, 50)
		button3.setFont(font)
		button3.setFixedSize(250, 50)
		button3.setStyleSheet("background-color: red")

		# Li aggiungo al layout di sinistra
		left_layout.addWidget(button1)
		left_layout.addWidget(button2)
		left_layout.addWidget(button3)

	# Funzione per la creazione del layout di destra
	def create_right_layout(self, right_layout):

		# API per il recupero di tutte le ferie richieste dai dipendenti
		data = self.getAllUsersHolidays()

		if not data:
			# Creo comunque la tabella senza nessuna richiesta
			data = list()

		# Creo la tabella
		columns_name = ["Email", "Nome", "Cognome", "Data", "Motivazione", "Stato"]
		table = QTableWidget(len(data), len(columns_name))
		table.setHorizontalHeaderLabels(columns_name)
		table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

		# Popolo la tabella con le richieste di ferie
		for i, row in enumerate(data):
			for j, value in enumerate(row.values()):

				# Se sono alla fine
				if j == table.columnCount()-1:

					# Se lo stato della ferie non è pendente, inserisco lo stato
					if row['type'] != HolidayState.Pending.value:

						text = "Errore"
						color = QColor("red")
						match row['type']:
							case HolidayState.Accepted.value:
								text = "Accettata"
								color = QColor("green")
							case HolidayState.Refused.value:
								text = "Rifiutata"

						item = QTableWidgetItem(text)
						item.setFlags(Qt.ItemIsEnabled)
						item.setForeground(color)
						item.setTextAlignment(Qt.AlignCenter)
						table.setItem(i, j, item)
						j += 1
						break

					# Creo i bottoni
					accept_button = QPushButton("Accetta")
					reject_button = QPushButton("Rifiuta")
					# Imposto lo stile dei bottoni
					accept_button.setFixedSize(75, 30)
					accept_button.setStyleSheet("background-color: green")
					reject_button.setFixedSize(75, 30)
					reject_button.setStyleSheet("background-color: red")
					# Imposto la funzione da invocare al click
					accept_button.clicked.connect(partial(self.updateRequest, row, HolidayState.Accepted.value, table, i))
					reject_button.clicked.connect(partial(self.updateRequest, row, HolidayState.Refused.value, table, i))

					# Creo un contenitore e aggiungo i bottoni al layout a griglia
					widget = QWidget()
					layout = QHBoxLayout()
					layout.addWidget(accept_button)
					layout.addWidget(reject_button)
					widget.setLayout(layout)
					table.setCellWidget(i, table.columnCount()-1, widget)
					break

				item = QTableWidgetItem(value)
				item.setFlags(Qt.ItemIsEnabled)
				item.setFont(QFont("Arial", 16))
				table.setItem(i, j, item)
				j += 1

			table.setRowHeight(i, 100)
			i += 1

		# Aggiungo la tabella al layout di destra
		right_layout.addWidget(table)

	# Funzione per il recupero di tutte le richieste di ferie dei dipendenti
	def getAllUsersHolidays(self):
		admin = self.dispatcher.get_class("Admin")

		headers = {'Authorization': 'Bearer ' + admin.get_token()}
		url = os.environ.get('URL_GET_ALL_USERS_HOLIDAYS') + '?email=' + admin.get_email()

		try:
			response = requests.get(url=url, headers=headers)
			result = response.json()

			if response.status_code == 200 and result != None:
				data = list()

				for user in result:
					for holiday in user['holidays']:
						value = {}
						value['email'] = user['email']
						value['name'] = user['name']
						value['surname'] = user['surname']

						value['date'] = str(holiday['day']) + '-' + str(holiday['month']) + '-' + str(holiday['year'])
						value['message'] = holiday['message']
						value['type'] = holiday['type']

						data.append(value)

				return data
			else:
				return

		except requests.exceptions.RequestException:
			# Gestione dell'eccezione
			print("Impossibile connettersi al server.")

	# Funzione per la risposta alla richiesta di ferie
	def updateRequest(self, row, type, table, index):
		admin = self.dispatcher.get_class("Admin")

		day, month, year = map(int, row['date'].split('-'))

		headers = {'Authorization': 'Bearer ' + admin.get_token()}
		url = os.environ.get('URL_UPDATE_REQUEST')
		json = {'email': row['email'], 'year': year, 'month': month, 'day': day, 'type': type}

		try:
			text = "Errore"
			color = QColor("red")
			response = requests.post(url=url, json=json, headers=headers)

			if response.status_code == 200:
				if type == HolidayState.Accepted.value:
					text = "Accettata"
					color = QColor("green")
				elif type == HolidayState.Refused.value:
					text = "Rifiutata"

		except requests.exceptions.RequestException:
			# Gestione dell'eccezione
			print("Impossibile connettersi al server.")

		finally:
			columns = table.columnCount()
			table.setCellWidget(index, columns-1, QWidget())
			item = QTableWidgetItem(text)
			item.setForeground(color)
			item.setTextAlignment(Qt.AlignCenter)
			item.setFlags(Qt.ItemIsEnabled)
			table.setItem(index, columns-1, item)

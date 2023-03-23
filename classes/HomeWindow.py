from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout, QTableWidget, QTableWidgetItem, QHBoxLayout
from PySide6.QtGui import QFont, QColor
import requests
import os

from functools import partial

class HomeWindow(QWidget):

	def __init__(self, dispatcher):
		# Costruttore classe padre e inizializzazione attributi
		super().__init__()

		# Inizializzo il riferimento al Dispatcher
		self.dispatcher = dispatcher

		# Definisco lo stile
		self.setWindowTitle("Home")
		self.resize(1600, 800)
		self.setFont(QFont("Arial", 24))

		self.create_interface()

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

		font = QFont("Arial", 22)
		button1.setFont(font)
		button1.setFixedSize(350, 50)
		button2.setFont(font)
		button2.setFixedSize(350, 50)
		button3.setFont(font)
		button3.setFixedSize(350, 50)
		button3.setStyleSheet("background-color: red")

		# Li aggiungo al layout di sinistra
		left_layout.addWidget(button1)
		left_layout.addWidget(button2)
		left_layout.addWidget(button3)

	# Funzione per la creazione del layout di destra
	def create_right_layout(self, right_layout):

		data = self.getAllUsersHolidays()

		# Creo la tabella
		table = QTableWidget(len(data), len(data[0])+1)
		columns_name = list(data[0].keys())
		columns_name.append("Azioni")
		table.setHorizontalHeaderLabels(columns_name)

		# Popolo la tabella con le richieste di ferie
		for i, row in enumerate(data):
			for j, value in enumerate(row.values()):
				item = QTableWidgetItem(value)
				item.setFlags(Qt.ItemIsEnabled)
				table.setItem(i, j, item)
				table.setColumnWidth(j, 300)
				j += 1

				# Se ho inserito tutti i campi, allora inserisco i bottoni
				if j == table.columnCount()-1:
					# Creo i bottoni
					accept_button = QPushButton("Accetta")
					reject_button = QPushButton("Rifiuta")
					# Imposto lo stile dei bottoni
					accept_button.setFixedSize(100, 50)
					accept_button.setStyleSheet("background-color: green")
					reject_button.setFixedSize(100, 50)
					reject_button.setStyleSheet("background-color: red")
					# Imposto la funzione da invocare al click
					accept_button.clicked.connect(partial(self.updateRequest, row, 1, table, i))
					reject_button.clicked.connect(partial(self.updateRequest, row, 2, table, i))
					# Creo un contenitore e aggiungo i bottoni al layout a griglia
					widget = QWidget()
					layout = QHBoxLayout()
					layout.addWidget(accept_button)
					layout.addWidget(reject_button)
					widget.setLayout(layout)
					table.setCellWidget(i, table.columnCount()-1, widget)
					table.setColumnWidth(table.columnCount()-1, 300)

			table.setRowHeight(i, 100)
			i += 1

		# Aggiungo la tabella al layout di destra
		right_layout.addWidget(table)

	# Funzione per il recupero di tutte le richieste di ferie dei dipendenti
	def getAllUsersHolidays(self):
		token = self.dispatcher.get_token()

		headers = {'Authorization': 'Bearer ' + token}
		url = os.environ.get('URL_GET_ALL_USERS_HOLIDAYS')

		try:
			response = requests.get(url=url, headers=headers)

			if response.status_code == 200:
				data = list()

				for holiday in response.json():
					value = {}
					value['Email'] = holiday['email']
					value['Nome'] = holiday['name']
					value['Cognome'] = holiday['surname']
					value['Data'] = str(holiday['day']) + '-' + str(holiday['month']) + '-' + str(holiday['year'])
					value['Motivazione'] = holiday['motivation']

					data.append(value)

				return data
			else:
				return {'Email':'','Nome':'','Cognome':'','Data':'','Motivazione':''}

		except requests.exceptions.RequestException:
			# Gestione dell'eccezione
			print("Impossibile connettersi al server.")

	# Funzione per la risposta alla richiesta di ferie
	def updateRequest(self, row, type, table, index):
		token = self.dispatcher.get_token()

		url = os.environ.get('URL_UPDATE_REQUEST')
		headers = {'Authorization': 'Bearer ' + token}
		json = {'email': row['email'], 'year': row['year'], 'month': row['month'], 'day': row['day'], 'type': type}

		try:
			text = "Errore"
			color = QColor("red")
			response = requests.post(url=url, json=json, headers=headers)

			if response.status_code == 200:
				if type == 1:
					text = "Accettata"
					color = QColor("green")
				elif type == 2:
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

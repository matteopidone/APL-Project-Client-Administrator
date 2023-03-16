from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout, QTableWidget, QTableWidgetItem, QHBoxLayout
from PySide6.QtGui import QFont
import requests
import os

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

		user1 = {'name':'tomas', 'surname':'prifti', 'date':'21 Marzo 2023'}
		user2 = {'name':'matteo', 'surname':'pidone', 'date':'22 Marzo 2023'}
		data = [user1, user2]

		# Creo la tabella
		table = QTableWidget(len(data), len(data[0])+1)
		l = list(data[0].keys())
		l.append("Azioni")
		table.setHorizontalHeaderLabels(l)

		# Popolo la tabella con le richieste di ferie
		i = 0
		for row in data:
			j=0
			for value in row.values():
				item = QTableWidgetItem(value)
				table.setItem(i, j, item)
				table.setColumnWidth(j, 300)
				if j == len(row)-1:
					# Creo i bottoni
					accept_button = QPushButton("Accetta")
					reject_button = QPushButton("Rifiuta")
					# Imposto lo stile dei bottoni
					accept_button.setFixedSize(100, 50)
					accept_button.setStyleSheet("background-color: green")
					reject_button.setFixedSize(100, 50)
					reject_button.setStyleSheet("background-color: red")
					# Imposto la funzione da invocare al click
					accept_button.clicked.connect(lambda: self.replyUserRequest(row, 1))
					reject_button.clicked.connect(lambda: self.replyUserRequest(row, 2))
					# Creo un contenitore e aggiungo i bottoni al layout a griglia
					widget = QWidget()
					layout = QHBoxLayout()
					layout.addWidget(accept_button)
					layout.addWidget(reject_button)
					widget.setLayout(layout)
					table.setCellWidget(i, j+1, widget)
					table.setColumnWidth(j+1, 300)
				j += 1
			table.setRowHeight(i, 100)
			i += 1

		# Aggiungo la tabella al layout di destra
		right_layout.addWidget(table)

	# Funzione per il recupero di tutte le richieste di ferie dei dipendenti
	def getAllUsersHolidays(self):
		url = os.environ.get('URL_GET_ALL_USERS_HOLIDAYS')

		try:
			response = requests.get(url)

			if response.status_code == 200:
				return response.json()
			else:
				return
		except requests.exceptions.RequestException:
			# Gestione dell'eccezione
			print("Impossibile connettersi al server.")

	# Funzione per la risposta alla richiesta di ferie
	def replyUserRequest(self, row, choice):
		url = os.environ.get('URL_REPLY_USER_REQUEST')
		row['choice'] = choice

		print(row)

		try:
			response = requests.post(url=url, json=row)

			if response.status_code == 200:
				# to define
				return
			else:
				# to define
				return
		except requests.exceptions.RequestException:
			# Gestione dell'eccezione
			print("Impossibile connettersi al server.")

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout, QTableWidget, QTableWidgetItem, QHBoxLayout
from PySide6.QtGui import QFont

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
		# Creo il layout per i bottoni
		left_layout = QVBoxLayout()

		# Creo i bottoni e li aggiungo al layout di sinistra
		button1 = QPushButton("Elenco dipendenti")
		button2 = QPushButton("Aggiungi dipendente")
		button3 = QPushButton("Esci")
		left_layout.addWidget(button1)
		left_layout.addWidget(button2)
		left_layout.addWidget(button3)

		# Creo il layout per la tabella sulla destra
		right_layout = QGridLayout()

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
			for key, value in row.items():
				item = QTableWidgetItem(value)
				table.setItem(i, j, item)
				table.setColumnWidth(j, 300)
				if j == len(row)-1:
					# Creo i bottoni
					accept_button = QPushButton("Accetta")
					reject_button = QPushButton("Rifiuta")
					# Imposto il colore di sfondo dei bottoni
					accept_button.setStyleSheet("background-color: green")
					reject_button.setStyleSheet("background-color: red")
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

		# Creo un layout principale per contenere i due layout precedenti
		main_layout = QHBoxLayout()
		main_layout.addLayout(left_layout)
		main_layout.addLayout(right_layout)

		# Imposto il layout della finestra
		self.setLayout(main_layout)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QFont

class AllEmployeesWindow(QWidget):

	def __init__(self, dispatcher):
		# Costruttore classe padre e inizializzazione attributi
		super().__init__()

		# Inizializzo il riferimento al Dispatcher
		self.dispatcher = dispatcher

		# Definisco lo stile
		self.setWindowTitle("Elenco Dipendenti")
		self.resize(1600, 800)
		self.setFont(QFont("Arial", 20))

	# Override funzione show per creare prima l'interfaccia
	def show(self):
		self.create_interface()
		super().show()

	# Funzione per la generazione dell'interfaccia grafica
	def create_interface(self):
		data = self.dispatcher.get_class("Admin").get_employees()

		# Creo la tabella
		columns_name = ["Email", "Nome", "Cognome"]
		table = QTableWidget(len(data), len(columns_name))
		table.setHorizontalHeaderLabels(columns_name)
		table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

		# Popolo la tabella con i dipendenti
		for i, row in enumerate(data):
			for j, value in enumerate(row.values()):

				item = QTableWidgetItem(value)
				item.setFlags(Qt.ItemIsEnabled)
				table.setItem(i, j, item)
				j += 1

			table.setRowHeight(i, 50)
			i += 1

		# Aggiungo la tabella al layout
		layout = QGridLayout()
		layout.addWidget(table)
		self.setLayout(layout)

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QFont

class HomeWindow(QWidget):

	def __init__(self, dispatcher):
		# Costruttore classe padre e inizializzazione attributi
		super().__init__()

		# Inizializzo il riferimento al Dispatcher
		self.dispatcher = dispatcher

		# Definisco lo stile
		self.setWindowTitle("Home")
		self.resize(800, 400)
		self.setFont(QFont("Arial", 32))

		self.create_interface()

	# Funzione per la generazione dell'interfaccia grafica
	def create_interface(self):
		pass

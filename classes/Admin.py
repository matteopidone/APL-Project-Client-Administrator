class Admin():

	def __init__(self, dispatcher):
		# Inizializzo il riferimento al Dispatcher
		self.dispatcher = dispatcher
		self.employees = list()

	# Funzione per inizializzare il token
	def set_token(self, token):
		self.token = token

	# Funzione per il recupero del token
	def get_token(self):
		return self.token

	# Funzione per inizializzare l'email dell'admin
	def set_email(self, email):
		self.email = email

	# Funzione per il recupero della mail dell'admin
	def get_email(self):
		return self.email

	# Funzione per aggiungere un dipendente alla lista
	def add_employee(self, employee):
		self.employees.append(employee)

	# Funzione per il recupero della lista di dipendenti
	def get_employees(self):
		return self.employees

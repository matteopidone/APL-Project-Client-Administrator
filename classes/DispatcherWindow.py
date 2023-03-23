class DispatcherWindow():
	windows = {}
	token = ''

	# Funzione per registrare le istanze delle classi
	def set_window(self, key, instance):
		self.windows[key] = instance

	# Funzione per il recupero delle istanze
	def get_window(self, key):
		return self.windows[key]

	# Funzione per inizializzare il token
	def set_token(self, token):
		self.token = token

	# Funzione per il recupero del token
	def get_token(self):
		return self.token

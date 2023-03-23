class DispatcherWindow():
	windows = {}

	# Funzione per registrare le istanze delle classi
	def set_window(self, key, instance):
		self.windows[key] = instance

	# Funzione per il recupero delle istanze
	def get_window(self, key):
		return self.windows[key]

class Dispatcher():
	classes = {}

	# Funzione per registrare le istanze delle classi
	def set_class(self, key, instance):
		self.classes[key] = instance

	# Funzione per il recupero delle istanze
	def get_class(self, key):
		return self.classes[key]

from PySide6.QtWidgets import QApplication
from dotenv import load_dotenv

from classes.DispatcherWindow import DispatcherWindow
from classes.LoginWindow import LoginWindow
from classes.HomeWindow import HomeWindow
from classes.Admin import Admin

if __name__ == "__main__":
	# Carico le variabili di ambiente presenti nel file .env
	load_dotenv()

	# Inizializzo l'applicazione
	app = QApplication([])
	dispatcher = DispatcherWindow()

	login_window = LoginWindow(dispatcher)
	home_window = HomeWindow(dispatcher)
	admin = Admin(dispatcher)

	dispatcher.set_window("LoginWindow", login_window)
	dispatcher.set_window("HomeWindow", home_window)
	dispatcher.set_window("Admin", admin)

	# Mostro il login
	login_window.show()
	app.exec()

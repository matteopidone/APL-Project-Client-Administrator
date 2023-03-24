from PySide6.QtWidgets import QApplication
from dotenv import load_dotenv

from classes.Dispatcher import Dispatcher
from classes.LoginWindow import LoginWindow
from classes.HomeWindow import HomeWindow
from classes.Admin import Admin

if __name__ == "__main__":
	# Carico le variabili di ambiente presenti nel file .env
	load_dotenv()

	# Inizializzo l'applicazione
	app = QApplication([])
	dispatcher = Dispatcher()

	admin = Admin(dispatcher)
	dispatcher.set_class("Admin", admin)

	login_window = LoginWindow(dispatcher)
	dispatcher.set_class("LoginWindow", login_window)

	home_window = HomeWindow(dispatcher)
	dispatcher.set_class("HomeWindow", home_window)

	# Mostro il login
	login_window.show()
	app.exec()

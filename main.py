from classes.LoginWindow import LoginWindow
from PySide6.QtWidgets import QApplication
from dotenv import load_dotenv

if __name__ == "__main__":
	# Carico le variabili di ambiente presenti nel file .env
	load_dotenv()

	# Inizializzo l'applicazione e mostro la finestra di login
	app = QApplication([])
	login_window = LoginWindow()
	login_window.show()
	app.exec()

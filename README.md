# Project - Advanced Programming Languages
Client per gli amministratori, sviluppato con il liguaggio di programmazione `Python`

## Installazione
Il client necessita di alcune librerie python per il suo funzionamento.<br>
Bisogna quindi eseguire i seguenti comandi :
```
pip install pyside6
pip install python-dotenv
pip install requests
```

## Utilizzo
Per poter utilizzare il client bisogna eseguire il comando :
```
python main.py
```

In questo modo verrà mostrata una finestra di login per accedere al sistema.

## Struttura
Il punto di ingresso del client è il file `main.py`, che gestisce la creazione di tutte le finestre presenti nel sistema.<br>
All'interno della directory `classes` sono presenti tutte le classi utilizzate, tra cui :
-	`Dispatcher` è la classe principale, che si occupa di gestire l'interazione tra le istanze di classe esistenti
-	`LoginWindow`, per la gestione del login dell'amministratore
-	`HomeWindow`, per la gestione della finestra di home
-	`Admin`, per la gestione delle informazioni dell'admin (dopo il login)
-	`EnumState`, per la gestione dello stato di `HolidayState` e `UserState`
-	`NewEmployeeWindow`, per la gestione della finestra per l'inserimento dei nuovi dipendenti
-	`AllEmployeesWindow`, per la gestione della finestra con l'elenco di tutti i dipendenti

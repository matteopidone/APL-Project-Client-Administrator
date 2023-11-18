# Project - Advanced Programming Languages
Administrator client developed using the `Python` programming language

## Installation
The client requires some Python libraries for its operation.<br>
Execute the following commands:
```bash
pip install pyside6
pip install python-dotenv
pip install requests
```

## Dependencies
-	`pyside6`, enabling the use of the `Qt` library for the graphical interface
-	`python-dotenv`, for loading environment variables from the `.env` file
-	`requests`, for making `HTTP` requests to the server

## Usage
To use the client, execute the following command:
```bash
python main.py
```
This will display a login window to access the system.

## Project Structure
The client's entry point is the `main.py` file, which manages the creation of all windows in the system.<br>
There is an `.env` file for managing constants used in `HTTP` requests.<br>
The classes used within the project are located in two different directories.

Directory `classes`:
-	`Dispatcher` is the main class that handles interaction between existing class instances
-	`Admin`, for managing admin information (after login)
-	`EnumState`, for managing the state of `HolidayState` and `UserState`

Directory `windows`:
-	`LoginWindow`, for managing the administrator's login
-	`HomeWindow`, for managing the home window
-	`NewEmployeeWindow`, for managing the window for entering new employees
-	`AllEmployeesWindow`, for managing the window with a list of all employees

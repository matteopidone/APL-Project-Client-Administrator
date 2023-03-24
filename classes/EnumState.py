from enum import Enum

class HolidayState(Enum):
	Pending = 0
	Accepted = 1
	Refused = 2

class UserState(Enum):
	Employee = 0
	Admin = 1

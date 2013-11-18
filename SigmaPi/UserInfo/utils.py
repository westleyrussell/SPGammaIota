# Utility functions for use within the UserInfo modules
from datetime import date

# Returns the current upcoming senior graduation year.
def get_senior_year():
	time_tuple = date.today().timetuple()

	year = time_tuple[0]
	month = time_tuple[1]

	if month >= 6:
		return year + 1
	else:
		return year

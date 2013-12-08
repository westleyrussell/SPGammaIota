"""
	Utility functions for use within the UserInfo modules
"""
from datetime import date

def get_senior_year():
	"""
		Returns the upcoming graduation year of the current seniors.
	"""
	
	time_tuple = date.today().timetuple()

	year = time_tuple[0]
	month = time_tuple[1]

	if month >= 6:
		return year + 1
	else:
		return year

def create_user(username):
	"""
		Creates a user with the given username and populates its info with the web scraper.
	"""
	user_info = scrapify.find_user(username)

	names = user_info['Name'].split(' ')

	try:
		user_obj = User.objects.create()
		user_obj.username = username
		user_obj.email = user_info['Email']
		user_obj.first_name = names[0]
		user_obj.last_name = names[len(names) - 1]

		password = User.objects.make_random_password()
		print(password)
		user_obj.set_password(password)

		user_info_obj = UserInfo.objects.create(user=user_obj)
		user_info_obj.hometown = user_info['Hometown']
		user_info_obj.major = user_info['Major']
		user_info_obj.graduationYear = int(user_info['Class'])

		user_obj.save()
		user_info_obj.save()
	except:
		if user_obj:
			user_obj.delete()
		raise

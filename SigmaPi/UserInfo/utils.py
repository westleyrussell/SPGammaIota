"""
	Utility functions for use within the UserInfo modules
"""
from datetime import date
from django.conf import settings
from django.core.mail import send_mail

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
		user_obj.email = username + "@wpi.edu"
		user_obj.first_name = names[0]
		user_obj.last_name = names[len(names) - 1]

		password = User.objects.make_random_password()
		user_obj.set_password(password)

		user_info_obj = UserInfo.objects.create(user=user_obj)
		user_info_obj.hometown = user_info['Hometown']
		user_info_obj.major = user_info['Major']
		user_info_obj.graduationYear = int(user_info['Class'])

		user_obj.save()
		user_info_obj.save()

		send_mail_to_new_user(user_obj.username, user_obj.email, password)
	except:
		if user_obj:
			user_obj.delete()
		raise

def send_mail_to_new_user(username, email, password):
	"""
		Sends a notice to a new user that their account has been setup
	"""
	subject = "Welcome to the Sigma Pi Gamma Iota Website"
	message = "Welcome to the Sigma Pi Gamma Iota website."
	message = message + " An account has been created for you.  Your username is: "
	message = message + username + ". Your password is: " + password + ". "
	message = message + "You may acess the website at: http://sigmapiwpi.webfactional.com. "
	message = message + "It is highly reccommended that you change your password upon logging in."

	send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])





"""
	Utility functions for use within the UserInfo modules
"""
from django.contrib.auth.models import User
from UserInfo.models import UserInfo
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

def create_user(username, first_name, last_name, major, year):
	"""
		Creates a user with the given username and populates its info with the web scraper.
	"""
	user_obj = None
	try:
		user_obj = User.objects.create(username=username)
		user_obj.email = username + "@wpi.edu"
		user_obj.first_name = first_name
		user_obj.last_name = last_name

		password = User.objects.make_random_password()
		user_obj.set_password(password)

		user_info_obj = UserInfo.objects.create(user=user_obj)
		user_info_obj.major = major
		user_info_obj.graduationYear = year

		user_obj.save()
		user_info_obj.save()

		if not settings.DEBUG:
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
	message = message + "You may acess the website at: https://sigmapigammaiota.org. "
	message = message + "It is highly reccommended that you change your password upon logging in."

	send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

def reset_password(username):
	"""
		Resets a user's password.
	"""
	user_obj = User.objects.get(username=username)

	password = User.objects.make_random_password()
	user_obj.set_password(password)
	user_obj.save()

	if not settings.DEBUG:
		send_mail_reset_password(user_obj.username, user_obj.email, password)

def send_mail_reset_password(username, email, password):
	"""
		Sends a notice to a user that their password has been reset
	"""
	subject = "Your Password has been Reset"
	message = "Your password for the Sigma Pi Gamma Iota website has been reset."
	message = message + " Your username is: "
	message = message + username + ". Your new password is: " + password + ". "
	message = message + "You may acess the website at: https://sigmapigammaiota.org. "
	message = message + "It is highly reccommended that you change your password upon logging in."

	send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


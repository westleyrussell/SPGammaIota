from bs4 import BeautifulSoup
import requests

"""
	Ryan Baker
	written 11/23/2013
"""

"""
	NOTE: 
	-- NO ERRORS ARE CAUGHT IN THIS FUNCTION
"""


def find_user(login):
	URL = "https://www.wpi.edu/cgi-bin/ldap-html"
	Params = {'get-student' : 'yes', 'login' : 'no', 'title' : '', 'department' : '', 'interpretation' : '1'}
	Params['name'] = str(login)
	r = requests.post(URL, data=Params)
	
	# use just the page from the response
	page = BeautifulSoup(r.text)
	# the data for the student
	data = page.table
	# the dictionary to be filled
	student = {"Name" : "", "Email" : "", "Major" : "", "Minor": '', "Class" : "", "Hometown" : ""}
	# the strings in the table containing
	# the data for the student taken from
	# the WPI directory
	fields = []
	# populate fields 
	for dat in data.stripped_strings:
		fields.append(dat)
	# populates student with values in field
	# if it's there 
	for f in range(len(fields)):
		# make it a string
		field = str(fields[f])
		# catch the hometown from the mailing
		# address
		if field == "Home Mailing Address":
			student['Hometown'] = str(fields[f+2])
		# if the field is a key in student
		# put the next string as the value
		if field in student:
			student[field] = str(fields[f+1])
		# catch a double major
		if field == "Major":
			if str(fields[f+2]) not in student:
				student['Major'] = student['Major']+'/'+str(fields[f+2])
	return student




if __name__ == '__main__':
	biddies = [
		'Foster Lee',
'Derek Calzada',
'Jared Danaher',
'Zach Robbins',
'Jarrett Jacobson',
'Sean Watson',
'Connor McGrath',
'Steve Laudage',
'Sam Ellison',
'Nate Jefferson',
'Dan Sturman',
'Garrett Brogan',
'Nan Zhang',
'Ryan Orlando',
'Peter Raspe',
'Chris Madden ',
'Tim Marschall',
'Eli Gonzalez',
'Nick Wong ',
'Austin Rose ',
'Bryan Sadowski',
'Jacob Alexander',
'Corin Rypkema',
'Dan Sanderson',
'Alex Zitoli',
'Tony Kassas',
'Anthony Dresser',
'Ziyao Xu',
'August Beers',
'Eric Plante',
'Himanshu Sahay',
'Alex Shoop',
'Justin Vitiello',
'Anthony Lawinger',
'Matt Nguyen',
'Seth Norton'
	]
	for bid in biddies:
		try:
			student = find_user(bid)
			print student['Email']
		except:
			print "manually find", bid


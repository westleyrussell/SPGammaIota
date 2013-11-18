import urllib
import urllib2


def directory_lookup(user):
	"""do a lookup of the supplied username in the wpi directory,
	and return the page (as HTML) as if it were read from a file. That
	is: an array of 'lines' where each line is delimited by a '\n' character"""
	
	url = "https://www.wpi.edu/cgi-bin/ldap-html"
	params = {'name': user, 'get-student' : 'yes', 'login' : 'yes'}

	req = urllib2.Request(url,params)
	req.add_data(urllib.urlencode(params))
	response = urllib2.urlopen(req)

	page = response.read()

	i=0
	lines=[]
	lines.append('')

	#the response comes in an ugly format, this splits the response into an
	#array of lines ()
	for char in page:
		lines[i]+=char
		if char == '\n':
			lines.append('')
			i+=1

	return lines
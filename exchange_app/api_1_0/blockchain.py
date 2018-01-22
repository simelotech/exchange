import urllib.request
import urllib.parse

#TODO: Get the actual url for blockchain api.
#TODO: Dont't hardcode this. Read from settings maybe?
base_url = "http://blockchain.api.com"

def get_url(path, values):
    """
    """
	
	if path[0] != '/' :
		path = '/' + path
		
	url = base_url + path
	
	if values != "" :
		url_values = urllib.parse.urlencode(values) 
		url = url + '?' + url_values
		
	with urllib.request.urlopen(url) as response:
		response_data = response.read()

	#TODO: convert to JSON before return
	return response_data
	

def post_url(path, values):
    """
    """
	
	if path[0] != '/' :
		path = '/' + path
		
	url = base_url + path
	
	url_values = urllib.parse.urlencode(values) 
	url_values = data.encode('ascii')
	with urllib.request.urlopen(url, url_values) as response:
		response_data = response.read()

	#TODO: convert to JSON before return
	return response_data

import requests
import json

#TODO: Get the actual url for blockchain api.
#TODO: Dont't hardcode this. Read from settings maybe?
base_url = "http://blockchain.api.com"

def form_url(base, path):
	
	if path[0] != '/':
		path = '/' + path
	
	if base[len(base) - 1] == '/' :
		base = base[0:len(base)-1]
	
	url = base + path
	
	return url

def get_url(path, values = ""):
	"""
	"""

	url = form_url(base_url, path)
	
	#resp = requests.get(url, params = values)
	#response_data = resp.json()
		
	response_data = {"Called": "get_url()", "url": url, "values:": values}

	return response_data
	

def post_url(path, values = ""):
	"""
	"""
	
	url = form_url(base_url, path)
	
	#resp = requests.post(url, data = values)
	#response_data = resp.json()
		
	response_data = {"Called": "post_url()", "url": url, "values:": values}

	return response_data

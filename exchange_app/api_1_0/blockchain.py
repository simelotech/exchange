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
	
		
def create_wallet():
	"""
	"""
	
	# generate new seed first
	#new_seed = requests.get(form_url(base_url, "/wallet/newSeed")).json()
	new_seed = {"seed": "helmet van actor peanut"} #TODO: revove this mock response
	
	# create the wallet from seed
	values = {"seed": new_seed["seed"], "label": "wallet123", "scan": "5"} #TODO: Where to get labels? How about scan?
	#new_wallet = requests.post(form_url(base_url, "/wallet/newSeed"), values).json()
	new_wallet = {"meta":{"coin": "sky", "filename": "2018-01-24-d554.wlt"}, #TODO: should we store filenames?
				  "entries":[{
					"address": "addressjdjebcjdhbjehc", 
					"public_key": "publicdwewewvefvfv",
					"secret_key": "privatewthbregvefvwef"}
					]} #TODO: remove this mock response.
	
	result = {"address": new_wallet["entries"][0]["address"]}
	
	return result #TODO: Error handling
	
	
def spend(values):
	"""
	"""
	#resp = requests.post(form_url(base_url, "/wallets/cashout"), data = values)
	result = resp.status_code
	result = 200
	
	return result #TODO: Error handling. Sometimes there is 200 response but there is error code in json

	
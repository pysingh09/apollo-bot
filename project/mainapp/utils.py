import requests

ROOT_URL = 'https://graph.facebook.com/v2.11/'
LIST_ALL_PAGES = 'me/accounts/?access_token='

def listUsersPage(token):
	res = requests.get(ROOT_URL+LIST_ALL_PAGES+token)
	return res.json()
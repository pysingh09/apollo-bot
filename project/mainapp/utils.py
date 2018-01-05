import requests

ROOT_URL = 'https://graph.facebook.com/v2.11/'
LIST_ALL_PAGES = 'me/accounts/?access_token='
PAGE_DETAILS = '?fields=username,followers_count,name,media{media_type,media_url,comments_count,id}'

def listUsersPage(token):
	res = requests.get(ROOT_URL+LIST_ALL_PAGES+token)
	return res.json()

def pageDetails(page_id):
	res = requests.get(ROOT_URL+page_id+PAGE_DETAILS)
	return res.json()
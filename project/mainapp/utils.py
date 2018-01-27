import requests

ROOT_URL = 'https://graph.facebook.com/v2.11/'
LIST_ALL_PAGES = 'me/accounts/?access_token='
PAGE_DETAILS = '?fields=username,followers_count,name,media{media_type,media_url,comments_count,id}'
FOLLOWERS_FOLLOWING = '?fields=follows_count,followers_count&access_token='
INSTAGRAM_BUSINESS_ACCOUNT = '?fields=instagram_business_account&access_token='
MEDIA_COUNTS = '?fields=media{like_count,comments_count}&access_token='

def listUsersPage(token):
	res = requests.get(ROOT_URL+LIST_ALL_PAGES+token)
	return res.json()

def pageDetails(page_id):
	res = requests.get(ROOT_URL+page_id+PAGE_DETAILS)
	return res.json()

def businessAccount(page_id, token):
	res = requests.get(ROOT_URL+page_id+INSTAGRAM_BUSINESS_ACCOUNT+token)
	return res.json()

def getFollowers(page_id, token):
	res = requests.get(ROOT_URL+page_id+FOLLOWERS_FOLLOWING+token)
	return res.json()

def mediaCounts(bussiness_account_id, token):
	res = requests.get(ROOT_URL+bussiness_account_id+MEDIA_COUNTS+token)
	return res.json()
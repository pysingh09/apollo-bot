from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.
class UserPage(models.Model):
	"""docstring for ClassName"""
	page_name =  models.CharField(max_length=70)
	page_id =  models.CharField(max_length=70)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	business_account_id = models.CharField(max_length=70, null=True, blank=True)

class BusinessAccountDetails(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	follows_count = models.IntegerField(default=0, blank=True)
	followers_count = models.IntegerField(default=0, blank=True)
	total_comment_count = models.IntegerField(default=0, blank=True)
	total_like_count = models.IntegerField(default=0, blank=True)
	date =  models.DateField(default=date.today,blank=True)
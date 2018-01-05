from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserPage(models.Model):
	"""docstring for ClassName"""
	page_name =  models.CharField(max_length=70)
	page_id =  models.CharField(max_length=70)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

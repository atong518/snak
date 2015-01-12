from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# temp user model
class User(models.Model):

	name = models.CharField(max_length=20)
	#USERNAME_FIELD = name
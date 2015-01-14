from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.
class GenericUser(AbstractBaseUser):
    email = models.EmailField(max_length=222, unique=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    homecountry = models.CharField(max_length=200)
    homestate = models.CharField(max_length=200)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'firstname', 'lastname']

    def get_fullname(self):
        return self.firstname + "" + self.lastname

class CollegeUser(GenericUser):
    bio = models.CharField(max_length=500)

class ProspieUser(GenericUser):
    pass


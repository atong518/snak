from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.
class GenericUserManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, homecountry, homestate=None, password=None):
        """
        Creates and saves a GenericUser with the given fields
        """
        if not email:
            raise ValueError('Users must have an email')

        user = self.model(
            email=email,
            firstname=firstname,
            lastname=lastname,
            homecountry=homecountry,
            homestate=homestate
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, lastname, homecountry, homestate, password):
        """
        Needed for Django functionality
        """
        user = self.create_user(email=email,
                                firstname=firstname,
                                lastname=lastname,
                                homecountry=homecountry,
                                homestate=homestate,
                                password=password,  
                                )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CollegeUserManager(GenericUserManager):
    def create_user(self, email, firstname, lastname, homecountry, homestate, bio, password=None):
        """
        Creates and saves a CollegeUser by creating a GenericUser and adding appropriate fields
        """
        user = super(CollegeUserManager, self).create_user(email=email, 
                                                           firstname=firstname, 
                                                           lastname=lastname, 
                                                           homecountry=homecountry,
                                                           homestate=homestate,
                                                           password=password)
        user.bio = bio
        user.save(using=self._db)
        return user

class ProspieUserManager(GenericUserManager):
    def create_user(self, email, firstname, lastname, homecountry, homestate, password=None):
        """
        Creates and saves a CollegeUser by creating a GenericUser and adding appropriate fields
        """
        user = super(ProspieUserManager, self).create_user(email=email, 
                                                           firstname=firstname, 
                                                           lastname=lastname, 
                                                           homecountry=homecountry,
                                                           homestate=homestate,
                                                           password=password)
        return user

class GenericUser(AbstractBaseUser):
    email = models.EmailField(max_length=222, unique=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    homecountry = models.CharField(max_length=200)
    homestate = models.CharField(max_length=200, null=True, blank=True)

    objects = GenericUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'firstname', 'lastname']

    def get_fullname(self):
        return self.firstname + "" + self.lastname

class CollegeUser(GenericUser):
    bio = models.CharField(max_length=500)

    objects = CollegeUserManager()

class ProspieUser(GenericUser):
    objects = ProspieUserManager()


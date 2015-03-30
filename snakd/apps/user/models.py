from django.db import models
from django.utils.crypto import get_random_string
from snakd.apps.interest.models import Interest
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import datetime

# Create your models here.
class GenericUserManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, homecountry, homestate, gender, password=None):
        """
        Creates and saves a GenericUser with the given fields
        """
        if not email:
            raise ValueError('Users must have an email')

        data = {
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'homecountry': homecountry,
            'homestate': homestate,
            'gender': gender,
            'password': password,
            'is_active': False
            }
        return data

    def create_superuser(self, email, firstname, lastname, homecountry, homestate, gender, password):
        """
        Needed for Django functionality
        """
        user = self.create_user(email=email,
                                firstname=firstname,
                                lastname=lastname,
                                homecountry=homecountry,
                                homestate=homestate,
                                gender=gender,
                                password=password,  
                                )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CollegeUserManager(GenericUserManager):
    def create_user(self, email, firstname, lastname, homecountry, homestate, gender, bio, max_match_frequency, password=None):
        """
        Creates and saves a CollegeUser by creating a GenericUser and adding appropriate fields
        """
        import pdb; pdb.set_trace()
        user = self.model(
                email=email,
                firstname=firstname,
                lastname=lastname,
                homecountry=homecountry,
                homestate=homestate,
                gender=gender,
                bio=bio,
                max_match_frequency=max_match_frequency,
                next_match=datetime.today())
        user.set_password(password)
        user.is_active = False
        user.activation_code = get_random_string(250)
        user.save()
        return user


class ProspieUserManager(GenericUserManager):
    def create_user(self, email, firstname, lastname, homecountry, homestate, gender, password=None):
        """
        Creates and saves a CollegeUser by creating a GenericUser and adding appropriate fields
        """

        user = self.model(
                email=email,
                firstname=firstname,
                lastname=lastname,
                homecountry=homecountry,
                homestate=homestate,
                gender=gender)
                homestate=homestate)
        user.set_password(password)
        user.is_active = False
        user.activation_code = get_random_string(250)
        user.save()
        return user


class GenericUser(AbstractBaseUser):
    email = models.EmailField(max_length=222, unique=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    homecountry = models.CharField(max_length=200)
    homestate = models.CharField(max_length=200, null=True, blank=True)
    activation_code = models.CharField(max_length=250)
    is_active = models.NullBooleanField(default=False)
    interests = models.ManyToManyField(Interest, null=True, related_name='user_set')
    gender = models.CharField(max_length=50, null=False, default="gender is a construct")

    objects = GenericUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def get_fullname(self):
        return self.firstname + "" + self.lastname

    def set_interest(self, interest_reference):
        self.interests.add(interest_reference)

    def getInterestList(self):
        return self.interests.all()

    def getInterestString(self):
        interestlist = self.getInterestList()
        lst = ""
        if interestlist:
            lst += interestlist[0]
            for interest in interestlist[1:len(interestlist)-1]:
                lst += ", " + interest
            lst += " and " + interestlist[len(interestlist)-1] + "\n"
        return lst

    def editableFields(self):
        return {
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "homecountry": self.homecountry,
            "homestate": self.homestate,
        }

    def updateUser(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()

    def matchInfo(self):
        interests = []
        for interest in self.getInterestList():
            interests.append(interest.name)
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "homecountry": self.homecountry,
            "homestate": self.homestate,
            "interests": list(interests),
            "id": self.id
        }

    def introText(self):
        intro = "Say hello to " + self.firstname + " " + self.lastname + "!\n"
        intro += self.getInterestString()
        return intro

class CollegeUser(GenericUser):
    # Match frequencies in seconds (for countdown)
    UNLIMITED = 0
    ONEDAY = 1
    THREEDAYS = 3
    ONEWEEK = 7
    TWOWEEKS = 14

    MAX_MATCH_FREQS = (
        (UNLIMITED, 'UNLIMITED'),
        (ONEDAY, 'ONEDAY'),
        (THREEDAYS, '3DAYS'),
        (ONEWEEK, 'ONEWEEK'),
        (TWOWEEKS, 'TWOWEEKS'),
    )

    bio = models.CharField(max_length=500)
    max_match_frequency = models.IntegerField(null=False, default=0)
    next_match = models.DateTimeField(null=False, default=datetime.now())

    objects = CollegeUserManager()
    matches = models.ManyToManyField("ProspieUser", related_name="matches", null=True)

    def editableFields(self):
        dic = super(CollegeUser, self).editableFields()
        dic["bio"] = self.bio
        dic["max_match_frequency"] = self.max_match_frequency
        return dic

    def matchInfo(self):
        dic = super(CollegeUser, self).matchInfo()
        dic["bio"] = self.bio
        return dic

    def introText(self):
        intro = super(CollegeUser, self).introText()
        if self.bio:
            intro += self.bio + "\n"
        return intro

class ProspieUser(GenericUser):
    objects = ProspieUserManager()


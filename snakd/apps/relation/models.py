from django.db import models
from snakd.apps.user.models import User
from snakd.apps.interest.models import Interest

class Relation(models.Model):

	user = models.ForeignKey(User)
	interest = models.ForeignKey(Interest)
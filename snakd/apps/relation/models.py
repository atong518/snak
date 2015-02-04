from django.db import models
from snakd.apps.user.models import GenericUser
from snakd.apps.interest.models import Interest

class Relation(models.Model):
	user = models.ForeignKey(GenericUser, null=True, blank=True)
	interest = models.ForeignKey(Interest, null=True, blank=True)

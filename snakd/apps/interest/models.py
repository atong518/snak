from django.db import models

class Interest(models.Model):

	name = models.CharField(max_length = 20)
	parent = models.ForeignKey('self')
	children = models.ManyToManyField('self', symmetrical = False)
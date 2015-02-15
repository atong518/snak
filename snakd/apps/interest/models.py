from django.db import models
#from snakd.apps.user.models import GenericUser


class Interest(models.Model):
	name    = models.CharField(max_length = 20, blank = False, default="Test")
	tooltip = models.CharField(max_length = 20, null = True)
	weight  = models.IntegerField(default = 0)
	parent  = models.ForeignKey('self', null=True, related_name='children')
	hidden  = models.BooleanField(default=False)

	def ChildList(self):
		return self.children.all()

	def getParent(self):
		return self.parent

	# https://docs.djangoproject.com/en/1.7/topics/db/examples/many_to_many/
	# http://stackoverflow.com/questions/13341173/django-get-objects-from-a-many-to-many-field
	def getFrequency(self):
		return len(self.related.all())

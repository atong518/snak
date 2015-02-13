from django.db import models
from snakd.apps.user.models import GenericUser


class Interest(models.Model):
	name    = models.CharField(max_length = 20, blank = False, default="Test")
	tooltip = models.CharField(max_length = 20, null = True) # or blank=True?
	weight  = models.IntegerField(default = 0)
	parent = models.ForeignKey('self', null=True, related_name='children')
	hidden = models.BooleanField(default=False)


	def ChildList(self):
		return self.children.all()



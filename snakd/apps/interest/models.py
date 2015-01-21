from django.db import models
from djutils import decorators.memoize

class Interest(models.Model):

	name = models.CharField(max_length = 20, blank = False)
	tooltip models.CharField(max_length = 20, null = True) # or blank=True?

	comp_weight = models.IntegerField(default = 0)

	parent = models.ManyToManyField("self", symmetrical = False)


	@memoize
	def build_subtree(self, ID):
		if ID.parent == None:
			return tree.make_head()

		tree.add( build_subtree(ID.parent) )
		
		return tree


	def __str__(self):
		return self.name
from django.db import models

class Interest(models.Model):

	name    = models.CharField(max_length = 20, blank = False)
	tooltip = models.CharField(max_length = 20, null = True) # or blank=True?
	weight  = models.IntegerField(default = 0)
	parent  = models.ForeignKey('self', null=True)
	# parent_id  = models.ForeignKey('self', null=True, blank=True)
	# parent needs to be manytomany with symmetrical = false


	# def build_subtree(self, ID):
	# 	if ID.parent == None:
	# 		return tree.make_head()

	# 	tree.add( build_subtree(ID.parent) )
		
	# 	return tree

	def __str__(self):
		return self.name
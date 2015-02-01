from django.db import models
# from snakd.apps.user.models import User


class FakeUser(models.Model):
	pass
	# name = models.CharField(max_length=20)
	#USERNAME_FIELD = name
	

class Fake(models.Model):
	pass
	# name = models.CharField(max_length=20)
	#USERNAME_FIELD = name
	

class Interest(models.Model):
	# name    = models.CharField(max_length = 20, blank = False)
	# tooltip = models.CharField(max_length = 20, null = True) # or blank=True?
	# weight  = models.IntegerField(default = 0)
	# parent  = models.ForeignKey('self', null=True)
	parent = models.ForeignKey('self', null=True, related_name='children')
	
	# user = models.ForeignKey(FakeUser, null=True, db_index=False)
	# interest = models.ForeignKey(Fake, null=True)
	# pass

	# parent = relationship("self", null=True)
	# id = Column(Integer, primary_key=True)
	# parent needs to be manytomany with symmetrical = false


	# def build_subtree(self, ID):
	# 	if ID.parent == None:
	# 		return tree.make_head()

	# 	tree.add( build_subtree(ID.parent) )
		
	# 	return tree

	# def __str__(self):
	# 	return self.name
from django.db import models
import cPickle as pickle
import base64

class Interest(models.Model):
	name    = models.CharField(max_length = 500, blank = False, default="Test")
	tooltip = models.CharField(max_length = 500, null = True)
	weight  = models.IntegerField(default = 1)
	parent  = models.ForeignKey('self', null=True, related_name='children')
	hidden  = models.BooleanField(default=False)
	gender  = models.CharField(max_length = 50, null=False, default="gender is a construct")
	freq    = models.IntegerField(default = 0)

	def ChildList(self):
		return self.children.all()

	def getParent(self):
		if not self.parent:
			return []
		return [self.parent]

	def __str__(self):
		return self.name

 	def get_kwargs(self):
 		return {
 			"name": self.name,
 			"tooltip": self.tooltip,
 			"weight": self.weight,
 			"hidden": self.hidden,
 			"id": self.id
 		}

	def getFrequency(self):
		return len(self.user_set.all())

	class Meta:
		ordering = ['name']


class SerializedDataField(models.TextField):
    """Because Django for some reason feels its needed to repeatedly call
    to_python even after it's been converted this does not support strings."""
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value is None: return
        if not isinstance(value, basestring): return value
        value = pickle.loads(base64.b64decode(value))
        return value

    def get_db_prep_save(self, value, connection):
        if value is None: return
        return base64.b64encode(pickle.dumps(value))

class InterestMatrix(models.Model):
	matrix = SerializedDataField(null=True)




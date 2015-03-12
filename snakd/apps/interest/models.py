from django.db import models
import cPickle as pickle
import base64

class Interest(models.Model):
	name    = models.CharField(max_length = 50, blank = False, default="Test")
	tooltip = models.CharField(max_length = 50, null = True)
	weight  = models.IntegerField(default = 0)
	parent  = models.ForeignKey('self', null=True, related_name='children')
	hidden  = models.BooleanField(default=False)

	def ChildList(self):
		return self.children.all()

	def getParent(self):
		if not self.parent:
			return []
		return [self.parent]

	# https://docs.djangoproject.com/en/1.7/topics/db/examples/many_to_many/
	# http://stackoverflow.com/questions/13341173/django-get-objects-from-a-many-to-many-field
	def getFrequency(self):
		return len(self.user_set.all())

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







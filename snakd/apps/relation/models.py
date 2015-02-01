# from django.db import models
# from snakd.apps.user.models import User
# from snakd.apps.interest.models import Interest

# class Relation(models.Model):
# 	pass
# 	# user = models.ForeignKey(User, null=True, blank=True)
# 	# interest = models.ForeignKey(Interest, null=True, blank=True)


from django.db import models

class Manufacturer(models.Model):
    # ...
    pass

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer)
    # ...
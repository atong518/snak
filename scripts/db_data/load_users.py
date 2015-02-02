import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'snakd.settings'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from snakd.apps.user.models import CollegeUser, ProspieUser

import django
django.setup()

college = {
	"email": "college@snakd.com",
	"password": "dartmouth",
	"firstname": "Summer",
	"lastname": "Tong",
	"homecountry": "USA",
	"homestate": "California",
	"activation_code": "000",
	"is_active": True,
	"bio": "Once upon a time, I didn't do homework and I hung out instead."
}

prospie = {
	"email": "prospie@snakd.com",
	"password": "highschool",
	"firstname": "Baby",
	"lastname": "19",
	"homecountry": "USA",
	"homestate": "Boston",
	"activation_code": "111",
	"is_active": True,
}

c, created = CollegeUser.objects.get_or_create(**college)
if created:
	c.save()

p, created = ProspieUser.objects.get_or_create(**prospie)
if created:
	p.save()



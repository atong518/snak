import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'snakd.settings'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from snakd.apps.interest.models import Interest

import django
django.setup()

dic = {
	"name": "HEAD",
	"tooltip": "Head node",
	"weight": 0,
	"parent": None,
}

i, created = Interest.objects.get_or_create(hidden=True, **dic)

count = 0
for name in ["Academics", "Athletics", "Social Life", "Extracurriculars"]:
	dic["name"] = name
	dic["parent"] = i
	x, created = Interest.objects.get_or_create(**dic)
	for j in range(0, 4):
		dic["name"] = count.__str__()
		dic["parent"] = x
		y, created = Interest.objects.get_or_create(**dic)
		count += 1





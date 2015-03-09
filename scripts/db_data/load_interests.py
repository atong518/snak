import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'snakd.settings'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from snakd.apps.interest.models import Interest
from snakd.lib.matrix import buildMatrix
import json

import django
django.setup()

dic = {
	"name": "HEAD",
	"tooltip": "Head node",
	"weight": 0,
	"parent": None,
}

# create the root
i, created = Interest.objects.get_or_create(hidden=True, **dic)

count = 0
for name in ["Academics", "Athletics", "Extracurriculars"]:
	dic["name"] = name
	dic["parent"] = i
	x, created = Interest.objects.get_or_create(**dic)
	for j in range(0, 4):
		dic["name"] = count.__str__()
		dic["parent"] = x
		y, created = Interest.objects.get_or_create(**dic)
		count += 1


def build_subtree(parent, **kwargs):
	children = kwargs.pop("children")
	kwargs["parent"] = parent
	i = Interest.objects.get_or_create(**kwargs)
	for child in children:
		build_subtree(i, **child)


# with open("interests.json") as jsonfile:
# 	for child in json.load(jsonfile):
# 		build_subtree(root, **child)



buildMatrix()

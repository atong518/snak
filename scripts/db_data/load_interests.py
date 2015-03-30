import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'snakd.settings'
FILE = os.path.dirname(__file__)
ROOT = os.path.dirname(os.path.dirname(FILE))
sys.path.append(ROOT)
from snakd.apps.interest.models import Interest
# from snakd.apps.interest.models import SportsInterest
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
root_node, created = Interest.objects.get_or_create(hidden=True, **dic)

# count = 0
# for name in ["Academics", "Athletics", "Extracurriculars"]:
# 	dic["name"] = name
# 	dic["parent"] = i
# 	x, created = Interest.objects.get_or_create(**dic)
# 	for j in range(0, 4):
# 		dic["name"] = count.__str__()
# 		dic["parent"] = x
# 		y, created = Interest.objects.get_or_create(**dic)
# 		count += 1
# 		for k in range(0, 3):
# 			dic["name"] = count.__str__()
# 			dic["parent"] = y
# 			z, created = Interest.objects.get_or_create(**dic)
# 			count += 1


def build_subtree(parent, **kwargs):
	children = kwargs.pop("children")
	kwargs["parent"] = parent

	# if kwargs.has_key("gender"):
	# 	i = SportsInterest.objects.get_or_create(**kwargs)
	# else:
	new_node, created = Interest.objects.get_or_create(**kwargs)
		
	for child in children:
		build_subtree(new_node, **child)


with open(os.path.join(FILE, "interests.json")) as jsonfile:
	for child in json.load(jsonfile):
		build_subtree(root_node, **child)



buildMatrix()

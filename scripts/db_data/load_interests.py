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

def build_subtree(parent, **kwargs):
	children = kwargs.pop("children", [])
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

'''
Editing interests test cases:
1) add a new interest
get_or_create() takes care of this
already built into the algorithm

2) delete an interest
deleted interest will be left out of new dist matrix, but will need to be deleted from the 
	database and removed from each user who has chosen it
interest_to_delete.user_set.all() gets the users who have chosen it

3) change a single interest name (assume no tooltip or any other identifier)
I think this has to happen manually
BEFORE running load_interests.py,
./manage.py shell
from snakd.apps.interest.models import Interest
i = Interest.objects.get_or_create(name="old_name")
i.name = "new_name"
i.save()
NOW that the name is changed in the db, the json file can be reloaded

4) two interests with the same name, change a tooltip
try:
	get_or_create(name="name_of_two_interests")
except Interest.MultipleObjectsReturned:
	get_or_create(tooltip="tooltip_of_one")
ACTUALLY I think this is just more easily done manually as well

5) two interests had the same name, one was changed in json
do step 3 first, but use tooltip or parent as an identifier in get_or_create()
can double check with id field: id = models.AutoField(primary_key=True)
'''


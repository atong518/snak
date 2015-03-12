import os
import json

DBDATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(DBDATA_DIR)))

os.environ['PYTHONPATH'] = ROOT_DIR
os.environ['DJANGO_SETTINGS_MODULE'] = os.path.join(ROOT_DIR, "snakd.settings.py")

from snakd.apps.interest.models import Interest

def build_subtree(parent, **kwargs):
	children = kwargs.pop("children")
	kwargs["parent"] = parent
	i = Interest(**kwargs)
	#i = Interest.objects.get_or_create(**kwargs)
	i.save()
	for child in children:
		build_subtree(i, **child)

#root = Interest.objects.get_or_create(name='head', weight=0)
root = Interest(name='head', weight=0)
root.save()

# quick fix to get the file path, should edit DBDATA_DIR though
with open(os.path.join(DBDATA_DIR, "db_data/interests.json")) as jsonfile:
	for child in json.load(jsonfile):
		build_subtree(root, **child)
		
import os
import json

DBDATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(DBDATA_DIR)))

os.environ['PYTHONPATH'] = ROOT_DIR
os.environ['DJANGO_SETTINGS_MODULE'] = os.path.join(ROOT_DIR, "snakd.settings.py")

# TODO: GETORCREATE NOT SAVE

from snakd.apps.interest.models import Interest

def build_subtree(parent, **kwargs):
	children = kwargs.pop("children")
	kwargs["parent"] = parent
	import pdb; pdb.set_trace()
	i = Interest(**kwargs)
	i.save()
	for child in children:
		build_subtree(i, **child)

import pdb; pdb.set_trace()
root = Interest(name='head', weight=0)
root.save()

with open(os.path.join(DBDATA_DIR, "interests.json")) as jsonfile:
	for child in json.load(jsonfile):
		build_subtree(root, **child)
		import pdb; pdb.set_trace()
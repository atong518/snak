import os
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['PYTHONPATH'] = ROOT_DIR
os.environ['DJANGO_SETTINGS_MODULE'] = os.path.join(ROOT_DIR, "snakd.settings.py")

from snakd.apps.interest.models import Interest

def build_subtree(parent, **kwargs):
	kwargs["parent"] = parent
	i = Interest(**kwargs).save()
	for child in kwargs.get("children"):
		build_subtree(i, **child)

root = Interest(name="head", weight=0)

root.save()

with open("interests.json") as jsonfile:
	for child in jsonfile:
		build_subtree(root, **child)
<<<<<<< HEAD
=======


>>>>>>> d118d1f72ea471bc67272baceeb3eab9638d0102

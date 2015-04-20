import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'snakd.settings'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from snakd.apps.interest.models import Interest
from memoize import memoize

# Returns root node of interest tree
def GetInterestRoot():
	return Interest.objects.get(name="HEAD")

# Returns interest tree as a list of dictionaries
@memoize()
def GetInterestTree():
	def GetSubtree(node):
		if not node:
			return {}
		l = {}
		children = node.ChildList()
		l["name"] = node.name
		l["tooltip"] = node.tooltip
		l["weight"] = node.weight
		l["id"] = node.id
		l["children"] = []
		l["hidden"] = node.hidden
		for child in children:
			l["children"].append(GetSubtree(child))
		return l

	root = GetInterestRoot()
	return GetSubtree(root)

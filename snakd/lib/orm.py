import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'snakd.settings'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from snakd.apps.interest.models import Interest

# Returns root node of interest tree
def GetInterestRoot():
	return Interest.objects.get(name="HEAD")

# Returns interest tree as a list of dictionaries
def GetInterestTree():
	def GetSubtree(node):
		if not node:
			return {}
		l = {}
		children = node.ChildList()
		for child in children:
			l[child] = GetSubtree(child)
		return l

	root = GetInterestRoot()
	return GetSubtree(root)
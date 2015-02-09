import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'snakd.settings'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from snakd.apps.interest.models import Interest

from matrix import *

# get all user's interests from relation objects
# need user or relation orm first to write this

def match(current, other, matrix):
	score = 0

	current_interests = getInterests(user)
	other_interests = getInterests(other)

	for int1 in current_interests:
		for int2 in other_interests:

			# need interest order list to iterate into matrix
			score += 1 / (matrix[my_int, other_int) * my_int.get_freq())

	return score / len(current_interests)
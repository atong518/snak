import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'snakd.settings'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from snakd.apps.interest.models import Interest
from snakd.apps.user.models import GenericUser

from matrix import *
from orm import GetInterestRoot

def match(matrix, user1, user2):
	score = 0

	ints1 = user1.getInterestList()
	ints2 = user2.getInterestList()

	root = orm.GetInterestRoot()
	# slightly worried about calling interestList in two places
    int_list = interestList(root)

	for int1 in ints1:
		for int2 in ints2:

			# need interest order list to iterate into matrix
			score += 1 / matrix[getInterestIndex(int1, int_list)][getInterestIndex(int2, int_list)]  # * int1.getFrequency())

	return score / len(ints1)

'''
TO DO:
make the matrix a class with an interest ID list that lines up with the 2D matrix
this will get rid of getInterestIndex and interestList, which are stupid and add to the time complexity
double check getFrequency() in interest models, because it probably won't just return number of users pointing to it
'''
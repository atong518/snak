import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'snakd.settings'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from snakd.apps.interest.models import Interest
from snakd.apps.user.models import GenericUser

from matrix import *

def match(matrix, user1, user2):
    score = 0.0

    ints1 = user1.getInterestList()
    ints2 = user2.getInterestList()

    for int1 in ints1:
        for int2 in ints2:

        	# watch out for dividing by 0
            score += 100 / ((matrix.getValFromInts(int1, int2) + 3) * int1.freq)

    return score / len(ints1)

'''
		### TO DO ###
- double check getFrequency() in interest models, because it probably won't just 
    return number of users pointing to it
- matrix needs to be built and potentially stored in the database, need to structure
	it so it can be easily stored and queried
- take priorities into account when user-interest relation model is rebuilt
'''
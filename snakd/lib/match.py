import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'snakd.settings'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from snakd.apps.interest.models import Interest
from snakd.apps.user.models import GenericUser

from heapq import heappush, heappop

def match(matrix, user1, user2):
    score = 0.0

    ints1 = user1.getInterestList()
    ints2 = user2.getInterestList()

    for int1 in ints1:
        for int2 in ints2:

        	# watch out for dividing by 0
            try:
                score += 100 / ((matrix.getValFromInts(int1, int2) + 3) * int1.getFrequency())
            except:
                pass

    return score / max(len(ints1), 1)

'''
		### TO DO ###
- matrix needs to be built and potentially stored in the database, need to structure
	it so it can be easily stored and queried
- take priorities into account when user-interest relation model is rebuilt
'''

def heapsort(iterable):
    h = []
    for value in iterable:
        heappush(h, value)
    return [heappop(h) for i in range(len(h))]

def bestmatch(matrix, user, opplist):
    options = []
    for opp in opplist:
        score = match(matrix, user, opp)
        options.append((-1*score, opp))
    heapsort(options)
    # TODO: How are we keeping last match?
    return options[0][1]
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

            dist = matrix.getValFromInts(int1, int2)
            score += 100 / math.pow(3, dist) #* int1.getFrequency())
            # right now, direct match is 9x more points than a sibling match

    return score / max(len(ints1), 1)


def heapsort(iterable):
    h = []
    for value in iterable:
        heappush(h, value)
    return [heappop(h) for i in range(len(h))]

def bestmatches(matrix, user, opplist):
    options = []
    for opp in opplist:
        score = match(matrix, user, opp)
        options.append((-1*score, opp))
    heapsort(options)
    # TODO: How are we keeping last match?
    length = min(len(options), 5)
    matches = []
    for i in range(0, length):
        matches.append(options[i][1])
    return matches




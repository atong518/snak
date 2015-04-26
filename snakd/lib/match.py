import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'snakd.settings'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from snakd.apps.interest.models import Interest
from snakd.apps.user.models import GenericUser, CollegeUser

from heapq import heappush, heappop
import math

def match(matrix, user1, user2):
    score = 0.0
    ints1 = user1.getInterestList()
    ints2 = user2.getInterestList()

    # slightly prioritize lower match frequency users
    if isinstance(user1, CollegeUser):
        score += user1.max_match_frequency * 2
    else:
        score += user2.max_match_frequency * 2

    for int1 in ints1:
        for int2 in ints2:
            dist = matrix.getValFromInts(int1, int2)

            # ln function for frequencies, scalable for many interests selected
            freq = math.ceil(math.log1p( int1.freq + int2.freq ))

            # direct match is 5x more points than a sibling match
            score += max( (100 / (math.pow( math.sqrt(5), dist))) - freq, 1)
            
    return score / max(len(ints1) + len(ints2) / 2, 1)


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
    options = heapsort(options)
    length = min(len(options), 5)
    matches = []
    for i in range(0, length):
        matches.append(options[i][1])
    return matches



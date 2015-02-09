import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'snakd.settings'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from snakd.apps.interest.models import Interest

from orm import GetInterestRoot
from orm import GetInterestTree

def interestList(node):
    new_list = [node]

    if node.ChildList() != None: # base case
        for child in node.ChildList():

            # append nodes themselves, not the lists
            for temp in interestList(child): 
                new_list.append(temp)

    return new_list

# could just be stored as a dictionary instead of this
def getInterestIndex(int_list, find_interest):
    for ind, interest in enumerate(int_list):
        if find_interest == interest:
            return ind

def adjList(graph, node):
    adj = []

    # append children
    if node.ChildList() != None:
        for temp in node.ChildList():
            adj.append(temp)

    # append parent
    for parent, child_list in graph.items():
        if node in child_list:
            adj.append(parent)
            break # only has one parent

    return adj

def bfs(graph, rows, start_node, int_list):
    # queue represented by a list
    queue = [start_node]
    visited = []

    depth = 0
    # counts down nodes to when depth increases
    timetodepth = len(queue)

    while len(queue) > 0:
        node = queue.pop(0)
        visited.append(node)
        timetodepth -= 1

        #rows[start_node.id][node.id] = depth
        rows[getInterestIndex(start_node, int_list)][getInterestIndex(node, int_list)] = depth

        for adj in adjList(graph, node):#in graph.get(node, []) for only children
            if adj not in visited:
                queue.append(adj)

        if timetodepth == 0:
            depth += 1
            timetodepth = len(queue)

    return rows

def build_matrix():
    root = orm.GetInterestRoot()

    # holds arbitrary order of interest references, parallels rows/columns of the matrix
    int_list = interestList(root)
    total = len(int_list)

    # distance matrix (square of size total by total)
    rows = []
    for i in range(total):
        rows.append([0] * total)

    tree = orm.GetInterestTree()

    for i, interest in enumerate(int_list):
        rows[i] = bfs(graph, rows, interest, int_list)
            
    return rows

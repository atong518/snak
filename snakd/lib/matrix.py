import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'snakd.settings'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from snakd.apps.interest.models import Interest, InterestMatrix

from orm import GetInterestRoot
from orm import GetInterestTree

class Matrix(object):
    def __init__(self, root):
        self.root = root
        self.order_list = self.interestList(self.root) 
        self.order_dict = self.setOrderDict(self.order_list)
        self.length = len(self.order_list)

        self.rows = []
        for i in range(self.length):
            self.rows.append([0] * self.length)

    def getIntAtIndex(self, index):
        return self.order_list[index]

    def getIndexFromInt(self, interest):
        return self.order_dict[interest]

    def getOrderList(self):
        return self.order_list

    def setValFromInts(self, int1, int2, value):
        self.setValue(self.getIndexFromInt(int1), self.getIndexFromInt(int2), value)

    def setValue(self, row, column, value):
        self.rows[row][column] = value

    def getValFromInts(self, int1, int2):
        return self.getValue(self.getIndexFromInt(int1), self.getIndexFromInt(int2))

    def getValue(self, row, column):
        return self.rows[row][column]

    def interestList(self, node):
        new_list = [node]

        if node.ChildList() != None: # base case
            for child in node.ChildList():

                # append nodes themselves, not the lists
                for temp in self.interestList(child): 
                    new_list.append(temp)

        return new_list

    def setOrderDict(self, order_list):
        d = {}

        for i, interest in enumerate(order_list):
            d[interest] = i

        return d

def bfs(graph, matrix, start_node):
    def concat(list1, list2):
        lst = []
        for item in list1 if list1 else []:
            lst.append(item)
        for item in list2 if list2 else []:
            lst.append(item)
        return lst

    # queue represented by a list
    queue = [start_node]
    visited = []

    depth = 0
    # counts down nodes to when depth increases
    timetodepth = len(queue)
    print("Here!")
    while len(queue) > 0:
        node = queue.pop(0) 
        visited.append(node)
        timetodepth -= 1

        matrix.setValFromInts(start_node, node, depth)

        adjList = concat(node.ChildList(), node.getParent())
        for adj in adjList:
            if adj not in visited:
                queue.append(adj)

        if timetodepth == 0:
            depth += 1
            timetodepth = len(queue)

    return matrix

def buildMatrix():
    print("Starting!")
    m = Matrix(GetInterestRoot())
    tree = GetInterestTree()
    for interest in m.getOrderList():
        print("Looping!")
        m = bfs(tree, m, interest)
    import pdb; pdb.set_trace()
    i = InterestMatrix(matrix = m)
    i.save()
    
def getMatrix():
    matlist = InterestMatrix.objects.all()
    if len(matlist) > 1:
        print("WARNING! Multiple matricies!")
    elif len(matlist) == 0:
        buildMatrix()
    return InterestMatrix.objects.all()[0].matrix



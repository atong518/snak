def buildAdjacencyGraph(node, graph):
    if node.children == None:
        return graph

    for child in node.children:
        graph = buildAdjacencyGraph(child, graph) # why does this work?

    graph[node] = node.children
    return graph

def interestList(node):
    new_list = [node]

    if node.children != None: # base case
        for child in node.children:

            # append nodes themselves, not the lists
            for temp in interestList(child): 
                new_list.append(temp)

    return new_list

def adjList(graph, node):
    adj = []

    # append children
    if node.children != None:
        for temp in node.children:
            adj.append(temp)

    # append parent
    for parent, child_list in graph.items():
        if node in child_list:
            adj.append(parent)
            break # only has one parent

    return adj

def bfs(graph, rows, start_node):
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

        rows[start_node.ID][node.ID] = depth

        for adj in adjList(graph, node):#graph.get(node, []) for only children
            if adj not in visited:
                queue.append(adj)

        if timetodepth == 0:
            depth += 1
            timetodepth = len(queue)

    return rows

def build_matrix(root):
    # holds arbitrary order of interest references, parallels rows/columns of the matrix
    int_list = interestList(root)
    total = len(int_list)

    # distance matrix (square of size total by total)
    rows = []
    for i in range(total):
        rows.append([0] * total)

    # create the adjacency matrix for the tree
    graph = buildAdjacencyGraph(root, {})

    for interest in int_list:
        rows = bfs(graph, rows, interest)
            
    return rows
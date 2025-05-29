

def solve_tsp(G):
    """
    A function for solving Traveling Salesman Problem (TSP) using a nearest-neighbor heuristic algorithm. Function
    takes a graph in the form of a matrix and uses the first node a starting point. From the starting point, the lowest
    cost neighbor is chosen and traveled to. The process is repeated until all vertices have been visited, and then the
    starting node is visited once again. The path taken is then returned.

    Example:    Input: The input Graph is provided in the form of a 2-D matrix (adjacency matrix). Consider the first
                node as the starting point.
                    G = [
                    [0, 2, 3, 20, 1],
                    [2, 0, 15, 2, 20],
                    [3, 15, 0, 20, 13],
                    [20, 2, 20, 0, 9],
                    [1, 20, 13, 9, 0],
                    ]

                Output: A list of indices indicating the path taken. You must return the sequence of nodes, the path
                taken starting from node 0. In this example, G is 5x5, indicating there are 5 nodes in this graph: 0-4.
                You will always begin with node 0, and your path should include every node exactly once, and only go
                between nodes with a nonzero edge between them. You path will end at the starting node.
                    Sample output (For above graph G): [0, 4, 3, 1, 2, 0]

    :param G:   The graph represented as a matrix
    :return:    The order of nodes traveled to
    """
    # creates a list of visited nodes, and adds the starting node to the list
    visited = [0]
    cur = 0
    # this loop will run until all nodes have been visited
    while len(visited) < len(G):
        # for each loop, a blank dictionary is created to store nodes and distances
        dist = {}
        # each node in the graph is added to the dictionary with the cost as the key and the node index as the value
        for i in range(len(G[cur])):
            dist[G[cur][i]] = i
        # remove nodes that have a cost of 0 (indicates no edge, therefore not a valid option)
        dist.pop(0)
        # this while loop removes any nodes that have already been visited, ensuring each is only visited once
        while dist[min(dist)] in visited:
            dist.pop(min(dist))
        # of the remaining unvisited nodes, the one with the lowest cost is visited next
        visited.append(dist[min(dist)])
        cur = dist[min(dist)]
    # after all other nodes have been visited, the starting node is added to the end of the list, completing the TSP
    visited.append(0)
    return visited


# -------------------------------------------------------------------------------------------------------------------- #


if __name__ == "__main__":

    g = [
        [0, 2, 3, 20, 1],
        [2, 0, 15, 2, 20],
        [3, 15, 0, 20, 13],
        [20, 2, 20, 0, 9],
        [1, 20, 13, 9, 0],
        ]

    test = solve_tsp(g)
    print(test)



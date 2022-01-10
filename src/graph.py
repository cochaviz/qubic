# class Node:
#     def __init__(self, id):
#         self.id = id
#         self.edges = []
#
#
# class Edge:
#     def __init__(self, node1, node2, key):
#         self.start = node1
#         self.end = node2
#         self.key = key
#
#
# class Graph:
#     def __init__(self):
#         self.nodes = []
#         self.edges = []
#
#     def add_node(self, id):
#         self.nodes[id] = Node(id)
#
#     def has_node(self, id):
#         return id in self.nodes
#
#     def add_edge(self, id1, id2, key):
#         if id1 not in self.nodes:
#             self.add_node(id1)
#
#         if id2 not in self.nodes:
#             self.add_node(id2)
#
#         edge = Edge(self.nodes[id1], self.nodes[id2], key)
#         reverse_edge = Edge(self.nodes[id2], self.nodes[id1], key)
#
#         self.nodes[id1].edges.append(edge)
#         self.nodes[id2].edges.append(reverse_edge)
#
#         self.edges[key] = edge
#
#     def is_cyclic(self, start_id):
#         return self.get_cycle(start_id)
#
#     def get_cycle(self, start_id):
#         """
#         return list of nodes and edges involved in a cycle
#         """
#         # graph is too small to have cycles
#         # if len(self.nodes) < 2:
#         #     return None
#
#         start = self.nodes[start_id]
#         visited = {}  # set of visited nodes
#         end_to_edge = {}  # map
#
#         for edge in start.edges:
#             if edge.end in visited:
#                 return [[edge.start.id, edge.end.id],
#                         [edge.key, end_to_edge[edge.end]]]
#
#             visited.add(edge.end)
#             end_to_edge[edge.end] = edge

from collections import defaultdict


class Graph:
    def __init__(self, vertices):
        # number of vertices
        self.vertices = vertices

        self.graph = defaultdict(list)

    # Function to add an edge to graph
    def add_edge(self, v, w):
        # Add w to v_s list
        self.graph[v].append(w)

        # Add v to w_s list
        self.graph[w].append(v)

    # A recursive function that uses
    # visited[] and parent to detect
    # cycle in subgraph reachable from vertex v.
    def is_cyclic_util(self, v, visited, parent):

        # Mark the current node as visited
        visited[v] = True

        # Recur for all the vertices
        # adjacent to this vertex
        for i in self.graph[v]:

            # If the node is not
            # visited then recurse on it
            if not visited[i]:
                if self.is_cyclic_util(i, visited, v):
                    return True
            # If an adjacent vertex is
            # visited and not parent
            # of current vertex,
            # then there is a cycle
            elif parent != i:
                return True

        return False

    # Returns true if the graph
    # contains a cycle, else false.
    def is_cyclic(self):

        # Mark all the vertices
        # as not visited
        visited = [False] * self.vertices

        # Call the recursive helper
        # function to detect cycle in different
        # DFS trees
        for i in range(self.vertices):

            # Don't recur for u if it
            # is already visited
            if not visited[i]:
                if self.is_cyclic_util(i, visited, -1):
                    return []

        return False

    # TODO: make function return a list of nodes where the cycle occurs
    def get_cycle(self, start):


from collections import defaultdict


class Node:
    def __init__(self, id):
        """
        a node has an id, equal to the index of the corresponding field in tic-tac-toe
        and an array of edges from this node
        """
        self.id = id
        self.edges = []


class Edge:
    def __init__(self, node1, node2, key):
        """
        store the ids of the two nodes and the key, which is equal to the turn number
        """
        self.start = node1
        self.end = node2
        self.key = key


def path(edge, prev):
    """
    return list of nodes and edges involved in a cycle

    @param edge: edge where the cycle was detected
    @param prev: dict previous node -> edge
    """
    cycle_node_ids = []
    cycle_edge_keys = [edge.key]

    curr_node = edge.start
    while prev.get(curr_node) is not None:
        curr_edge = prev[curr_node]
        cycle_node_ids.append(curr_node.id)
        cycle_edge_keys.append(curr_edge.key)
        curr_node = curr_edge.start

    cycle_node_ids.append(curr_node.id)

    curr_node = edge.end
    while prev.get(curr_node) is not None:
        curr_edge = prev[curr_node]
        cycle_node_ids.insert(0, curr_node.id)
        cycle_edge_keys.insert(0, curr_edge.key)
        curr_node = curr_edge.start

    return [cycle_node_ids, cycle_edge_keys]


class Graph:
    def __init__(self):
        """
        use dicts for key assignment, like nodes[id]
        """
        self.nodes = dict()
        self.edges = dict()

    def add_node(self, id):
        self.nodes[id] = Node(id)

    def has_node(self, id):
        return id in self.nodes

    def add_edge(self, id1, id2, key):
        if id1 not in self.nodes:
            self.add_node(id1)

        if id2 not in self.nodes:
            self.add_node(id2)

        edge = Edge(self.nodes[id1], self.nodes[id2], key)
        reverse_edge = Edge(self.nodes[id2], self.nodes[id1], key)

        self.nodes[id1].edges.append(edge)
        self.nodes[id2].edges.append(reverse_edge)

        self.edges[key] = edge

    def get_cycle(self, start_id):
        """
        return list of nodes and edges involved in a cycle
        """
        # graph is too small to have cycles
        if len(self.nodes) < 2:
            return None

        start = self.nodes[start_id]
        visited = []  # list of visited nodes
        end_to_edge = {}  # map

        # quick check for cycles with len = 2
        for edge in start.edges:
            if edge.end in visited:
                return [[edge.start.id, edge.end.id],
                        [edge.key, end_to_edge[edge.end].key]]

            visited.append(edge.end)
            end_to_edge[edge.end] = edge

        # do proper cycles search for cycles with len > 2
        q = [start]
        layers = defaultdict()
        prev = dict()
        layers[start] = 0
        prev[start] = None

        while q is not None and len(q) > 0:
            # shift the list
            curr = q[0]
            del q[0]

            layer = layers[curr]

            for edge in curr.edges:
                if edge.end in layers:
                    if layers[edge.end] == layer - 1:
                        continue
                    else:
                        return path(edge, prev)
                q.append(edge.end)
                layers[edge.end] = layer + 1
                prev[edge.end] = edge

    def remove_cycle(self, node_edge_list):
        """
        Remove all nodes and edges in the node_edge_list from the graph
        node_edge_list has the following form: [[nodes], [edges]]
        """
        for i in node_edge_list[1]:
            self.edges.pop(i)

        for i in node_edge_list[0]:
            self.nodes.pop(i)


def test1():
    g = Graph()
    g.add_node('1')
    g.add_node('2')
    g.add_node('3')
    g.add_edge('1', '2', 'ab')
    g.add_edge('2', '3', 'bc')
    g.add_edge('3', '1', 'ca')

    print(g.get_cycle('1'))
    # expected: [['3', '2', '1'], ['ca', 'bc', 'ab']]


def test2():
    g = Graph()
    g.add_node('1')
    g.add_node('2')
    g.add_edge('1', '2', 'a')
    g.add_edge('1', '2', 'b')

    print(g.get_cycle('1'))


def test3():
    g = Graph()
    g.add_node('1')
    g.add_node('2')
    g.add_edge('1', '2', 'a')
    g.add_edge('2', '1', 'b')

    print(g.get_cycle('1'))


def test4():
    g = Graph()
    g.add_node('a')
    g.add_node('b')

    g.add_edge('a', 'b', 'x1')
    print(g.get_cycle('b'))
    # expect: None


if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()

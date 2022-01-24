from random import getrandbits
from queue import Queue
from collections import defaultdict
import threading

from circuit_solver import quantum_coin_flip
from util import GameProperties

# todo: could implement classical random solver or one where the plaer chooses which tile/state to collapse to


def resolve_superposition(board, graph, cycle, quantic=True):
    [_, edges_id] = cycle

    # select first edge to decide collapse
    edge_id = edges_id[0]
    edge = graph.edges[edge_id]

    # decide the coin toss
    # coin_toss_res = quantum_coin_flip()
    if quantic:
        #todo: thread this statement
        list_argument = []
        thread1 = threading.Thread(target=quantum_coin_flip, args=(list_argument,))
        thread1.start()
        thread1.join(2.5)
        if len(list_argument) == 0:
            print("Timeout happened :(")
            coin_toss_res = getrandbits(1)
        else:
            print("Quantic result!")
            coin_toss_res = int(list_argument[0])
    else:
        coin_toss_res = getrandbits(1)

    # either the key of this edge lands on the start or end node
    # it lands on the start node if coin toss is a 0, on the end node otherwise
    node_id = edge.start.id
    if coin_toss_res == 1:
        node_id = edge.end.id

    # Use a queue of tuples to resolve all edges, where the tuples contain:
    # (key of edge, id of node where this key must land)
    queue = Queue(maxsize=9)
    queue.put((edge_id, node_id))
    return_dict = defaultdict(lambda: -1)
    decided_node_ids = []

    # TODO: add a restraint for adding edges that have already been decided:
    # use the defaultdict return_dict's default value maybe?
    while not queue.empty():
        elem = queue.get()
        node = graph.nodes[elem[1]]
        for edge_iter in node.edges:
            if edge_iter.key is not elem[0] and edge_iter.end.id not in decided_node_ids:
                queue.put((edge_iter.key, edge_iter.end.id))
        row, col = GameProperties.id_to_position(node.id)
        board[row][col] = elem[0][0]
        return_dict[node.id] = elem[0]
        decided_node_ids.append(node.id)

    return return_dict

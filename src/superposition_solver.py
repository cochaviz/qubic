from random import getrandbits
from queue import Queue
from collections import defaultdict
import random

from circuit_solver import quantum_coin_flip
from util import id_to_position


# todo: not sure if it actually needs to return final marks too
def resolve_superposition_quantic(board, graph, cycle):
    """
    returns dictionary containing tile -> final mark

    """
    [nodes_id, _] = cycle

    # select square to be the collapse point
    node_id = nodes_id[0]

    [row, col] = id_to_position(node_id)

    # collapse state on board tile
    coin_toss_res = quantum_coin_flip()
    mark = board[row][col][coin_toss_res]  # get one random mark to collapse

    # handle collapse
    visited = {mark}
    return handle_collapse(mark, node_id, board, graph, visited)


def handle_collapse(mark, node_id, board, graph, visited):
    """
    collapses all states involved in cycle on the board.

    @param mark: final, collapsed mark to placed on initial tile.
    @param node_id: id of tile where the mark should be placed.
    @param board: Board
    @param graph: Graph
    @param visited: set of states marks that have already been collapsed.
    """
    [row, col] = id_to_position(node_id)
    board[row][col] = mark[0]  # get mark body: o or x

    res = dict()
    res[node_id] = mark

    for edge in graph.nodes[node_id].edges:
        if edge.key not in visited:
            visited.add(edge.key)
            res = {**handle_collapse(edge.key, edge.end.id, board, graph, visited),
                   **res}  # union of dict objects
    return res

# todo: could implement classical random solver or one where the plaer chooses which tile/state to collapse to


def resolve_superposition_quantic(board, graph, cycle):
    [_, edges_id] = cycle

    # select first edge to decide collapse
    edge_id = edges_id[0]
    edge = graph.edges[edge_id]

    # decide the coin toss
    # coin_toss_res = quantum_coin_flip()
    coin_toss_res = 0
    if random.random() > 0.5:
        coin_toss_res = 1

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
        [row, col] = id_to_position(node.id)
        board[row][col] = elem[0][0]
        return_dict[node.id] = elem[0][0]
        decided_node_ids.append(node.id)

    return return_dict

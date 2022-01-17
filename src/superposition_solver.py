from random import getrandbits

from circuit_solver import quantum_coin_flip
from util import id_to_position


# todo: not sure if it actually needs to return final marks too
def resolve_superposition(board, graph, cycle, quantic=True):
    """
    returns dictionary containing tile -> final mark

    """
    [nodes_id, _] = cycle

    # select square to be the collapse point
    node_id = nodes_id[0]

    row, col = id_to_position(node_id)

    # collapse state on board tile
    if quantic:
        coin_toss_res = quantum_coin_flip()
    else:
        coin_toss_res = getrandbits(1)
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
    row, col = id_to_position(node_id)
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

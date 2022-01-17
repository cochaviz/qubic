import math


def id_to_position(node_id):
    return math.floor(node_id / 4), node_id % 4


def position_to_id(row, col):
    return row * 4 + col

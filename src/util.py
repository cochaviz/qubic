import math


def id_to_position(node_id):
    return [math.floor(node_id / 3), node_id % 3]

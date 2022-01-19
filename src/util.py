import math
from enum import Enum


class GameProperties:
    __instance = None

    @staticmethod
    def get_instance():
        if GameProperties.__instance is None:
            raise EnvironmentError('Singleton has not been initialized yet!')
        return GameProperties.__instance

    def __init__(self, dim, view):
        self.dim = dim
        self.view = view

        GameProperties.__instance = self

    @staticmethod
    def id_to_position(node_id):
        if GameProperties.__instance.dim is None:
            raise EnvironmentError('Board dimension has not been defined yet!')

        return math.floor(node_id / GameProperties.__instance.dim), node_id % GameProperties.__instance.dim

    @staticmethod
    def position_to_id(row, col):
        if GameProperties.__instance is None:
            raise EnvironmentError('Board dimension has not been defined yet!')

        return row * GameProperties.__instance.dim + col

    @staticmethod
    def view():
        return GameProperties.__instance.view


class Views(Enum):
    HOME = 1
    BOARD = 2

import math


class GameProperties:
    __instance = None

    @staticmethod
    def get_instance():
        if GameProperties.__instance is None:
            GameProperties()
        return GameProperties.__instance

    def __init__(self, dim=3):
        self.dim = dim

        GameProperties.__instance = self

    @staticmethod
    def id_to_position(node_id):
        if GameProperties.__instance is None:
            raise EnvironmentError('Singleton has not been initialized yet!')

        return math.floor(node_id / GameProperties.__instance.dim), node_id % GameProperties.__instance.dim

    @staticmethod
    def position_to_id(row, col):
        if GameProperties.__instance is None:
            raise EnvironmentError('Singleton has not been initialized yet!')

        return row * GameProperties.__instance.dim + col

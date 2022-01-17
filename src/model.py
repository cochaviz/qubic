import graph as graphlib
from superposition_solver import resolve_superposition
from util import id_to_position, position_to_id


class Board:
    def __init__(self):
        self.board = None
        self.final = None
        self.winner = None  # can either be 'o', 'x', or '-' for a draw
        self.turnNum = 1
        self.subTurnNum = 0
        self.prevSubTurnIndex = None
        self.graph = graphlib.Graph()

        self.reset()

    def reset(self):
        """
        Resets the board
        """
        # 2d array with empty lists in every cell
        # todo: refactor
        self.board = [[[], [], [], []],
                      [[], [], [], []],
                      [[], [], [], []],
                      [[], [], [], []]]
        self.final = [[False] * 4, [False] * 4, [False] * 4, [False] * 4]
        self.winner = None
        self.turnNum = 1
        self.subTurnNum = 0
        self.prevSubTurnIndex = None
        self.graph = graphlib.Graph()

    def check_win(self):
        """
        Checks which player has won, returns a tuple where the first element is the winner and the
        second a tuple with coordinates for which column/row/diagonal is the winning one
        """
        # check if there is already a winner
        if self.winner is not None:
            return self.winner, None

        # check that it is player's final move
        if self.subTurnNum == 0:
            # checking for winning rows
            for row in range(0, 4):
                if self.final[row][0] and self.final[row][1] and self.final[row][2] and self.final[row][3] and \
                        (self.board[row][0] == self.board[row][1] == self.board[row][2] == self.board[row][3]):
                    self.winner = self.board[row][0]
                    return self.winner, ((row, 0), (row, 3))

            # checking for winning columns
            for col in range(0, 4):
                if self.final[0][col] and self.final[1][col] and self.final[2][col] and self.final[3][col] and \
                        (self.board[0][col] == self.board[1][col] == self.board[2][col] == self.board[3][col]):
                    self.winner = self.board[0][col]
                    return self.winner, ((0, col), (3, col))

            # check for diagonal winners
            if self.final[0][0] and self.final[1][1] and self.final[2][2] and self.final[3][3] and \
                    (self.board[0][0] == self.board[1][1] == self.board[2][2] == self.board[3][3]):
                # game won diagonally left to right
                self.winner = self.board[0][0]
                return self.winner, ((0, 0), (3, 3))

            if self.final[0][3] and self.final[1][2] and self.final[2][1] and self.final[3][0] and \
                    (self.board[0][3] == self.board[1][2] == self.board[2][1] == self.board[3][0]):
                # game won diagonally right to left
                self.winner = self.board[0][2]
                return self.winner, ((0, 3), (3, 0))

        if self.turnNum > 32:
            self.winner = '-'
            return self.winner, None
        return None, None

    def place_x(self, row, col):
        """
        Places an X on the specified location
        """
        self.place(row, col, 'x' + str(self.turnNum))

    def place_o(self, row, col):
        """
        Places an O on the specified location
        """
        self.place(row, col, 'o' + str(self.turnNum))

    def place(self, row, col, char):
        """
        This method updates the board with the new character to be placed,
        and checks if a cycle needs to be collapsed, and does so if it is necessary
        """
        new_index = position_to_id(row, col)
        self.board[row][col].append(char)

        if self.prevSubTurnIndex is not None:
            self.graph.add_edge(self.prevSubTurnIndex, new_index, char)
            self.prevSubTurnIndex = None

            cycle = self.graph.get_cycle(new_index)
            if cycle is not None:
                tile_to_mark = resolve_superposition(self.board, self.graph, cycle, quantic=False)

                # Mark all nodes in the cycle as final
                for node_id in tile_to_mark.keys():
                    row, col = id_to_position(node_id)
                    self.final[row][col] = True

                # Remove all edges and nodes that were in the cycle
                self.graph.remove_cycle(cycle)


class GameState:
    def __init__(self):
        self.board = Board()
        self.reset()

    def x_moves(self):
        """
        Returns true if its X's turn to move
        """
        return self.board.turnNum % 2 == 1

    def take_turn(self, row, col):
        """
        Places an X or an O on the specified location
        """
        if self.x_moves():
            self.board.place_x(row, col)
        else:
            self.board.place_o(row, col)

        if self.board.subTurnNum == 1:
            self.board.turnNum += 1
        else:
            self.board.prevSubTurnIndex = position_to_id(row, col)

        self.board.subTurnNum = (self.board.subTurnNum + 1) % 2

    def reset(self):
        self.board.reset()

    def is_invalid_move(self, row, col):
        """
        Checks to see if a move is valid or not, based on the row and column coordinates
        Returns True if the move is valid, a message containing info on why not otherwise
        """
        if self.board.turnNum > 32 or self.board.winner is not None:
            return "The game is already over!"

        if row > 3 or col > 3 or row < 0 or col < 0:
            return "Please click somewhere on the grid"

        if self.board.final[row][col]:
            return "This tile is final, and cannnot be chosen"

        # Check if the player does their two submoves on different tiles
        new_index = position_to_id(row, col)
        if self.board.prevSubTurnIndex == new_index:
            return "Your second move needs to be a different tile"

        return False

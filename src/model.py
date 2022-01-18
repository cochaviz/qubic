import graph as graphlib
from superposition_solver import resolve_superposition
from util import GameProperties

# winning diagonal lines
THREE_BY_THREE_WINNING_LINES = [[0, 4, 8], [2, 4, 6]]
FOUR_BY_FOUR_WINNING_LINES = [[0, 5, 10, 15], [3, 6, 9, 12]]
FIVE_BY_FIVE_WINNING_LINES = [[0, 6, 12, 18], [6, 12, 18, 24],
                              [1, 7, 13, 19], [5, 11, 17, 23],
                              [4, 8, 12, 16], [8, 12, 16, 20],
                              [3, 7, 11, 15], [9, 13, 17, 21]]


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
        dim = GameProperties.get_instance().dim
        # dim x dim array with empty lists in every cell
        self.board = [[[] for _ in range(dim)] for _ in range(dim)]
        # dim x dim array with False in every cell
        self.final = [[False] * dim for _ in range(dim)]

        # self.board = [[[], [], [], []],
        #               [[], [], [], []],
        #               [[], [], [], []],
        #               [[], [], [], []]]
        # self.final = [[False] * 4, [False] * 4, [False] * 4, [False] * 4]
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

        dim = GameProperties.get_instance().dim
        # check that it is player's final move
        if self.subTurnNum == 0:
            # checking for winning rows
            for row in range(0, dim):
                if self.check_winning_row(row, dim):
                    # if self.final[row][0] and self.final[row][1] and self.final[row][2] and self.final[row][3] and \
                    #         (self.board[row][0] == self.board[row][1] == self.board[row][2] == self.board[row][3]):
                    self.winner = self.board[row][0]
                    return self.winner, ((row, 0), (row, dim - 1))

            # checking for winning columns
            for col in range(0, dim):
                if self.check_winning_col(col, dim):
                    # if self.final[0][col] and self.final[1][col] and self.final[2][col] and self.final[3][col] and \
                    #         (self.board[0][col] == self.board[1][col] == self.board[2][col] == self.board[3][col]):
                    self.winner = self.board[0][col]
                    return self.winner, ((0, col), (dim - 1, col))

            # check for diagonal winners
            diag_winner = self.check_diagonal_win(dim)
            if diag_winner is not None:
                winner, winstate = diag_winner
                self.winner = winner
                return winner, winstate

            # if self.final[0][0] and self.final[1][1] and self.final[2][2] and self.final[3][3] and \
            #         (self.board[0][0] == self.board[1][1] == self.board[2][2] == self.board[3][3]):
            #     # game won diagonally left to right
            #     self.winner = self.board[0][0]
            #     return self.winner, ((0, 0), (3, 3))
            #
            # if self.final[0][3] and self.final[1][2] and self.final[2][1] and self.final[3][0] and \
            #         (self.board[0][3] == self.board[1][2] == self.board[2][1] == self.board[3][0]):
            #     # game won diagonally right to left
            #     self.winner = self.board[0][2]
            #     return self.winner, ((0, 3), (3, 0))

        # todo: add comments
        if self.turnNum > dim ** 2:
            self.winner = '-'
            return self.winner, None
        return None, None

    def check_winning_row(self, row, dim):
        if dim < 2:
            raise ValueError('board dimension is too small.')
        tiles_are_final = True
        mark = self.board[row][0]
        tiles_have_same_mark = True
        for col in range(dim):
            tiles_are_final = tiles_are_final and self.final[row][col]
            tiles_have_same_mark = tiles_have_same_mark and mark == self.board[row][col]

        return tiles_are_final and tiles_have_same_mark

    def check_winning_col(self, col, dim):
        if dim < 2:
            raise ValueError('board dimension is too small.')
        tiles_are_final = True
        mark = self.board[0][col]
        tiles_have_same_mark = True
        for row in range(dim):
            tiles_are_final = tiles_are_final and self.final[row][col]
            tiles_have_same_mark = tiles_have_same_mark and mark == self.board[row][col]

        return tiles_are_final and tiles_have_same_mark

    def check_diagonal_win(self, dim):
        if dim == 3:
            lines = THREE_BY_THREE_WINNING_LINES
        elif dim == 4:
            lines = FOUR_BY_FOUR_WINNING_LINES
        elif dim == 5:
            lines = FIVE_BY_FIVE_WINNING_LINES
        else:
            raise ValueError('board dimension is not implemented.')

        for line in lines:
            tiles_are_final = True
            tiles_have_same_mark = True
            mark = None
            for node_id in line:
                row, col = GameProperties.id_to_position(node_id)
                # todo: think about this
                if mark is None:
                    mark = self.board[row][col]
                tiles_are_final = tiles_are_final and self.final[row][col]
                tiles_have_same_mark = tiles_have_same_mark and mark == self.board[row][col]
            if tiles_are_final and tiles_have_same_mark:
                row, col = GameProperties.id_to_position(line[0])
                last_row, last_col = GameProperties.id_to_position(line[-1])
                return self.board[row][col], ((row, col), (last_row, last_col))

        return None

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
        new_index = GameProperties.position_to_id(row, col)
        self.board[row][col].append(char)

        if self.prevSubTurnIndex is not None:
            self.graph.add_edge(self.prevSubTurnIndex, new_index, char)
            self.prevSubTurnIndex = None

            cycle = self.graph.get_cycle(new_index)
            if cycle is not None:
                tile_to_mark = resolve_superposition(self.board, self.graph, cycle, quantic=False)

                # Mark all nodes in the cycle as final
                for node_id in tile_to_mark.keys():
                    row, col = GameProperties.id_to_position(node_id)
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
            self.board.prevSubTurnIndex = GameProperties.position_to_id(row, col)

        self.board.subTurnNum = (self.board.subTurnNum + 1) % 2

    def reset(self):
        self.board.reset()

    def is_invalid_move(self, row, col):
        """
        Checks to see if a move is valid or not, based on the row and column coordinates
        Returns True if the move is valid, a message containing info on why not otherwise
        """
        dim = GameProperties.get_instance().dim
        if self.board.turnNum > dim**2 or self.board.winner is not None:
            return "The game is already over!"

        if row >= dim or col >= dim or row < 0 or col < 0:
            return "Please click somewhere on the grid"

        if self.board.final[row][col]:
            print(row, col)
            print(self.board.final[row][col])
            return "This tile is final, and cannot be chosen"

        # Check if the player does their two sub-moves on different tiles
        new_index = GameProperties.position_to_id(row, col)
        if self.board.prevSubTurnIndex == new_index:
            return "Your second move needs to be a different tile"

        return False

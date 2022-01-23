from collections import defaultdict

import graph as graphlib
from gate import Gate
from superposition_solver import resolve_superposition
from util import GameProperties
from circuit_solver import resolve_circuit

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
        self.marks = set()
        self.graph = graphlib.Graph()

        self.gates_list = []

        self.reset()

    def reset(self):
        """
        Resets the board
        """
        dim = GameProperties.get_instance().dim
        # dim x dim array with empty lists in every cell
        self.board = [[[] for _ in range(dim)] for _ in range(dim)]
        # dim x dim array with False in every cell
        self.final = [[0] * dim for _ in range(dim)]

        self.winner = None
        self.turnNum = 1
        self.subTurnNum = 0
        self.prevSubTurnIndex = None
        self.marks.clear()
        self.graph = graphlib.Graph()
        self.gates_list.clear()

    def check_win(self):
        """
        Checks which player has won, returns a tuple where the first element is the winner and the
        second a tuple with coordinates for which column/row/diagonal is the winning one
        """
        # Keep track of the lowest maximal subscript, to calculate the correct winner
        lowest_max_subscript = 1000
        return_value = None, None
        dim = GameProperties.get_instance().dim

        # check if there is already a winner
        if self.winner is not None:
            return self.winner, None

        # check that it is player's final move
        if self.subTurnNum == 0:
            # check for winning rows
            for row in range(0, dim):
                # winning mark, winning position, highest_final
                winning_row = self.get_winning_row(row, dim, lowest_max_subscript)
                if winning_row:
                    return_value = winning_row[0], winning_row[1]
                    lowest_max_subscript = winning_row[2]

            # check for winning columns
            for col in range(0, dim):
                winning_col = self.get_winning_col(col, dim, lowest_max_subscript)
                if winning_col:
                    return_value = winning_col[0], winning_col[1]
                    lowest_max_subscript = winning_col[2]

            # check for diagonal winners
            winning_diag = self.get_winning_diag(dim, lowest_max_subscript)
            if winning_diag is not None:
                return_value = winning_diag[0][0], winning_diag[0][1]
                lowest_max_subscript = winning_diag[1]

        # max allowed number of moves is equal to the number of squares on board
        elif self.turnNum > dim ** 2 and return_value[0] is None:
            return_value = '-', None

        self.winner = return_value[0]
        return return_value

    def get_winning_row(self, row, dim, lowest_max_subscript):
        if dim < 2:
            raise ValueError('board dimension is too small.')

        return_value = None

        if dim == 3 or dim == 4:
            all_final = True
            all_equal = True
            first_elem = self.board[row][0]
            highest_final = self.final[row][0]

            for col in range(1, dim):
                all_final &= self.final[row][col] > 0
                all_equal &= first_elem == self.board[row][col]
                highest_final = self.final[row][col] if self.final[row][col] > highest_final else highest_final

            if all_equal and all_final and first_elem is not None and highest_final < lowest_max_subscript:
                lowest_max_subscript = highest_final
                return_value = [first_elem, ((row, 0), (row, dim - 1)), lowest_max_subscript]

        elif dim == 5:
            for starting_col in range(2):
                for row in range(dim):
                    all_final = True
                    all_equal = True
                    first_elem = self.board[row][starting_col]
                    highest_final = self.final[row][starting_col]

                    for col in range(starting_col + 1, dim):
                        all_final &= self.final[row][col] > 0
                        all_equal &= first_elem == self.board[row][col]
                        highest_final = self.final[row][col] if self.final[row][col] > highest_final else highest_final

                    if all_equal and all_final and first_elem is not None and highest_final < lowest_max_subscript:
                        lowest_max_subscript = highest_final
                        return_value = [first_elem, ((row, 0), (row, dim - 1)), lowest_max_subscript]

        return return_value

    def get_winning_col(self, col, dim, lowest_max_subscript):
        if dim < 2:
            raise ValueError('board dimension is too small.')

        return_value = None
        if dim == 3 or dim == 4:
            all_final = True
            all_equal = True
            first_elem = self.board[0][col]
            highest_final = self.final[0][col]
            for row in range(1, dim):
                all_final &= self.final[row][col] > 0
                all_equal &= first_elem == self.board[row][col]
                highest_final = self.final[row][col] if self.final[row][col] > highest_final else highest_final

            if all_equal and all_final and first_elem is not None and highest_final < lowest_max_subscript:
                lowest_max_subscript = highest_final
                return_value = first_elem, ((0, col), (dim - 1, col)), lowest_max_subscript
        elif dim == 5:
            for starting_row in range(2):
                all_final = True
                all_equal = True
                first_elem = self.board[starting_row][col]
                highest_final = self.final[starting_row][col]
                for row in range(1, dim):
                    all_final &= self.final[row][col] > 0
                    all_equal &= first_elem == self.board[row][col]
                    highest_final = self.final[row][col] if self.final[row][col] > highest_final else highest_final

                if all_equal and all_final and first_elem is not None and highest_final < lowest_max_subscript:
                    lowest_max_subscript = highest_final
                    return_value = first_elem, ((0, col), (dim - 1, col)), lowest_max_subscript

        return return_value

    def get_winning_diag(self, dim, lowest_max_subscript):
        if dim == 3:
            lines = THREE_BY_THREE_WINNING_LINES
        elif dim == 4:
            lines = FOUR_BY_FOUR_WINNING_LINES
        elif dim == 5:
            lines = FIVE_BY_FIVE_WINNING_LINES
        else:
            raise ValueError('board dimension is not implemented.')

        return_value = None
        for line in lines:
            all_final = True
            all_equal = True

            # position of first node in line
            row, col = GameProperties.id_to_position(line[0])

            first_elem = self.board[row][col]
            highest_final = self.final[row][col]
            for node_id in line:
                row, col = GameProperties.id_to_position(node_id)
                all_final &= self.final[row][col] > 0
                all_equal &= first_elem == self.board[row][col]

            # if all_equal and all_final and first_elem is not None and highest_final < lowest_max_subscript:
            #     lowest_max_subscript = highest_final
            #     return_value = first_elem, ((0, 2), (2, 0))
            if all_equal and all_final and first_elem is not None and highest_final < lowest_max_subscript:
                last_row, last_col = GameProperties.id_to_position(line[-1])
                lowest_max_subscript = highest_final
                return_value = first_elem, ((row, col), (last_row, last_col))

        return [return_value, lowest_max_subscript] if return_value is not None else None

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

        if self.prevSubTurnIndex is not None and self.prevSubTurnIndex != new_index:
            self.graph.add_edge(self.prevSubTurnIndex, new_index, char)
            self.marks.add(char)
            self.prevSubTurnIndex = None

            cycle = self.graph.get_cycle(new_index)
            if cycle is not None:
                # first node in cycle
                nodes = self.graph.get_connected_nodes(cycle[0][0])

                marks_in_nodes = set()

                for node in nodes:
                    row, col = GameProperties.id_to_position(node)
                    marks_in_nodes.update(self.board[row][col])

                # gates involved in measurement
                gates = []

                for gate in self.gates_list:
                    if gate.target_state in marks_in_nodes or gate.control_state in marks_in_nodes:
                        gates.append(gate)

                measurements = resolve_circuit(gates)

                tile_to_mark = resolve_superposition(self.graph, cycle, quantic=False)

                # todo: remove mark from self.marks
                # todo: remove gate from self.gates_list
                for tile, mark in tile_to_mark.items():
                    row, col = GameProperties.id_to_position(tile)
                    if mark in measurements.keys():
                        self.board[row][col] = 'x' if measurements[mark] == 1 else 'o'
                    else:
                        self.board[row][col] = mark[0]

                # Mark all nodes in the cycle as final
                for node_id in tile_to_mark.keys():
                    row, col = GameProperties.id_to_position(node_id)
                    self.final[row][col] = int(tile_to_mark[node_id][1:])

                # Remove all edges and nodes that were in the cycle
                self.graph.remove_cycle(cycle)
        # When there is 1 possible spot left:
        elif self.prevSubTurnIndex == new_index:
            self.board[row][col] = char[0]
            self.final[row][col] = int(char[1:])


# TODO: only measure gates that are inside the cycle
class GameState:
    def __init__(self):
        self.board = Board()
        self.games_played = -1

        # queue of players
        # todo: update reset/new game method
        self.players = [Player(), Player()]

        self.first_player_uses = 'o'
        self.player1_score = 0
        self.player2_score = 0

        self.board.reset()

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
            self.players.append(self.players.pop(0))
        else:
            self.board.prevSubTurnIndex = GameProperties.position_to_id(row, col)

        self.board.subTurnNum = (self.board.subTurnNum + 1) % 2

    # todo: move this to Board
    def place_gate(self, gate, mark, control_state_index=None):
        if self.board.subTurnNum != 0 or self.get_moving_player().gates_count[gate] == 0 or mark not in self.board.marks:
            return False
        if gate is Gate.Gates.CNOT:
            if control_state_index is None or control_state_index not in self.board.marks:
                return False
            self.board.gates_list.append(Gate(mark, gate.value, control_state_index))
        else:
            self.board.gates_list.append(Gate(mark, gate.value))

        self.get_moving_player().gates_count[gate] -= 1

        self.board.turnNum += 1
        self.players.append(self.players.pop(0))

        return True

    def new_game(self):
        self.games_played += 1
        self.first_player_uses = 'x' if self.first_player_uses == 'o' else 'o'
        self.board.reset()

    def is_invalid_move(self, row, col):
        """
        Checks to see if a move is valid or not, based on the row and column coordinates
        Returns True if the move is valid, a message containing info on why not otherwise
        """
        dim = GameProperties.get_instance().dim
        if self.board.turnNum > dim ** 2 or self.board.winner is not None:
            return "The game is already over!"

        if row >= dim or col >= dim or row < 0 or col < 0:
            return "Please click somewhere on the grid"

        if self.board.final[row][col]:
            return "This tile is final, and cannot be chosen"

        # Check if the player does their two sub-moves on different tiles when it's not the last move
        new_index = GameProperties.position_to_id(row, col)
        if self.board.turnNum < dim ** 2 and self.board.prevSubTurnIndex == new_index:
            return "Your second move needs to be a different tile"

        # When it is the last move, check if the player can move on another tile
        elif self.board.turnNum == dim ** 2 and self.board.prevSubTurnIndex == new_index:
            # Check to see how many spots are left (self.final[row][col] == 0) and allow the move
            # if there is only 1 spot left
            num_of_zeros = 0
            for i in self.board.final:
                for j in i:
                    if j == 0:
                        num_of_zeros += 1
            if num_of_zeros > 1:
                return "Your second move needs to be a different tile"

        return False

    def get_moving_player(self):
        return self.players[0]

    def update_scores(self):
        if self.board.winner == '-':
            self.player1_score += 1
            self.player2_score += 1
        elif self.board.winner == 'x':
            if self.first_player_uses == 'x':
                self.player1_score += 2
            else:
                self.player2_score += 2
        else:
            if self.first_player_uses == 'x':
                self.player2_score += 2
            else:
                self.player1_score += 2


class Player:
    def __init__(self):
        self.gates_count = defaultdict()

        self.reset_gates_count()

    def reset_gates_count(self):
        dim = GameProperties.get_instance().dim

        for gate in Gate.Gates:
            # 1 of each gate for 3x3 game
            # 2 per 4x4 game
            # 3 per 5x5 game
            self.gates_count[gate] = dim - 2

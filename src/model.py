class Board():
    def __init__(self):
        self.board = None
        self.winner = None # can either be 'o', 'x', or '-' for a draw

        self.reset()

    def reset(self):
        """
        Resets the board
        """
        self.board = [[None]*3,[None]*3,[None]*3]
        self.winner = None

    def check_win(self):
        """
        Checks which player has won, returns a tuple where the first element is the winner and the
        second a tuple with coordinates for which column/row/diagonal is the winning one
        """
        # check if there is already a winner
        if self.winner is not None:
            return self.winner, None

        # checking for winning rows
        for row in range(0, 3):
            if((self.board[row][0] == self.board[row][1] == self.board[row][2]) and (self.board [row][0] is not None)):
                self.winner = self.board[row][0]
                return self.winner, ((row, 0), (row, 2))

        # checking for winning columns
        for col in range(0, 3):
            if((self.board[0][col] == self.board[1][col] == self.board[2][col]) and (self.board[0][col] is not None)):
                winner = self.board[0][col]
                self.winner = self.board[0][col]
                return self.winner, ((0, col), (2, col))

        # check for diagonal winners
        if (self.board[0][0] == self.board[1][1] == self.board[2][2]) and (self.board[0][0] is not None):
            # game won diagonally left to right
            self.winner = self.board[0][0]
            return self.winner, ((0, 0), (2, 2))

        if (self.board[0][2] == self.board[1][1] == self.board[2][0]) and (self.board[0][2] is not None):
            # game won diagonally right to left
            self.winner = self.board[0][2]
            return self.winner, ((0, 2), (2, 0))

        if(all([all(row) for row in self.board]) and winner is None ):
            return '-'

        return None, None

    def place_x(self, row, col):
        """
        Places an X on the specified location, returns False if the move was unsuccessful and True if succesful
        """
        return self.place(row, col, 'x')

    def place_o(self, row, col):
        """
        Places an O on the specified location, returns False if the move was unsuccessful and True if succesful
        """
        return self.place(row, col, 'o')

    def place(self, row, col, char):
        if (row > 2 or col > 2 or row < 0 or col < 0):
            raise IndexError("Out of bounds")

        if (self.board[row][col] is not None):
            return False

        self.board[row][col] = char
        return True

class GameState():
    def __init__(self):
        self.board = Board()
        self.reset()

    def take_turn(self, row, col):
        if self.board.winner is not None:
            return self.board.check_win()

        if self.turn:
            self.board.place_o(row, col)
        else:
            self.board.place_x(row, col)

        self.turn = not self.turn
        return self.board.check_win()

    def reset(self):
       self.turn = True
       self.board.reset()

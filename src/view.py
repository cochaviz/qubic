from string2png import str2png
import pygame as pg

IMG_RATIO = 118/84
NEW_IMG_HEIGHT = 48

class Drawer():
    def __init__(self, RATIO=16/10, HEIGHT=720):
        # general settings
        self.HEIGHT = HEIGHT
        self.WIDTH = RATIO * self.HEIGHT

        self.TOOLBAR_HEIGHT = 100
        self.STATUS_HEIGHT = 100

        # colors
        self.BG = (52, 52, 52)
        self.BG_ALT = (80, 80, 80)
        self.LINE_COLOR = (144, 144, 144)

        # font
        self.mono_font = pg.font.Font("assets/FiraCode.ttf", 30)

        # grid settings
        self.h_padding_grid = 100
        self.margin_grid = 50
        self.parse_grid_settings()

        # pygame init
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT), 0, 32)
        pg.display.set_caption("My Tic Tac Toe")

    def parse_grid_settings(self):
        """
        Parses the settings defined in the init function to generate some paramaters to improve quality of life
        """
        self.grid_left = self.h_padding_grid
        self.grid_right = self.WIDTH - self.h_padding_grid
        self.grid_top = self.STATUS_HEIGHT
        self.grid_bottom = self.HEIGHT - self.TOOLBAR_HEIGHT

        self.grid_cell_width = (self.grid_right - self.grid_left) / 3
        self.grid_cell_height = (self.grid_bottom - self.grid_top) / 3

    def draw_grid(self, margin=30, line_thickness=2):
        """
        Draws the grid according to the given parameters
        """
        self.screen.fill(self.BG)
        self.screen.fill(self.BG_ALT, (self.h_padding_grid, self.STATUS_HEIGHT, self.WIDTH - 2 * self.h_padding_grid, self.HEIGHT - self.TOOLBAR_HEIGHT - self.STATUS_HEIGHT))

        width = self.grid_right - self.grid_left
        height = self.grid_bottom - self.grid_top

        left = self.grid_left + margin
        right = self.grid_right - margin
        top = self.grid_top + margin
        bottom = self.grid_bottom - margin

        # drawing vertical lines
        pg.draw.line(self.screen, self.LINE_COLOR, (width / 3 + self.grid_left, top), (width / 3 + self.grid_left, bottom), line_thickness)
        pg.draw.line(self.screen, self.LINE_COLOR, (width / 3 * 2 + self.grid_left, top), (width / 3 * 2 + self.grid_left, bottom), line_thickness)

        # drawing horizontal lines
        pg.draw.line(self.screen, self.LINE_COLOR, (left, height / 3 + self.grid_top), (right, height / 3 + self.grid_top), line_thickness)
        pg.draw.line(self.screen, self.LINE_COLOR, (left, height / 3 * 2 + self.grid_top), (right, height / 3 * 2 + self.grid_top), line_thickness)

    def init_window(self):
        """
        Initializes the window with the grid and status
        """
        self.draw_grid()
        self.draw_status(1, 0, None, None)

    def draw_status(self, turn_num, sub_turn_num, winner, coords):
        """
        Draws the status bar
        TODO Separate the status- and toolbars
        """
        if winner is None:
            if turn_num % 2 == 0:
                message = "O's Turn"
            else:
                message = "X's Turn"

            if sub_turn_num % 2 == 1:
                message += " Again"

        elif winner == '-':
            message = "Game Draw !"
        else:
            message = winner + " won !"

        # setting the font properties like
        # color and WIDTH of the text
        text = self.mono_font.render(message, 1, (255, 255, 255))

        # copy the rendered message onto the board
        # creating a small block at the bottom of the main display
        self.screen.fill(self.BG, (0, 0, self.WIDTH, self.STATUS_HEIGHT))
        text_rect = text.get_rect(center=(self.WIDTH / 2, self.STATUS_HEIGHT/2))
        self.screen.blit(text, text_rect)
        pg.display.update()


    def draw_quantum_xo(self, board, row, col, padding=15):
        """
        Draws an X or O in the given (row, col) depending on the board state
        """
        posx = self.grid_left + self.grid_cell_width * col + ((len(board.board[row][col]) - 1) % 3) * (IMG_RATIO * NEW_IMG_HEIGHT + padding) + padding
        border_y = int((len(board.board[row][col]) - 1) / 3) * NEW_IMG_HEIGHT
        posy = self.grid_top + self.grid_cell_height * row + border_y + padding

        correct_turnNum = board.turnNum

        if board.subTurnNum % 2 == 0:
            correct_turnNum -= 1

        # X's turn
        if correct_turnNum % 2 == 1:
            string = "X" + str(correct_turnNum)

            x_img = pg.image.load("assets/"+string+".png")
            x_img = pg.transform.smoothscale(x_img, (IMG_RATIO * NEW_IMG_HEIGHT, NEW_IMG_HEIGHT))

            self.screen.blit(x_img, (posx, posy))
        else:
            string = "O" + str(correct_turnNum)

            o_img = pg.image.load("assets/"+string+".png")
            o_img = pg.transform.smoothscale(o_img, (IMG_RATIO * NEW_IMG_HEIGHT, NEW_IMG_HEIGHT))

            self.screen.blit(o_img, (posx, posy))

        pg.display.update()

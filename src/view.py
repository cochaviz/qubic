from string2png import str2png
import pygame as pg

# loading the images as python object

# x_img_data = str2png("X")
# o_img_data = str2png("O")

# x_img = pg.image.frombuffer(x_img_data.tobytes(), x_img_data.size, x_img_data.mode)
# o_img = pg.image.frombuffer(o_img_data.tobytes(), o_img_data.size, o_img_data.mode)

# resizing images
# x_img = pg.transform.scale(x_img, (80, 80))
# o_img = pg.transform.scale(o_img, (80, 80))

class Drawer():
    def __init__(self, RATIO=16/10, HEIGHT=720):
        self.HEIGHT = HEIGHT
        self.WIDTH = RATIO * self.HEIGHT

        self.initiating_window = pg.image.load("assets/modified_cover.png")
        self.initiating_window = pg.transform.scale(self.initiating_window, (self.WIDTH, self.HEIGHT + 100))

        self.BG = (52, 52, 52)
        self.BG_ALT = (80, 80, 80)
        self.LINE_COLOR = (144, 144, 144)

        self.TOOLBAR_HEIGHT = 100
        self.STATUS_HEIGHT = 100

        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT), 0, 32)
        pg.display.set_caption("My Tic Tac Toe")

    def draw_grid(self, h_padding=100, margin=50, line_thickness=3):
        self.screen.fill(self.BG)
        self.screen.fill(self.BG_ALT, (h_padding, self.STATUS_HEIGHT, self.WIDTH - 2 * h_padding, self.HEIGHT - self.TOOLBAR_HEIGHT - self.STATUS_HEIGHT))

        left = h_padding + margin
        right = self.WIDTH - h_padding - margin
        top = self.STATUS_HEIGHT + margin
        bottom = self.HEIGHT - self.TOOLBAR_HEIGHT - margin

        # drawing vertical lines
        pg.draw.line(self.screen, self.LINE_COLOR, (right / 3 + left / 2, top), (right / 3 + left / 2, bottom), line_thickness)
        pg.draw.line(self.screen, self.LINE_COLOR, (right / 3 * 2 + left / 2, top), (right / 3 * 2 + left / 2, bottom), line_thickness)

        # drawing horizontal lines
        pg.draw.line(self.screen, self.LINE_COLOR, (left, bottom / 3 + top / 2), (right, bottom / 3 + top / 2), line_thickness)
        pg.draw.line(self.screen, self.LINE_COLOR, (left, bottom / 3 * 2 + top / 2), (right, bottom / 3 * 2 + top / 2), line_thickness)

    def init_window(self):
        self.draw_grid()
        self.draw_status(1, 0, None, None)

    def draw_status(self, turn_num, sub_turn_num, winner, coords):
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

        # setting a font object
        font = pg.font.Font(None, 30)

        # setting the font properties like
        # color and WIDTH of the text
        text = font.render(message, 1, (255, 255, 255))

        # copy the rendered message onto the board
        # creating a small block at the bottom of the main display
        self.screen.fill(self.BG, (0, 0, self.WIDTH, self.STATUS_HEIGHT))
        text_rect = text.get_rect(center=(self.WIDTH / 2, self.STATUS_HEIGHT/2))
        self.screen.blit(text, text_rect)
        pg.display.update()


    def draw_quantum_xo(self, board, row, col, screen):
        posx = self.WIDTH / 3 * col + 6 + (len(board.board[row][col]) % 3) * 50

        border_y = int(len(board.board[row][col]) / 3) * 50
        posy = self.HEIGHT / 3 * row + 6 + border_y

        # X's turn
        if board.turnNum % 2 == 1:
            string = "X" + str(board.turnNum)

            x_img_data = str2png(string)
            x_img = pg.image.frombuffer(x_img_data.tobytes(), x_img_data.size, x_img_data.mode)
            # x_img = pg.transform.scale(x_img, (80, 80))
            x_img = pg.transform.scale(x_img, (50, 50))

            self.screen.blit(x_img, (posx, posy))
        else:
            string = "O" + str(board.turnNum)

            o_img_data = str2png(string)
            o_img = pg.image.frombuffer(o_img_data.tobytes(), o_img_data.size, o_img_data.mode)
            # o_img = pg.transform.scale(o_img, (80, 80))
            o_img = pg.transform.scale(o_img, (50, 50))

            self.screen.blit(o_img, (posx, posy))

        pg.display.update()

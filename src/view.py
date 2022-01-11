from main import WIDTH, HEIGHT
from string2png import str2png
import pygame as pg

# loading the images as python object
initiating_window = pg.image.load("assets/modified_cover.png")

# x_img_data = str2png("X")
# o_img_data = str2png("O")

# x_img = pg.image.frombuffer(x_img_data.tobytes(), x_img_data.size, x_img_data.mode)
# o_img = pg.image.frombuffer(o_img_data.tobytes(), o_img_data.size, o_img_data.mode)

# resizing images
initiating_window = pg.transform.scale(initiating_window, (WIDTH, HEIGHT + 100))
# x_img = pg.transform.scale(x_img, (80, 80))
# o_img = pg.transform.scale(o_img, (80, 80))

line_color = (0, 0, 0)


def init_window(screen):
    screen.fill((255, 255, 255))

    # drawing vertical lines
    pg.draw.line(screen, line_color, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), 7)
    pg.draw.line(screen, line_color, (WIDTH / 3 * 2, 0), (WIDTH / 3 * 2, HEIGHT), 7)

    # drawing horizontal lines
    pg.draw.line(screen, line_color, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), 7)
    pg.draw.line(screen, line_color, (0, HEIGHT / 3 * 2), (WIDTH, HEIGHT / 3 * 2), 7)
    draw_status(1, 0, None, None, screen)


def draw_status(turn_num, sub_turn_num, winner, coords, screen):
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
    screen.fill((0, 0, 0), (0, HEIGHT, WIDTH, 100))
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT + 50))
    screen.blit(text, text_rect)
    pg.display.update()


def draw_quantum_xo(board, row, col, screen):
    posx = WIDTH / 3 * col + 6 + (len(board.board[row][col]) % 3) * 50

    border_y = int(len(board.board[row][col]) / 3) * 50
    posy = HEIGHT / 3 * row + 6 + border_y

    # X's turn
    if board.turnNum % 2 == 1:
        string = "X" + str(board.turnNum)

        x_img_data = str2png(string)
        x_img = pg.image.frombuffer(x_img_data.tobytes(), x_img_data.size, x_img_data.mode)
        # x_img = pg.transform.scale(x_img, (80, 80))
        x_img = pg.transform.scale(x_img, (50, 50))

        screen.blit(x_img, (posx, posy))
    else:
        string = "O" + str(board.turnNum)

        o_img_data = str2png(string)
        o_img = pg.image.frombuffer(o_img_data.tobytes(), o_img_data.size, o_img_data.mode)
        # o_img = pg.transform.scale(o_img, (80, 80))
        o_img = pg.transform.scale(o_img, (50, 50))

        screen.blit(o_img, (posx, posy))

    pg.display.update()

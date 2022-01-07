from main import WIDTH, HEIGHT
import pygame as pg

# loading the images as python object
initiating_window = pg.image.load("assets/modified_cover.png")
x_img = pg.image.load("assets/X_modified.png")
y_img = pg.image.load("assets/o_modified.png")

# resizing images
initiating_window = pg.transform.scale(initiating_window, (WIDTH, HEIGHT + 100))
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(y_img, (80, 80))

line_color = (0, 0, 0)

def init_window(screen):
    screen.fill((255, 255, 255))

    # drawing vertical lines
    pg.draw.line(screen, line_color, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), 7)
    pg.draw.line(screen, line_color, (WIDTH / 3 * 2, 0), (WIDTH / 3 * 2, HEIGHT), 7)

    # drawing horizontal lines
    pg.draw.line(screen, line_color, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), 7)
    pg.draw.line(screen, line_color, (0, HEIGHT / 3 * 2), (WIDTH, HEIGHT / 3 * 2), 7)
    draw_status(True, None, None, screen)

def draw_status(turn, winner, coords, screen):
    if winner is None:
        if turn:
            message = "O's Turn"
        else:
            message = "X's Turn"
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
    screen.fill ((0, 0, 0), (0, HEIGHT, WIDTH, 100))
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT + 50))
    screen.blit(text, text_rect)
    pg.display.update()



def draw_xo(turn, row, col, screen):
    posx = WIDTH / 3 * row + 30
    posy = HEIGHT / 3 * col + 30

    if turn:
        screen.blit(o_img, (posy, posx))
    else:
        screen.blit(x_img, (posy, posx))

    pg.display.update()

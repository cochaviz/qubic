# importing the required libraries
import pygame as pg
import sys
import time

from model import *
from view import *

WIDTH = 500
HEIGHT = 500
FPS = 30


class Game:
    def __init__(self):
        self.state = GameState()

        # initializing the pygame window
        pg.init()

        # this is used to track time
        self.CLOCK = pg.time.Clock()

        # this method is used to build the
        # infrastructure of the display
        self.screen = pg.display.set_mode((WIDTH, HEIGHT + 100), 0, 32)

        # setting up a nametag for the
        # game window
        pg.display.set_caption("My Tic Tac Toe")

        self.reset()

    def run(self):
        while (True):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print("Bye...")
                    pg.quit()
                    sys.exit()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.state.board.winner is not None:
                        self.reset()
                        break

                    row, col = self.user_click()
                    draw_xo(self.state.board, row, col, self.screen)

                    winner, winstate = self.state.take_turn(row, col)
                    draw_status(self.state.board.turnNum, self.state.board.subTurnNum, winner, winstate, self.screen)

            pg.display.update()
            self.CLOCK.tick(FPS)

    def reset(self):
        self.state.reset()
        init_window(self.screen)
        time.sleep(.1)

    def user_click(self):
        # get coordinates of mouse click
        x, y = pg.mouse.get_pos()

        # get column of mouse click (1-3)
        if (x < WIDTH / 3):
            col = 0

        elif (x < WIDTH / 3 * 2):
            col = 1

        elif (x < WIDTH):
            col = 2

        else:
            col = None

        # get row of mouse click (1-3)
        if (y < HEIGHT / 3):
            row = 0

        elif (y < HEIGHT / 3 * 2):
            row = 1

        elif (y < HEIGHT):
            row = 2

        else:
            row = None

        return row, col


if __name__ == "__main__":
    game = Game()
    game.run()

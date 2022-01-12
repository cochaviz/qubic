# importing the required libraries
import pygame as pg
import sys
import time

from model import *
from view import *

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
        self.drawer = Drawer()

        # setting up a nametag for the
        # game window

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
                    self.drawer.draw_quantum_xo(self.state.board, row, col)

                    winner, winstate = self.state.take_turn(row, col)
                    self.drawer.draw_status(self.state.board.turnNum, self.state.board.subTurnNum, winner, winstate)

            pg.display.update()
            self.CLOCK.tick(FPS)

    def reset(self):
        self.state.reset()
        self.drawer.init_window()
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
        if (y < self.drawer.HEIGHT / 3):
            row = 0

        elif (y < self.drawer.HEIGHT / 3 * 2):
            row = 1

        elif (y < self.drawer.HEIGHT):
            row = 2

        else:
            row = None

        return row, col


if __name__ == "__main__":
    game = Game()
    game.run()

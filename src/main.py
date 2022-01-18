# importing the required libraries
import pygame as pg
import sys
import time

from model import *
from src.util import GameProperties
from view import *

FPS = 30


class Game:
    def __init__(self, dim=5):
        GameProperties(dim)

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
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print("Bye...")
                    pg.quit()
                    sys.exit()

                elif event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                    if self.state.board.winner is not None:
                        self.reset()
                        break

                    row, col = self.user_click()

                    # Message is false if the move is valid
                    message = self.state.is_invalid_move(row, col)
                    if message:
                        self.drawer.draw_status_message(message)
                        break

                    self.state.take_turn(row, col)
                    winner, winstate = self.state.board.check_win()

                    if winner is False:
                        break

                    self.drawer.draw_quantum_xo(self.state.board, row, col)
                    self.drawer.draw_status(self.state.board.turnNum, self.state.board.subTurnNum, winner, winstate)
                    self.drawer.draw_final(self.state.board)

            pg.display.update()
            self.CLOCK.tick(FPS)

    def reset(self):
        self.state.reset()
        self.drawer.init_window()
        time.sleep(.1)

    def user_click(self):
        # get coordinates of mouse click
        x, y = pg.mouse.get_pos()

        dim = GameProperties.get_instance().dim

        col = -1
        row = -1
        # get row of col of user click
        for i in range(0, dim):
            if x > self.drawer.grid_left + i * self.drawer.grid_cell_width:
                col = i
            if y > self.drawer.grid_top + i * self.drawer.grid_cell_height:
                row = i

        # check if outside grid
        if x > self.drawer.grid_left + dim * self.drawer.grid_cell_width:
            col = -1
        if y > self.drawer.grid_top + dim * self.drawer.grid_cell_height:
            row = -1

        return row, col


if __name__ == "__main__":
    game = Game()
    game.run()

# importing the required libraries
import sys
import time

from model import *
from util import Views
from view import *
import threading

FPS = 30


class Game:
    def __init__(self):
        # init game properties
        GameProperties(None, Views.HOME)

        # game state
        self.state = None

        # initializing the pygame window
        pg.init()

        # this is used to track time
        self.CLOCK = pg.time.Clock()

        # this method is used to build the
        # infrastructure of the display
        self.drawer = Drawer()

        # start on home window
        self.drawer.init_home_window()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print("Bye...")
                    pg.quit()
                    sys.exit()

                elif event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                    if GameProperties.view() == Views.HOME:
                        for button in self.drawer.button_group:
                            # user clicked on button
                            if button[0].collidepoint(event.pos):
                                # change dimension to what user selected
                                # and update view
                                GameProperties(button[1], Views.BOARD)
                                self.reset()
                                break

                    elif GameProperties.view() == Views.BOARD:
                        # todo: refactor
                        if self.state.board.winner is not None:
                            self.state.update_scores()
                            self.reset()
                            break

                        winner = None

                        # gate selection
                        if self.drawer.gate_panel.collidepoint(event.pos):
                            for [rect, gate] in self.drawer.button_group:
                                # user clicked on gate button
                                if rect.collidepoint(event.pos) and self.state.get_moving_player().gates_count[gate] > 0:
                                    # change status
                                    self.drawer.draw_status_message("Select target and control states in console...")

                                    message = "You selected {} gate, please type in a target state (ie: x1, o4): "\
                                        .format(str.capitalize(gate.value))
                                    print('\n' + message + '\nTarget state:')
                                    target_state = input()
                                    control_state = None
                                    if gate == Gate.Gates.CNOT:
                                        print('\nControl state:')
                                        control_state = input()
                                    if target_state == '' or control_state == '':
                                        print('Gate not placed')
                                    if self.state.place_gate(gate, target_state, control_state):
                                        print("Gate placed")
                                    else:
                                        print('Gate not placed')
                                    break

                        else:
                            row, col = self.user_click()

                            # Message is false if the move is valid
                            message = self.state.is_invalid_move(row, col)
                            if message:
                                self.drawer.draw_status_message(message)
                                break

                            self.state.take_turn(row, col)
                            cycle = self.state.board.has_cycle(row, col)
                            if cycle is not None:
                                thread1 = threading.Thread(target=self.state.board.resolve_cycle, args=(cycle,),
                                                           daemon=True)
                                thread1.start()
                                self.drawer.draw_quantum_xo(self.state.board, row, col)
                                self.drawer.draw_status_message("Resolving superposition, please wait some time...")
                                thread1.join()

                            winner, winstate = self.state.board.check_win()
                            if winner is False:
                                break

                            self.drawer.draw_quantum_xo(self.state.board, row, col)
                            self.drawer.draw_final(self.state.board)

                        self.drawer.draw_status(self.state.board.turnNum, self.state.board.subTurnNum,
                                                winner, self.state.first_player_uses)
                        self.drawer.draw_gate_panel(self.state.get_moving_player().gates_count, self.state.board.gates_list)
            pg.display.update()
            self.CLOCK.tick(FPS)

    def reset(self):
        # todo: refactor
        if self.state is None:
            self.state = GameState()

        self.state.new_game()
        self.drawer.init_window(self.state, self.state.get_moving_player().gates_count, self.state.board.gates_list)
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

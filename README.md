# Quantum Tic-Tac-Toe

This version of quantum Tic-Tac-Toe is a spin on the existing [quantum tic-tac-toe](https://en.wikipedia.org/wiki/Quantum_tic-tac-toe).
The size of the board be selected to be 3x3, 4x4 or 5x5. It also runs part of the game on an actual quantum computer!

The reason the repository is called qubic, while that is originally a term for 3D tic-tac-toe (as explained in the wikipedia page of [3D tic-tac-toe](https://en.wikipedia.org/wiki/3D_tic-tac-toe)),
is because that was the original plan of this project. Unfortunately, due to time constraints and other priorities, this did not end up happening in the end. 

## Rules
The rules of the quantum tic-tac-toe game are the following:

- Each player places two states per turn: one player places two |0>'s each turn, while the other player places two |1>'s each turn.
- The player must place these two states on two different tiles, and these tiles then become entangled.
- When a cycle of these entangled states is detected, the cycle collapses. For example:
    1. Player one places |1> in tile 1 and 2. Player two then places |0> in tile 2 and 3, and player one places |1> in tiles 3 and one.
    2. A cycle has now been created, because you can 'walk' via the entanglements from tile 1, to tile 2, to tile 3 and back to tile 1.
    3. The cycle collapses, by choosing the spot the last placed state will end up, so the |1> placed in tile 3 and 1 will end up in either tile 3 or 1.
    4. The game asks a quantum computer to flip a coin, and that result determines on which end of the entanglement the state that completed the cycle ends up. 
  In this example, the coin flip decides if the |1> state ends up being either in the tile 1 or in tile 3. (See Quantum-Inspire setup below)
    5. If the |1> ends up in tile 3, it means that the |0> state that entangled tile 2 and 3 cannot end up in tile 3 anymore, and thus collapses to tile 2. 
  This in turn prohibits the |1> state that entangled tile 1 and 2 to be placed in tile 2, so this one must collapse to tile 1. Now the cycle has collapsed, and the values for tile 1, 2 and 3 are |1>, |0> and |1> respectively.
    6. If the |1> ends up in tile 1, it means that the |1> state that entangled tile 1 and 2 cannot end up in tile 1 anymore, so it must collapse to tile 2.
  That then means, that the |0> state, that entangled tile 2 and 3 cannot be placed in tile 2, and thus must collapse to tile 3. With this version of the cycle collapse, the values for tile 1, 2 and 3 are |1>, |1> and |0> respectively.
- When a cycle collapses, the tiles are filled in with the states that have been collapsed into them, and cannot be selected anymore when placing your two basis states in a turn.
- The game is over when a winner is decided, or when all spots are final.

## Deciding the winner
The winner is decided in the following way:
- After a collapse, you can check for a winner like you would in classical tic-tac-toe. This means, you check to see if there are 3 in a row of the same final tiles, vertically, horizontally or diagonally.
- If the collapse leads to only 1 3-in a row, then that player is automatically the winner of the game.
- If the collapse leads to 2 or more 3-in a rows, then the game considers the turn on which the basis state was placed. For example:
    - Player 1 has a 3-in a row after the collapse event, where these basis states were placed in turn 7, 3 and 5,
  and player 2 has a 3-in a row after the same collapse event, where the basis states were placed in turn 4, 2 and 6.
    - The game now looks for the highest number for each 3-in a row. For player 1, the highest number is selected from 7, 3 and 5, and thus is 7.
  For player 2, the highest number is selected from 4, 2 and 6, which is 6. 
    - Now, these numbers are compared, and the 3-in a row with the lowest number is declared the winner.
- If all states have been collapsed, and no 3-in a row has been achieved by either player, the game is a draw.
- A player receives 2 points if they win, and both players receive 1 point if the game ends in a draw.

In this implementation, players can choose if they want to play on a 3x3, 4x4 or 5x5 grid. The rules and winner decision are equal to the 3x3 grid for the larger grids, besides that
the player must need 4-in a row, for both the 4x4 and the 5x5 grid. This is because otherwise the player with the middle most tile has too big an advantage over the other player on the 5x5 grid.


## Quantum Inspire setup
To make use of the quantum computer for the coin flips, you need to setup the Quantum Inspire SDK.
To do this, you can follow the video tutorial via this [clickable link](https://www.quantum-inspire.com/kbase/advanced-guide/).

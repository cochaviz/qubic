# qubic

Qubic is a spin on the existing [quantum tic-tac-toe](https://en.wikipedia.org/wiki/Quantum_tic-tac-toe). It also allows players to apply quantum gates in order to make the gameplay more interesting. It also runs part of the game on an actual computer!

## Rules
- each player places two states per turn: |0> or |1>
- the tiles are super entangled
quantum gates can be traded for a turn (choose to put down two states or to put down gate)
- when cycle is made, must first measure what the qubits become, then collapse to one superposition (state that collapsed is replaced by the state that was measured)
- collapsing can also be measured with a quantum coin flip (dont let the player choose)
- gates are operated in the order that they were placed on the state
- possible gates: H, CX, X, Z+H, Z

First apply gates, then the gates disappear and the cycle superposition measurement is made. Then we start again.
gates going out from cycles (to superpositions that are not in the cycle) are discarded
gate can only be picked up once per player per game

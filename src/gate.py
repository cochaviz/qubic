from enum import Enum


class Gate:
    def __init__(self, target_state, gate, control_state=None):
        """
        @param target_state: mark , subscript of mark.
        """
        self.target_state = target_state
        self.control_state = control_state
        self.gate_char = gate

    class Gates(Enum):
        HADAMARD = 'h'
        NOT = 'x'
        Z = 'z'
        ZH = 'zh'
        CNOT = 'cx'

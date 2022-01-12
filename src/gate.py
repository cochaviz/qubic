class Gate:
    def __init__(self, target_state, gate, control_state=None):
        self.target_state = target_state
        self.control_state = control_state
        self.gate_char = gate

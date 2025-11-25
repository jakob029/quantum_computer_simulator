from gates import HadamardGate, ControlledRGate

QFT_3_qubit_circuit = [{"qubit_in": 0, "qubit_out": 0, "gate": HadamardGate()},
                         {"qubit_in": 0, "qubit_out": 1, "gate": ControlledRGate(2)},
                         {"qubit_in": 0, "qubit_out": 2, "gate": ControlledRGate(3)},
                         {"qubit_in": 1, "qubit_out": 1, "gate": HadamardGate()},
                         {"qubit_in": 1, "qubit_out": 2, "gate": ControlledRGate(2)},
                         {"qubit_in": 2, "qubit_out": 2, "gate": HadamardGate()},
                         ]

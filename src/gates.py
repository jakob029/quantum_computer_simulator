import numpy as np

class AbstractGate:
    """Abstract class for quantum gate unitary matrix."""
    gate_identifier: str
    gate: list[list[int]]
    scalar: float #TODO this should be scaled to scaling factor instead.

    def exe_gate(self, qubit_state):
        return self.gate * qubit_state

class PauliXGate(AbstractGate):
    """
    X|0⟩=|1⟩
    X|1⟩=|0⟩
    """

    def __init__(self):
        self.gate = np.matrix([[0, 1],
                     [1,0]])
        self.scalar = 1

class HadamardGate(AbstractGate):
    """"""

    def __init__(self):
        scalar = 1/(2**0.5)
        self.gate = np.matrix([[1,1],
                     [1,-1]]) * scalar

        self.gate_identifier = "H"

    def multi_qubit(self, n: int, qubit_num: int) -> np.ndarray: #TODO, this should probably be initiated from the constructor.
        """Hadamard gate is applied per qubit.

        Hadamard gate is applied on the k'th qubit by taking the tensor product with the 2x2 identity matrix n times,
          where the H gate is at the k'th position in the tensor multiplication chain, and n is the number of total qubits.

        Args:
            n: Number of qubits in system
            qubit_num: Specific qubit number.

        """
        if n == 1:
            return self.gate

        identity_matrix = np.eye(2)
        tensor_chain = [identity_matrix] * n
        tensor_chain[qubit_num-1] = self.gate

        tensor_product = np.kron(tensor_chain[0], tensor_chain[1])

        for multiplier in tensor_chain[2:]:
            tensor_product = np.kron(tensor_product, multiplier)

        return tensor_product

class PairwiseSwapGate(AbstractGate):
    """What is often referred to as a SWAP gate in QFT.

    Note:
        This gate is not necessary, as it can be interpreted after reading qubits.
    """

    @property
    def SWAP2(self):
        return np.matrix([[1,0,0,0],
                          [0,0,1,0],
                          [0,1,0,0],
                          [0,0,0,1]]
                          )

    @property
    def SWAP3(self):
        pass

    def SWAPN(self, n: int):
        if n == 2:
            return self.SWAP2

        return np.kron(np.eye(2), self.SWAP2)

    def _matrix_row_insertion():
        pass


class CNOTGate(AbstractGate):
    def __init__(self):
        self.gate = [[1,1],
                     [1,-1]]

        self.scalar = 1

class ControlledRGate(AbstractGate):
    """Applies rotation to qubit if in state |1>."""

    def __init__(self, k):
        self.gate_identifier = f"R{k}"
        scalar = 2 / 2**k
        transform_value = np.exp(np.pi * scalar * 1j)

        self.gate = [[1, 0],
                    [0, transform_value]]

def construct_phase_shift_gate(n):
    """Construct a phase shift gate defined as
    [1 0
     0 omega_{N}]
    where N is 2^n (n is number of qubits), and omega_{N} = e^{2pi i N^{-1}}

    Args:
    ----
        n: Number of qubits.
    """

    hilbert_space_dimensions = 2**n
    scalar_element = np.exp(2 * np.pi * 1j * (hilbert_space_dimensions)**(-1))

    return np.matrix([[1,0],[0, scalar_element]])

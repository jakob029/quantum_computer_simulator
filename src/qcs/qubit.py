from typing import Any, Callable

from numpy import sin, cos, matrix, array, ndarray, vstack, kron
import numpy as np

from conf import SCALER, PLANKS_CONSTANT
from gates import HadamardGate

class Qubit:
    qubit_vec: matrix

    def __init__(self, angle: int | float | None = None, vector: list | tuple | matrix | None = None):
        """Constructor

        Args:
        ----
            Angle: Theta angle in complex plane, given in radians.
            vector: Defined vector.
        """
        if angle is not None:
            self.qubit_vec = matrix(self._reinterpret_vector(angle))
            return
        if vector is None:
            raise ValueError("The qubit constructor requires either an angel or a vector.")

        vector = array(vector, dtype=complex)
        if vector.shape == (2,):
            vector = vector.reshape(-1, 1)

        #TODO implement check that vector lenght must be 1.
        self.qubit_vec = matrix(vector) #TODO, this needs to be unpacked and scaled.

    @staticmethod
    def _reinterpret_vector(angle: int | float, resolution: int = PLANKS_CONSTANT) -> tuple:
        """Take an integer representing some angle in the complex plane and represent it by discrete vector values.

        Args:
            angle: Theta angle in complex plane, given in radians.
            resolution: Defined discrete resolution in vector room.

        Returns:
        -------
            Tuple containing two dimensional vector values.
        """

        return cos(angle), sin(angle)

    def is_compitational_basis_state(self) -> bool:
        """Find if qubit is in compitational basis state."""
        return self.qubit_vec[0] in [0,1] and self.qubit_vec[1] in [0,1] and self.qubit_vec[0] != self.qubit_vec[1]

    def __str__(self):
        if all(self.qubit_vec == matrix([[1],[0]])):
            return "|0>"
        if all(self.qubit_vec == matrix([[0],[1]])):
            return "|1>"
        return self.qubit_vec #TODO maybe calculate angle instead


class Register:
    """Quantum Computer register with n number of qubits, represented as ket{<STATE1> ... <STATEn>}"""

    size: int
    hilbert_dimensions: int
    state: ndarray

    def __init__(self, size: int):
        self.size = size
        self.hilbert_dimensions = 2 ** size

        self.state = [1] + [0] * (self.hilbert_dimensions - 1) #resulting in [1,0,0, ...] (which is tesnor product for |0> \otimes |0> ... \otimes |0>)
        self.state = vstack(self.state, dtype=complex)

    def __str__(self):
        return str(self.state)

    def update_state(self, new_state: list, scalar: int):
        """Given a flat list and scalar value, write over the value."""
        self.state = vstack(new_state, dtype=complex) * scalar

    def exectute_gate(self, gate: Any, qubit: int): #TODO, this is not scalable, full matrix multiplications should not be done.
        """Execute a given gate on the current state.

        Args:
        ----
            gate: Gate to execute.
            qubit: Qubit number.
        """
        gate_matrix = self.upscale_gate(gate, qubit, self.size)
        self.state = gate_matrix * self.state

    def execute_gate_all_qubits(self, gate: np.matrix):
        """Execute a gate constructed to be executed on all qubits in the register.

        Args:
        ----
            gate: Gate to execute.
        """
        self.state = gate * self.state

    @staticmethod
    def upscale_gate(gate: matrix, qubit: int, size: int) -> matrix:
        """Execute tensor product between gate matrix and identity matrix to scale, 
          with correct qubit positioning."""
        constructed_matrix = matrix([1])
        identity_matrix = matrix([[1,0], [0,1]])
        for i in range(size):
            if i == qubit:
                constructed_matrix = kron(constructed_matrix, gate) #Tensor product
                continue
            constructed_matrix = kron(constructed_matrix, identity_matrix) #Tensor product
        return constructed_matrix

    def read_basis_states(self):
        """Read state vector with ket state notation."""
        ket_string = ""
        for index, element in enumerate(self.state):
            if element == 0:
                continue
            element_str = element.real if np.isclose(element.imag, 0, atol=1e-12) else element
            if isinstance(element_str, matrix):
                element_str = element_str[0,0]
            ket_string += " + " * bool(ket_string) + f"{element_str}*|{format(index, f'0{self.size}b')}>"
        return ket_string


def entangle_registers(register_1: Register ,register_2: Register, seconf_reg_method: Callable):
    """Entagle two matrixes, where the second matric should start with |0>."""
    reg_1_len = len(register_1.state)
    reg_2_len = len(register_2.state)

    if int(register_2.state[0].real) != 1:
        raise ValueError("The second register does not start with |0>.")

    result = np.zeros(reg_1_len * reg_2_len, dtype=complex)

    for a in range(reg_1_len):
        amplitude = register_1.state[a]
        y = seconf_reg_method(a)
        index = a * reg_2_len + y #Index for amplitude 

        result[index] = amplitude

    return result

def measure_register(register):
    """Measure single register."""
    reg_values = np.abs(register.real)

    if np.round(sum(reg_values)) != 1:
        reg_values = reg_values * 1/sum(reg_values)

    return np.random.choice(len(register), p=reg_values)

def measure_register_2(state, register_1, register_2):
    """Measure register two, (meaning pick a value using the amplitude as the probability)."""
    reg_1_len = len(register_1.state)
    reg_2_len = len(register_2.state)

    state_2d = state.reshape(reg_1_len, reg_2_len)
    probs = np.sum(np.abs(state_2d)**2, axis=0)
    probs = probs / probs.sum()

    #Pick one of the elements in register 2 at random, after the prob amplitudes has been set.
    measured_y = np.random.choice(reg_2_len, p=probs)

    return measured_y


def collapse_entangled_regisers(state, register_1, register_2, value):
    """Collapse entangled registers into one, represented as a matrix scaled reg_1_len x reg_2_len."""
    reg_1_len = len(register_1.state)
    reg_2_len = len(register_2.state)
    state_2d = state.reshape(reg_1_len, reg_2_len)
    collapsed = np.zeros_like(state_2d)
    collapsed[:, value] = state_2d[:, value]
    norm = np.linalg.norm(collapsed)

    if norm > 0:
        collapsed /= norm

    return collapsed.reshape(reg_1_len, reg_2_len)

def reduce_collapsed_matrix(collapsed_matrix: ndarray, value: int):
    """After one register in a 2 register intagelment has collapsed, remove all |k>*0 and flatten structure."""
    result: list = []
    for row in collapsed_matrix:
        result.append(float(np.abs(row[value])))
    return result
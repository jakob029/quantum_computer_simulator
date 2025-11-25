from numpy import sin, cos, matrix, array, ndarray, vstack

from conf import SCALER, PLANKS_CONSTANT

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

        vector = array(vector)
        if vector.shape == (2,):
            vector = vector.reshape(-1, 1)
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


class BasisState:
    """Basis state for quantum computer with n number of qubits, represented as ket{<STATE1> ... <STATEn>}"""

    hilbert_dimensions: int
    state: ndarray

    def __init__(self, state: list[Qubit]):
        self._check_qubits(state)
        self.hilbert_dimensions = 2 ** len(state)

        self._translate_basis_state(state)
        self.state = vstack(self.state)

    @staticmethod
    def _check_qubits(state: list[Qubit]) -> None:
        """Method checks that all qubit's are valid inputs."""

        for qubit in state:
            if not qubit.is_compitational_basis_state():
                raise ValueError("Qubit used in basis state shall have compitational basis state.")

    def _translate_basis_state(self, state: list[Qubit]):
        """Translate qubit comutational state into hilbert dimension vector."""
        self.state = array([0]*self.hilbert_dimensions)
        ket = []
        for qubit in state:
            ket.append(self._get_qubit_state(qubit))
        basis_index = int(''.join(map(str, ket)), 2)

        self.state[basis_index] = 1

    @staticmethod
    def _get_qubit_state(qubit: Qubit):
        """Returns: |0> for alpha=1, beta=0
                    |1> for alpha=0, beta=1
        """
        if qubit.qubit_vec[0] == 1 and qubit.qubit_vec[1] == 0:
            return 0
        if qubit.qubit_vec[0] == 0 and qubit.qubit_vec[1] == 1:
            return 1
        raise ValueError("Qubit used in basis state shall have compitational basis state.")

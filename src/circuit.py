""""""
from PIL import Image, ImageDraw, ImageFont
from examples.example_circuit import QFT_3_qubit_circuit
from qubit import Qubit, BasisState
import numpy as np

class circuit:

    gate_matrix: dict[list] #Matrix where row is qubit id and column is gate instance.

    quantum_circuit: list
    num_qubits: int

    PBS : int = 20 #Picture box size.
    PBD : int = 40 #Picture box distance.
    PQD: int = 50 #Picture qubit distance.

    def __init__(self, quantum_circuit):
        self.quantum_circuit = quantum_circuit

    def simulate_circuit(self, *qubit: Qubit):
        qubits = tuple(qubit)
        for section in self.quantum_circuit:
            r_qubit = section.get("qubit_in")
            quantum_gate = section.get("gate")
            qubits[r_qubit].qubit_vec = quantum_gate.exe_gate(qubits[r_qubit].qubit_vec)

        return qubits

    @staticmethod
    def normalize_vector(superposition_vector: np.ndarray) -> np.ndarray:
        """For a vec

        """
        vec_norm = np.linalg.norm(superposition_vector)

        return superposition_vector / vec_norm


    def generate_picture(self):
        """Generates a diagram in png format of the quantum circuit, saved to 'diagram.png'."""
        w, h = 400, 300
        img = Image.new("RGB", (w, h), "white")
        draw = ImageDraw.Draw(img)

        self._generate_picture_horizontal_lines(draw=draw)
        self._generate_picture_boxes(draw=draw)
        img.save("diagram.png")

    def _generate_picture_horizontal_lines(self, draw):
        for i in range(self.num_qubits):
            box = (self.PBS,
                    self.PBS + (self.PBD*i),
                    self.PBD,
                    self.PBD + (self.PBD*i))
            draw.rectangle(box, outline="white", width=2)
            font = ImageFont.load_default()

            draw.text((box[0] + 6, box[1] + 5), f"q{i}", fill="black", font=font)
            draw.line((self.PBD, self.PBD - (self.PBS / 2) + (self.PBD*i), self.PBD + 350, self.PBD - (self.PBS / 2) + (self.PBD*i)), fill="black", width=2)

    def _generate_picture_boxes(self, draw):
        x0 = self.PBS + (self.PBD /2)
        y0 = x0 - (self.PBS /2)
        for i, circuit_box in enumerate(self.quantum_circuit):
            qubit_id = circuit_box.get("qubit_in")
            end_qubit = circuit_box.get("qubit_out")

            lower_x = x0 + (self.PQD * i)
            lower_y =  y0 + (self.PBD * qubit_id) - (self.PBS /2)
            box = (lower_x, lower_y, lower_x + self.PBS, lower_y + self.PBS)
            draw.rectangle(box, outline="black", width=2, fill="white")
            font = ImageFont.load_default()
            draw.text((box[0] + 6, box[1] + 5), circuit_box.get("gate").gate_identifier, fill="black", font=font)

            if end_qubit == qubit_id:
                continue

            draw.line((lower_x + (self.PBS/2), lower_y + (self.PBS), lower_x  + (self.PBS/2), lower_y + (self.PBS/2) + ((end_qubit - qubit_id) * self.PBD)), fill="black", width=2)

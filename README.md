# Warning

This project is currently under construction, currently existing methods might/do not work as intended.

# Run instructions

Construct a circuit following the format outlined in the [example](examples/example_circuit.py).

Use the circuit.generate_picture picture method to generate a visualization of the constructed circuit (example can be found [here](examples/diagram.png)).

# Gates

## Hadamard gate
Hadamards gate is applied per qubit, and is defined as:
$$
\begin{align}
  \frac{1}{\sqrt{2}}
  \left[
    \begin{aligned}
        1 &\ &1 \\
        1 &\ &-1 
    \end{aligned}
  \right]
\end{align}
$$

Applying the gate on the $k'th$ qubit is done by:

$I_1 \otimes I_2 \otimes ... \otimes I_k \otimes  ...  \otimes H \otimes I_{k+1} \otimes I_{k+2} \otimes... \otimes I_n$

Where $H$ is Hadamard gate, $I$ is the $2x2$ identify matrix, and $n$ is the number of qubits in the system.

## Controlled R gate
Applies rotation of $e^{\frac{2 \pi i}{2^k}}$ to qubit if in state $\ket{1}$, where $k$ is a variable (affecting the phase).

$$
\begin{align}
  R_k =
  \left[
    \begin{aligned}
        1 &\ &0 \\
        0 &\ & e^{\frac{2 \pi i}{2^k}}
    \end{aligned}
  \right]
\end{align}
$$

# Quantum algorithms

## Quantum fourier transformation
$$
\begin{align}
QFT(k) = \frac{1}{\sqrt{N}} \sum_{k = 0}^{N - 1} e^{2 \pi i \frac{jk}{n}} \ket{k}
\end{align}
$$

# Backlog

 * Change qubit structure to scale with integer values derived from minimum distance h (floating point numbers shall not be used).

import random as r

import numpy as np

from qubit import Register, collapse_entangled_regisers, entangle_registers, measure_register_2, reduce_collapsed_matrix, measure_register
from gates import HadamardGate, qft
from tools import plot_after_qft


HADAMARD = HadamardGate()
N = 6

def _find_q(n: int):
    """Find q so that n^2 <= q < 2n^2"""
    q = 1
    while not (n**2 <= q < 2*n**2):
        q *= 2
    return q

def _find_binary_size(size: int):
    """Based on some size arguemnt, find the smallest number 2^t where t ∈ N, greater than size."""
    return (1 << size.bit_length()).bit_length() - 1

def generate_ket_print_for_reduced(flat_register): #TODO, move this to another file.
    """Generate a ket print output for a list of values."""
    values = ""
    for index, value in enumerate(flat_register):
        if value != 0:
            values += f"|{index}> + "
    print(values.rstrip("+ "))

def quantum_prime_factorization(n: int, x: int = 2) -> list:
    """Execute shors algorithm, resulting in superposition with non negative amplitudes
        for sequence separated by period (r) number of elements.

    Args:
        n: Prime number to factor.
        x: Pick x so that gcd(x,n) = 1 is True (2 can be used since number otherwise simply can be divided with 2).
    
    Note:
        If post processing calculations results in x^(r/2) ≅ -1 mod (n), try another value for x.
    """
    if n % 2 == 0:
        print("Please pick a number not devicible by 2.")
        return []

    size_register_1 = _find_binary_size(n**2)
    size_register_2 = _find_binary_size(n)

    print(f"Size of register 1: {size_register_1}")
    print(f"Size of register 2: {size_register_2}")

    register_1 = Register(size_register_1)
    register_2 = Register(size_register_2)

    print(f"x was picked at random to: {x}")

    q = _find_q(n)
    print(f"q was found to be: {q}")
    #Step 1; Put equal amplitudes to all states smaller than q (state q can be ignored).
    register_1.execute_gate_all_qubits(HADAMARD.multi_qubit(size_register_1))

    #Step 2; Compute x^a (mod n) in the register 2 (register 2 multiplication is dependent on register 1).
    def r_2_spin(a):
        return pow(x, a, n)

    entangled_registers = entangle_registers(register_1, register_2, r_2_spin)
    print("Register 1 and two has been entangled.")

    reg_2_measured_value = measure_register_2(entangled_registers, register_1, register_2)
    print(f"Register 2 was measured, it became: {reg_2_measured_value}")

    collapesed_register = collapse_entangled_regisers(entangled_registers, register_1, register_2, reg_2_measured_value)
    print("Entangled registers have collapsed due to measurement of register 2.")

    reduced_collapse = reduce_collapsed_matrix(collapesed_register, reg_2_measured_value)

    print("\nShores algorithm has produced a probability distrobution in the first register,"
          f" where the distance between non-zero probability values should be equal to the period of 2^r mod({n})")
    print("The state is:\n")
    print(" ------------------------------- Register 1 state ------------------------------- ")
    generate_ket_print_for_reduced(reduced_collapse)
    print(" -------------------------------------------------------------------------------- ")
    return reduced_collapse


def interactive_shors_algorithm():
    str_n = input("What number would you like to factor?\n")
    while not str_n.isdigit():
        str_n = input("Please select a digit: ")
    n = int(str_n)

    overwrite_x = input("Would you like to overwrite x? (either enter digit or press enter for no overwrite):\n")
    x = 2 if not overwrite_x.isdigit() else int(overwrite_x)

    print(f"Finding the period for 2^r mod{n} using shors algorithm: \n\n")
    amplitudes = quantum_prime_factorization(n, x)

    print("\nShors algorithm has now been executed, however, in a real world scenario, merely one value could be read from register 1 (concidering the colapse).")
    print("Hence, a quantom forier transformation is executed.\n")
    probabilities = qft(amplitudes)

    plot = input("\nWould you like to plot the probability amplitudes in register one after executing the quantum forier transformation? (y/N)\n")
    if plot in ["y", "yes"]:
        plot_after_qft(list(probabilities.real))

    measured_reg_1 = measure_register(probabilities)
    print(f"Register 1 was measured to: c = {measured_reg_1}\n")

    print(f"Throught continous fractions, the period r can now be found from the relation:")
    print(f"c/N = {measured_reg_1}/{len(probabilities)} = k/r, where k is an abetrary intager.\n")

    period = input(f"Did you find the period? If so, provide r to calcaulate the prime factors: ")
    while not period.isdigit():
        period = input(f"Please provide r: ")

    int_period = int(period)
    period_calculation = int(x**(int_period/2))
    prime_factors = (int(np.gcd(period_calculation - 1, n)), int(np.gcd(period_calculation + 1, n)))
    print(f"The following prime factors were found: {prime_factors}")
    return prime_factors

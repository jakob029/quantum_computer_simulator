import matplotlib.pyplot as plt

def plot_after_qft(amplitudes: list):
    probabilities = [amplitude**2 for amplitude in amplitudes]
    len(probabilities)
    plt.plot(probabilities)
    plt.show()

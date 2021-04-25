from scipy.fft import fft

from acoustic_surveillance_subsystem.processing.processing_base import ProcessingBase
from acoustic_surveillance_subsystem.signal import Signal

import numpy as np
import matplotlib.pyplot as plt


class FastFourierTransform(ProcessingBase):
    def measure(self) -> float:
        return self.__fft_amplitude(self.signal)

    def __fft_amplitude(self, signal: Signal) -> float:
        fft_ = fft(signal.samples)
        # Turn all imaginary values into regular numbers.
        fft_regular = [int(val) for val in fft_]
        # Since the signal is placed around the 0 on y axis, it goes to both positive and negative values.
        # Output strength of the signal is measured in positive numbers, therefore we can turn all numbers absolute.
        fft_absolute = [abs(val) for val in fft_regular]

        N = int(signal.length)
        T = 1 / N

        # Everything divided by 2, because half the spectrum is a mirror.
        x_axis = np.linspace(0.0, 1.0 / (2.0 * T), int(N / 2))
        y_axis = 2.0 / N * np.abs(fft_[:N // 2])

        # fig, ax = plt.subplots()
        # ax.plot(x_axis, y_axis)
        # plt.show()

        # The highest value of fourier transform is considered to be the amplitude of the signal.
        return y_axis.max()

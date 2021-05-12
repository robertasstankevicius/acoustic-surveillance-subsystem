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

        # Only half a specter is relevant, therefore [:N // 2]
        #   This means that every value in the remaining spectre has to be multiplied by two.
        #   Source: https://www.sjsu.edu/people/burford.furman/docs/me120/FFT_tutorial_NI.pdf
        y_axis = 2.0 / N * np.array(fft_absolute[:N // 2])

        # x_axis = np.linspace(0.0, 1.0 / (2.0 * T), int(N / 2))
        # fig, ax = plt.subplots()
        # ax.plot(x_axis, y_axis)
        # plt.show()

        # The highest value of fourier transform is considered to be the amplitude of the signal.
        return y_axis.max()

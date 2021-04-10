from scipy.fft import fft

from acoustic_surveillance_subsystem.processing.processing_base import ProcessingBase
from acoustic_surveillance_subsystem.signal import Signal


class FastFourierTransform(ProcessingBase):
    def measure(self) -> float:
        return self.__fft_amplitude(self.signal)

    def __fft_amplitude(self, signal: Signal) -> float:
        fft_ = fft(signal.samples)
        # Turn all imaginary values into regular numbers.
        fft_ = [int(val) for val in fft_]
        # Since the signal is placed around the 0 on y axis, it goes to both positive and negative values.
        # Output strength of the signal is measured in positive numbers, therefore we can turn all numbers absolute.
        fft_ = [abs(val) for val in fft_]
        # The highest value of fourier transform is considered to be the amplitude of the signal.
        fft_ = max(fft_)
        return fft_

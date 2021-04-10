import math

from acoustic_surveillance_subsystem.processing.processing_base import ProcessingBase
from acoustic_surveillance_subsystem.signal import Signal


class PowerOfASignal(ProcessingBase):
    def measure(self) -> float:
        return self.__root_mean_square(self.signal)

    def __root_mean_square(self, signal: Signal):
        # RMS amplitude is defined as the square root of the
        # mean over time of the square of the amplitude.
        # so we need to convert this string of bytes into
        # a string of 16-bit samples...

        # we will get one short out for each
        # two chars in the string.

        # iterate over the block.
        sum_squares = 0.0
        for sample in signal.samples:
            # sample is a signed short in +/- 32768.
            # normalize it to 1.0

            # n = sample * (1.0 / 32768.0)
            # sum_squares += n * n

            n = sample
            sum_squares += n * n

        return math.sqrt(sum_squares / signal.length)

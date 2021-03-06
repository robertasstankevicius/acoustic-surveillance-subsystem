import math
import struct
from typing import Iterable


class Signal:
    def __init__(self, signal: Iterable[float], length: int):
        self.__signal = signal
        self.__length = length

    @property
    def signal(self):
        return self.__signal

    @property
    def length(self):
        return self.__signal

    @classmethod
    def from_bytes(cls, b: bytes) -> 'Signal':
        length = int(len(b) / 2)
        format_ = f'{length}h'
        signal = struct.unpack(format_, b)

        return cls(signal, length)

    def root_mean_square(self):
        # RMS amplitude is defined as the square root of the
        # mean over time of the square of the amplitude.
        # so we need to convert this string of bytes into
        # a string of 16-bit samples...

        # we will get one short out for each
        # two chars in the string.

        # iterate over the block.
        sum_squares = 0.0
        for sample in self.__signal:
            # sample is a signed short in +/- 32768.
            # normalize it to 1.0

            # n = sample * (1.0 / 32768.0)
            # sum_squares += n * n

            n = sample
            sum_squares += n * n

        return math.sqrt(sum_squares / self.__length)

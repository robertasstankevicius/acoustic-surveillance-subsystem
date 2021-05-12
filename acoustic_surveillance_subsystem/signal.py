import struct
from typing import Iterable


class Signal:
    def __init__(self, samples: Iterable[float], length: int):
        self.__samples = samples
        self.__length = length

    @property
    def samples(self):
        return self.__samples

    @property
    def length(self):
        return self.__length

    @classmethod
    def from_bytes(cls, b: bytes) -> 'Signal':
        length = int(len(b) / 2)
        # pyaudio aInt16 and 'h' correspond.
        format_ = f'{length}h'
        signal = struct.unpack(format_, b)

        return cls(signal, length)

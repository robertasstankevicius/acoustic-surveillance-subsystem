import abc

from acoustic_surveillance_subsystem.signal import Signal


class ProcessingBase(abc.ABC):
    def __init__(self, signal: Signal):
        self.signal = signal

    @abc.abstractmethod
    def measure(self) -> float:
        pass

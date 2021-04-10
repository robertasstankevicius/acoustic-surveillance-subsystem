from acoustic_surveillance_subsystem.processing.processing_base import ProcessingBase
from acoustic_surveillance_subsystem.signal import Signal


class DynamicRange(ProcessingBase):
    def measure(self) -> float:
        return self.__amplitude(self.signal)

    def __amplitude(self, signal: Signal) -> float:
        return max(signal.samples) - min(signal.samples)

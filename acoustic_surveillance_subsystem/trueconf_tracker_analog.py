from typing import Optional, Type

from acoustic_surveillance_subsystem.processing.processing_base import ProcessingBase
from acoustic_surveillance_subsystem.signal import Signal


class TrueConfTrackerAnalog:
    """
    Class dedicated to processing audio signals and measuring the direction
    that the audio is coming from in a plane.

    It is a copy of TrueConf Tracker technology. This is purely for methodology comparison.
    Source: https://trueconf.com/products/tracker.html
    """

    def __init__(self, angle1: float, angle2: float, angle3: float, processor: Type[ProcessingBase]):
        """

        :param angle1: Angle at which the first microphone is pointed.
        :param angle2: Angle at which the second microphone is pointed.
        :param angle3: Angle at which the third microphone is pointed.
        :param processor: Audio processing class to use when processing audio signals.
        """
        self.__angle1 = angle1
        self.__angle2 = angle2
        self.__angle3 = angle3
        self.__processor = processor

    def measure_angle(self, signal1: Signal, signal2: Signal, signal3: Signal) -> Optional[float]:
        """
        Calculates at which angle the audio is coming from using the provided audio processor.


        :param signal1: Signal wave.
        :param signal2: Signal wave.
        :param signal3: Signal wave.

        :return: Angle at which the audio came from if it can be measured, otherwise return None.
        """

        loudness1 = self.__processor(signal1).measure()
        loudness2 = self.__processor(signal2).measure()
        loudness3 = self.__processor(signal3).measure()

        if loudness1 > loudness2 and loudness1 > loudness3:
            return self.__angle1

        if loudness2 > loudness1 and loudness2 > loudness3:
            return self.__angle2

        if loudness3 > loudness2 and loudness3 > loudness1:
            return self.__angle3

        elif loudness1 == loudness2 == loudness3:
            return None

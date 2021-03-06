from typing import Optional

from acoustic_surveillance_subsystem.signal import Signal
from acoustic_surveillance_subsystem.utils import normalize_sequence, calculate_degrees_between_angle


class PlaneAudioDirection:
    """
    Class dedicated to processing audio signals and measuring the direction
    that the audio is coming from in a plane.
    """

    def __init__(self, angle1: float, angle2: float, angle3: float):
        self.__angle1 = angle1
        self.__angle2 = angle2
        self.__angle3 = angle3

    def measure_angle_rms(self, signal1: Signal, signal2: Signal, signal3: Signal) -> Optional[float]:
        """
        Calculates at which angle the audio is coming from using Power of a Signal method which relies on measuring
        root mean square of each signal.

        :param signal1: Signal wave.
        :param signal2: Signal wave.
        :param signal3: Signal wave.

        :return: Angle at which the audio came from if it can be measured, otherwise return None.
        """

        normalized1, normalized2, normalized3 = normalize_sequence((signal1.root_mean_square(), signal2.root_mean_square(), signal3.root_mean_square()))

        if normalized1 == 0:
            available_angle = self.__angle3 - self.__angle2
            return self.__angle2 + calculate_degrees_between_angle(normalized2, normalized3, available_angle)

        elif normalized2 == 0:
            available_angle = 360 - self.__angle3 + self.__angle1
            return (self.__angle3 + calculate_degrees_between_angle(normalized3, normalized1, available_angle)) % 360

        elif normalized3 == 0:
            available_angle = self.__angle2 - self.__angle1
            return self.__angle1 + calculate_degrees_between_angle(normalized1, normalized2, available_angle)

        elif normalized1 == normalized2 == normalized3:
            return None

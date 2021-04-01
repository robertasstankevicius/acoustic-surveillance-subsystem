import socket
from typing import Tuple

import numpy as np


def normalize_sequence(arr: Tuple[float, ...]) -> Tuple[np.float64, ...]:
    """
    Normalizes a sequence of numbers to [0, 1] range.

    :param arr: Sequence of numbers to normalize.

    :return: Sequence of normalized numbers.
    """

    normalized_arr = (np.array(arr) - np.min(arr)) / (np.max(arr) - np.min(arr))

    return tuple(normalized_arr)


def calculate_degrees_between_angle(norm_1, norm_2, angle):
    """
    Takes two normalized values in a range of [0, 1] and calculates a proportion inside an angle.

    :param norm_1: First normalized value.
    :param norm_2: Second normalized value.
    :param angle: Angle in which to calculate the proportion.

    :return: Calculated angle.
    """

    norm_total = norm_1 + norm_2
    min_norm = min([norm_1, norm_2])
    i = int(min_norm == norm_2)
    x = angle * min_norm / norm_total

    if i == 0:
        return angle - x
    else:
        return x


def send_packet_and_close(ip: str, port: int, packet: bytes) -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    s.connect((ip, port))
    s.send(packet)
    s.close()

import time

import vlc

from acoustic_surveillance_subsystem.secrets import full_address
from acoustic_surveillance_subsystem.utils import send_packet_and_close


class Ipc365VideoDevice:
    LEFT_MOST_ANGLE = 8
    RIGHT_MOST_ANGLE = 354

    TOP_MOST_ANGLE = 90
    BOTTOM_MOST_ANGLE = -23

    MAX_TURN_PER_STEP = 180

    def __init__(self):
        self.current_horizontal_angle = 179  # pretty sure this is right, or it can be 178
        self.current_vertical_angle = 0

        player = vlc.MediaPlayer(full_address)

        # There is an issue, that at around 30 or 60 seconds of RTSP stream, the connection just closes for no reason.
        # This is a temporary solution.
        while True:
            player.play()
            time.sleep(20)
            player.stop()

    def turn_right(self, angle: int):
        next_angle = self.current_horizontal_angle + angle
        if next_angle > self.RIGHT_MOST_ANGLE:
            raise Exception(f'Reached invalid horizontal angle.')

        self.current_horizontal_angle = next_angle

        packet_start = b'\xcc\xdd\xee\xff\x77\x4f\x00\x00\xe3\x12\x69\x00\x48\x00\x00\x00\x00\x00\x00\x00\xaf\x93\xc6\x3b\x09\xf7\x4b\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        angle = bytes([angle])
        packet_end = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        packet = packet_start + angle + packet_end

        send_packet_and_close('192.168.0.118', 23456, packet)

    def turn_left(self, angle: int):
        next_angle = self.current_horizontal_angle - angle
        if next_angle < self.LEFT_MOST_ANGLE:
            raise Exception(f'Reached invalid horizontal angle.')

        self.current_horizontal_angle = next_angle

        packet_start = b'\xcc\xdd\xee\xff\x77\x4f\x00\x00\xe3\x12\x69\x00\x48\x00\x00\x00\x00\x00\x00\x00\xaf\x93\xc6\x3b\x09\xf7\x4b\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        angle = bytes([255 - angle])
        packet_end = b'\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        packet = packet_start + angle + packet_end

        send_packet_and_close('192.168.0.118', 23456, packet)

    def turn_up(self, angle: int):
        next_angle = self.current_vertical_angle + angle
        if next_angle > self.TOP_MOST_ANGLE:
            raise Exception(f'Reached invalid vertical angle.')

        self.current_vertical_angle = next_angle

        packet_start = b'\xcc\xdd\xee\xff\x77\x4f\x00\x00\xe3\x12\x69\x00\x48\x00\x00\x00\x00\x00\x00\x00\xaf\x93\xc6\x3b\x09\xf7\x4b\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        angle = bytes([angle])
        packet_end = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        packet = packet_start + angle + packet_end

        send_packet_and_close('192.168.0.118', 23456, packet)

    def turn_down(self, angle: int):
        next_angle = self.current_vertical_angle - angle
        if next_angle < self.BOTTOM_MOST_ANGLE:
            raise Exception(f'Reached invalid vertical angle.')

        self.current_vertical_angle = next_angle

        packet_start = b'\xcc\xdd\xee\xff\x77\x4f\x00\x00\xe3\x12\x69\x00\x48\x00\x00\x00\x00\x00\x00\x00\xaf\x93\xc6\x3b\x09\xf7\x4b\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        angle = bytes([255 - angle])
        packet_end = b'\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        packet = packet_start + angle + packet_end

        send_packet_and_close('192.168.0.118', 23456, packet)

    def turn_to_horizontal_angle(self, angle: int) -> None:
        if angle > self.RIGHT_MOST_ANGLE:
            angle = self.RIGHT_MOST_ANGLE
        elif angle < self.LEFT_MOST_ANGLE:
            angle = self.LEFT_MOST_ANGLE

        remaining_turn_angle = angle - self.current_horizontal_angle

        first_iteration = True

        turn_function = self.turn_right
        if remaining_turn_angle < 0:
            turn_function = self.turn_left
            remaining_turn_angle = -remaining_turn_angle

        while remaining_turn_angle > 0:
            print(remaining_turn_angle)
            if first_iteration:
                first_iteration = False
            else:
                time.sleep(2)
            next_turn = remaining_turn_angle if remaining_turn_angle > self.MAX_TURN_PER_STEP else remaining_turn_angle
            remaining_turn_angle -= next_turn
            turn_function(next_turn)
            # TODO: debug, because there are still some random exceptions...

    def turn_to_vertical_angle(self, angle: int) -> None:
        if angle > self.TOP_MOST_ANGLE:
            angle = self.TOP_MOST_ANGLE
        elif angle < self.BOTTOM_MOST_ANGLE:
            angle = self.BOTTOM_MOST_ANGLE

        remaining_turn_angle = angle - self.current_vertical_angle

        first_iteration = True

        while remaining_turn_angle > 0:
            if first_iteration:
                first_iteration = False
            else:
                time.sleep(2)
            next_turn = remaining_turn_angle if remaining_turn_angle > self.MAX_TURN_PER_STEP else remaining_turn_angle
            remaining_turn_angle -= next_turn
            self.turn_up(next_turn)

        while remaining_turn_angle < 0:
            if first_iteration:
                first_iteration = False
            else:
                time.sleep(2)
            next_turn = remaining_turn_angle if remaining_turn_angle < self.MAX_TURN_PER_STEP else remaining_turn_angle
            remaining_turn_angle += next_turn
            self.turn_down(-next_turn)

    def __validate_horizontal_angles(self, angle: int) -> None:
        next_angle = self.current_horizontal_angle + angle
        if next_angle < self.LEFT_MOST_ANGLE or next_angle > self.RIGHT_MOST_ANGLE:
            raise Exception(
                f'Reached invalid horizontal angle. Allowed angles: {self.LEFT_MOST_ANGLE} to {self.RIGHT_MOST_ANGLE}. Horizontal angle: {self.current_horizontal_angle}.')

    def __validate_vertical_angles(self) -> None:
        if self.current_vertical_angle < self.BOTTOM_MOST_ANGLE or self.current_vertical_angle > self.TOP_MOST_ANGLE:
            raise Exception(f'Reached invalid vertical angle. Allowed angles: {self.BOTTOM_MOST_ANGLE} to {self.TOP_MOST_ANGLE}. Vertical angle: {self.current_vertical_angle}.')

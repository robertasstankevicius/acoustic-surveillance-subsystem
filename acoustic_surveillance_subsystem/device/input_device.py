from typing import Optional

import pyaudio

from acoustic_surveillance_subsystem.device.audio_device import AudioDevice


class InputDevice:
    def __init__(self, device: AudioDevice):
        if device.max_input_channels == 0:
            raise ValueError('Provided device is not a microphone.')

        self.__device = device
        self.__on = False

    def record(
            self,
            chunk_size: int = 1024,
            pa_format: int = pyaudio.paInt16,
            channels: Optional[int] = None,
            sample_rate: Optional[int] = None
    ):
        p = pyaudio.PyAudio()

        stream = p.open(
            format=pa_format,
            channels=channels or self.__device.max_input_channels,
            rate=sample_rate or self.__device.default_sample_rate,
            input=True,
            input_device_index=self.__device.index,
            frames_per_buffer=chunk_size
        )

        self.__on = True

        while self.__on:
            yield stream.read(chunk_size)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop(self):
        self.__on = False

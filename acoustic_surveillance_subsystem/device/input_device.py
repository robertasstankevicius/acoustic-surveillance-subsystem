from typing import Optional, Generator, Dict, Any

import pyaudio

from acoustic_surveillance_subsystem.device.audio_device import AudioDevice


class InputDevice(AudioDevice):
    def __init__(
            self,
            device: Dict[str, Any],
            chunk_size: int = 1024,
            pa_format: int = pyaudio.paInt16,
            channels: Optional[int] = None,
            sample_rate: Optional[int] = None
    ):
        super().__init__(device)

        if self.max_input_channels == 0:
            raise ValueError('Provided device is not a microphone.')

        self.__on = False

        self.pa_format = pa_format
        self.chunk_size = chunk_size
        self.channels = channels or self.max_input_channels
        self.sample_rate = sample_rate or self.default_sample_rate

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pa_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            input_device_index=self.index,
            frames_per_buffer=self.chunk_size
        )

    def record(
            self,
    ) -> Generator[str, None, None]:
        self.__on = True

        while self.__on:
            yield self.stream.read(self.chunk_size)

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def stop(self):
        self.__on = False

    @property
    def time_per_chunk(self):
        """
        Seconds what time of span a single chunk records.

        :return: Float number of seconds.
        """
        return self.chunk_size / self.sample_rate

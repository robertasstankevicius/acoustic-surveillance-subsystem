from typing import Optional, Any, Dict

import pyaudio

FORMAT = pyaudio.paInt16


class MicrophoneStream:
    def __init__(self, mic: Dict[str, Any]):
        self.__mic = mic
        self.__on = False

    def record(
            self,
            chunk_length: float,
            total: float,
            channels: Optional[int] = None,
            sample_rate: Optional[int] = None
    ):
        sample_rate = sample_rate or self.default_sample_rate

        chunk = int(sample_rate * chunk_length)

        p = pyaudio.PyAudio()
        stream = p.open(
            format=FORMAT,
            channels=channels or self.max_input_channels,
            rate=sample_rate,
            input=True,
            input_device_index=self.index,
            frames_per_buffer=chunk
        )

        self.__on = True

        elapsed = 0.0

        while elapsed < total:
            yield stream.read(chunk)
            elapsed += chunk_length

        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop(self):
        self.__on = False

    @property
    def name(self):
        return self.__mic['name']

    @property
    def index(self):
        return self.__mic['index']

    @property
    def max_input_channels(self):
        return self.__mic['maxInputChannels']

    @property
    def default_sample_rate(self):
        return int(self.__mic['defaultSampleRate'])

    @property
    def default_high_input_latency(self):
        return self.__mic['defaultHighInputLatency']

    @property
    def default_high_output_latency(self):
        return self.__mic['defaultHighOutputLatency']

    @property
    def default_low_input_latency(self):
        return self.__mic['defaultLowInputLatency']

    @property
    def default_low_output_latency(self):
        return self.__mic['defaultLowOutputLatency']

    @property
    def host_api(self):
        return self.__mic['hostApi']

    @property
    def max_output_channels(self):
        return self.__mic['maxOutputChannels']

    @property
    def struct_version(self):
        return self.__mic['structVersion']

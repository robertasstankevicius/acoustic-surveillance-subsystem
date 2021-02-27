from typing import Any, Dict


class AudioDevice:
    """
    An interface for PyAudio Device for easier parameter management.
    """

    def __init__(self, device: Dict[str, Any]):
        self.__device = device

    @property
    def name(self):
        return self.__device['name']

    @property
    def index(self):
        return self.__device['index']

    @property
    def max_input_channels(self):
        return self.__device['maxInputChannels']

    @property
    def default_sample_rate(self):
        return int(self.__device['defaultSampleRate'])

    @property
    def default_high_input_latency(self):
        return self.__device['defaultHighInputLatency']

    @property
    def default_high_output_latency(self):
        return self.__device['defaultHighOutputLatency']

    @property
    def default_low_input_latency(self):
        return self.__device['defaultLowInputLatency']

    @property
    def default_low_output_latency(self):
        return self.__device['defaultLowOutputLatency']

    @property
    def host_api(self):
        return self.__device['hostApi']

    @property
    def max_output_channels(self):
        return self.__device['maxOutputChannels']

    @property
    def struct_version(self):
        return self.__device['structVersion']

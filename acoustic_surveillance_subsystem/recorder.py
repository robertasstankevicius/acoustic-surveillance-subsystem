import wave
from typing import Dict, Generator, Iterable, Optional

from acoustic_surveillance_subsystem.device.input_device import InputDevice


class Recorder:
    def __init__(self):
        self.__input_devices: Dict[str, InputDevice] = {}
        self.__time_per_chunk: Optional[float] = None

    def add_device(self, name: str, device: InputDevice):
        if self.__input_devices.get('name'):
            raise Exception(f'Device with name {name} already exists.')

        self.__input_devices[name] = device

        # Make sure all input record the same span of time per audio chunk.
        if self.__time_per_chunk is None:
            self.__time_per_chunk = device.time_per_chunk
        elif device.time_per_chunk != self.__time_per_chunk:
            raise Exception('All devices must record the same span of time per chunk.')

    def record(self) -> Generator[Dict[str, str], None, None]:
        iterators: Dict[str, Iterable] = {}
        for device_name, device in self.__input_devices.items():
            iterators[device_name] = iter(device.record())

        while True:
            yield {device_name: next(iterator) for device_name, iterator in iterators.items()}

    def record_to_files(self, duration: Optional[float]) -> Generator[Dict[str, str], None, None]:
        time_elapsed = 0.0

        files = {}

        for device_name, device in self.__input_devices.items():
            file = wave.open(f'{device_name}.wav', 'wb')
            file.setnchannels(device.channels)
            file.setsampwidth(device.p.get_sample_size(device.pa_format))
            file.setframerate(device.sample_rate)

            files[device_name] = file

        for batches in self.record():
            for name, batch in batches.items():
                files[name].writeframes(batch)

            yield batches

            time_elapsed += self.__time_per_chunk
            print(time_elapsed)
            if duration and duration <= time_elapsed:
                break

        for file in files.values():
            file.close()

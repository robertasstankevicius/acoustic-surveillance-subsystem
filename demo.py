import threading
from typing import List

import pyaudio

from acoustic_surveillance_subsystem.microphone_stream import MicrophoneStream

p = pyaudio.PyAudio()

microphone_name = 'USB Condenser'

devices: List[MicrophoneStream] = []

for i in range(p.get_device_count()):
    device = p.get_device_info_by_index(i)
    if microphone_name in device.get('name', ''):
        devices.append(MicrophoneStream(device))

threads: List[threading.Thread] = []

m1, m2, m3 = devices

x1 = threading.Thread(target=lambda: [print(m1.index) for data in m1.record(0.1, 2)])
x2 = threading.Thread(target=lambda: [print(m2.index) for data in m2.record(0.1, 2)])
x3 = threading.Thread(target=lambda: [print(m3.index) for data in m3.record(0.1, 2)])

x1.start()
x2.start()
x3.start()

x1.join()
x2.join()
x3.join()

# for mic in devices:
#     print(f'starting {mic.index}')
#     t =threading.Thread(target=lambda: [print(mic.index) for data in mic.record(0.1, 2)])
#     t.start()
#     t.join()

# for t in threads:
#     t.start()
#     t.join()


# for a in mic.record(0.1):
#     print(mic.index)

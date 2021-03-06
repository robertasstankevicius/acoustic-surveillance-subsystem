import threading
from typing import List

import pyaudio

from acoustic_surveillance_subsystem.device.input_device import InputDevice
from acoustic_surveillance_subsystem.plane_virtualisation import PlaneAudioDirection
from acoustic_surveillance_subsystem.recorder import Recorder
from acoustic_surveillance_subsystem.signal import Signal

p = pyaudio.PyAudio()

microphone_name = 'USB Condenser'

devices: List[InputDevice] = []

for i in range(p.get_device_count()):
    device = p.get_device_info_by_index(i)
    if microphone_name in device.get('name', ''):
        devices.append(InputDevice(device=device, chunk_size=2048, channels=1))

threads: List[threading.Thread] = []

m1, m2, m3 = devices

recorder = Recorder()

recorder.add_device('1', m1)
recorder.add_device('2', m2)
recorder.add_device('3', m3)

import time

pad = PlaneAudioDirection(0, 120, 240)

start_time = time.time()
for a in recorder.record():
    signals = (Signal.from_bytes(a['2']), Signal.from_bytes(a['3']), Signal.from_bytes(a['1']))
    signal1, signal2, signal3 = signals
    # print(tuple(signal.root_mean_square() for signal in signals))

    b = pad.measure_angle_rms(signal1, signal2, signal3)
    print(b)

print("--- %s seconds ---" % (time.time() - start_time))

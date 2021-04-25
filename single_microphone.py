import threading
from pprint import pprint
from typing import List, Optional

import pyaudio

from acoustic_surveillance_subsystem.device.input_device import InputDevice
from acoustic_surveillance_subsystem.plane_virtualisation import PlaneAudioDirection
from acoustic_surveillance_subsystem.processing.dynamic_range import DynamicRange
from acoustic_surveillance_subsystem.processing.fast_fourier_transform import FastFourierTransform
from acoustic_surveillance_subsystem.processing.power_of_a_signal import PowerOfASignal
from acoustic_surveillance_subsystem.recorder import Recorder
from acoustic_surveillance_subsystem.signal import Signal
import numpy as np
import matplotlib.pyplot as plt

p = pyaudio.PyAudio()

microphone_name = 'Microsoft Sound Mapper - Input'

main_device: Optional[InputDevice] = None

for i in range(p.get_device_count()):
    device = p.get_device_info_by_index(i)
    pprint(device)
    if microphone_name in device.get('name', ''):
        main_device = InputDevice(device=device, chunk_size=2048, channels=1)

recorder = Recorder()

recorder.add_device('1', main_device)

for a in recorder.record():
    signal = Signal.from_bytes(a['1'])

    print(
        PowerOfASignal(signal).measure(),
        DynamicRange(signal).measure(),
        FastFourierTransform(signal).measure()
    )

    # plt.axis([PowerOfASignal(signal).measure(),
    #           DynamicRange(signal).measure(),
    #           FastFourierTransform(signal).measure()])

#     for i in range(10):
#         y = np.random.random()
#         plt.scatter(i, y)
#         plt.pause(0.05)
#     plt.show()
# plt.axis([0, 10, 0, 1])

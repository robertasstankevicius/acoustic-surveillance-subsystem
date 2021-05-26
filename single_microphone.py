import threading
from pprint import pprint
from typing import List, Optional

import pyaudio

from acoustic_surveillance_subsystem.device.input_device import InputDevice
from acoustic_surveillance_subsystem.plane_audio_direction import PlaneAudioDirection
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

plt.axis()

linewidth = 0.5
samples_elapsed = 0
i_list = []
poas_list = []
dr_list = []
fft_list = []
for i, a in enumerate(recorder.record(.25)):
    signal = Signal.from_bytes(a['1'])

    poas = PowerOfASignal(signal).measure()
    dr = DynamicRange(signal).measure()
    fft = FastFourierTransform(signal).measure()

    i_list.append(i)
    poas_list.append(poas)
    dr_list.append(dr)
    fft_list.append(fft)

    print(poas, dr, fft)

    # plt.plot(list(range(samples_elapsed, samples_elapsed + signal.length)), signal.samples, color='blue', linewidth=linewidth)
    # samples_elapsed += signal.length

plt.scatter(i_list, poas_list, c='blue', marker='o', label='Power of a Signal')
plt.scatter(i_list, dr_list, c='brown', marker='v', label='Dynamic Range')
plt.scatter(i_list, fft_list, c='red', marker='x', label='Fast Fourier Transform')
plt.legend()

plt.show()
# plt.pause(0.1)
# plt.axis([0, 10, 0, 1])

import os
import threading
from typing import List

import pyaudio

from acoustic_surveillance_subsystem.device.input_device import InputDevice
from acoustic_surveillance_subsystem.plane_audio_direction import PlaneAudioDirection
from acoustic_surveillance_subsystem.processing.dynamic_range import DynamicRange
from acoustic_surveillance_subsystem.processing.fast_fourier_transform import FastFourierTransform
from acoustic_surveillance_subsystem.processing.power_of_a_signal import PowerOfASignal
from acoustic_surveillance_subsystem.recorder import Recorder
from acoustic_surveillance_subsystem.signal import Signal

p = pyaudio.PyAudio()

microphone_name = 'USB Condenser'

devices: List[InputDevice] = []

for i in range(p.get_device_count()):
    device = p.get_device_info_by_index(i)
    if microphone_name in device.get('name', ''):
        devices.append(InputDevice(device=device, chunk_size=2048*10, channels=1))

threads: List[threading.Thread] = []

m1, m2, m3 = devices

recorder = Recorder()

recorder.add_device('1', m1)
recorder.add_device('2', m2)
recorder.add_device('3', m3)

import time

start_time = time.time()
for a in recorder.record():
    signals = (Signal.from_bytes(a['1']), Signal.from_bytes(a['2']), Signal.from_bytes(a['3']))
    signal1, signal2, signal3 = signals

    poas = (int(PowerOfASignal(signal1).measure()), int(PowerOfASignal(signal2).measure()), int(PowerOfASignal(signal3).measure()))
    print(poas)

    # dr = (int(DynamicRange(signal1).measure()), int(DynamicRange(signal2).measure()), int(DynamicRange(signal3).measure()))
    # fft = (int(FastFourierTransform(signal1).measure()), int(FastFourierTransform(signal2).measure()), int(FastFourierTransform(signal3).measure()))
    #
    # print('----------POAS----------------------DR------------------------FFT--------------')
    # print(f'{poas}\t\t\t\t{dr}\t\t\t\t\t{fft}')

print("--- %s seconds ---" % (time.time() - start_time))

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
from trueconf_tracker_analog import TrueConfTrackerAnalog
from utils import FileWriter

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

angle1 = 135
angle2 = 180
angle3 = 225

power_of_a_signal_in_plane = PlaneAudioDirection(angle1, angle2, angle3, PowerOfASignal)
dynamic_range_in_plane = PlaneAudioDirection(angle1, angle2, angle3, DynamicRange)
fast_fourier_transform_in_plane = PlaneAudioDirection(angle1, angle2, angle3, FastFourierTransform)

power_of_a_signal_in_plane_tc = TrueConfTrackerAnalog(angle1, angle2, angle3, PowerOfASignal)
dynamic_range_in_plane_tc = TrueConfTrackerAnalog(angle1, angle2, angle3, DynamicRange)
fast_fourier_transform_in_plane_tc = TrueConfTrackerAnalog(angle1, angle2, angle3, FastFourierTransform)


angle = '145'
distance = '2'
wavelength = '2500'
comment ='135-180-225'

file_writer = FileWriter(f'benchmark_{angle}degrees_{distance}m_{wavelength}Hz_{comment}.txt')
file_writer_tc = FileWriter(f'benchmark_{angle}degrees_{distance}m_{wavelength}Hz_{comment}_trueconf.txt')
file_writer.write('n, poas, dr, fft', new_line=False)
file_writer_tc.write('n, poas, dr, fft', new_line=False)

start_time = time.time()
for i, a in enumerate(recorder.record(48)):
    # If I connect them one by one, this is the correct order of microphones.
    signals = (Signal.from_bytes(a['1']), Signal.from_bytes(a['2']), Signal.from_bytes(a['3']))
    signal1, signal2, signal3 = signals

    poas = power_of_a_signal_in_plane.measure_angle(signal1, signal2, signal3)
    dr = dynamic_range_in_plane.measure_angle(signal1, signal2, signal3)
    fft = fast_fourier_transform_in_plane.measure_angle(signal1, signal2, signal3)

    file_writer.write(f'{i},{poas},{dr},{fft}')

    print(f'{i}, {poas}, {dr}, {fft}')

print("--- %s seconds ---" % (time.time() - start_time))

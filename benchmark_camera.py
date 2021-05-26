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
from device.ipc365_video_device import Ipc365VideoDevice
from trueconf_tracker_analog import TrueConfTrackerAnalog

p = pyaudio.PyAudio()

microphone_name = 'USB Condenser'

devices: List[InputDevice] = []

for i in range(p.get_device_count()):
    device = p.get_device_info_by_index(i)
    if microphone_name in device.get('name', ''):
        devices.append(InputDevice(device=device, chunk_size=2048 * 4, channels=1))

threads: List[threading.Thread] = []

m1, m2, m3 = devices

recorder = Recorder()

recorder.add_device('1', m1)
recorder.add_device('2', m2)
recorder.add_device('3', m3)

angle1 = 135
angle2 = 180
angle3 = 225

processor_n = input('Loudness measurement method\n'
                    '\t1 - Power of a Signal\n'
                    '\t2 - Dynamic Range\n'
                    '\t3 - Fast Fourier Transform\n'
                    'Input: ')

if processor_n == '1':
    processor = PowerOfASignal
elif processor_n == '2':
    processor = DynamicRange
elif processor_n == '3':
    processor = FastFourierTransform
else:
    raise Exception('Please select one of the suggested options.')

direction_n = input('Input direction measurement method\n'
                    '\t1 - Proposed method\n'
                    '\t2 - TrueConf Tracker\n'
                    'Input: ')

if direction_n == '1':
    direction = PlaneAudioDirection(angle1, angle2, angle3, processor)
elif direction_n == '2':
    direction = TrueConfTrackerAnalog(angle1, angle2, angle3, processor)
else:
    raise Exception('Please select one of the suggested options.')

measurement_threshold = 200
if processor_n == '2':
    measurement_threshold *= 10

camera = Ipc365VideoDevice(show_view=False)

for i, a in enumerate(recorder.record()):
    # If I connect them one by one, this is the correct order of microphones.
    signals = (Signal.from_bytes(a['2']), Signal.from_bytes(a['3']), Signal.from_bytes(a['1']))
    signal1, signal2, signal3 = signals

    # Filter out silence
    signal1_loudness = processor(signal1).measure()
    signal2_loudness = processor(signal2).measure()
    signal3_loudness = processor(signal3).measure()

    print(f'Loudness: {signal1_loudness, signal2_loudness, signal3_loudness}')
    if signal1_loudness < measurement_threshold \
            and signal2_loudness < measurement_threshold \
            and signal3_loudness < measurement_threshold:
        continue

    angle = direction.measure_angle(signal1, signal2, signal3)
    print(f'Angle: {angle}')

    if angle and not camera.is_turning:
        camera.turn_to_horizontal_angle(int(angle))

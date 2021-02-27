import math
import struct
import threading
from pprint import pprint
from typing import List

import pyaudio

from acoustic_surveillance_subsystem.device.input_device import InputDevice
from acoustic_surveillance_subsystem.recorder import Recorder

p = pyaudio.PyAudio()

microphone_name = 'USB Condenser'

devices: List[InputDevice] = []

for i in range(p.get_device_count()):
    device = p.get_device_info_by_index(i)
    if microphone_name in device.get('name', ''):
        devices.append(InputDevice(device))

threads: List[threading.Thread] = []

m1, m2, m3 = devices

recorder = Recorder()

recorder.add_device('1', m1)
recorder.add_device('2', m2)
recorder.add_device('3', m3)

import time
start_time = time.time()
for a in recorder.record_to_files(100):
    # print(a)
    pass
print("--- %s seconds ---" % (time.time() - start_time))


exit()
def to_signal(block):
    length = int(len(block) / 2)
    format = f'{length}h'
    signal = struct.unpack(format, block)

    return length, signal


def get_rms(block):
    # RMS amplitude is defined as the square root of the
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into
    # a string of 16-bit samples...

    # we will get one short out for each
    # two chars in the string.
    length, signal = to_signal(block)

    # iterate over the block.
    sum_squares = 0.0
    for sample in signal:
        # sample is a signed short in +/- 32768.
        # normalize it to 1.0
        n = sample * (1.0 / 32768.0)
        sum_squares += n * n

    return math.sqrt(sum_squares / length)

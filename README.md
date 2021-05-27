# acoustic-surveillance-subsystem
The acoustic alarm subsystem would perform the auxiliary tracking function of the monitored (threat) object. If the subject occupies a small area in the camera image, it is difficult to identify  the subject  by motion detection algorithms, However, they could be assisted by an acoustic subsystem that "hears" certain types of sounds, determines their propagation direction, and rotates the surveillance camera in that direction.

### Audio level detection example
The first step is to find your microphone using PyAudio.
```python
import pyaudio
p = pyaudio.PyAudio()

# Devices can be listed using this command.
p.get_device_count()

# A specific device must be selected. Note the index provided, it must be a number the previous command.
device = p.get_device_info_by_index(0)
```

The second step is to prepare the device for recording.
```python
from acoustic_surveillance_subsystem.device.input_device import InputDevice

input_device = InputDevice(device=device, chunk_size=2048, channels=1)
```

Then one of the following the audio level measurement methods must be selected.
```python
from acoustic_surveillance_subsystem.processing.dynamic_range import DynamicRange
from acoustic_surveillance_subsystem.processing.fast_fourier_transform import FastFourierTransform
from acoustic_surveillance_subsystem.processing.power_of_a_signal import PowerOfASignal

processor = PowerOfASignal | DynamicRange | FastFourierTransform
```

Start recording and processing the audio.
```python
from acoustic_surveillance_subsystem.recorder import Recorder
from acoustic_surveillance_subsystem.signal import Signal

recorder = Recorder()

# Add the existing device to the recorder.
recorder.add_device('device_name', input_device)

for i, a in enumerate(recorder.record()):
    signal = Signal.from_bytes(a['device_name'])
    audio_level = processor(signal).measure()
```

### Audio direction detection example
A direction measurement class must be initiated and the selected processing class should be provided.
```python
import pyaudio
from acoustic_surveillance_subsystem.plane_audio_direction import PlaneAudioDirection
from acoustic_surveillance_subsystem.recorder import Recorder
from acoustic_surveillance_subsystem.processing.dynamic_range import DynamicRange
from acoustic_surveillance_subsystem.signal import Signal
from acoustic_surveillance_subsystem.device.input_device import InputDevice


p = pyaudio.PyAudio()

device1 = p.get_device_info_by_index(0)
device2 = p.get_device_info_by_index(1)
device3 = p.get_device_info_by_index(2)
input_device1 = InputDevice(device=device1, chunk_size=2048, channels=1)
input_device2 = InputDevice(device=device2, chunk_size=2048, channels=1)
input_device3 = InputDevice(device=device3, chunk_size=2048, channels=1)

recorder = Recorder()

recorder.add_device('1', input_device1)
recorder.add_device('2', input_device2)
recorder.add_device('3', input_device3)

# Set the angles where the microphones are actually pointed at.
angle1 = 0
angle2 = 120
angle3 = 240

direction_calculator = PlaneAudioDirection(angle1, angle2, angle3, DynamicRange)
for i, a in enumerate(recorder.record()):
    # Make sure that when microphones are connected, this is the correct order.
    signals = (Signal.from_bytes(a['1']), Signal.from_bytes(a['2']), Signal.from_bytes(a['3']))
    signal1, signal2, signal3 = signals

    direction_angle = direction_calculator.measure_angle(signal1, signal2, signal3)
```
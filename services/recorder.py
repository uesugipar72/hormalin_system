import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename="input.wav", duration=5, fs=44100):

    device_id = 8
    device_info = sd.query_devices(device_id, 'input')
    channels = device_info['max_input_channels']

    print("Recording...")

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=channels,
        device=device_id
    )

    sd.wait()
    write(filename, fs, recording)

    print("Recording finished")
    return filename

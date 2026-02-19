import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

def record_audio(filename="input.wav", duration=5, fs=44100):
    print("録音開始...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, recording)
    print("録音終了")
    return filename

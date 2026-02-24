import sounddevice as sd
import soundfile as sf

def record_audio(duration=5, filename="input.wav"):
    fs = 44100
    device_id = 0  # 入力デバイス

    print("Recording...")
    recording = sd.rec(int(duration * fs),
                       samplerate=fs,
                       channels=1,
                       dtype='float32',
                       device=device_id)
    sd.wait()
    print("Recording finished")

    sf.write(filename, recording, fs)
    return filename
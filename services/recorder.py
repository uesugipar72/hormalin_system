import sounddevice as sd
import soundfile as sf
import numpy as np

def record_audio(filename="input.wav"):
    fs = 44100
    device_id = 0
    recording = []
    is_recording = True

    def callback(indata, frames, time, status):
        if status:
            print(status)
        recording.append(indata.copy())

    print("Recording... Press Enter to stop.")
    
    with sd.InputStream(samplerate=fs,
                        channels=1,
                        dtype='float32',
                        device=device_id,
                        callback=callback):
        input()  # Enterで停止
    
    audio = np.concatenate(recording, axis=0)
    sf.write(filename, audio, fs)

    print("Recording finished")
    return filename
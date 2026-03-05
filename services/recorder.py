import sounddevice as sd
import soundfile as sf
import numpy as np

def record_audio(filename="input.wav"):
    fs = 16000
    device_id = 1
    channels = 1

    recording = []

    def callback(indata, frames, time, status):
        if status:
            print(status)
        recording.append(indata.copy())

    print("Recording... Press Enter to stop.")

    with sd.InputStream(
        samplerate=fs,
        channels=channels,
        dtype='float32',
        device=device_id,
        callback=callback
    ):
        input()

    if len(recording) == 0:
        raise Exception("録音データが取得できませんでした（マイク入力なし）")

    audio = np.concatenate(recording, axis=0)

    print("Recording finished")
    return filename
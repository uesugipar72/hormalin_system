import sounddevice as sd
import soundfile as sf
import numpy as np

def record_audio(filename="input.wav"):

    fs = 16000
    device_id = 1      # Logi C270 マイク
    channels = 1

    recording = []

    def callback(indata, frames, time, status):
        if status:
            print(status)
        recording.append(indata.copy())

    print("録音開始... Enterキーで終了")

    try:
        with sd.InputStream(
                samplerate=fs,
                channels=channels,
                dtype="float32",
                device=device_id,
                callback=callback):

            input()  # Enter待ち

    except Exception as e:
        print("録音エラー:", e)
        return None

    if len(recording) == 0:
        print("録音データがありません")
        return None

    audio = np.concatenate(recording, axis=0)

    sf.write(filename, audio, fs)

    print("録音終了")
    return filename
import whisper

# Whisperモデル読み込み（起動時1回だけ）
model = whisper.load_model("large")

def speech_to_text(audio_file):

    result = model.transcribe(
        audio_file,
        language="ja",
        fp16=False
    )

    text = result["text"]

    print("認識:", text)

    return text
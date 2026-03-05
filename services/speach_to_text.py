import whisper

model = whisper.load_model("medium")

def transcribe(file_path):

    result = model.transcribe(
        file_path,
        language="ja"
    )

    text = result["text"]

    print("”FŽ¯Œ‹‰Ê:", text)

    return text
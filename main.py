import os
from dotenv import load_dotenv

from services.recorder import record_audio
from services.speech_service import transcribe
from services.ai_parser import parse_command
from services.inventory_service import update_inventory

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print("APIキー読み込み確認:", api_key[:5])

def main():

    audio_file = record_audio(duration=5)
    text = transcribe(audio_file)
    print("認識結果:", text)

    command = parse_command(text)
    print("解析結果:", command)

    update_inventory(
        command["item"],
        command["quantity"],
        command["action"]
    )

if __name__ == "__main__":
    main()

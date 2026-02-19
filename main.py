from services.recorder import record_audio
from services.speech_service import transcribe
from services.ai_parser import parse_command
from services.inventory_service import update_inventory
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print("APIキー読み込み確認:", api_key[:5])

def main():

    audio = record_audio(duration=5)

    text = transcribe(audio)
    print("認識結果:", text)

    command = parse_command(text)
    print("解析結果:", command)

    update_inventory(
        command["name"],
        command["quantity"],
        command["action"]
    )

if __name__ == "__main__":
    main()

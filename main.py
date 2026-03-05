from services.recorder import record_audio
from services.speech_to_text import transcribe
from services.text_normalizer import normalize_text,separate_action_and_number
from services.item_matcher import detect_item
from services.ai_parser import parse_department

import re


def extract_quantity(text):

    m = re.search(r'\d+',text)

    if m:
        return int(m.group())

    return 0


def detect_action(text):

    if "出庫" in text:
        return "出庫"

    if "入庫" in text:
        return "入庫"

    return None


def main():

    audio = record_audio()

    text = transcribe(audio)

    text = normalize_text(text)

    text = separate_action_and_number(text)

    print("正規化:",text)

    item = detect_item(text)

    quantity = extract_quantity(text)

    action = detect_action(text)

    dept = parse_department(text)

    result = {

        "name":item,
        "action":action,
        "quantity":quantity,
        "department":dept["department"]

    }

    print("解析結果")

    print(result)


if __name__ == "__main__":
    main()
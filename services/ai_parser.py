from dotenv import load_dotenv
import openai
import json
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_command(text):

    prompt = f"""
    次の文章から在庫操作情報をJSONで抽出してください。

    文章: {text}

    出力形式:
    {{
        "action": "IN or OUT",
        "name": "chemical name",
        "quantity": number
    }}

    JSONのみを出力してください。
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.choices[0].message.content)

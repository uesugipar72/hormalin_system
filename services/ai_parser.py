from gpt4all import GPT4All
import json
import re

model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

def parse_command(text):

    prompt = f"""
    あなたは在庫管理AIです。
    次の文章からJSONのみを出力してください。

    文章:
    {text}

    出力形式:
    {{
        "name": "品名",
        "action": "入庫 または 出庫",
        "quantity": 数値
    }}

    JSONのみ出力してください。
    """

    with model.chat_session():
        response = model.generate(prompt)

    # JSON抽出
    match = re.search(r'\{.*\}', response, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            print("JSON解析失敗:", response)
            return None
    else:
        print("JSONが見つかりません:", response)
        return None
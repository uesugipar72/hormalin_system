from gpt4all import GPT4All
import json
import re

model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

def parse_command(text):

    prompt = f"""
あなたは在庫管理AIです。
必ず有効なJSONのみを出力してください。
説明文は絶対に出力しないでください。

【抽出ルール】
- 数値は quantity に整数で入れる
- 「個」「本」「リットル」などの単位は除去する
- 「と」「に」「を」「から」「の」などの助詞は除去する
- 部署名のみを counterparty_department に入れる
- 品名が無い場合は null
- 部署が無い場合は null

文章:
{text}

出力形式:
{{
  "name": null,
  "action": "入庫 または 出庫",
  "quantity": 0,
  "counterparty_department": null
}}
"""

    with model.chat_session():
        response = model.generate(prompt, max_tokens=300)

    # 最初のJSONブロックのみ抽出
    matches = re.findall(r'\{[^{}]*\}', response)
    if matches:
        for m in matches:
            try:
                return json.loads(m)
            except:
                continue

    print("JSON解析失敗:", response)
    return None
from openai import OpenAI
import json

def parse_command(text):

    client = OpenAI()

    prompt = f"""
    次の文章から、在庫管理コマンドをJSON形式で抽出してください。

    文章:
    {text}

    出力形式:
    {{
        "item": "品名",
        "action": "入庫 or 出庫",
        "quantity": 数値
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    if content.startswith("```"):
        content = content.split("```")[1]

    try:
        return json.loads(content)
    except:
        print("JSON変換失敗:", content)
        return None
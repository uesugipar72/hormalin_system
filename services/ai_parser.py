from openai import OpenAI
import json
import re

client = OpenAI()

def parse_with_llm(text):

    prompt = f"""
あなたは医療在庫管理AIです。
次の文章からJSONのみ出力してください。

文章:
{text}

出力形式:
{{
 "item": "品名",
 "action": "入庫 または 出庫",
 "quantity": 数値,
 "department": "部署名"
}}

JSONのみ出力
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    # JSON抽出
    match = re.search(r'\{.*\}', content, re.DOTALL)
    if match:
        return json.loads(match.group())

    print("JSON解析失敗:", content)
    return None
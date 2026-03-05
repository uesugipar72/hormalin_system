from gpt4all import GPT4All
import json
import re

model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

def parse_department(text):

    prompt = f"""
次の文章から部署名だけ抽出してください。
JSONのみ出力してください。

文章
{text}

出力
{{
 "department": "部署名"
}}
"""

    with model.chat_session():
        response = model.generate(prompt,max_tokens=200)

    match = re.search(r'\{.*\}', response, re.DOTALL)

    if match:
        try:
            return json.loads(match.group())
        except:
            return {"department":None}

    return {"department":None}
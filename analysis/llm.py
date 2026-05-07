import json
import time
from tqdm import tqdm
from openai import OpenAI
from analysis.prompts import *
from dotenv import load_dotenv

MODEL = "gpt-5.4-mini"
BATCH_SIZE_PASS1 = 15
BATCH_SIZE_PASS2 = 50
RETRY_COUNT = 3
SLEEP_BETWEEN = 1.2

load_dotenv("secret/.env")
client = OpenAI()


def process(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]

    # Pass 1 for transformation score
    pass1_results = {}
    for batch in tqdm(chunk_list(data, BATCH_SIZE_PASS1), desc="PASS 1"):
        result = run_pass1(batch)
        for item in result or []:
            pass1_results[item["id"]] = item
        time.sleep(SLEEP_BETWEEN)

    # Pass 2 for author and tags
    pass2_results = {}
    for batch in tqdm(chunk_list(data, BATCH_SIZE_PASS2), desc="PASS 2"):
        result = run_pass2(batch)
        for item in result or []:
            pass2_results[item["id"]] = item
        time.sleep(SLEEP_BETWEEN)

    final = []
    for item in data:
        _id = item["id"]

        merged = {
            "id": _id,
            "text": item["text"],
            **pass1_results.get(_id, {}),
            **pass2_results.get(_id, {})
        }

        final.append(merged)

    with open(output_path, "w", encoding="utf-8") as f:
        for row in final:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Saved to {output_path}")


def run_pass1(batch):
    user_content = json.dumps(batch, ensure_ascii=False)

    messages = [
        {"role": "system", "content": PASS1_SYSTEM},
        {"role": "user", "content": f"Analyze (JSON array of objects with id and text):\n{user_content}"}
    ]

    raw = call_llm(messages)
    if raw is None:
        return []

    parsed = parse_json_safe(raw)
    return parsed if parsed is not None else []


def run_pass2(batch):
    user_content = json.dumps(batch, ensure_ascii=False)

    messages = [
        {"role": "system", "content": PASS2_SYSTEM},
        {"role": "user", "content": f"Process (JSON array of objects with id and text):\n{user_content}"}
    ]

    raw = call_llm(messages)
    if raw is None:
        return []

    parsed = parse_json_safe(raw)
    return parsed if parsed is not None else []


def call_llm(messages):
    for attempt in range(RETRY_COUNT):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Retry {attempt+1} due to error: {e}")
            time.sleep(2 * (attempt + 1))
    return None


def chunk_list(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]


def parse_json_safe(text):
    try:
        return json.loads(text)
    except:
        return None

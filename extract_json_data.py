import json
import pandas as pd
from content_utils import *


def get_type(row):
    if isinstance(row["text"], (list, str)) and len(row["text"]) > 0:
        return "text"
    if pd.notna(row.get("photo")):
        return "photo"
    if pd.notna(row.get("media_type")):
        return "video"
    return "other"


def extract_content(obj):
    if not isinstance(obj, list):
        return ""
    text = " ".join(i.get("text", "") for i in obj if isinstance(i, dict))

    return text


def build_dataframe_json(json_file, label):
    with open(json_file, 'r') as f:
        data = json.load(f)
        # Expected raw_data keys ['name', 'type', 'id', 'messages']

        if 'messages' in data:
            df = pd.json_normalize(data['messages'])
            # Expected columns:
            # ['id', 'type', 'date', 'date_unixtime', 'from', 'from_id', 'text',
            #        'text_entities', 'inline_bot_buttons', 'photo', 'photo_file_size',
            #        'width', 'height', 'file', 'file_size', 'thumbnail',
            #        'thumbnail_file_size', 'media_type', 'mime_type', 'duration_seconds',
            #        'file_name', 'edited', 'edited_unixtime']

            required_columns = {"text", "date", "text_entities", "photo", "media_type"}

            missing = required_columns - set(df.columns)
            if missing:
                print("Missing columns in JSON {f}:", missing)
                return None

            df["type"] = df.apply(get_type, axis=1)
            df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)
            df["raw_content"] = df["text_entities"].apply(extract_content)
            df["content"] = df["raw_content"].apply(simplify_content)
            df["content_structured"] = df["raw_content"].apply(normalize_content)
            df["source"] = label

        else:
            print(f'JSON data keys do not match expectations: check JSON file {json_file}')
            return None
    return df[['type', 'date', 'content', 'content_structured', 'source']]


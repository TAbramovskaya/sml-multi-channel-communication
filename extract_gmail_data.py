import base64
from content_utils import *
import pandas as pd
from email.utils import parsedate_to_datetime


SENDER_EMAIL = "clients@simulative.ru"


def get_header(payload, name):
    for h in payload.get("headers", []):
        if h["name"] == name:
            return h["value"]
    return None


def get_messages(service):
    all_messages = []
    page_token = None

    while True:
        response = service.users().messages().list(
            userId="me",
            q="from:" + SENDER_EMAIL,
            pageToken=page_token
        ).execute()

        messages = response.get("messages", [])
        all_messages.extend(messages)

        page_token = response.get("nextPageToken")

        if not page_token:
            break

    return all_messages


def extract_body(payload):
    if payload is None:
        return None

    mime_type = payload.get("mimeType", "")
    body = payload.get("body", {})

    # if plain text - get raw_data
    if mime_type == "text/plain" and "data" in body:
        return base64.urlsafe_b64decode(body["data"]).decode("utf-8", errors="ignore")

    # if multipart - go deeper
    if "parts" in payload:
        for part in payload["parts"]:
            result = extract_body(part)
            if result:
                return result

    return None


def build_dataframe_gmail(service, label):
    messages_meta = get_messages(service)
    rows = []

    for m in messages_meta:
        msg = service.users().messages().get(
            userId="me",
            id=m["id"],
            format="full"
        ).execute()

        payload = msg.get("payload", {})

        date = get_header(payload, "Date")
        body = extract_body(payload)

        rows.append({
            "type": "text",
            "date": parsedate_to_datetime(date) if date else None,
            "content": simplify_content(body),
            "content_structured": normalize_content(body),
            "source": label
        })

    df = pd.DataFrame(rows)

    df = df[df["content"].str.len() > 0] # drop empty content

    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)

    return df

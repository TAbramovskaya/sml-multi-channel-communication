import re
import unicodedata
import emoji

def simplify_content(text):
    if not text:
        return ""

    text = text.replace("\u00A0", " ")  # normalize non-breaking spaces
    # text = re.sub(r"[^a-zA-Zа-яА-Я]+", " ", text) # remove all characters except Latin and Cyrillic letters
    text = re.sub(r"[^а-яА-Я]+", " ", text) # allow Cyrillic letters only
    text = re.sub(r"\s+", " ", text)    # collapse whitespace

    return text.strip().lower()


def normalize_content(text):
    if not text:
        return ""

    # Normalize unicode
    text = unicodedata.normalize("NFKC", text)

    # Remove emojis
    # text = emoji.replace_emoji(text, replace="")

    # Replace non-breaking spaces with normal spaces
    text = text.replace("\u00A0", " ")

    # Normalize tabs to spaces
    text = text.replace("\t", " ")

    # cleaned_lines = [
    #     re.sub(r" +", " ", line).strip()
    #     for line in text.splitlines()
    #     if line.strip()
    # ]

    # return "\n".join(cleaned_lines).strip()
    return text.strip()
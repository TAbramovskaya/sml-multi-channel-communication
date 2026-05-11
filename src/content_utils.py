import re
import unicodedata
import emoji


def simplify_content(text):
    if not text:
        return ""

    text = text.replace("\u00A0", " ")  # normalize Non-Breaking SPaces
    text = text.replace("\u2028", " ")  # normalize Line Separator
    text = text.replace("\u2029", " ")  # normalize Paragraph Separator
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

    text = text.replace("\u00A0", " ")     # normalize Non-Breaking SPaces
    text = text.replace("\u2028", " ")     # normalize Line Separator
    text = text.replace("\u2029", " ")     # normalize Paragraph Separator
    text = text.replace("\u200C", " ")     # normalize Zero Width Non-Joiner
    text = re.sub(r" +", " ", text)     # collapse multiple spaces
    text = text.strip()

    # Normalize tabs to spaces
    # text = text.replace("\t", " ")

    # cleaned_lines = [
    #     re.sub(r" +", " ", line).strip()
    #     for line in text.splitlines()
    #     if line.strip()
    # ]

    # return "\n".join(cleaned_lines).strip()
    return text.strip()

# audio/hotword.py

from config import HOTWORD


def detect_hotword(text: str | None) -> bool:
    if not text:
        return False
    return HOTWORD in text.lower()
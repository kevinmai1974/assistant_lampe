# core/logger.py

import json
import os
from datetime import datetime
from config import LOG_FILE


def log_command(command_text: str, intent: str, result: str, state: str) -> None:
    """
    Journalisation minimale :
    - commande texte
    - intention d�tect�e
    - date/heure
    - r�sultat
    - �tat
    """
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "command_text": command_text,
        "intent": intent,
        "result": result,
        "state": state
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
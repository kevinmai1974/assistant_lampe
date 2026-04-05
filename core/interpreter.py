# core/interpreter.py

import re


def normalize_text(text: str) -> str:
    return text.lower().strip()


def interpret_command(text: str) -> dict:
    """
    Transforme le texte en intention.
    Le projet demande au moins 3 regex robustes.
    Ici on en fournit 5.
    """
    if not text:
        return {
            "intent": "unknown",
            "command_text": "",
            "response": "Je n'ai rien compris."
        }

    normalized = normalize_text(text)

    rules = [
        (
            r"\b(allume|active|mets)\b.*\b(lampe|del|lumi[e�]re)\b",
            "turn_on",
            "J'allume la lampe."
        ),
        (
            r"\b([�e]teins|d�sactive|coupe|ferme)\b.*\b(lampe|del|lumi[e�]re)\b",
            "turn_off",
            "J'�teins la lampe."
        ),
        (
            r"\b(fais clignoter|clignote|clignoter)\b.*\b(lampe|del|lumi[e�]re)?\b",
            "blink",
            "Je fais clignoter la lampe."
        ),
        (
            r"\b(donne[- ]?moi l['�]?[�e]tat|quel est l['�]?[�e]tat|[�e]tat de la lampe)\b",
            "get_state",
            "Je v�rifie l'�tat de la lampe."
        ),
        (
            r"\b(active|mets|passe en)\b.*\b(mode nuit|nuit)\b",
            "night_mode",
            "J'active le mode nuit."
        ),
    ]

    for pattern, intent, response in rules:
        if re.search(pattern, normalized):
            return {
                "intent": intent,
                "command_text": text,
                "response": response
            }

    return {
        "intent": "unknown",
        "command_text": text,
        "response": "Commande non reconnue."
    }
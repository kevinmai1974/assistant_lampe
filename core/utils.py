# core/utils.py

import json


def safe_json_load(payload: str) -> dict:
    try:
        return json.loads(payload)
    except Exception:
        return {}
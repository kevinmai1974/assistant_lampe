# audio/stt.py

import speech_recognition as sr
from config import (
    LANGUAGE,
    LISTEN_TIMEOUT,
    PHRASE_TIME_LIMIT,
    AMBIENT_ADJUST_DURATION,
)

recognizer = sr.Recognizer()


def listen_once() -> str | None:
    """
    �coute une seule phrase et retourne le texte reconnu.
    G�re au minimum :
    - silence
    - bruit
    - timeout
    """
    try:
        with sr.Microphone() as source:
            print("[STT] Ajustement au bruit ambiant...")
            recognizer.adjust_for_ambient_noise(source, duration=AMBIENT_ADJUST_DURATION)

            print("[STT] �coute en cours...")
            audio = recognizer.listen(
                source,
                timeout=LISTEN_TIMEOUT,
                phrase_time_limit=PHRASE_TIME_LIMIT
            )

        text = recognizer.recognize_google(audio, language=LANGUAGE)
        text = text.lower().strip()
        print(f"[STT] Reconnu : {text}")
        return text

    except sr.WaitTimeoutError:
        print("[STT] Timeout : aucun son d�tect�.")
        return None
    except sr.UnknownValueError:
        print("[STT] Audio non compris.")
        return None
    except sr.RequestError as e:
        print(f"[STT] Erreur service STT : {e}")
        return None
    except Exception as e:
        print(f"[STT] Erreur inattendue : {e}")
        return None
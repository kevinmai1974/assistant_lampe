# run_assistant.py

import json
import threading
import time

from audio.hotword import detect_hotword
from audio.stt import listen_once
from audio.tts import speak
from config import MQTT_TOPIC_COMMAND, MQTT_TOPIC_STATUS
from core.interpreter import interpret_command
from core.logger import log_command
from core.mqtt_helper import MQTTClient


latest_status = {
    "intent": "",
    "result": "",
    "state": "unknown"
}
status_event = threading.Event()


def on_status_message(client, userdata, msg):
    global latest_status
    try:
        payload = msg.payload.decode("utf-8")
        print(f"[ASSISTANT] Statut re�u : {payload}")

        data = json.loads(payload)
        latest_status = {
            "intent": data.get("intent", ""),
            "result": data.get("result", ""),
            "state": data.get("state", "unknown")
        }
        status_event.set()
    except Exception as e:
        print(f"[ASSISTANT] Erreur lecture statut MQTT : {e}")


def wait_for_status(timeout: float = 10.0) -> dict:
    received = status_event.wait(timeout=timeout)
    if received:
        status_event.clear()
        return latest_status.copy()

    return {
        "intent": "",
        "result": "Aucune reponse du module lampe.",
        "state": "unknown"
    }


def main():
    mqtt_client = MQTTClient(client_id="voice-assistant")
    mqtt_client.connect()

    mqtt_client.client.on_message = on_status_message
    mqtt_client.client.subscribe(MQTT_TOPIC_STATUS)

    speak("Assistant pret. Dites assistant pour commencer.")

    try:
        while True:
            print("\n=== Attente du mot d'activation ===")
            heard_text = listen_once()

            if not heard_text:
                continue

            if not detect_hotword(heard_text):
                print("[HOTWORD] Mot d'activation non detecte.")
                continue

            speak("Je vous ecoute.")

            command_text = listen_once()

            if not command_text:
                speak("Je n'ai pas entendu de commande.")
                log_command("", "none", "Aucune commande entendue", "unknown")
                continue

            analysis = interpret_command(command_text)
            intent = analysis["intent"]

            if intent == "unknown":
                speak("Commande non reconnue.")
                log_command(command_text, intent, "Commande non reconnue", "unknown")
                continue

            mqtt_payload = {
                "intent": intent,
                "command_text": command_text
            }

            status_event.clear()
            mqtt_client.publish_json(MQTT_TOPIC_COMMAND, mqtt_payload)

            status = wait_for_status(timeout=10.0)

            result_text = status.get("result", "Aucune reponse.")
            state_text = status.get("state", "unknown")

            speak(result_text)
            log_command(command_text, intent, result_text, state_text)

            time.sleep(0.3)

    except KeyboardInterrupt:
        print("\n[ASSISTANT] Arret du programme.")
        speak("Arret de l'assistant.")
    finally:
        mqtt_client.stop()


if __name__ == "__main__":
    main()

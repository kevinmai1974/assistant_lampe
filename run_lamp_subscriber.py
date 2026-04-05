# run_lamp_subscriber.py

import json
import signal
import sys

from config import MQTT_TOPIC_COMMAND, MQTT_TOPIC_STATUS
from core.mqtt_helper import MQTTClient
from device.lamp_controller import LampController


mqtt_client = MQTTClient(client_id="lamp-subscriber")
lamp = LampController()


def handle_command(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        print(f"[LAMPE] Message recu : {payload}")

        data = json.loads(payload)
        intent = data.get("intent", "unknown")

        result_data = lamp.execute_intent(intent)

        status_payload = {
            "intent": intent,
            "result": result_data["result"],
            "state": result_data["state"]
        }

        mqtt_client.publish_json(MQTT_TOPIC_STATUS, status_payload)

    except Exception as e:
        print(f"[LAMPE] Erreur traitement message : {e}")
        mqtt_client.publish_json(
            MQTT_TOPIC_STATUS,
            {
                "intent": "unknown",
                "result": f"Erreur c�t� lampe : {e}",
                "state": lamp.state
            }
        )


def shutdown_handler(signum, frame):
    print("\n[LAMPE] Arret demande.")
    lamp.cleanup()
    mqtt_client.stop()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    mqtt_client.connect()
    mqtt_client.client.on_message = handle_command
    mqtt_client.client.subscribe(MQTT_TOPIC_COMMAND)

    print(f"[LAMPE] Abonne au topic : {MQTT_TOPIC_COMMAND}")
    print("[LAMPE] En attente des commandes...")

    try:
        while True:
            signal.pause()
    except AttributeError:
        # Compatibilite minimale si signal.pause n'existe pas
        import time
        while True:
            time.sleep(1)


if __name__ == "__main__":
    main()

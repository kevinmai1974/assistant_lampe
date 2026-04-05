# core/mqtt_helper.py

import json
import time
import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE


class MQTTClient:
    def __init__(self, client_id: str):
        self.client = mqtt.Client(client_id=client_id)
        self.connected = False

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc):
        self.connected = (rc == 0)
        if self.connected:
            print("[MQTT] Connect� au broker.")
        else:
            print(f"[MQTT] �chec de connexion. Code retour = {rc}")

    def _on_disconnect(self, client, userdata, rc):
        self.connected = False
        print("[MQTT] D�connect� du broker.")

    def connect(self):
        self.client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        self.client.loop_start()

        for _ in range(20):
            if self.connected:
                return
            time.sleep(0.2)

        print("[MQTT] Connexion non confirm�e dans le d�lai pr�vu.")

    def stop(self):
        try:
            self.client.loop_stop()
            self.client.disconnect()
        except Exception:
            pass

    def publish_json(self, topic: str, payload: dict):
        data = json.dumps(payload, ensure_ascii=False)
        self.client.publish(topic, data)
        print(f"[MQTT] Publication sur {topic} : {data}")
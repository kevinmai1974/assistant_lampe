# device/lamp_controller.py

import time
from config import (
    GPIO_PIN,
    BLINK_TIMES,
    BLINK_INTERVAL,
    NIGHT_MODE_BLINKS,
    NIGHT_MODE_ON_TIME,
    NIGHT_MODE_OFF_TIME,
)

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except Exception:
    GPIO_AVAILABLE = False


class LampController:
    def __init__(self):
        self.pin = GPIO_PIN
        self.state = "off"

        if GPIO_AVAILABLE:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.output(self.pin, GPIO.LOW)
            print(f"[GPIO] Initialis� sur GPIO {self.pin}")
        else:
            print("[GPIO] RPi.GPIO non disponible : mode simulation activ�.")

    def _write(self, value: bool):
        if GPIO_AVAILABLE:
            GPIO.output(self.pin, GPIO.HIGH if value else GPIO.LOW)
        else:
            print(f"[SIMULATION GPIO] {'HIGH' if value else 'LOW'} sur GPIO {self.pin}")

    def turn_on(self) -> dict:
        self._write(True)
        self.state = "on"
        return {
            "result": "Lampe allum�e",
            "state": self.state
        }

    def turn_off(self) -> dict:
        self._write(False)
        self.state = "off"
        return {
            "result": "Lampe �teinte",
            "state": self.state
        }

    def blink(self, times: int = BLINK_TIMES, interval: float = BLINK_INTERVAL) -> dict:
        for _ in range(times):
            self._write(True)
            time.sleep(interval)
            self._write(False)
            time.sleep(interval)

        self.state = "off"
        return {
            "result": "Clignotement termin�",
            "state": self.state
        }

    def night_mode(self) -> dict:
        for _ in range(NIGHT_MODE_BLINKS):
            self._write(True)
            time.sleep(NIGHT_MODE_ON_TIME)
            self._write(False)
            time.sleep(NIGHT_MODE_OFF_TIME)

        self.state = "night"
        return {
            "result": "Mode nuit activ�",
            "state": self.state
        }

    def get_state(self) -> dict:
        if self.state == "on":
            text = "La lampe est allum�e"
        elif self.state == "off":
            text = "La lampe est �teinte"
        elif self.state == "night":
            text = "La lampe est en mode nuit"
        else:
            text = "�tat inconnu"

        return {
            "result": text,
            "state": self.state
        }

    def execute_intent(self, intent: str) -> dict:
        if intent == "turn_on":
            return self.turn_on()
        elif intent == "turn_off":
            return self.turn_off()
        elif intent == "blink":
            return self.blink()
        elif intent == "night_mode":
            return self.night_mode()
        elif intent == "get_state":
            return self.get_state()
        else:
            return {
                "result": "Commande non reconnue c�t� lampe",
                "state": self.state
            }

    def cleanup(self):
        try:
            self._write(False)
            if GPIO_AVAILABLE:
                GPIO.cleanup()
                print("[GPIO] Nettoyage effectu�.")
        except Exception as e:
            print(f"[GPIO] Erreur cleanup : {e}")
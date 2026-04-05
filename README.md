# Assistant vocal à Lampe intelligente

## Lien GitHub

https://github.com/kevinmai1974/assistant_lampe

---

## Description

Ce projet permet de contrôler une lampe connectée à un Raspberry Pi à l'aide de commandes vocales.

Le programme écoute la voix de l'utilisateur, transforme la parole en texte, interprète la commande et envoie un message via MQTT pour allumer ou éteindre la lampe.

---

## Fonctionnement

Le système fonctionne en plusieurs étapes :

1. Capture de la voix avec un microphone USB
2. Conversion de la parole en texte
3. Analyse de la commande
4. Envoi d'un message MQTT
5. Activation du GPIO pour contrôler la lampe

---

## Structure du projet

* `audio/` : gestion du son (reconnaissance vocale et synthèse vocale)
* `core/` : logique principale (interprétation, MQTT, outils)
* `device/` : contrôle du matériel (lampe via GPIO)
* `config.py` : paramètres du projet
* `run_assistant.py` : lance l'assistant vocal
* `run_lamp_subscriber.py` : gére la lampe

---

## Prérequis

### Matériel

* Raspberry Pi
* LED ou lampe connectée au GPIO 17
* Microphone USB

### Logiciel

* Python 3
* Mosquitto (MQTT)

---

## Installation

### 1. Installer les dépendances système

```bash
sudo apt update
sudo apt install -y python3-venv portaudio19-dev python3-pyaudio espeak ffmpeg mosquitto mosquitto-clients
```

### 2. Cloner le projet

```bash
git clone https://github.com/kevinmai1974/assistant_lampe.git
cd assistant_lampe
```

### 3. Créer un environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Installer les d�pendances Python

```bash
pip install -r requirements.txt
```

---

## Lancement

### 1. Démarrer MQTT

```bash
sudo systemctl start mosquitto
```

### 2. Lancer le programme de la lampe

```bash
python run_lamp_subscriber.py
```

### 3. Lancer l'assistant vocal (dans un autre terminal)

```bash
source .venv/bin/activate
python run_assistant.py
```

---

## Utilisation

Dire :

* "assistant"
* puis "allume la lampe" ou "éteins la lampe"

---

## Important

* Le microphone USB est nécessaire pour utiliser la reconnaissance vocale
* Sans micro, seule la logique du programme peut être testée

---

## Auteur

Kevin Mai

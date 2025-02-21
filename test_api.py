import requests
from datetime import datetime

def test_api():
    url = "https://logger-five-eta.vercel.app/api/keystrokes"
    
    test_data = {
        "timestamp": datetime.now().isoformat(),
        "keystrokes": "Test de l'API - ça fonctionne !"
    }
    
    try:
        print(f"Envoi de la requête à : {url}")
        print(f"Données envoyées : {test_data}")
        
        response = requests.post(url, json=test_data)
        print(f"\nCode de statut: {response.status_code}")
        print(f"Réponse: {response.json()}")
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    test_api() 
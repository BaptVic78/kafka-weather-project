import time
import json
import random
from kafka import KafkaProducer
from datetime import datetime
from kafka.errors import NoBrokersAvailable

producer = None

while producer is None:
    try:
        producer = KafkaProducer(
            bootstrap_servers=['kafka:29092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8')
        )
    except NoBrokersAvailable:
        print("Kafka broker non disponible, nouvelle tentative dans 5 secondes...")
        time.sleep(5)

print("démarrage du simulateur de capteurs...")

topic_name='weather_data'

try:
    while True:
        #on génère la donnée aléatoire
        température=round(random.uniform(5.0, 35.0), 2)
        formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = {
            'sensor_id': 1,
            'température': température, 
            "city": "Paris",
            'timestamp': formatted_date
        }

        producer.send(
            topic_name, 
            key='sensor_1',
            value=message
        )
        
        producer.flush()

        print(f"Envoyé ! {message}")

        time.sleep(1)

except KeyboardInterrupt:
    print("Arrêt du producteur")
    producer.close()
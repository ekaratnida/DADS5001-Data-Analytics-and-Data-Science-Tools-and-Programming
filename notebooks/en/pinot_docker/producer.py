# Producer
from confluent_kafka import Producer
from bson import json_util
import json

p = Producer({'bootstrap.servers':'localhost:9092'})

data = {
    "movieId": 1,
    "title": "Inception",
    "genres": "Action, Sci-Fi",
    "rating": 4.8
}

p.produce('movies-topic', key="", value=json.dumps(data, default=json_util.default).encode('utf-8'))
    
p.flush()

print("flush")
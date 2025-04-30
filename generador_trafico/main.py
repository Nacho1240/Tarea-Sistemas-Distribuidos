import os
import requests
import time
from pymongo import MongoClient
from random import shuffle, gauss

mongoClient = MongoClient(
    host="mongodb",
    port=27017,
    username="admin",
    password="password",
    authSource="admin",
    authMechanism='SCRAM-SHA-256'
)

def get_events_db():
    db = mongoClient.admin
    events_collection = db.waze_events
    return list(events_collection.find({}))

def get_events_random():
    events = get_events_db()
    shuffle(events)
    return events

def get_events_normal():
    events = get_events_db()
    n = len(events)
    # ajusta media y desviación estándar a tu gusto:
    mean = n / 2
    stddev = n / 6   # aprox. el 99.7% estará en [0, n]
    # generamos un "peso" gaussiano para cada evento
    weighted = [(gauss(mean, stddev), e) for e in events]
    # ordenamos por ese peso
    weighted.sort(key=lambda x: x[0])

    return [e for _, e in weighted]

def make_requests_events(events):
    for event in events:
        event.pop("_id", None)
        try:
            requests.post("http://cachechito:9090", json=event)
        except:
            pass

def main():
    modo = os.getenv("MODO_DISTRIBUCION", "aleatorio")
    print(f"GENERADOR DE TRÁFICO - DISTRIBUCIÓN: {modo}")
    mul = int(os.getenv("MULTIPLICADOR", "1"))

    for i in range(mul, 0, -1):
        if modo == "normal":
            eventos = get_events_normal()
        else:
            eventos = get_events_random()
        
        make_requests_events(eventos)

if __name__ == "__main__":

    time.sleep(5)
    main()

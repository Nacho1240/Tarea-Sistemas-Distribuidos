import math
import asyncio
import httpx
import time
import json
import glob
import datetime
import os
from pymongo import MongoClient


def insertar_archivos_json_a_db():
    json_files = glob.glob("alertas*.json")  # busca archivos tipo 'alertas.json', 'alertas_*.json', etc.

    if not json_files:
        print("No se encontraron archivos de alertas.")
        return

    client = MongoClient(
        host="mongodb", 
        port=27017, 
        username="admin", 
        password="password", 
        authSource="admin", 
        authMechanism='SCRAM-SHA-256'
    )
    db = client.admin
    events_collection = db.waze_events

    total_insertados = 0

    for file in json_files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and data:
                    events_collection.insert_many(data)
                    total_insertados += len(data)
                    print(f"Insertados {len(data)} eventos desde {file}")
                else:
                    print(f"El archivo {file} está vacío o no contiene una lista.")
        except Exception as e:
            print(f"Error procesando {file}: {e}")

    print(f"\n Total de alertas insertadas: {total_insertados}")
    print(f"total de eventos en la db: {events_collection.count_documents({})}")

async def fetch(client, url):
    response = await client.get(url)
    while response.status_code == 429:
        print("ME BANEARON!! AAAAAA\nesperando 20 segundos")
        time.sleep(20)   
        response = await client.get(url)
    return response.json()

total = 0

async def main():
    center_lat = -33.44637373669101
    center_lon = -70.66048144891103

    km_per_step = 10

    step_lat = (km_per_step / 111.32)
    step_lon = km_per_step / (111.32 * math.cos(math.radians(center_lat)))

    num_steps = 5

    grid = []
    urls = []

    for i in range(-num_steps, num_steps + 1):
        for j in range(-num_steps, num_steps + 1):
            bottom = center_lat + i * step_lat
            top = bottom + step_lat
            left = center_lon + j * step_lon
            right = left + step_lon

            grid.append({
                'top': top,
                'bottom': bottom,
                'left': left,
                'right': right,
            })

    for block in grid:
        url = f"https://www.waze.com/live-map/api/georss?top={block['top']}&bottom={block['bottom']}&left={block['left']}&right={block['right']}&env=row&types=alerts,traffic"
        urls.append(url)


    alerts = []

    async with httpx.AsyncClient(timeout=None) as client:
        tasks = [fetch(client, url) for url in urls]
        responses = await asyncio.gather(*tasks)

        for jsonResponse in responses:
            try:
                alerts.extend(jsonResponse["alerts"])
            except KeyError:
                pass

    total += len(alerts)
    print(f"Total de alertas obtenidas: {total}")

    if alerts:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"alertas_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(alerts, f, ensure_ascii=False, indent=4)

        insertar_archivos_json_a_db()

if __name__ == "__main__":
    modo = os.getenv("MODO_ALERTAS", "usar_existentes")  # default: usar archivos existentes
    print(f"Modo de operación: {modo}")

    if modo == "generar":
        while total < 10 * 1000:
            asyncio.run(main())
    else:
        insertar_archivos_json_a_db()

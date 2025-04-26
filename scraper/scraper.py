import math
import asyncio
import httpx
import time

async def fetch(client, url):
    response = await client.get(url)
    while response.status_code == 429:
        print("ME BANEARON!! AAAAAA\nesperando 10 segundos")
        time.sleep(10)   
        response = await client.get(url)
    return response.json()

async def main():
    center_lat = -33.44637373669101
    center_lon = -70.66048144891103

    km_per_step = 10

    step_lat = (km_per_step / 111.32)
    step_lon = km_per_step / (111.32 * math.cos(math.radians(center_lat)))

    num_steps = 10

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
    jams = []

    async with httpx.AsyncClient(timeout=None) as client:
        tasks = [fetch(client, url) for url in urls]
        responses = await asyncio.gather(*tasks)

        for jsonResponse in responses:
            try:
                alerts.extend(jsonResponse["alerts"])
            except KeyError:
                pass

            try:
                jams.extend(jsonResponse["jams"])
            except KeyError:
                pass

            total = len(alerts) + len(jams)
            print(f"total: {total}")

    total = len(alerts) + len(jams)
    print(f"Total final: {total}")

if __name__ == "__main__":
    asyncio.run(main())

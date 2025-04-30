# generador de trafico -> cache -> (verificar si esta en cache; sino retornar desde la db y guardar en cache segun corresponda)

from http.server import BaseHTTPRequestHandler, HTTPServer
import redis
import json
import os
import time

total = 0
hits = 0
miss = 0

eviction_policy = os.environ.get('EVICTION_POLICY', 'allkeys-lru')

valid_policies = ['allkeys-lru', 'allkeys-random']
if eviction_policy not in valid_policies:
    raise ValueError(f"Política de remoción no válida: {eviction_policy}. Usa 'allkeys-lru' o 'allkeys-random'.")

r = redis.Redis(host='redis', port=6379, db=0)
r.config_set('maxmemory', '2mb')
r.config_set('maxmemory-policy', eviction_policy)

class ListenServer(BaseHTTPRequestHandler):

    def do_POST(self):
        global total, hits, miss

        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length)

        try:
            data = json.loads(post_body.decode("utf-8"))
            client_id = str(data["id"])
            total += 1
            if r.exists(client_id):
                hits += 1
                value = r.get(client_id).decode()
                print(f"HIT: id={client_id}, valor={value}")
            else:
                miss += 1
                r.set(client_id, json.dumps(data), ex=None)  # sin TTL
                print(f"MISS: id={client_id}, almacenado.")

            hitrate = hits / total
            missrate = miss / total
            print(f"HITRATE: {hitrate:.2f}, MISSRATE: {missrate:.2f}, TOTAL: {len(r.keys())}")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        except Exception as e:
            print(f"error: {e}")
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())

def main():
    hostName = "cachechito"
    serverPort = 9090
    webServer = HTTPServer((hostName, serverPort), ListenServer)
    print(f"Escuchando eventos: http://{hostName}:{serverPort}")
    print(f"Política de remoción: {eviction_policy}")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Servidor detenido.")

if __name__ == "__main__":
    time.sleep(3)
    main()

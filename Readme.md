# Proyecto Sistemas Distribuidos

## Requisitos
- Docker

## Instrucciones de uso
- Descargar o clonar el repositorio de git
- Abrir una terminal dentro de la carpeta clonada
- Usar el comando 'docker compose build' o 'docker-compose build' (dependiendo de la version) para buildears las imagenes de docker
- Usar el comando 'docker compose up' o 'docker-compose up' (dependiendo de la version) para iniciar la ejecución

La primera vez que se inicie como no habran datos en la DB los generadores de trafico no haran nada asi que habra que esperar hasta que se scrapeen algunos eventos, una vez se tengan al menos 10k se debe reiniciar los contenedores usando 'docker compose restart', eso hara que esta vez si inicien los generadores de trafico, cabe destacar que si el sraper detecta que hay mas de 10k eventos en la DB no scrapeara nuevos eventos

## Variables de entorno
El generador de trafico, scraper y cache tienen algunas variables de entorno para modificar su comportamiento estas son: 
### Scraper:
- MODO_ALERTAS:
    - generar: scrapea nuevas alertas desde waze
    - usar_existentes: usa alertas ya scrapeadas (estas tienen que estar en archivos json con el formato alerta*.json)
## Cache
- EVICTION_POLICY:
    - allkeys-random: usa la politica de remocion aleatoria
    - allkeys-lru: usa la politica de remocion LRU
## Generador de trafico
- MODO_DISTRIBUCION:
    - aleatorio: usa una distribucion aleatoria para generar el trafico
    - normal: usa una distribucion normal (o gaussiana) para generar el trafico
- MULTIPLICADOR:
    - N (entero) : cantidad de veces que se ejecutara el generador de trafico

FROM ubuntu:latest

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN pip install requests httpx pymongo --break-system-packages

#CMD ["cat", "scraper.py"]
CMD ["python3", "scraper.py"]

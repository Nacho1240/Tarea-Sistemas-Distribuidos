FROM ubuntu:latest

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN pip install pymongo requests --break-system-packages

CMD ["python3", "main.py"]

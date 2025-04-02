FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/hail75/LightRAG.git && \
    pip install -e LightRAG

EXPOSE 8000

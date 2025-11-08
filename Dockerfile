# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY . .

# 🔹 Explicitly ensure ontology folder is included
COPY ontology ./ontology

RUN mkdir -p logs

EXPOSE 10000

CMD ["sh", "-c", "gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:${PORT:-10000}"]

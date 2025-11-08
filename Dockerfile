# ==========================================================
# 🏥 Ontology-Driven Hospital KPI Intelligence — Dockerfile
# ==========================================================

# --- Base image ---
FROM python:3.11-slim

# --- Environment setup ---
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=10000

# --- Working directory ---
WORKDIR /app

# --- System dependencies (optional but useful for pandas, rdflib parsers, etc.) ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# --- Copy and install Python dependencies ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Copy the full project into container ---
COPY . .

# --- Ensure ontology folder & logs exist (Render sometimes drops empty dirs) ---
RUN mkdir -p /app/ontology /app/logs \
    && if [ -d "./ontology" ]; then cp -r ontology/* /app/ontology/; fi \
    && ls -R /app/ontology || true

# --- Expose Render port ---
EXPOSE 10000

# --- Start command (Gunicorn + Eventlet for SocketIO) ---
CMD ["sh", "-c", "gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:${PORT:-10000}"]

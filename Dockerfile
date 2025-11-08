# ==========================================================
# 🏥 Ontology-Driven Hospital KPI Intelligence — Dockerfile
# ==========================================================

# --- Base image
FROM python:3.11-slim

# --- Set working directory
WORKDIR /app

# --- Copy dependency list first (for caching)
COPY requirements.txt .

# --- Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# --- Copy entire project into the image
COPY . .

# --- 🔹 Make sure ontology directory exists and contains files
# Some Render builds skip empty folders, so force-create and copy explicitly
RUN mkdir -p /app/ontology \
    && cp -r ontology/* /app/ontology/ || true \
    && ls -R /app/ontology

# --- Optional: ensure logs folder exists
RUN mkdir -p logs

# --- Expose Render port
EXPOSE 10000

# --- Run the Flask-SocketIO app using Gunicorn + Eventlet
CMD ["sh", "-c", "gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:${PORT:-10000}"]

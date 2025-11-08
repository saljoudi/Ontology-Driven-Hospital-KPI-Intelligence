# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files and folders into the image
COPY . .

# ✅ Explicitly copy ontology folder (important!)
COPY ontology ./ontology

# Ensure logs directory exists
RUN mkdir -p logs

# Expose Render's dynamic port
EXPOSE 10000

# Start using Gunicorn with eventlet for Flask-SocketIO
CMD ["sh", "-c", "gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:${PORT:-10000}"]

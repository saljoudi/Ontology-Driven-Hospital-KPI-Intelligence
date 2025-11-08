# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY . .

# Ensure logs directory exists
RUN mkdir -p logs

# Expose port (Render provides $PORT dynamically)
EXPOSE 10000

# Use Gunicorn with eventlet for Flask-SocketIO
CMD ["sh", "-c", "gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:${PORT:-10000}"]

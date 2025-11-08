FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs

# Expose port
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "120"]
FROM python:3.12-slim

# Install system dependencies for Demucs
RUN apt-get update && apt-get install -y ffmpeg git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Create storage folder
RUN mkdir -p storage

# EXPOSE the port
EXPOSE 10000

# THE FIX: Use gevent instead of eventlet
CMD ["gunicorn", "--worker-class", "gevent", "--bind", "0.0.0.0:10000", "app:app"]

# Use a Python base that supports PyTorch wheels
FROM python:3.12-slim

# Install system audio dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create storage directory and set permissions
RUN mkdir -p storage/uploads storage/separated
RUN chmod -R 777 storage

# Expose the port Render uses
EXPOSE 10000

# Start the application using Eventlet for SocketIO support
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:10000", "app:app"]
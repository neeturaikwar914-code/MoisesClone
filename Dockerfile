FROM python:3.12-slim

RUN apt-get update && apt-get install -y ffmpeg build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p storage/uploads storage/separated
RUN chmod -R 777 storage

EXPOSE 10000

# CHANGED: eventlet -> gevent
CMD ["gunicorn", "--worker-class", "gevent", "-w", "1", "--bind", "0.0.0.0:10000", "app:app"]

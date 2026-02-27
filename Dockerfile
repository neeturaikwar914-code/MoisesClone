FROM python:3.12-slim

RUN apt-get update && apt-get install -y ffmpeg git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p storage
EXPOSE 10000

# Using gevent to stop the 'Bad file descriptor' and restart errors
CMD ["gunicorn", "--worker-class", "gevent", "--bind", "0.0.0.0:10000", "app:app"]

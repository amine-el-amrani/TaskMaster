FROM python:3.10-slim

WORKDIR /app

# Installer le client PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client && apt-get clean

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
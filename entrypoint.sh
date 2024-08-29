#!/bin/bash

# Exit immédiatement si une commande échoue
set -e

# Attendre que la base de données soit prête avant de continuer
echo "Waiting for the database to be ready..."

# Essayer de se connecter à la base de données plusieurs fois avant d'abandonner
until pg_isready -h db -p 5432 -U "${POSTGRES_USER}"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 5
done

echo "Postgres is up - continuing"

# Appliquer les migrations à la base de données
flask db upgrade

# Démarrer l'application Flask
exec python app.py
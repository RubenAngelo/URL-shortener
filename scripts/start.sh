#!/bin/bash

# start.sh
set -e

DB_CONTAINER="pg-test"

echo "🔍 Verificando se o container já existe..."
if docker ps -a --format 'table {{.Names}}' | grep -q "^${DB_CONTAINER}$"; then
    echo "📦 Container ${DB_CONTAINER} já existe. Removendo..."
    docker rm -f ${DB_CONTAINER}
fi

echo "🐘 Iniciando PostgreSQL com Docker..."
docker run --name ${DB_CONTAINER} \
    -e POSTGRES_PASSWORD=1234 \
    -e POSTGRES_USER=usuario \
    -e POSTGRES_DB=testdb \
    -p 5432:5432 \
    -d postgres

echo "⏳ Aguardando PostgreSQL ficar pronto..."
until docker exec ${DB_CONTAINER} pg_isready -U usuario -d testdb; do
    echo "Aguardando PostgreSQL..."
    sleep 2
done

echo "✅ PostgreSQL está pronto!"
echo "🚀 Iniciando aplicação com Poetry..."
poetry run uvicorn app.main:app --reload --port 8000
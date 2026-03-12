#!/bin/bash
set -euo pipefail  # останавливаем скрипт при любой ошибке

echo "🔄 Pulling latest changes..."
git pull origin || { echo "❌ Git pull failed"; exit 1; }

echo "🔨 Rebuilding and restarting services..."
docker compose up -d --build --force-recreate || { echo "❌ Docker operation failed"; exit 1; }

# Optional: clean up dangling images to free up space
docker image prune -f

echo "✅ Deploy completed successfully!"
#!/bin/bash

# Pull latest changes
git pull origin || { echo "Error: Git pull failed"; exit 1; }

# Rebuild and restart Docker Compose
docker compose down && docker compose up -d --build || { echo "Error: Docker operation failed"; exit 1; }

echo "✅ Pull and rebuild completed successfully"
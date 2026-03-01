# Photobook Telegram Bot — Universal Deployment Guide

## Supported Platforms
Any VPS or dedicated server with Ubuntu 22.04 / 24.04 (recommended). Works on:
- Hetzner Cloud
- DigitalOcean
- Contabo
- Oracle Cloud (when available)
- Any other provider with root access

## Prerequisites
- Fresh Ubuntu 22.04 or 24.04 server
- Minimum 2 GB RAM, 1 CPU core (4 GB RAM + 2 cores recommended for production)
- Root or sudo access
- Public IP address

## Step-by-Step Deployment

### 1. Install Docker & Docker Compose
~~~bash
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
sudo apt install docker-compose-plugin -y
~~~

### 2. Clone the Repository
~~~bash
git clone https://github.com/Your-MVP/photobook_tg_bot.git photobook_bot
cd photobook_bot
~~~

### 3. Configure Environment Variables
~~~bash
cp .env.example .env
nano .env
~~~
Fill in:
- `BOT_TOKEN=your_telegram_bot_token`
- `REDIS_HOST=redis`
- `POSTGRES_HOST=postgres`
- `POSTGRES_USER=...`
- `POSTGRES_PASSWORD=...`

### 4. Start the Services
~~~bash
docker compose up -d --build
~~~

### 5. Verify & Useful Commands
~~~bash
# Check logs
docker compose logs -f bot

# Restart bot only
docker compose restart bot

# Update after git pull
git pull && docker compose up -d --build

# Stop everything
docker compose down
~~~

## Production Hardening (Recommended)
- Install UFW and open ports 80, 443, 22
- Use Caddy / Nginx Proxy Manager for automatic HTTPS
- Enable automatic Docker restart on boot (already handled by docker-compose)
- Set up monitoring (optional: Watchtower for auto-updates)

## Local Development
Use Dev Containers in VSCode + Cline as described in .clinerules/01-development-environment.md.

This guide is valid as of March 2026 and works on any modern Linux VPS.
# Deploy on Oracle Cloud Always Free Tier

1. Create VM (Ubuntu 22.04, Ampere A1 4 OCPU/24GB).
2. SSH and run:
   sudo apt update && sudo apt install docker.io docker-compose git -y
   sudo usermod -aG docker $USER
   git clone your-repo && cd photobook_bot
   cp .env.example .env
3. Open ports 80, 443, 22 in OCI Security List.
4. docker compose up -d --build
5. (Optional) Add Nginx + Let's Encrypt for webhook later.

Test: docker compose logs -f bot
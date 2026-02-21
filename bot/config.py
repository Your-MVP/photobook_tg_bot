from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    def __init__(self):
        self.bot_token = os.getenv("BOT_TOKEN")
        self.redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
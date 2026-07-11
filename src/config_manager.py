import os
from dotenv import load_dotenv

class ConfigManager:
    def __init__(self):
        load_dotenv()
        self.config = {
            "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
            "EMAIL_SENDER": os.getenv("EMAIL_SENDER"),
            "EMAIL_PASSWORD": os.getenv("EMAIL_PASSWORD"),
            "EMAIL_RECEIVER": os.getenv("EMAIL_RECEIVER"),
            "DATABASE_URL": os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'career_agent.db')}"),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
            "CHECK_INTERVAL_MINUTES": int(os.getenv("CHECK_INTERVAL_MINUTES", 60)),
        }

    def get(self, key, default=None):
        return self.config.get(key, default)

config_manager = ConfigManager()

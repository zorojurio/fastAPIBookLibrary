import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'INFO')
    MARIA_USERNAME: str = os.getenv("MARIA_USERNAME")
    MARIA_PASSWORD = os.getenv("MARIA_PASSWORD")
    MARIA_ENDPOINT: str = os.getenv("MARIA_ENDPOINT")
    MARIA_PORT: str = os.getenv("MARIA_PORT", 3306)
    MARIA_DB_NAME: str = os.getenv("MARIA_DB_NAME")
    DATABASE_URL = f"mysql+pymysql://{MARIA_USERNAME}:{MARIA_PASSWORD}@{MARIA_ENDPOINT}:{MARIA_PORT}/{MARIA_DB_NAME}"


settings = Settings()

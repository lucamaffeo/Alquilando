from os import environ, path
import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Base configuration."""
    SECRET_KEY = environ.get("SECRET_KEY", "my_precious")
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session Configuration
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    ITEMS_PER_PAGE = 5


class ProductionConfig(Config):
    """Production specific configuration."""
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }

    DB_NAME = environ.get("DATABASE_URL")
    DB_USER = environ.get("DATABASE_USERNAME")
    DB_PASS = environ.get("DATABASE_PASSWORD")
    DB_HOST = environ.get("DATABASE_HOST")
    DB_PORT = environ.get("DATABASE_PORT")
    DEBUG = False


class DevelopmentConfig(Config):
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASS = os.getenv('DB_PASS', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'grupo63')
    
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

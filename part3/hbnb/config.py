import os
from dotenv import load_dotenv

# Charger les variables d'environnement du fichier .env
load_dotenv()


class Config:
    """Configuration de base (valable pour tous les environnements)."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dec_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_dev_key')
    SQLALCHEMY_TRACK_MODIFICATION = False


class DevelopmentConfig(Config):
    """Configuration pour l'environnement de développement."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///hbnb_dev.db'  # par défaut SQLite local
    )


class ProductionConfig(Config):
    """Configuration pour l'environnement de production."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # ex: MySQL


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
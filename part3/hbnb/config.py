"""Configuration settings for the HBnB application."""

import os


class Config:
    """Base configuration class with default settings."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    """Development configuration with debug mode enabled."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}

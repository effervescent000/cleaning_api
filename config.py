"""Flask configuration variables."""
from os import environ
from datetime import timedelta


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get("SECRET_KEY")

    # Database
    SQLALCHEMY_DATABASE_URI = "sqlite:///cleaning.sqlite"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT config
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = True
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
    JWT_SESSION_COOKIE = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=6)

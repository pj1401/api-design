"""
Load env variables to a config object.
module: src/config/config.py
"""

import os
from dotenv import load_dotenv
from flask import Config

load_dotenv()


class TypedConfig(Config):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    FLASK_DEBUG: str
    SECRET_KEY: str
    JWT_PRIVATE_KEY: str
    JWT_PUBLIC_KEY: str
    JWT_ALGORITHM: str


def create_config() -> TypedConfig:
    """Get the config object."""
    config = TypedConfig(root_path=".")
    config.from_mapping(
        {
            "DB_HOST": os.getenv("POSTGRES_DEV_HOST"),
            "DB_NAME": os.getenv("POSTGRES_DB"),
            "DB_USER": os.getenv("POSTGRES_USER"),
            "DB_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "DB_PORT": int(os.getenv("POSTGRES_PORT", "5432")),
            "FLASK_DEBUG": os.getenv("FLASK_DEBUG", "True"),
            "SECRET_KEY": os.getenv("FLASK_SECRET_KEY"),
            "JWT_PRIVATE_KEY": os.getenv("JWT_PRIVATE_KEY"),
            "JWT_PUBLIC_KEY": os.getenv("JWT_PUBLIC_KEY"),
            "JWT_ALGORITHM": "ES512",
        }
    )
    return config

import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("POSTGRES_DEV_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT")
FLASK_DEBUG = os.getenv("FLASK_DEBUG")
SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
JWT_PRIVATE_KEY = os.getenv("JWT_PRIVATE_KEY")
JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY")
JWT_ALGORITHM = "ES512"

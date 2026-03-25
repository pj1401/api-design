from flask import Flask
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

load_dotenv()

JWT_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

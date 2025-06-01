from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from api.getstories import getstories_bp
from api.submitlore import submitlore_bp
import os

load_dotenv()

from models.db import db


# Environment variables for database connection
AIVEN_USER = os.getenv("AIVEN_USER")
AIVEN_PASSWORD = os.getenv("AIVEN_PASSWORD")
AIVEN_HOST = os.getenv("AIVEN_HOST")
AIVEN_PORT = os.getenv("AIVEN_PORT")
AIVEN_DB = os.getenv("AIVEN_DB")

if not all([AIVEN_USER, AIVEN_HOST, AIVEN_PASSWORD, AIVEN_DB, AIVEN_PORT]):
    raise ValueError("Missing database credentials")

app=Flask(__name__)
CORS(app, origins = [
    "http://localhost:3000",
    "https://bangkoklore.netlify.app"
])
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{AIVEN_USER}:{AIVEN_PASSWORD}@{AIVEN_HOST}:{AIVEN_PORT}/{AIVEN_DB}"

# SSL Configuration for Aiven Cloud MySQL
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "connect_args": {
        "ssl": {
            "ssl-mode": "REQUIRED",
        }
    }
}

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(getstories_bp)
app.register_blueprint(submitlore_bp)

if __name__ == "__main__":
    app.run(debug=True)

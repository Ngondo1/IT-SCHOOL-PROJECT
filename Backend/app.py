from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv

#loading environ variables from .env file
load_dotenv(dotenv_path='.env')
print("environment variables loaded successfully")

app = Flask(__name__)
CORS(app)

# setting secret key for session management
app.secret_key = os.getenv('SECRET_KEY', 'ggj')

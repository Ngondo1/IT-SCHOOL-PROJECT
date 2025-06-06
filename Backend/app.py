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


# Fetching the necessary environment variables from the datbase  connection
db_username = os.getenv('MYSQL_USER')
db_password = os.getenv('MYSQL_PASSWORD', 'kimemia04')
db_host = os.getenv('MYSQL_HOST')
db_port = os.getenv('MYSQL_PORT')
db_name = os.getenv('MYSQL_DATABASE')

#output values of the db connection 
if not all([db_username, db_password, db_host, db_port, db_name]):
    print("One or more environment variables are missing.")
else:
    print(f"DB Username: {db_username}")
    print(f"DB Password: {db_password}")
    print(f"DB Host: {db_host}")
    print(f"DB Port: {db_port}")
    print(f"DB Name: {db_name}")
    
# Configure SQLAchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import and initialize the database
from models import db
db.init_app(app)

# Import and register the Blueprint
from routes import routes
app.register_blueprint(routes)

# Run the flask App
if __name__ == '__main__':
    app.run(debug=True)

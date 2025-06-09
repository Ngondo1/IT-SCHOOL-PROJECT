from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv(dotenv_path='.env')
print("✅ Environment variables loaded successfully")

# Create Flask app
app = Flask(__name__)
CORS(app)

# Secret key for sessions
app.secret_key = os.getenv('SECRET_KEY', '3h@92Jfks8!we91Llk8^d3sd09')

# Get MySQL database credentials from .env
db_username = os.getenv('MYSQL_USER')
db_password = os.getenv('MYSQL_PASSWORD', 'root')
db_host = os.getenv('MYSQL_HOST', 'localhost')
db_port = os.getenv('MYSQL_PORT', '3306')
db_name = os.getenv('MYSQL_DATABASE')

# Warn if something is missing
if not all([db_username, db_password, db_host, db_port, db_name]):
    print("⚠️ One or more DB environment variables are missing.")
else:
    print(f"🔗 Connecting to MySQL: {db_username}@{db_host}:{db_port}/{db_name}")

# Configure SQLAlchemy for MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise DB and Migrations
from models import db
db.init_app(app)
migrate = Migrate(app, db)

# Register route Blueprints
from routes.job import job_bp
from routes.application import application_bp
from routes.matches import match_bp
from routes.reviews import review_bp
from routes.employees import employee_bp
from routes.employers import employer_bp

app.register_blueprint(job_bp)
app.register_blueprint(application_bp)
app.register_blueprint(match_bp)
app.register_blueprint(review_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(employer_bp)

# Optional test route
@app.route('/')
def home():
    return {'message': '✅ Blue-Collar Job Matching API is running'}

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
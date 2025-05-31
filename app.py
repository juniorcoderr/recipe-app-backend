import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from models import db
from auth import auth_bp
from recipes import recipe_bp

load_dotenv()

app = Flask(__name__)
CORS(app)  # enabling CORS so that frontend can safely communicate with backend

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///data.db')  # using sqlite database
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY',
                                         'default-secret-key')  # to encrypt JWT token secret key is set

# Init extensions
db.init_app(app)  # db is connected with flask app
jwt = JWTManager(app)  # initialize JWT manager for authentication

# Registering Routes
app.register_blueprint(auth_bp, url_prefix='/auth')  # handle auth related routes
app.register_blueprint(recipe_bp, url_prefix='/api')  # handle recipes related routes

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # db tables are created in app context
    app.run(debug=True)

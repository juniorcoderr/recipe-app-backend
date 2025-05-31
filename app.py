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

# CORS configuration - allow your React app
CORS(app, origins=['http://localhost:3000'])

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warning
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-secret-key')

# Init extensions
db.init_app(app)
jwt = JWTManager(app)

# Registering Routes
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(recipe_bp, url_prefix='/api')


# Test route for debugging
@app.route('/test')
def test():
    return {'message': 'Flask is working!', 'status': 'success'}


# Run the app
if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()  # Create database tables
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Database error: {e}")

    app.run(debug=True, host='127.0.0.1', port=5000)

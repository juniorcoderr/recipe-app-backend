from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import db, User

# Create a Flask Blueprint for authentication routes
# Blueprint allows us to organize related routes into separate modules
# This keeps auth functionality separate from main app logic
auth_bp = Blueprint('auth', __name__)  # blueprint in which auth-related routes are defined


@auth_bp.route('/register', methods=['POST'])
def register():
    """
       User registration endpoint
       Accepts POST request with username and password in JSON format
       Creates new user account with hashed password
       """

    # Get JSON data from the request body
    data = request.json

    # Input validation - ensure required fields are present
    if not data or not data.get('username') or not data.get('password'):
        return jsonify(msg="Username and password required"), 400

    # Check if username already exists in database
    # User.query.filter_by() searches for existing user with same username
    if User.query.filter_by(username=data['username']).first():
        return jsonify(msg="Username already exists"), 400

    try:
        # Hash the password using Werkzeug's secure hashing function
        # Never store plain text passwords in database
        hashed = generate_password_hash(data['password'])

        # Create new User object with username and hashed password
        new_user = User(username=data['username'], password=hashed)

        # Add user to database session (staging area)
        db.session.add(new_user)

        # Commit changes to actually save to database
        db.session.commit()

        return jsonify(msg="Registered successfully")

    except Exception as e:
        # If any error occurs during database operation, rollback changes
        # This prevents partial/corrupted data from being saved
        db.session.rollback()
        return jsonify(msg="Registration failed"), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
        User login endpoint
        Accepts POST request with username and password
        Returns JWT token if credentials are valid
        """
    data = request.json

    # Find user in database by username
    user = User.query.filter_by(username=data['username']).first()

    # Verify user exists AND password matches
    # check_password_hash() safely compares plain text password with stored hash
    if user and check_password_hash(user.password, data['password']):
        # Create JWT access token using user ID as identity
        # Token will be used for authenticating future requests
        token = create_access_token(identity=str(user.id))
        return jsonify(token=token)

    # Return error if user doesn't exist or password is wrong
    # Don't specify which part failed for security reasons
    return jsonify(msg="Invalid credentials"), 401

# blueprint = to make authentication routes modular

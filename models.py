from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy database object
# This will be used to interact with the database throughout the application
# SQLAlchemy is an ORM (Object-Relational Mapping) that lets us work with databases using Python objects
db = SQLAlchemy()


class User(db.Model):
    """
    User model - represents users table in database
    Each user can create multiple recipes (one-to-many relationship)
    """
    # Primary key - unique identifier for each user record
    # Auto-increments with each new user (1, 2, 3, etc.)
    id = db.Column(db.Integer, primary_key=True)  # primary key (every user has unique id)

    # Username field - must be unique across all users and cannot be empty
    # String(80) limits username to 80 characters maximum
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Password field - stores hashed password, cannot be empty
    # String(200) allows enough space for hashed passwords (typically 60-100+ chars)
    password = db.Column(db.String(200), nullable=False)

    # Relationship to Recipe model - defines one-to-many relationship
    # One user can have many recipes, but each recipe belongs to one user
    # backref='creator' creates a reverse reference on Recipe model
    # This means you can access recipe.creator to get the user who created it
    recipes = db.relationship('Recipe',
                              backref='creator')  # define relationship (One to Many)  - backref='creator' -  to get the recipe user

    def __repr__(self):
        """String representation of User object for debugging"""
        return f'<User {self.username}>'


class Recipe(db.Model):
    """
    Recipe model - represents recipes table in database
    Each recipe belongs to one user (many-to-one relationship)
    """
    # Primary key - unique identifier for each recipe record
    id = db.Column(db.Integer, primary_key=True)

    # Recipe title - String(100) limits title to 100 characters
    # Could be made nullable=False if title is always required
    title = db.Column(db.String(100))

    # Recipe ingredients - Text allows for longer content than String
    # Text fields can store large amounts of text (ingredients list, etc.)
    ingredients = db.Column(db.Text)

    # Recipe instructions - Text allows for detailed cooking instructions
    instructions = db.Column(db.Text)

    # Foreign key that links each recipe to its creator (user)
    # References the 'id' field in the 'user' table
    # This establishes the many-to-one relationship (many recipes -> one user)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # foreign key which uses user id reference

    def __repr__(self):
        """String representation of Recipe object for debugging"""
        return f'<Recipe {self.title}>'

# Database Relationship Summary:
# - User (1) ←→ Recipe (Many)
# - Each User can have multiple Recipes
# - Each Recipe belongs to exactly one User
# - Access patterns:
#   - user.recipes → get all recipes by a user
#   - recipe.creator → get the user who created a recipe
#   - recipe.creator_id → get the ID of the user who created a recipe

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Recipe

# Create a Flask Blueprint for recipe-related routes
# Keeps recipe functionality separate and organized
recipe_bp = Blueprint('recipes', __name__)  # contains recipe related routes


@recipe_bp.route('/recipes', methods=['GET'])
def get_recipes():
    """
    Public endpoint to get all recipes from all users
    No authentication required - anyone can view all recipes
    Returns a list of all recipes in the database
    """
    # Query all recipes from database
    recipes = Recipe.query.all()

    # Convert recipe objects to JSON format using list comprehension
    # This creates a dictionary for each recipe with selected fields
    return jsonify([
        {'id': r.id, 'title': r.title, 'ingredients': r.ingredients, 'instructions': r.instructions}
        for r in recipes
    ])


@recipe_bp.route('/add', methods=['POST'])
@jwt_required()  # Decorator ensures user must be logged in (valid JWT token required)
def add_recipe():
    """
    Protected endpoint to add a new recipe
    Requires valid JWT token - only authenticated users can add recipes
    Associates the recipe with the currently logged-in user
    """
    # Extract user ID from JWT token
    # get_jwt_identity() returns the identity we stored when creating the token (user ID as string)
    user_id_str = get_jwt_identity()
    user_id = int(user_id_str)  # Convert string back to integer for database

    # Get recipe data from request body (JSON)
    data = request.json

    # Create new Recipe object with form data and current user as creator
    recipe = Recipe(
        title=data['title'],
        ingredients=data['ingredients'],
        instructions=data['instructions'],
        creator_id=user_id  # Link recipe to the authenticated user
    )

    # Add recipe to database session and commit changes
    db.session.add(recipe)
    db.session.commit()
    return jsonify(msg="Recipe added!")


# Additional recipe management endpoints below

@recipe_bp.route('/myrecipes', methods=['GET'])
@jwt_required()  # Authentication required to see personal recipes
def get_user_recipes():
    """
    Get recipes for the currently logged-in user only
    Returns only recipes created by the authenticated user
    """
    # Get current user's ID from JWT token
    user_id = int(get_jwt_identity())

    # Filter recipes by creator_id to get only user's own recipes
    recipes = Recipe.query.filter_by(creator_id=user_id).all()

    # Return user's recipes in JSON format
    return jsonify([
        {'id': r.id, 'title': r.title, 'ingredients': r.ingredients,
         'instructions': r.instructions}
        for r in recipes
    ])


@recipe_bp.route('/recipes/<int:recipe_id>', methods=['GET'])
@jwt_required()  # Authentication required to view specific recipe details
def get_recipe(recipe_id):
    """
    Get a specific recipe by ID
    <int:recipe_id> in route captures recipe ID as integer from URL
    """
    # get_or_404() finds recipe by ID or returns 404 error if not found
    recipe = Recipe.query.get_or_404(recipe_id)

    # Return single recipe as JSON object
    return jsonify({
        'id': recipe.id,
        'title': recipe.title,
        'ingredients': recipe.ingredients,
        'instructions': recipe.instructions
    })


@recipe_bp.route('/recipes/<int:recipe_id>', methods=['PUT'])
@jwt_required()  # Authentication required to update recipes
def update_recipe(recipe_id):
    """
    Update a specific recipe
    Only the creator of the recipe can update it (ownership verification)
    PUT method is RESTful standard for updating resources
    """
    # Get current user ID from JWT token
    user_id = int(get_jwt_identity())

    # Find the recipe to update
    recipe = Recipe.query.get_or_404(recipe_id)

    # Security check - verify recipe ownership
    # Prevent users from editing other users' recipes
    if recipe.creator_id != user_id:
        return jsonify(msg="Unauthorized to edit this recipe"), 403

    # Get updated data from request
    data = request.json

    # Update recipe fields - use .get() with fallback to current value
    # This allows partial updates (only update fields that are provided)
    recipe.title = data.get('title', recipe.title)
    recipe.ingredients = data.get('ingredients', recipe.ingredients)
    recipe.instructions = data.get('instructions', recipe.instructions)

    # Commit changes to database
    db.session.commit()
    return jsonify(msg="Recipe updated successfully")


@recipe_bp.route('/recipes/<int:recipe_id>', methods=['DELETE'])
@jwt_required()  # Authentication required to delete recipes
def delete_recipe(recipe_id):
    """
    Delete a specific recipe
    Only the creator of the recipe can delete it (ownership verification)
    DELETE method is RESTful standard for removing resources
    """
    # Get current user ID from JWT token
    user_id = int(get_jwt_identity())

    # Find the recipe to delete
    recipe = Recipe.query.get_or_404(recipe_id)

    # Security check - verify recipe ownership
    # Prevent users from deleting other users' recipes
    if recipe.creator_id != user_id:
        return jsonify(msg="Unauthorized to delete this recipe"), 403

    # Remove recipe from database
    db.session.delete(recipe)
    db.session.commit()
    return jsonify(msg="Recipe deleted successfully")

# API Endpoint Summary:
# GET  /recipes           - Public: Get all recipes from all users
# POST /add               - Protected: Add new recipe (auth required)
# GET  /myrecipes         - Protected: Get current user's recipes only
# GET  /recipes/<id>      - Protected: Get specific recipe by ID
# PUT  /recipes/<id>      - Protected: Update recipe (owner only)
# DELETE /recipes/<id>    - Protected: Delete recipe (owner only)

# Security Features:
# - JWT authentication protects most endpoints
# - Ownership verification prevents unauthorized recipe modifications
# - Input validation through JSON parsing
# - Database error handling with get_or_404()

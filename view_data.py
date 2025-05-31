from models import User, Recipe
from app import app

with app.app_context():
    print("=== USERS ===")
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}")

    print("\n=== RECIPES ===")
    recipes = Recipe.query.all()
    for recipe in recipes:
        creator = User.query.get(recipe.creator_id)
        print(f"ID: {recipe.id}")
        print(f"Title: {recipe.title}")
        print(f"Creator: {creator.username if creator else 'Unknown'}")
        print(f"Ingredients: {recipe.ingredients[:50]}...")
        print("---")

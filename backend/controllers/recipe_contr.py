import re
from flask_login import current_user, login_user
from flask import Blueprint, abort, jsonify, request
from marshmallow import ValidationError
from psycopg2 import IntegrityError
from database.bootstrapDB import *
import sys

from controllers.user import insert_db_if_misses
sys.path.append("../")

bp = Blueprint('recipe', __name__)

recipe_schema = RecipeSchema()

@bp.route('', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return recipe_schema.jsonify(recipes, many=True)


@bp.route('', methods=['POST'])
def create_recipe():
    try:
        recipe = recipe_schema.load(request.json, session=session)
        session.add(recipe)
        session.commit()
        return recipe_schema.jsonify(recipe)
    except ValidationError as e:
        return {'message': e.messages}, 400
    except IntegrityError:
        session.rollback()
        return {'message': 'Recipe already exists.'}, 409


@bp.route('/<int:id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        return {'message': 'Recipe not found.'}, 404
    return recipe_schema.jsonify(recipe)


@bp.route('/<int:id>', methods=['PUT'])
def update_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    try:
        recipe = recipe_schema.load(request.json, instance=recipe,
                                    session=session)
        session.commit()
        return recipe_schema.jsonify(recipe)
    except ValidationError as e:
        return {'message': e.messages}, 400


@bp.route('/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    session.delete(recipe)
    session.commit()
    return '', 204


""" @bp.route("/recipes", methods=["GET"])
def recipes():
    user = User(id=100000, name="vai mo",
                email="tina cipollari", profile_pic="www.goo")

    # Doesn't exist? Add it to the database.
    insert_db_if_misses(user)

    # Begin user session by logging the user in
    login_user(user)

    return getRecipeList(current_user.id)


@bp.route("/chosen-recipes", methods=["GET"])
def chosen_recipes():

    user = User(id=100000, name="vai mo",
                email="tina cipollari", profile_pic="www.goo")

    # Doesn't exist? Add it to the database.
    insert_db_if_misses(user)

    # Begin user session by logging the user in
    login_user(user)

    return getChosenRecipes(current_user.id)


@bp.route("/add-recipe", methods=["POST"])
def add_feeback():

    user = User(id=100000, name="vai mo",
                email="tina cipollari", profile_pic="www.goo")

    # Doesn't exist? Add it to the database.
    insert_db_if_misses(user)

    # Begin user session by logging the user in
    login_user(user)
    result = add_feeback(
        current_user.id, request.json["is_chosen"], request.json["recipe_id"])
    if result is None:
        abort(404)
    else:
        return jsonify(result)


# Endpoints controller
recipe_schema = RecipeSchema()

def getRecipeList(user_id):
    # Create a list of serialized recipe dictionaries
    noFeedbackRecipes = session.query(Recipe).outerjoin(
        Feedback).filter(Feedback.id == None).all()

    recipe_list = []
    for recipe in noFeedbackRecipes:
        recipe_dict = RecipeSchema().dump(recipe)
        recipe_list.append(recipe_dict)

    # Return the list of recipe dictionaries in a JSON response
    return jsonify(recipe_list)


def getChosenRecipes(user_id):

    recipes = session.query(Recipe).join(Feedback).filter(
        Feedback.is_chosen == True, Feedback.user_id == user_id).all()

    recipe_list = []
    for recipe in recipes:
        recipe_dict = RecipeSchema().dump(recipe)
        recipe_list.append(recipe_dict)

    # Return the list of recipe dictionaries in a JSON response
    return jsonify(recipe_list)
 """


def InsertRecipe(title, category, ingredients, steps, image_url):
    try:
        # Check if recipe already exists
        existingRecipe = session.query(Recipe).filter(
            Recipe.title == title).first()
        if existingRecipe:
            return

        # Create new recipe object
        new_recipe = Recipe(title=title, category=category,
                            image_url=image_url)

        # Add recipe to session
        session.add(new_recipe)

        # Create and add recipe ingredients to session
        recipe_ingredients = []
        for ingredientName, quantityAndUnit in ingredients:
            match = re.search(r"^(\d+)\s*(g|gr|ml)", quantityAndUnit)
            if match:
                quant = int(match.group(1))
                unit = match.group(2)
            else:
                quant = -1
                unit = ""

            # Check if ingredient already exists
            existingIngr = session.query(Ingredient).filter_by(
                name=ingredientName).first()

            # If ingredient doesn't exist, create new ingredient object and add to session
            if not existingIngr:
                ingr = Ingredient(name=ingredientName, unit=unit)
                session.add(ingr)
            else:
                ingr = existingIngr

            # Create new recipe ingredient object and add to session
            recipe_ingr = RecipeIngredient(
                ingredient=ingr, recipe=new_recipe, amount=quant, amount_text=quantityAndUnit)

            session.add(recipe_ingr)
            recipe_ingredients.append(recipe_ingr)

            session.commit()

        # Create and add recipe steps to session
        recipe_steps = []
        for i, (url, exp) in enumerate(steps):
            new_step = Step(recipe=new_recipe, n_step=i,
                            image_url=url, explaining=exp)
            session.add(new_step)
            recipe_steps.append(new_step)

        # Commit all changes to session
        session.commit()

    except Exception as e:
        # Roll back changes to session if an error occurs
        session.rollback()
        print("An error occurred while adding recipe:", e)

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from psycopg2 import IntegrityError
from database.bootstrapDB import *
import sys
sys.path.append("../")

bp = Blueprint('recipeingredient', __name__)
recipeingredient_schema = RecipeIngredientSchema()
recipeingredients_schema = RecipeIngredientSchema(many=True)


@bp.route('/recipe_ingredients', methods=['GET'])
def get_recipe_ingredients():
    recipe_ingredients = session.query(RecipeIngredient).all()
    return jsonify(recipeingredients_schema.dump(recipe_ingredients))


@bp.route('/recipe_ingredients/<int:ingredient_id>', methods=['GET'])
def get_recipe_ingredient(ingredient_id):
    recipe_ingredient = session.query(RecipeIngredient).get(ingredient_id)
    if not recipe_ingredient:
        return jsonify({'error': 'Ingredient not found'}), 404
    return jsonify(recipeingredient_schema.dump(recipe_ingredient))


@bp.route('/recipe_ingredients', methods=['POST'])
def create_recipe_ingredient():
    try:
        recipe_ingredient = recipeingredient_schema.load(request.json, session=session)
        session.add(recipe_ingredient)
        session.commit()
        return jsonify(request.json)
    except ValidationError as e:
        return {'message': e.messages}, 400
    except IntegrityError:
        session.rollback()
        return {'message': 'Recipe already exists.'}, 409


@bp.route('/recipe_ingredients/<int:ingredient_id>', methods=['PUT'])
def update_recipe_ingredient(ingredient_id):
    #To check consistency (the product given has same id)

    ingredient = session.query(Ingredient).get(ingredient_id)
    if not ingredient:
        return jsonify({'error': 'Ingredient not found'}), 404
    
    try:
        recipe_ingredient = recipeingredient_schema.load(request.json, session=session)
        session.query(RecipeIngredient).get(ingredient_id).update(recipe_ingredient)
        session.commit()
        return jsonify(request.json)
    except ValidationError as e:
        return {'message': e.messages}, 400
    except IntegrityError:
        session.rollback()
        return {'message': 'Recipe already exists.'}, 409


@bp.route('/recipe_ingredients/<int:ingredient_id>', methods=['DELETE'])
def delete_recipe_ingredient(ingredient_id):
    recipe_ingredient = session.query(Ingredient).get(ingredient_id)
    if not recipe_ingredient:
        return jsonify({'error': 'Recipe Ingredient not found'}), 404
    session.delete(recipe_ingredient)
    session.commit()
    return '', 204

import sys
from psycopg2 import IntegrityError
sys.path.append("../")
from database.bootstrapDB import *
from flask_login import login_user
from flask import Blueprint, jsonify, request

bp = Blueprint('ingredient', __name__)
ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)


@bp.route('/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = session.query(Ingredient).all()
    return jsonify(ingredients_schema.dump(ingredients))


@bp.route('/ingredients', methods=['POST'])
def add_ingredient():
    data = request.json
    new_ingredient = ingredient_schema.load(data, session=session)
    try:
        session.add(new_ingredient)
        session.commit()
        return ingredient_schema.jsonify(new_ingredient), 201
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'Ingredient with the given name already exists'}), 400


@bp.route('/ingredients/<int:ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({'error': 'Ingredient not found'}), 404
    data = request.json
    updated_ingredient = ingredient_schema.load(data, session=session, instance=ingredient, partial=True)
    try:
        session.commit()
        return ingredient_schema.jsonify(updated_ingredient)
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'Ingredient with the given name already exists'}), 400


@bp.route('/ingredients/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({'error': 'Ingredient not found'}), 404
    session.delete(ingredient)
    session.commit()
    return '', 204

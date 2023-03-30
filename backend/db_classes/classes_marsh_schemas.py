import sys
from flask_login import UserMixin
from sqlalchemy import ARRAY, Boolean, Column, Float, Integer, String, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import fields

from db_classes.classes import *



class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = auto_field()
    name = auto_field()
    email = auto_field()
    profile_pic = auto_field()

    feedback = fields.Nested('FeedbackSchema', many=True, exclude=('user','recipe'))
    feedbacked_recipes = fields.List(fields.Nested('RecipeSchema', many=True, exclude=('users_who_feedback','steps','recipe_ingredient','feedback')))
    fridges = fields.List(fields.Nested('FridgeSchema', many=True, exclude=('users',)))


class FeedbackSchema(SQLAlchemySchema):
    class Meta:
        model = Feedback
        load_instance = True

    id = auto_field()
    user_id = auto_field()
    recipe_id = auto_field()
    rating = auto_field()
    notes = auto_field()
    user = fields.Nested('UserSchema', exclude=('feedback',))
    recipe = fields.Nested('RecipeSchema', exclude=('feedback',))


class RecipeSchema(SQLAlchemySchema):
    class Meta:
        model = Recipe
        load_instance = True

    id = auto_field()
    title = auto_field()
    category = auto_field()
    image_url = auto_field()
    
    feedback = fields.Nested('FeedbackSchema', many=True, exclude=('recipe','user'))
    users_who_feedback = fields.List(fields.Nested('UserSchema', exclude=('feedbacked_recipes','fridges','feedback')))
    steps = fields.Nested('StepSchema', many=True,exclude=())
    recipe_ingredients = fields.Nested('RecipeIngredientSchema', many=True, exclude=('ingredient',))


class StepSchema(SQLAlchemySchema):
    class Meta:
        model = Step
        load_instance = True

    id = auto_field()
    recipe_id = auto_field()
    n_step = auto_field()
    image_url = auto_field()
    explaining = auto_field()


class RecipeIngredientSchema(SQLAlchemySchema):
    class Meta:
        model = RecipeIngredient
        load_instance = True

    id = auto_field()
    recipe_id = auto_field()
    ingredient_id = auto_field()
    amount_text = auto_field()
    amount = auto_field()

    ingredient = fields.Nested('IngredientSchema', exclude=('relative_products',))
    product = fields.Nested('ProductSchema', exclude=('used_in_recipe_ingredient',))


class IngredientSchema(SQLAlchemySchema):
    class Meta:
        model = Ingredient
        load_instance = True

    id = auto_field()
    name = auto_field()
    unit = auto_field()
    relative_products = fields.Nested('ProductSchema', many=True, exclude=('can_be_used_as',))


class ProductSchema(SQLAlchemySchema):
    class Meta:
        model = Product
        load_instance = True

    id = auto_field()
    barcode = auto_field()
    ingredient_id = auto_field()
    name = auto_field()
    brand = auto_field()
    labels = auto_field()
    eco_score = auto_field()
    nova_score = auto_field()
    big_image_url = auto_field()
    mini_image_url = auto_field()
    meal = auto_field()
    allergens = auto_field()
    quantity = auto_field()
    used_in_recipe_ingredient = fields.Nested('RecipeIngredientSchema', exclude=('product',))
    used_in_fridge_product = fields.Nested('FridgeProductSchema', exclude=('product',))


class FridgeSchema(SQLAlchemySchema):
    class Meta:
        model = Fridge
        load_instance = True

    id = auto_field()
    name = auto_field()

    """ users = fields.Nested('UserSchema', many=True)
    fridge_products = fields.Nested('FridgeProductSchema', many=True) """


class UserFridgeSchema(SQLAlchemySchema):
    class Meta:
        model = UserFridge
        load_instance = True

    id = auto_field()
    user_id = auto_field()
    fridge_id = auto_field()
    is_admin = auto_field()
    is_owner = auto_field()


class FridgeProductSchema(SQLAlchemySchema):
    class Meta:
        model = FridgeProduct
        load_instance = True

    id = auto_field()
    fridge_id = auto_field()
    product_id = auto_field()
    quantity = auto_field()
    fridge = fields.Nested('FridgeSchema')
    product = fields.Nested('ProductSchema')

import sys
from flask_login import UserMixin
from sqlalchemy import ARRAY, Boolean, Column, Float, Integer, String, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import fields

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    profile_pic = Column(String)

    # Relationships
    feedback = relationship('Feedback', back_populates='user')
    feedbacked_recipes = relationship('Recipe', secondary='feedback', back_populates='users_who_feedback',overlaps="feedback") 
    fridges = relationship('Fridge', secondary='user_fridge', back_populates='users', overlaps='user')


class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    is_chosen = Column(Boolean)
    rating = Column(Integer)
    notes = Column(String)

    # Relationships
    user = relationship("User", back_populates='feedback',overlaps="feedbacked_recipes")
    recipe = relationship('Recipe', back_populates='feedback',overlaps="feedbacked_recipes")



class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String)
    category = Column(String)
    image_url = Column(String)

    # Relationships
    feedback = relationship('Feedback', back_populates='recipe')
    users_who_feedback = relationship('User', secondary='feedback',back_populates='feedbacked_recipes', lazy='dynamic', overlaps="feedback,user,recipe")
    steps = relationship('Step', back_populates='recipe')
    recipe_ingredients = relationship('RecipeIngredient', back_populates='recipe')



class Step(Base):
    __tablename__ = 'step'
    id = Column(Integer, autoincrement=True, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    n_step = Column(Integer)
    image_url = Column(String)
    explaining = Column(String)

    # Relationships
    recipe = relationship('Recipe', back_populates='steps')


class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredient'
    id = Column(Integer, autoincrement=True, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    amount_text = Column(String)
    amount = Column(Float)

    # Relationships
    recipe = relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = relationship('Ingredient', back_populates='contained_in_recipes')
    product = relationship('Product', uselist=False, back_populates='used_in_recipe_ingredient')


class Ingredient(Base):
    __tablename__ = 'ingredient'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    unit = Column(String)

    # Relationships
    relative_products = relationship(
        "Product",
        primaryjoin="Product.ingredient_id==Ingredient.id",
        foreign_keys="Product.ingredient_id",
        backref="can_be_used_as"
    )
    contained_in_recipes = relationship("RecipeIngredient", back_populates='ingredient')


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    barcode = Column(String, unique=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'))
    name = Column(String)
    brand = Column(String)
    labels = Column(ARRAY(Boolean))  # Gluten Free, Vegan etc.
    eco_score = Column(Integer)
    nova_score = Column(Integer)
    big_image_url = Column(String)
    mini_image_url = Column(String)
    meal = Column(ARRAY(Boolean))  # Breakfast, Lunch, Snack, Dinner
    allergens = Column(ARRAY(String))
    quantity = Column(Integer)

    used_in_recipe_ingredient = relationship('RecipeIngredient', back_populates='product', uselist=False)
    used_in_fridge_product = relationship('FridgeProduct', back_populates='product', uselist=False)

class Fridge(Base):
    __tablename__ = 'fridge'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    # Relationships
    users = relationship('User', secondary='user_fridge', back_populates='fridges')
    fridge_products = relationship('FridgeProduct', back_populates='fridge')

class UserFridge(Base):
    __tablename__ = 'user_fridge'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    fridge_id = Column(Integer, ForeignKey('fridge.id'))
    is_admin = Column(Boolean)
    is_owner = Column(Boolean)

    # Relationships

class FridgeProduct(Base):
    __tablename__ = 'fridge_product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fridge_id = Column(Integer, ForeignKey('fridge.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)

    # Relationships
    fridge = relationship('Fridge', back_populates='fridge_products')
    product = relationship('Product', back_populates='used_in_fridge_product')

metadata = Base.metadata
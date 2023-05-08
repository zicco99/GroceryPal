from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy import ARRAY, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry, relationship

from ..DBootstrap import custom_base


class Product(custom_base):
    __tablename__ = 'product'
    barcode = Column(Integer, primary_key=True)
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

    used_in_recipe_ingredient = relationship(
        'RecipeIngredient', back_populates='product')
    used_in_fridge_product = relationship(
        'FridgeProduct', back_populates='product')

    def __init__(self, barcode, ingredient_id=0, name="", brand="", labels=[], eco_score=0, nova_score=0, big_image_url="", mini_image_url="", meal=[False, False, False, False], allergens=[], quantity=0):
        
        self.barcode = barcode
        self.ingredient_id = ingredient_id
        self.name = name
        self.brand = brand
        self.labels = labels
        self.eco_score = eco_score
        self.nova_score = nova_score
        self.big_image_url = big_image_url
        self.mini_image_url = mini_image_url
        self.meal = meal
        self.allergens = allergens
        self.quantity = quantity


class ProductSchema(SQLAlchemySchema):
    class Meta:
        model = Product
        load_instance = True

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
    used_in_recipe_ingredient = fields.Nested(
        'RecipeIngredientSchema', exclude=('product',))
    used_in_fridge_product = fields.Nested(
        'FridgeProductSchema', exclude=('product',))

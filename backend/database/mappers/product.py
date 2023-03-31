from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy import ARRAY, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,registry
from marshmallow import fields

from ..DBootstrap import custom_base
#################### Class and Schema definition ###############################


class Product(custom_base):
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

    used_in_recipe_ingredient = relationship(
        'RecipeIngredient', back_populates='product', uselist=False)
    used_in_fridge_product = relationship(
        'FridgeProduct', back_populates='product', uselist=False)


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
    used_in_recipe_ingredient = fields.Nested(
        'RecipeIngredientSchema', exclude=('product',))
    used_in_fridge_product = fields.Nested(
        'FridgeProductSchema', exclude=('product',))

####################################################################################


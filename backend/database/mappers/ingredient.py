from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,registry
from marshmallow import fields

from ..DBootstrap import custom_base
#################### Class and Schema definition ###############################


class Ingredient(custom_base):
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
    contained_in_recipes = relationship(
        "RecipeIngredient", back_populates='ingredient')


class IngredientSchema(SQLAlchemySchema):
    class Meta:
        model = Ingredient
        load_instance = True

    id = auto_field()
    name = auto_field()
    unit = auto_field()
    relative_products = fields.Nested(
        'ProductSchema', many=True, exclude=('can_be_used_as',))


####################################################################################


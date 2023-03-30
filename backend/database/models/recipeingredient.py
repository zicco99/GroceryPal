from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from marshmallow import fields

Base = declarative_base()

#################### Class and Schema definition ###############################


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
    ingredient = relationship(
        'Ingredient', back_populates='contained_in_recipes')
    product = relationship('Product', uselist=False,
                           back_populates='used_in_recipe_ingredient')


class RecipeIngredientSchema(SQLAlchemySchema):
    class Meta:
        model = RecipeIngredient
        load_instance = True

    id = auto_field()
    recipe_id = auto_field()
    ingredient_id = auto_field()
    amount_text = auto_field()
    amount = auto_field()

    ingredient = fields.Nested(
        'IngredientSchema', exclude=('relative_products',))
    product = fields.Nested(
        'ProductSchema', exclude=('used_in_recipe_ingredient',))

####################################################################################
